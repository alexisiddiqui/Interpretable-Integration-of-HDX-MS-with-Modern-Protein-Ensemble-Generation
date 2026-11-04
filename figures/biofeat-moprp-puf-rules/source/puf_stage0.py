"""Stage 0: project the rule variables onto the MI+PB frames, which have only ever been seen as PC scores. Cα of PrP 123-223 are read
from the pipeline's corrected.xtc; core-fit and self-fit RMSD follow puf_cvs.py (core 175-187, 201-216), thresholds from puf_final.json.
Reports the frames, walkers and time windows of each rule, as the seed pool for Stage 2.

Usage: puf_stage0.py <pca101_scores.npz> <puf_final.json> <campaign_dir> <out.npz>"""
import json, sys
from pathlib import Path
import numpy as np
from biotite.structure.io import load_structure
from biotraj import XTCTrajectoryFile
scores, thr, campaign, out = sys.argv[1:5]
S = np.load(scores, allow_pickle=True); meta = json.loads(str(S["meta"])); T = json.load(open(thr))["thresholds_nm"]
BUILD = {"ph4": "builds/moprp_ph4/e989dc85f669", "ph7": "builds/moprp_ph7/b2dd4eee2b73"}
RES = np.arange(123, 224); inn = lambda a, b: (RES >= a) & (RES <= b)
nat = (S["ph4_center"] * S["ph4_scale"]).reshape(101, 3)
core = np.flatnonzero(inn(175, 187) | inn(201, 216))
RIG = {"b1": (127, 132), "loop": (133, 143), "a1": (144, 153), "a1N": (144, 148), "a1C": (149, 153), "b2": (154, 167), "a3C": (217, 223), "unit": (144, 167)}


def kabsch(P, Q):
    pc, qc = P.mean(1, keepdims=True), Q.mean(0)
    H = np.einsum("nmi,mj->nij", P - pc, Q - qc); U, _, Vt = np.linalg.svd(H); d = np.sign(np.linalg.det(U @ Vt))
    D = np.zeros_like(H); D[:, 0, 0] = 1; D[:, 1, 1] = 1; D[:, 2, 2] = d
    return U @ D @ Vt, pc, qc


def measures(X):
    R, pc, qc = kabsch(X[:, core], nat[core]); Y = (X - pc) @ R + qc
    r = {"core": np.sqrt(((Y[:, core] - nat[core]) ** 2).sum(-1).mean(1))}
    for n, (a, b) in RIG.items():
        ix = np.flatnonzero(inn(a, b)); r[n + "_corefit"] = np.sqrt(((Y[:, ix] - nat[ix]) ** 2).sum(-1).mean(1))
        R2, p2, q2 = kabsch(X[:, ix], nat[ix]); r[n + "_selffit"] = np.sqrt((((X[:, ix] - p2) @ R2 + q2 - nat[ix]) ** 2).sum(-1).mean(1))
    return r


save = {}
for ph in ("ph4", "ph7"):
    key = f"{ph}_mmpb"; t = load_structure(str(Path(campaign) / BUILD[ph] / "generated_gromacs/protein.gro"))
    ca = np.flatnonzero((t.atom_name == "CA") & (t.res_id >= 2) & (t.res_id <= 102)); assert len(ca) == 101, len(ca)
    seg, frame, rep, tim = S[f"{key}_seg"], S[f"{key}_frame"], S[f"{key}_replica"], S[f"{key}_time"]; sc = S[key]
    acc = {}
    for s in np.unique(seg):
        rows = np.flatnonzero(seg == s)
        with XTCTrajectoryFile(meta[key]["segments"][int(s)], "r") as fh:
            xyz = fh.read()[0]
        X = xyz[frame[rows]][:, ca, :].astype(np.float64)
        m = measures(X)
        for k, v in m.items():
            acc.setdefault(k, np.zeros(len(seg)))[rows] = v
        print(ph, "segment", int(s), len(rows), "frames", flush=True)
    r = acc; o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    print(f"\n=== {ph} MI+PB: {len(seg)} frames, walkers {np.unique(rep).tolist()}; Folded circle check, mean b1 core-fit near (12,-20): {r['b1_corefit'][np.hypot(sc[:,0]-12, sc[:,1]+20) < 10].mean():.2f}; near (92,42): {r['b1_corefit'][np.hypot(sc[:,0]-92, sc[:,1]-42) < 10].mean():.2f}")
    rules = {"b1 alone": b1 & ~lp & ~a1n & ok, "PUF1 cand (b1+loop+a1N)": b1 & lp & a1n & ok, "PUF1 text (b1+loop+a3C)": b1 & lp & a3 & ok, "b1+loop+a1N+a3C": b1 & lp & a1n & a3 & ok, "unit off, b1 kept": un & ~b1 & ok, "a3C off, b1 kept": a3 & ~b1, "core distorted": ~ok}
    for tb in (T["b2_corefit"], .30, .35, .50):
        b2 = r["b2_corefit"] > tb
        rules[f"PUF2 cand b2>{tb:.2f}"] = b1 & a1 & b2 & ok; rules[f"a1+b2 off, b1 kept, b2>{tb:.2f}"] = a1 & b2 & ~b1 & ok
    for n, m in rules.items():
        if m.sum():
            per = {int(w): int((m & (rep == w)).sum()) for w in np.unique(rep[m])}; tt = tim[m] / 1000
            win = len(np.unique((tt // 5).astype(int) + 100000 * rep[m]))
            print(f"  {n:34s} {m.sum():6d} frames  walkers {per}  distinct 5 ns windows {win:4d}  median PC ({np.median(sc[m,0]):.0f},{np.median(sc[m,1]):.0f})  b2 {r['b2_corefit'][m].mean():.2f}  a1 {r['a1_corefit'][m].mean():.2f}  a3C {r['a3C_corefit'][m].mean():.2f}", flush=True)
        else:
            print(f"  {n:34s}      0 frames", flush=True)
    save.update({f"{ph}_{k}": v.astype(np.float32) for k, v in r.items()}); save[f"{ph}_pc"] = sc; save[f"{ph}_rep"] = rep; save[f"{ph}_time"] = tim
np.savez_compressed(out, **save)
print("done", flush=True)
