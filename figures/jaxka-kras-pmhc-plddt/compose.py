"""Compose the overview and P6 close-up renders with editable text.

Set KRAS_OUT_DIR to compose a test render from another folder. Sizes are in SVG
units: 1800 units span the 160 mm text width, so 28 units is about 7 pt.
"""
from html import escape
from pathlib import Path
import base64
import hashlib
import json
import os
import subprocess

root = Path(__file__).resolve().parent
out = Path(os.environ.get('KRAS_OUT_DIR', root))
panels = json.loads((out / 'panels.json').read_text())

WIDTH = 1800
INK, MUTED, RULE = '#1d2127', '#6b7280', '#c9ced6'
PINK, TEAL, GOLD = '#c2185b', '#0f7a7f', '#e0a100'
FONT = 'Helvetica Neue,Helvetica,Arial,sans-serif'
THREE_LETTER = {'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'LEU': 'L'}

# Common-chain iPTM from candidate-results.csv, the one interface score defined in all contexts.
OVERVIEWS = [('mutant', 'A', 'G12D pMHC', '0.854'), ('wt', 'B', 'WT pMHC', '0.738'),
             ('empty', 'C', 'Peptide-free MHC', '0.192')]
DETAILS = [('mutant', 'D', 'G12D: D6 contacts four hit residues'),
           ('wt', 'E', 'WT: G6 contacts one hit residue')]

OVERVIEW_TOP, OVERVIEW_W = 104, 600
DETAIL_TOP, DETAIL_W, DETAIL_GAP = 944, 680, 20
OVERVIEW_H = OVERVIEW_W * panels['overview']['size'][1] / panels['overview']['size'][0]
DETAIL_H = DETAIL_W * panels['detail']['size'][1] / panels['detail']['size'][0]
HEIGHT = round(DETAIL_TOP + DETAIL_H + 10)

# Label offsets from each anchor, shared by both close-ups so the panels compare directly.
RESIDUE_OFFSETS = {289: (-120, 8), 290: (150, -90), 291: (150, -40), 298: (120, 30)}
P6_OFFSET = (-130, -25)

parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" '
         f'viewBox="0 0 {WIDTH} {HEIGHT}">', f'<rect width="{WIDTH}" height="{HEIGHT}" fill="white"/>']


def text(x, y, label, size=28, colour=INK, bold=False, anchor='start', halo=False):
    style = (f'x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" text-anchor="{anchor}" '
             f'font-weight="{"bold" if bold else "normal"}"')
    body = escape(label)
    if halo:
        parts.append(f'<text {style} fill="white" stroke="white" stroke-width="7" '
                     f'stroke-linejoin="round">{body}</text>')
    parts.append(f'<text {style} fill="{colour}">{body}</text>')


def line(x1, y1, x2, y2, colour=MUTED, width=1.8, dash=None):
    extra = f' stroke-dasharray="{dash}"' if dash else ''
    parts.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{colour}" '
                 f'stroke-width="{width}" stroke-linecap="round"{extra}/>')


def image(name, x, y, width, height):
    data = base64.b64encode((out / f'{name}.png').read_bytes()).decode()
    parts.append(f'<image x="{x}" y="{y}" width="{width}" height="{height:.1f}" '
                 f'href="data:image/png;base64,{data}"/>')


def inset(name, x, y, width, height):
    """Clip a close-up to a rounded frame so its crop reads as deliberate."""
    parts.append(f'<clipPath id="clip-{name}"><rect x="{x}" y="{y}" width="{width}" height="{height:.1f}" '
                 f'rx="14"/></clipPath><g clip-path="url(#clip-{name})">')
    image(name, x, y, width, height)
    parts.append('</g>')


def frame(x, y, width, height):
    parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height:.1f}" rx="14" fill="none" '
                 f'stroke="{RULE}" stroke-width="2"/>')


def callout(anchor, offset, label, **style):
    """Text at anchor+offset with a leader line that stops short of the text."""
    x, y = anchor
    tx, ty = x + offset[0], y + offset[1]
    line(x, y, tx, ty - 9)
    text(tx, ty, label, anchor='end' if offset[0] < 0 else 'start', halo=True, **style)
    return tx, ty


def overview_point(name, key, x0):
    fx, fy = panels['overview']['anchors'][name][key]
    return x0 + fx * OVERVIEW_W, OVERVIEW_TOP + fy * OVERVIEW_H


for i, (name, letter, title, iptm) in enumerate(OVERVIEWS):
    x0 = i * OVERVIEW_W
    image(f'{name}-pymol', x0, OVERVIEW_TOP, OVERVIEW_W, OVERVIEW_H)
    text(x0 + 6, 38, letter, 34, bold=True)
    text(x0 + 46, 38, title, 32, bold=True)
    text(x0 + 46, 76, f'common-chain iPTM {iptm}', 28, MUTED)

