"""Stage 1: the three fixed tests on the 24 held-out pH 7 #3 seeds (odd seeds at each target pH), as written in kb/experiments/bf-moprp.md
before the runs. labels(), stays() and the return logic are copied from puf_transitions.py; measures() from puf_stage0.py.

Two checks run before any held-out frame is read, and the script stops if either fails:
  A. half-1 labels and tests recomputed from the stored measures must give the recorded 5/0, 0/5 and 2/8
  B. the even pH 7 #3 seeds, measured here from qc/whole.xtc, must match the stored measures frame by frame

Usage: puf_stage1.py <pca101_scores.npz> <puf_final.json> <puf_cvs_tight.npz> <cartesian_features.npz> <campaign_dir> <task_list> <out.json> <out.npz>"""
import json, sys, zipfile
from collections import Counter
from pathlib import Path
import numpy as np
from biotite.structure.io import load_structure
from biotraj import XTCTrajectoryFile
from scipy.stats import fisher_exact

scores, thr_file, cvs, feats, campaign, task_list, out_json, out_npz = sys.argv[1:9]
S = np.load(scores, allow_pickle=True); T = json.load(open(thr_file))["thresholds_nm"]; Z = np.load(cvs)
keys = [n[:-4] for n in zipfile.ZipFile(feats).namelist() if n != "feature_names.npy"]
rn = [str(s) for s in Z["rig_names"]]; DT = 0.1; STRIDE = 10
RUNS = Path(campaign) / "seeded_apo/runs"
BUILD = {ph: Path((Path(campaign) / f"{ph}-build-path.txt").read_text().strip()) for ph in ("ph4", "ph7")}
RES = np.arange(123, 224); inn = lambda a, b: (RES >= a) & (RES <= b)
nat = (S["ph4_center"] * S["ph4_scale"]).reshape(101, 3)
core = np.flatnonzero(inn(175, 187) | inn(201, 216))
RIG = {"b1": (127, 132), "loop": (133, 143), "a1": (144, 153), "a1N": (144, 148), "a1C": (149, 153), "b2": (154, 167), "a3C": (217, 223), "unit": (144, 167)}
ST = ["F", "ARM", "P1", "P2", "B1X", "CORE", "A3", "UNIT"]
COARSE = dict(F="F", ARM="ARM", P1="BAND", P2="BAND", B1X="BAND", CORE="LOBE", A3="A3", UNIT="UNIT"); CS = ["F", "ARM", "BAND", "LOBE", "A3", "UNIT"]
CMAP = np.array([CS.index(COARSE[s]) for s in ST])
SEG = [("b1", "b1_corefit"), ("loop", "loop_corefit"), ("a1N", "a1N_corefit")]


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


def labels(r):
    o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    lab = np.zeros(len(b1), int)
    lab[~b1 & un & ok] = 7; lab[~b1 & a3] = 6; lab[~b1 & ~ok] = 5; lab[b1] = 4
    lab[b1 & ~lp & ~a1n & ok] = 1; lab[b1 & lp & a1n & ok] = 2; lab[b1 & a1 & b2 & ok] = 3
    return lab


def stays(lab, n_state, w):
    c = np.stack([np.convolve(lab == k, np.ones(w), "same") for k in range(n_state)]); m = c.argmax(0)
    e = np.flatnonzero(np.diff(m)) + 1; st = np.r_[0, e]; ln = np.diff(np.r_[st, len(m)])
    keep = [(int(m[a]), int(a), int(l)) for a, l in zip(st, ln) if l >= w]
    out = []
    for s in keep:
        if out and out[-1][0] == s[0]:
            out[-1] = (s[0], out[-1][1], s[1] + s[2] - out[-1][1])
        else:
            out.append(s)
    return out


def returns(r, thr):
    t = {}
    for s, n in SEG:
        x = np.convolve(r[n], np.ones(10) / 10, "same"); below = x < thr[n]; hold = 50; ret = None
        if x[:20].mean() < thr[n]:
            t[s] = "start"; continue
        run_len = 0
        for i, b in enumerate(below):
            run_len = run_len + 1 if b else 0
            if run_len >= hold:
                ret = (i - hold + 1) * DT; break
        t[s] = ret
    return t


