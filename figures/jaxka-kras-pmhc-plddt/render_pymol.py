"""Render the KRAS pMHC panels. Run with PyMOL's Python via make.py.

Alignment is baked into coordinates once, then every overview shares one camera
and both P6 close-ups share a second camera. Contacts are recalculated here and
checked against the candidate table, and panels.json records where each labelled
atom lands so compose.py can place editable text.

Environment: KRAS_RENDER_SCALE (1), KRAS_OUT_DIR (this folder), KRAS_CAMERA_JSON
(replacement overview view) and KRAS_DETAIL_CAMERA_JSON (replacement close-up view).
"""
from pathlib import Path
import hashlib
import json
import math
import os

import numpy as np
from pymol import cmd

root = Path(__file__).resolve().parent
out = Path(os.environ.get('KRAS_OUT_DIR', root))
out.mkdir(parents=True, exist_ok=True)
scale = float(os.environ.get('KRAS_RENDER_SCALE', '1'))

STATES = ['mutant', 'wt', 'empty']
LOADED = ['mutant', 'wt']
HIT_CHAIN = {'mutant': 'D', 'wt': 'D', 'empty': 'C'}
P6 = 6
CONTACT_CUTOFF = 4.5
EXPECTED_P6_CONTACTS = {'mutant': 4, 'wt': 1}  # candidate-results.csv
DETAIL_RESIDUES = [289, 290, 291, 298]  # union of P6 contacts over both states
PATCH_RESIDUES = [100, 290, 291]  # one-based original screened patch
LOOP = 'resi 280-305'
OVERVIEW_ANGLES = (0, 20)  # yaw, tilt
# At zero yaw the single WT contact runs along the view axis and disappears.
DETAIL_ANGLES = (50, 8)
OVERVIEW_PX = (1200, 1520)
DETAIL_PX = (1380, 1200)

PLDDT_BINS = [('verylow', '#ff7d45', None), ('low', '#ffdb13', 50),
              ('confident', '#65cbf3', 70), ('veryhigh', '#0053d6', 90)]
FIXED_COLOURS = {'hla_grey': '#bcc2ca', 'b2m_grey': '#858e99', 'hla_ghost': '#b4bbc4',
                 'peptide_teal': '#0f7a7f', 'mutation_pink': '#c2185b', 'contact_ink': '#1d2127'}


def rgb(hex_colour):
    return [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]


def xyz(selection):
    return cmd.get_coords(selection).astype(float)


def hla(name):
    return xyz(f'{name} and chain A and name CA and resi 1-180')


def heavy_atoms(selection):
    atoms = cmd.get_model(f'({selection}) and not elem H').atom
    return atoms, np.array([a.coord for a in atoms], dtype=float)


# Load and align.
cmd.reinitialize()
receipt = {'structures': {}, 'alignment': {}, 'engine': 'PyMOL ray',
           'confidence_source': 'CIF B_iso_or_equiv, 0-100 pLDDT'}
for name in STATES:
    path = root / 'structures' / f'{name}.cif'
    cmd.load(str(path), name)
    atoms = cmd.get_model(name).atom
    values = [a.b for a in atoms]
    assert all(0 <= b <= 100 for b in values)
    receipt['structures'][name] = {
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'atoms': len(atoms),
        'plddt_range': [min(values), max(values)], 'hit_chain': HIT_CHAIN[name]}

ref = hla('mutant')
fixed = ref - ref.mean(0)
# Explicit Kabsch fit, no object matrices and no iterative atom rejection.
for name in STATES[1:]:
    mobile = hla(name)
    assert mobile.shape == ref.shape == (180, 3)
    u, _, vt = np.linalg.svd((mobile - mobile.mean(0)).T @ fixed)
    rotation = u @ np.diag([1, 1, np.sign(np.linalg.det(u @ vt))]) @ vt
    coords = xyz(name)
    aligned = (coords - mobile.mean(0)) @ rotation + ref.mean(0)
    assert np.allclose(np.linalg.norm(np.diff(coords, axis=0), axis=1),
                       np.linalg.norm(np.diff(aligned, axis=0), axis=1), atol=1e-3)
    cmd.load_coords(aligned, name)
    rmsd = float(np.sqrt(np.mean(np.sum((hla(name) - ref) ** 2, axis=1))))
    receipt['alignment'][name] = {
        'HLA_CA_RMSD_angstrom': rmsd, 'residues': 180, 'rotation': rotation.tolist(),
        'translation': (ref.mean(0) - mobile.mean(0) @ rotation).tolist()}