# Direct labels replace a target key on the first panel.
x, y = overview_point('mutant', 'hla', 0)
callout((x + 118, y + 30), (70, -8), 'HLA')
x, y = overview_point('mutant', 'b2m', 0)
callout((x + 56, y + 8), (120, 18), 'β2m')
x, y = overview_point('mutant', 'groove', 0)
callout((x, y), (-125, -42), 'P6', colour=PINK, bold=True)
x, y = overview_point('mutant', 'hit', 0)
callout((x + 172, y - 62), (52, -58), 'Hit')
x, y = overview_point('empty', 'groove', 2 * OVERVIEW_W)
callout((x, y), (30, -120), 'Empty groove')

for i, (name, letter, title) in enumerate(DETAILS):
    x0 = i * (DETAIL_W + DETAIL_GAP)
    anchors = panels['detail']['anchors'][name]
    inset(f'{name}-groove', x0, DETAIL_TOP, DETAIL_W, DETAIL_H)
    text(x0 + 6, DETAIL_TOP - 24, letter, 34, bold=True)
    text(x0 + 46, DETAIL_TOP - 24, title, 30, bold=True)
    for residue, info in anchors['residues'].items():
        residue = int(residue)
        fx, fy = info['at']
        label = THREE_LETTER[info['name']] + str(residue)
        tx, ty = callout((x0 + fx * DETAIL_W, DETAIL_TOP + fy * DETAIL_H), RESIDUE_OFFSETS[residue], label,
                         colour=INK if info['contact'] else MUTED, bold=info['contact'])
        if residue in panels['patch_residues']:
            width = len(label) * 17.5
            left = tx - width if RESIDUE_OFFSETS[residue][0] < 0 else tx
            line(left, ty + 8, left + width, ty + 8, GOLD, 5)
    fx, fy = anchors['p6_ca']
    p6_name = 'D6' if name == 'mutant' else 'G6'
    callout((x0 + fx * DETAIL_W, DETAIL_TOP + fy * DETAIL_H), P6_OFFSET, p6_name, colour=PINK, bold=True)
    frame(x0, DETAIL_TOP, DETAIL_W, DETAIL_H)

# Key.
key_x = 1432
text(key_x, DETAIL_TOP + 40, 'Hit pLDDT', 28, bold=True)
row = DETAIL_TOP + 84
for colour, label in [('#0053d6', '≥90'), ('#65cbf3', '70–90'), ('#ffdb13', '50–70')]:
    parts.append(f'<rect x="{key_x}" y="{row - 22}" width="44" height="26" rx="3" fill="{colour}"/>')
    text(key_x + 60, row, label)
    row += 44
row += 26
text(key_x, row, 'Peptide', 28, bold=True)
row += 44
parts.append(f'<rect x="{key_x}" y="{row - 22}" width="44" height="26" rx="3" fill="{TEAL}"/>')
text(key_x + 60, row, 'P1–P10')
row += 44
parts.append(f'<rect x="{key_x}" y="{row - 22}" width="44" height="26" rx="3" fill="{PINK}"/>')
text(key_x + 60, row, 'P6 (KRAS 12)')
row += 70
text(key_x, row, 'Close-ups', 28, bold=True)
row += 44
line(key_x, row - 9, key_x + 44, row - 9, INK, 3.5, '6 7')
text(key_x + 60, row, 'Contact ≤4.5 Å')
row += 44
line(key_x, row - 3, key_x + 44, row - 3, GOLD, 5)
text(key_x + 60, row, 'Screened patch')

parts.append('</svg>')
(out / 'fig.svg').write_text('\n'.join(parts))
for fmt in ['pdf', 'png']:
    subprocess.run(['rsvg-convert', '-f', fmt, '-o', str(out / f'fig.{fmt}'), str(out / 'fig.svg')], check=True)

receipt = json.loads((out / 'pymol-provenance.json').read_text())
receipt['build_command'] = 'python3 figures/jaxka-kras-pmhc-plddt/make.py'
tracked = ['make.py', 'render_pymol.py', 'compose.py', 'camera.json', 'groove-camera.json', 'panels.json',
           'fig.pdf', 'fig.svg', 'fig.png', 'aligned.pse']
files = [root / n for n in tracked[:3]] + [out / n for n in tracked[3:]]
files += [p for p in out.iterdir() if p.name.endswith(('-pymol.png', '-groove.png'))]
receipt['hashes'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(out / 'provenance.json').write_text(json.dumps(receipt, indent=2) + '\n')