def summarise(r, thr):
    lab = labels(r); w = 10
    fine = stays(lab, 8, w); coarse = stays(CMAP[lab], len(CS), w)
    return dict(ret=returns(r, thr), end_fine=ST[fine[-1][0]], end_coarse=CS[coarse[-1][0]], start_coarse=CS[coarse[0][0]],
                occ={s: float((lab == i).mean()) for i, s in enumerate(ST)}, seq=[ST[s[0]] for s in fine])


def tests(rows):
    """rows[ph] -> list of summaries. Returns the fixed tests with the fine and coarse readings of test 3."""
    returned = lambda v, s: v["ret"][s] not in (None, "start")
    cnt = {
        "1 b1 returns (expect pH 4 > pH 7)": [sum(returned(v, "b1") for v in rows[p]) for p in ("ph4", "ph7")],
        "2 loop returns (expect pH 7 > pH 4)": [sum(returned(v, "loop") for v in rows[p]) for p in ("ph4", "ph7")],
        "3 ends in b1 alone, coarse stays (expect pH 7 > pH 4)": [sum(v["end_coarse"] == "ARM" for v in rows[p]) for p in ("ph4", "ph7")],
        "3 ends in b1 alone, fine stays (expect pH 7 > pH 4)": [sum(v["end_fine"] == "ARM" for v in rows[p]) for p in ("ph4", "ph7")],
        "a1N returns (not a fixed test)": [sum(returned(v, "a1N") for v in rows[p]) for p in ("ph4", "ph7")],
    }
    res = {}
    for k, (a, b) in cnt.items():
        n4, n7 = len(rows["ph4"]), len(rows["ph7"])
        res[k] = dict(ph4=a, ph7=b, n=[n4, n7], p=float(fisher_exact([[a, n4 - a], [b, n7 - b]])[1]))
    return res


def show(res):
    for k, v in res.items():
        print(f"  {k:58s} pH 4 {v['ph4']:2d}/{v['n'][0]}  pH 7 {v['ph7']:2d}/{v['n'][1]}  Fisher p {v['p']:.3f}", flush=True)


# stored half-1 frames
D = {}
for ph in ("ph4", "ph7"):
    r = {n: Z[f"{ph}_rig"][:, i].astype(float) for i, n in enumerate(rn)}
    D[ph] = dict(r=r, lab=labels(r), run=Z[f"{ph}_run"], src=Z[f"{ph}_src"], keys=[k for k in keys if k.startswith(ph + "__")])
thr = {n: float(np.percentile(np.concatenate([D[p]["r"][n][D[p]["lab"] == 0] for p in D]), 99)) for _, n in SEG}
print("return thresholds from half-1 Folded-like frames:", {k: round(v, 3) for k, v in thr.items()}, flush=True)

# check A
half1 = {}; stored = {}
for ph, d in D.items():
    half1[ph] = []
    for u in np.unique(d["run"][d["src"] == "ph7_3"]):
        ii = np.flatnonzero(d["run"] == u)
        if len(ii) < 500:
            continue
        rr = {n: v[ii] for n, v in d["r"].items()}; half1[ph].append(summarise(rr, thr)); stored[d["keys"][u]] = rr
print(f"\nCheck A, half 1 from stored measures, runs per pH {len(half1['ph4'])}, {len(half1['ph7'])}", flush=True)
t1 = tests(half1); show(t1)
got = [(t1[k]["ph4"], t1[k]["ph7"]) for k in list(t1)[:3]]
assert got == [(5, 0), (0, 5), (2, 8)], f"half-1 tests not reproduced: {got}"

# check B
idx = {}
for ph in ("ph4", "ph7"):
    t = load_structure(str(BUILD[ph] / "generated_gromacs/protein.gro"))
    idx[ph] = np.array([np.flatnonzero((t.atom_name == "CA") & (t.res_id == i))[0] for i in range(2, 103)])


def frames(entry):
    ph = entry.split("/")[0]
    with XTCTrajectoryFile(str(RUNS / entry / "qc/whole.xtc"), "r") as fh:
        xyz, tim, _, _ = fh.read(stride=STRIDE)
    return xyz[:, idx[ph]].astype(np.float64), np.asarray(tim, float)