# Shared display frame: P6 at the origin, peptide N-to-C along x, groove normal
# along y. This matches the orientation of the radial maps.
peptide_ca = xyz('mutant and chain C and name CA')
origin = peptide_ca[P6 - 1]
axis_x = peptide_ca[-1] - peptide_ca[0]
axis_x /= np.linalg.norm(axis_x)
normal = np.linalg.svd(fixed)[2][2]
if normal @ (xyz('mutant and chain D and name CA').mean(0) - ref.mean(0)) < 0:
    normal = -normal
axis_y = normal - axis_x * (axis_x @ normal)
axis_y /= np.linalg.norm(axis_y)
basis = np.array([axis_x, axis_y, np.cross(axis_x, axis_y)]).T
for name in STATES:
    cmd.load_coords((xyz(name) - origin) @ basis, name)
for name in STATES[1:]:
    rmsd = float(np.sqrt(np.mean(np.sum((hla(name) - hla('mutant')) ** 2, axis=1))))
    assert abs(rmsd - receipt['alignment'][name]['HLA_CA_RMSD_angstrom']) < 1e-3
    receipt['alignment'][name]['verified_display_RMSD_angstrom'] = rmsd
receipt['shared_frame'] = {'origin': origin.tolist(), 'basis': basis.tolist()}

# Contacts between the hit and peptide position 6, from heavy atoms.
contacts = {}
for name in LOADED:
    p6_atoms, p6_xyz = heavy_atoms(f'{name} and chain C and resi {P6}')
    hit_atoms, hit_xyz = heavy_atoms(f'{name} and chain D')
    distances = np.linalg.norm(hit_xyz[:, None, :] - p6_xyz[None, :, :], axis=2)
    closest = {}
    for i, j in zip(*np.where(distances <= CONTACT_CUTOFF)):
        residue = int(hit_atoms[i].resi)
        if residue not in closest or distances[i, j] < closest[residue]['distance']:
            closest[residue] = {'distance': float(distances[i, j]), 'residue': hit_atoms[i].resn,
                                'hit_atom': hit_atoms[i].name, 'p6_atom': p6_atoms[j].name}
    assert len(closest) == EXPECTED_P6_CONTACTS[name], (name, closest)
    assert set(closest) <= set(DETAIL_RESIDUES), closest
    nearest = {}
    for residue in DETAIL_RESIDUES:
        _, residue_xyz = heavy_atoms(f'{name} and chain D and resi {residue}')
        nearest[residue] = float(np.linalg.norm(
            residue_xyz[:, None, :] - p6_xyz[None, :, :], axis=2).min())
    contacts[name] = {'p6_residue': p6_atoms[0].resn, 'contacts': closest, 'nearest_angstrom': nearest}
receipt['p6_contacts'] = {'cutoff_angstrom': CONTACT_CUTOFF, 'states': contacts}

# Representation and lighting.
for colour, hex_colour, _ in PLDDT_BINS:
    cmd.set_color(colour, rgb(hex_colour))
for colour, hex_colour in FIXED_COLOURS.items():
    cmd.set_color(colour, rgb(hex_colour))
cmd.hide('everything')
cmd.dss()
cmd.color('verylow')
for colour, _, threshold in PLDDT_BINS[1:]:
    cmd.color(colour, f'b > {threshold - 0.001}')
cmd.color('hla_grey', 'chain A')
cmd.color('b2m_grey', 'chain B')
for name in LOADED:
    cmd.color('peptide_teal', f'{name} and chain C')
    cmd.color('mutation_pink', f'{name} and chain C and resi {P6}')
    ghost = f'{name}_hla'
    cmd.create(ghost, f'{name} and chain A and resi 1-180')
    cmd.color('hla_ghost', ghost)
    cmd.set('cartoon_transparency', 0.62, ghost)
    for residue, contact in contacts[name]['contacts'].items():
        label = f'{name}_contact_{residue}'
        cmd.distance(label, f'{name} and chain D and resi {residue} and name {contact["hit_atom"]}',
                     f'{name} and chain C and resi {P6} and name {contact["p6_atom"]}')
        cmd.hide('labels', label)
