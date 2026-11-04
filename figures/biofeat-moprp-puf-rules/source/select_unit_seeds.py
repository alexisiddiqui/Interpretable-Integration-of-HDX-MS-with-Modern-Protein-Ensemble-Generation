"""Stage 2b seeds: 12 unit-off frames from the MI+PB ensembles, six per source pH, by the rule fixed in kb/experiments/bf-moprp.md. Frame reading and
PDB writing follow select_seeds.py. Each written frame is measured again from its coordinates and must carry the unit-off label.

Usage: select_unit_seeds.py <figures_dir> <pca101_scores.npz> <puf_final.json> <puf_stage0_mipb.npz> <out_dir> <manifest.json>"""
import json, sys
from pathlib import Path
import numpy as np
from biotite.structure.io import load_structure, save_structure
from biotraj import XTCTrajectoryFile

figures, scores, thr_file, stage0, out, manifest_path = map(Path, sys.argv[1:7])
sys.path.insert(0, str(figures))
from campaign_paths import BUILDS  # noqa: E402
S = np.load(scores, allow_pickle=True); meta = json.loads(str(S["meta"])); T = json.load(open(thr_file))["thresholds_nm"]; M = np.load(stage0)
rng = np.random.default_rng(20261104); TERMINI = {"NGLY": "GLY", "CSER": "SER"}
N, MIN_BLOCK, GAP_NS, SEP_NS = 6, 20, 2.0, 5.0
RES = np.arange(123, 224); inn = lambda a, b: (RES >= a) & (RES <= b)
nat = (S["ph4_center"] * S["ph4_scale"]).reshape(101, 3); core = np.flatnonzero(inn(175, 187) | inn(201, 216)); unit = np.flatnonzero(inn(144, 167))
assert not out.exists() or not any(out.iterdir()), out
out.mkdir(parents=True, exist_ok=True)


def unit_rmsd(x):
    p, q = x[core] - x[core].mean(0), nat[core] - nat[core].mean(0)
    U, _, Vt = np.linalg.svd(p.T @ q); d = np.sign(np.linalg.det(U @ Vt)); R = U @ np.diag([1, 1, d]) @ Vt
    y = (x - x[core].mean(0)) @ R + nat[core].mean(0)
    return float(np.sqrt(((y[unit] - nat[unit]) ** 2).sum(-1).mean()))


manifest = []; k = 0
for tag, ph in (("ph4", "pH 4"), ("ph7", "pH 7")):
    key = f"{tag}_mmpb"; rep, tim, seg, frame = S[f"{key}_replica"], S[f"{key}_time"], S[f"{key}_seg"], S[f"{key}_frame"]
    assert np.array_equal(rep, M[f"{tag}_rep"]) and np.array_equal(tim, M[f"{tag}_time"])
    r = lambda n: M[f"{tag}_{n}"]; o = lambda n: r(n) > T[n]
    lab = o("unit_corefit") & ~o("b1_corefit") & (r("core") <= T["core"]) & ~(o("a3C_corefit") | o("a3C_selffit"))
    med = float(np.median(r("unit_corefit")[lab])); blocks = {}
    for w in np.unique(rep[lab]):
        ii = np.flatnonzero(lab & (rep == w)); ii = ii[np.argsort(tim[ii])]
        parts = np.split(ii, np.flatnonzero(np.diff(tim[ii]) / 1000 > GAP_NS) + 1)
        good = sorted([b for b in parts if len(b) >= MIN_BLOCK and (r("unit_corefit")[b] >= med).any()], key=len, reverse=True)
        if good:
            blocks[int(w)] = good
    print(f"{tag}: label {int(lab.sum())} frames, median unit {med:.3f}, usable blocks per walker", {w: [len(b) for b in v] for w, v in blocks.items()}, flush=True)
    picks = []; turn = {w: 0 for w in blocks}
    while len(picks) < N:
        progress = False
        for w in sorted(blocks):
            if len(picks) == N:
                break
            n_b = len(blocks[w])
            for step in range(n_b):
                b = blocks[w][(turn[w] + step) % n_b]
                c = [i for i in b[r("unit_corefit")[b] >= med] if all(rep[p] != w or abs(tim[i] - tim[p]) / 1000 >= SEP_NS for p in picks)]
                if c:
                    picks.append(int(rng.choice(c))); turn[w] += step + 1; progress = True
                    break
        assert progress, f"{tag}: only {len(picks)} frames satisfy the rule"
    template = load_structure(BUILDS[ph] / "generated_gromacs/protein.gro"); heavy = template.element != "H"
    ca = np.array([np.flatnonzero((template.atom_name == "CA") & (template.res_id == i))[0] for i in range(2, 103)])
    for row in sorted(picks, key=lambda i: (rep[i], tim[i])):
        path = meta[key]["segments"][int(seg[row])]
        with XTCTrajectoryFile(path, "r") as fh:
            fh.seek(int(frame[row])); xyz, t_ps, _, _ = fh.read(n_frames=1)
        assert abs(float(t_ps[0]) - float(tim[row])) < 1e-3, (path, frame[row])
        u = unit_rmsd(xyz[0][ca].astype(float)); assert abs(u - float(r("unit_corefit")[row])) < 1e-3 and u > T["unit_corefit"], (u, r("unit_corefit")[row])
        model = template.copy(); model.coord = xyz[0] * 10.0; model.chain_id[:] = "A"
        model.res_name = np.array([TERMINI.get(x, x) for x in model.res_name])
        f = out / f"seed_{k:02d}.pdb"; save_structure(f, model[heavy])
        manifest.append(dict(seed=k, ph_source=ph, source_trajectory=path, frame=int(frame[row]), time_ps=float(tim[row]), walker=int(rep[row]),
                             pc=[round(float(v), 2) for v in S[key][row]], unit_nm=round(u, 3), a1N_nm=round(float(r("a1N_corefit")[row]), 3), b1_nm=round(float(r("b1_corefit")[row]), 3)))
        print(f" seed_{k:02d} {tag} walker {int(rep[row])} t {float(tim[row]) / 1000:7.2f} ns unit {u:.3f} a1N {float(r('a1N_corefit')[row]):.2f} b1 {float(r('b1_corefit')[row]):.2f} PC ({S[key][row][0]:.0f},{S[key][row][1]:.0f})", flush=True)
        k += 1
manifest_path.write_text(json.dumps(manifest, indent=1)); print("wrote", manifest_path, len(manifest), flush=True)