worst = 0.0; nchk = 0
for k, rr in stored.items():
    X, _ = frames(k.replace("__", "/"))
    m = measures(X)
    assert len(m["core"]) == len(rr["core"]), (k, len(m["core"]), len(rr["core"]))
    worst = max(worst, max(float(np.abs(m[n] - rr[n]).max()) for n in rr)); nchk += 1
print(f"\nCheck B, {nchk} even seeds re-measured from whole.xtc: max |difference| from stored measures {worst:.2e} nm", flush=True)
assert worst < 1e-3, worst

# held-out runs
entries = Path(task_list).read_text().split(); assert len(entries) == 24, len(entries)
rows = {"ph4": [], "ph7": []}; names = {"ph4": [], "ph7": []}; save = {}
E = {p: np.zeros((8, 8), int) for p in rows}; dwell = {p: np.zeros(8) for p in rows}
for e in entries:
    ph = e.split("/")[0]; assert int(e[-2:]) % 2 == 1 and e.split("/")[1] == "ph7_3", e
    X, tim = frames(e)
    assert len(X) == 1001 and abs(tim[-1] - 100000) < 1 and abs(tim[1] - tim[0] - 100) < 1, (e, len(X), tim[:2], tim[-1])
    m = measures(X); s = summarise(m, thr); rows[ph].append(s); names[ph].append(e[-2:])
    ss = stays(labels(m), 8, 10)
    for a in ss:
        dwell[ph][a[0]] += a[2] * DT
    for a, b in zip(ss, ss[1:]):
        E[ph][a[0], b[0]] += 1
    save[e.replace("/", "__")] = np.column_stack([m[n] for n in rn]).astype(np.float32)

print("\nHeld-out runs: seed  b1/loop/a1N return ns (s started below, - never)  start > end (coarse)  end (fine)", flush=True)
fmt = lambda x: "s" if x == "start" else "-" if x is None else f"{x:.0f}"
for ph in rows:
    print(f" {ph}")
    for n, v in zip(names[ph], rows[ph]):
        print(f"  {n}  {fmt(v['ret']['b1']):>3s}/{fmt(v['ret']['loop']):>3s}/{fmt(v['ret']['a1N']):>3s}  {v['start_coarse']:>5s} > {v['end_coarse']:<5s} {v['end_fine']}", flush=True)
print("\nFixed tests, held-out set")
t2 = tests(rows); show(t2)
print("\nPooled, half 1 + held out, descriptive only")
pool = {p: half1[p] + rows[p] for p in rows}; t3 = tests(pool); show(t3)
print("\nOccupancy, mean % of frames per run, held out")
print("        " + "".join(f"{s:>7s}" for s in ST))
for p in rows:
    print(f"  {p}  " + "".join(f"{100 * np.mean([v['occ'][s] for v in rows[p]]):7.1f}" for s in ST))
print("Occupancy, half 1 pH 7 #3 seeds")
for p in rows:
    print(f"  {p}  " + "".join(f"{100 * np.mean([v['occ'][s] for v in half1[p]]):7.1f}" for s in ST))
print("\nEvents between 1 ns stays, held out (rows from, cols to)")
for p in rows:
    print(f" {p}  " + "".join(f"{s:>6s}" for s in ST) + "   dwell ns")
    for i, s in enumerate(ST):
        print(f"  {s:5s}" + "".join(f"{v:6d}" if v else f"{'.':>6s}" for v in E[p][i]) + f"  {dwell[p][i]:8.0f}")
    print(f"  runs reaching P1 {sum('P1' in v['seq'] for v in rows[p])}, P2 {sum('P2' in v['seq'] for v in rows[p])}, F {sum('F' in v['seq'] for v in rows[p])}", flush=True)
json.dump(dict(thresholds=thr, check_b_max_nm=worst, half1=t1, held_out=t2, pooled=t3, runs={p: dict(zip(names[p], rows[p])) for p in rows},
               events={p: E[p].tolist() for p in E}, dwell_ns={p: dwell[p].tolist() for p in dwell}, states=ST), open(out_json, "w"), indent=1, default=str)
np.savez_compressed(out_npz, rig_names=np.array(rn), **save)
print("done", flush=True)