receipt['colour_scope'] = 'Hit uses pLDDT; HLA and beta2m grey; peptide teal; P6 pink.'

settings = {
    'orthoscopic': 1, 'bg_rgb': [1, 1, 1], 'ray_opaque_background': 1, 'antialias': 2, 'max_threads': 8,
    'cartoon_fancy_helices': 1, 'cartoon_flat_sheets': 1, 'cartoon_smooth_loops': 1,
    'cartoon_sampling': 14, 'cartoon_loop_radius': 0.24, 'cartoon_oval_length': 1.25,
    'cartoon_rect_length': 1.3, 'cartoon_side_chain_helper': 0,
    'ambient': 0.5, 'direct': 0.38, 'reflect': 0.22, 'specular': 0.06, 'shininess': 18,
    'ray_trace_gain': 0.02, 'ray_trace_color': 'contact_ink', 'ray_shadow_decay_factor': 0.15,
    'ray_shadow_decay_range': 6, 'fog_start': 0.45, 'fog': 0.55,
    'stick_radius': 0.27, 'sphere_scale': 0.92, 'dash_color': 'contact_ink', 'dash_radius': 0.075,
    'dash_gap': 0.28, 'dash_length': 0.32, 'dash_round_ends': 1,
}
for key, value in settings.items():
    cmd.set(key, value)


def shade(detail):
    """Outlines separate pale sticks in close-up but clog the 620-residue overview."""
    cmd.set('ray_trace_mode', 1 if detail else 0)
    cmd.set('ray_shadows', 0 if detail else 1)
    cmd.set('depth_cue', 0 if detail else 1)


def camera_for(coords, angles, aspect, margin):
    """Fit an orthographic camera around coords, using PyMOL's own rotation."""
    cmd.set_view((1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, -100, 0, 0, 0, 10, 400, 0))
    cmd.turn('y', angles[0])
    cmd.turn('x', angles[1])
    rotation = np.array(cmd.get_view()[:9]).reshape(3, 3)
    camera = coords @ rotation
    low, high = camera.min(0), camera.max(0)
    height = max(high[1] - low[1], (high[0] - low[0]) / aspect) * (1 + margin)
    fov = math.radians(float(cmd.get('field_of_view')))
    distance = height / (2 * math.tan(fov / 2))
    centre = (low + high) / 2 @ rotation.T
    depth = high[2] - low[2] + 40
    flag = cmd.get_view()[17]
    return [*rotation.ravel(), 0, 0, -distance, *centre, distance - depth, distance + depth, flag]


def project(points, view, aspect):
    """Return panel fractions (0-1 from the top left) for orthographic points."""
    rotation = np.array(view[:9]).reshape(3, 3)
    camera = (np.atleast_2d(points) - np.array(view[12:15])) @ rotation
    fov = math.radians(float(cmd.get('field_of_view')))
    height = 2 * abs(view[11]) * math.tan(fov / 2)
    return np.c_[0.5 + camera[:, 0] / (height * aspect), 0.5 - camera[:, 1] / height]


def saved_view(variable, fallback):
    custom = os.environ.get(variable)
    return json.loads(Path(custom).read_text()) if custom else fallback


def render(panel, size):
    width, height = (int(round(v * scale)) for v in size)
    cmd.png(str(out / f'{panel}.png'), width=width, height=height, dpi=300, ray=1, quiet=1)


overview_aspect = OVERVIEW_PX[0] / OVERVIEW_PX[1]
detail_aspect = DETAIL_PX[0] / DETAIL_PX[1]
all_coords = np.vstack([xyz(name) for name in STATES])
overview_view = saved_view('KRAS_CAMERA_JSON', camera_for(all_coords, OVERVIEW_ANGLES, overview_aspect, 0.03))
detail_coords = np.vstack([xyz(f'{name} and ((chain C and resi 3-9) or (chain D and resi 286-300))')
                           for name in LOADED])
detail_view = saved_view('KRAS_DETAIL_CAMERA_JSON', camera_for(detail_coords, DETAIL_ANGLES, detail_aspect, 0.16))
(out / 'camera.json').write_text(json.dumps(overview_view, indent=2) + '\n')
(out / 'groove-camera.json').write_text(json.dumps(detail_view, indent=2) + '\n')

panels = {'contact_cutoff_angstrom': CONTACT_CUTOFF, 'patch_residues': PATCH_RESIDUES,
          'overview': {'size': OVERVIEW_PX, 'anchors': {}},
          'detail': {'size': DETAIL_PX, 'anchors': {}}}


def fraction(selection, view, aspect):
    return [round(float(v), 5) for v in project(xyz(selection).mean(0), view, aspect)[0]]


# Overview panels.
shade(detail=False)
for name in STATES:
    cmd.disable('all')
    cmd.enable(name)
    cmd.hide('everything', name)
    cmd.show('cartoon', name)
    if name in LOADED:
        cmd.hide('cartoon', f'{name} and chain C')
        cmd.show('spheres', f'{name} and chain C')
    cmd.set_view(overview_view)
    cmd.scene(name, 'store')
    render(f'{name}-pymol', OVERVIEW_PX)
    hit = f'{name} and chain {HIT_CHAIN[name]}'
    panels['overview']['anchors'][name] = {
        'hit': fraction(f'{hit} and name CA', overview_view, overview_aspect),
        'hla': fraction(f'{name} and chain A and name CA and resi 1-180', overview_view, overview_aspect),
        'alpha3': fraction(f'{name} and chain A and name CA and resi 181-276', overview_view, overview_aspect),
        'b2m': fraction(f'{name} and chain B and name CA', overview_view, overview_aspect),
        'groove': fraction(f'mutant and chain C and resi {P6} and name CA', overview_view, overview_aspect)}

# P6 close-ups. Every labelled residue is shown in both states, so only the
# contact lines and the P6 side chain differ between the panels.
shade(detail=True)
for name in LOADED:
    cmd.disable('all')
    cmd.enable(name)
    cmd.enable(f'{name}_hla')
    cmd.hide('everything', name)
    cmd.show('cartoon', f'{name}_hla')
    cmd.show('cartoon', f'{name} and chain D and {LOOP}')
    cmd.show('sticks', f'{name} and chain C')
    cmd.show('spheres', f'{name} and chain C and resi {P6} and name CA')
    cmd.set('sphere_scale', 0.42, f'{name} and chain C and resi {P6} and name CA')
    cmd.show('sticks', f'{name} and chain D and resi {"+".join(map(str, DETAIL_RESIDUES))}')
    for residue in contacts[name]['contacts']:
        cmd.enable(f'{name}_contact_{residue}')
    cmd.set_view(detail_view)
    cmd.scene(f'{name}_groove', 'store')
    render(f'{name}-groove', DETAIL_PX)
    anchors = {'p6_ca': fraction(f'{name} and chain C and resi {P6} and name CA', detail_view, detail_aspect),
               'p6': fraction(f'{name} and chain C and resi {P6}', detail_view, detail_aspect),
               'residues': {}}
    for residue in DETAIL_RESIDUES:
        selection = f'{name} and chain D and resi {residue}'
        # Labels point at the atom a contact line ends on, so each line traces to a name.
        contact = contacts[name]['contacts'].get(residue, contacts['mutant']['contacts'][residue])
        anchors['residues'][str(residue)] = {
            'at': fraction(f'{selection} and name {contact["hit_atom"]}', detail_view, detail_aspect),
            'name': cmd.get_model(f'{selection} and name CA').atom[0].resn,
            'contact': residue in contacts[name]['contacts']}
    panels['detail']['anchors'][name] = anchors

cmd.disable('all')
cmd.scene('mutant', 'recall')
cmd.set_view(overview_view)
cmd.save(str(out / 'aligned.pse'))
receipt.update({'camera': overview_view, 'detail_camera': detail_view, 'scale': scale,
                'pymol_version': cmd.get_version()[0]})
(out / 'panels.json').write_text(json.dumps(panels, indent=2) + '\n')
(out / 'pymol-provenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('P6 contacts verified:', {k: sorted(v['contacts']) for k, v in contacts.items()})
print('HLA alignment verified:', {k: round(v['HLA_CA_RMSD_angstrom'], 3) for k, v in receipt['alignment'].items()})
