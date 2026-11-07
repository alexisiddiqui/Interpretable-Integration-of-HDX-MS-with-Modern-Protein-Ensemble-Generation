"""Stage 2b: the fixed tests on the 12 unit-off seed pairs, as written in kb/experiments/bf-moprp.md before the runs. measures(), labels(), stays(),
frames(), compare() and bh() are copied from puf_stage1.py and puf_stage1b.py, which run on import and so cannot be imported.

Checks, all before any test is computed, and the script stops if one fails:
  A. a held-out pH 7 #3 run, measured here from qc/whole.xtc, must match its stored measures in puf_stage1_rig.npz frame by frame
  B. seed NN must have the same backbone at both target pH, and its unit RMSD must match the seed manifest
  C. run integrity: 1001 frames to 100 ns at 100 ps, no LINCS or SETTLE warnings, no bond at or above 0.30 nm in any 10 ps frame

Primary, Benjamini-Hochberg across the two: unit-off occupancy and mean unit core-fit RMSD, each expected higher at pH 4.
Secondary, no claim: unit-off exit rate, Folded-like > unit-off rate, unit-off occupancy at 0.50 nm, Folded-like occupancy, core-distorted occupancy,
mean a1N core-fit RMSD. Statistic pH 4 minus pH 7 on pooled values, two-sided exact sign-flip over the 12 pairs, intervals from resampled pairs.
Outcome: supported if a primary has q < 0.05 in the expected direction and the other has the same direction; not supported if the 95 % interval on the
pH 4 / pH 7 occupancy ratio lies below 2; otherwise inconclusive. Everything after the outcome line is descriptive and carries no claim.

Usage: puf_stage2b.py <pca101_scores.npz> <puf_final.json> <puf_stage1_rig.npz> <campaign_dir> <out.json> <out.npz>"""
import json, sys
from pathlib import Path
import numpy as np
from biotite.structure.io import load_structure
from biotraj import XTCTrajectoryFile
from biofeaturisers.examples.PLUMED.topology_pipeline.analysis.trajectory import topology_bonds

scores, thr_file, rig, campaign, out_json, out_npz = sys.argv[1:7]
S = np.load(scores, allow_pickle=True); T0 = json.load(open(thr_file))["thresholds_nm"]; H = np.load(rig)
rn = [str(s) for s in H["rig_names"]]; DT = 0.1; STRIDE = 10; rng = np.random.default_rng(20261105)
HERE = Path(campaign) / "seeded_apo"; RUNS = HERE / "runs"; MAN = json.load(open(HERE / "seeds_unit_off_manifest.json"))
BUILD = {ph: Path((Path(campaign) / f"{ph}-build-path.txt").read_text().strip()) for ph in ("ph4", "ph7")}
RES = np.arange(123, 224); inn = lambda a, b: (RES >= a) & (RES <= b)
nat = (S["ph4_center"] * S["ph4_scale"]).reshape(101, 3)
core = np.flatnonzero(inn(175, 187) | inn(201, 216))
RIG = {"b1": (127, 132), "loop": (133, 143), "a1": (144, 153), "a1N": (144, 148), "a1C": (149, 153), "b2": (154, 167), "a3C": (217, 223), "unit": (144, 167)}
ST = ["F", "ARM", "P1", "P2", "B1X", "CORE", "A3", "UNIT"]; F, CORE, UNIT = 0, 5, 7
OCC, RMS = "unit-off occupancy, %", "unit RMSD, nm"; PRIMARY = (OCC, RMS)


def kabsch(P, Q):
    pc, qc = P.mean(1, keepdims=True), Q.mean(0)
    Hm = np.einsum("nmi,mj->nij", P - pc, Q - qc); U, _, Vt = np.linalg.svd(Hm); d = np.sign(np.linalg.det(U @ Vt))
    D = np.zeros_like(Hm); D[:, 0, 0] = 1; D[:, 1, 1] = 1; D[:, 2, 2] = d
    return U @ D @ Vt, pc, qc


def measures(X):
    R, pc, qc = kabsch(X[:, core], nat[core]); Y = (X - pc) @ R + qc
    r = {"core": np.sqrt(((Y[:, core] - nat[core]) ** 2).sum(-1).mean(1))}
    for n, (a, b) in RIG.items():
        ix = np.flatnonzero(inn(a, b)); r[n + "_corefit"] = np.sqrt(((Y[:, ix] - nat[ix]) ** 2).sum(-1).mean(1))
        R2, p2, q2 = kabsch(X[:, ix], nat[ix]); r[n + "_selffit"] = np.sqrt((((X[:, ix] - p2) @ R2 + q2 - nat[ix]) ** 2).sum(-1).mean(1))
    return r


def labels(r, T):
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


def events(lab, w):
    f = stays(lab, 8, w); dw = np.zeros(8); E = np.zeros((8, 8))
    for s in f:
        dw[s[0]] += s[2] * DT
    for a, b in zip(f, f[1:]):
        E[a[0], b[0]] += 1
    return f, dw, E


def metrics(r, w):
    """Numerator and denominator of each measure for one run, so that pooled values are sums over runs."""
    lab = labels(r, T0); lab50 = labels(r, dict(T0, unit_corefit=.50)); _, dw, E = events(lab, w)
    return {OCC: (100 * (lab == UNIT).mean(), 1.0), RMS: (r["unit_corefit"].mean(), 1.0),
            "unit-off exit rate, /us": (1000 * E[UNIT].sum(), dw[UNIT]), "Folded-like > unit-off, /us": (1000 * E[F, UNIT], dw[F]),
            "unit-off occupancy at 0.50 nm, %": (100 * (lab50 == UNIT).mean(), 1.0), "Folded-like occupancy, %": (100 * (lab == F).mean(), 1.0),
            "core-distorted occupancy, %": (100 * (lab == CORE).mean(), 1.0), "a1N RMSD, nm": (r["a1N_corefit"].mean(), 1.0)}


def compare(pairs, w):
    """pairs: list of (run at pH 4, run at pH 7). Returns measure -> pH 4, pH 7, difference, 95 % interval, p."""
    M4 = [metrics(a, w) for a, _ in pairs]; M7 = [metrics(b, w) for _, b in pairs]; n = len(pairs); res = {}
    flips = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(bool); boot = rng.integers(0, n, (5000, n))
    ratio = lambda a, b: np.divide(a, b, out=np.zeros_like(a, dtype=float), where=b > 0)
    for k in M4[0]:
        n4, d4 = np.array([m[k] for m in M4], float).T; n7, d7 = np.array([m[k] for m in M7], float).T
        v4, v7 = n4.sum() / max(d4.sum(), 1e-12), n7.sum() / max(d7.sum(), 1e-12); obs = v4 - v7
        pn4, pd4 = np.where(flips, n7, n4).sum(1), np.where(flips, d7, d4).sum(1)
        pn7, pd7 = np.where(flips, n4, n7).sum(1), np.where(flips, d4, d7).sum(1)
        perm = ratio(pn4, pd4) - ratio(pn7, pd7); p = float((np.abs(perm) >= abs(obs) - 1e-9).mean())
        b = ratio(n4[boot].sum(1), d4[boot].sum(1)) - ratio(n7[boot].sum(1), d7[boot].sum(1))
        res[k] = dict(ph4=float(v4), ph7=float(v7), diff=float(obs), lo=float(np.percentile(b, 2.5)), hi=float(np.percentile(b, 97.5)), p=p)
    return res


def bh(res):
    k = list(res); p = np.array([res[x]["p"] for x in k]); o = np.argsort(p); q = np.empty(len(p)); run = 1.0
    for rank, i in zip(range(len(p), 0, -1), o[::-1]):
        run = min(run, p[i] * len(p) / rank); q[i] = run
    for x, v in zip(k, q):
        res[x]["q"] = float(v)


def occ_ratio(pairs):
    """pH 4 / pH 7 unit-off occupancy with a pair-bootstrap interval. A resample with no pH 7 occupancy has an infinite ratio, which sorts to the top."""
    o = np.array([[(labels(a, T0) == UNIT).mean(), (labels(b, T0) == UNIT).mean()] for a, b in pairs]); n = len(o)
    idx = rng.integers(0, n, (20000, n)); s4, s7 = o[idx, 0].sum(1), o[idx, 1].sum(1)
    with np.errstate(divide="ignore", invalid="ignore"):
        r = s4 / s7
    undefined = int(np.isnan(r).sum()); r = np.sort(r[~np.isnan(r)])
    return dict(ratio=float(o[:, 0].sum() / o[:, 1].sum()) if o[:, 1].sum() else float("inf"), lo=float(r[int(.025 * len(r))]), hi=float(r[int(.975 * len(r))]),
                undefined_resamples=undefined)


idx = {}; bonds = {}
for ph in ("ph4", "ph7"):
    t = load_structure(str(BUILD[ph] / "generated_gromacs/protein.gro"))
    idx[ph] = np.array([np.flatnonzero((t.atom_name == "CA") & (t.res_id == i))[0] for i in range(2, 103)])
    bonds[ph] = topology_bonds(BUILD[ph] / "generated_gromacs/protein.top")


def read(entry, stride):
    with XTCTrajectoryFile(str(RUNS / entry / "qc/whole.xtc"), "r") as fh:
        xyz, tim, _, _ = fh.read(stride=stride)
    return np.asarray(xyz), np.asarray(tim, float)


def frames(entry):
    xyz, tim = read(entry, STRIDE)
    return xyz[:, idx[entry.split("/")[0]]].astype(np.float64), tim


# check A
k = "ph4__ph7_3__seed_01"; m = measures(frames(k.replace("__", "/"))[0]); stored = {n: H[k][:, i].astype(float) for i, n in enumerate(rn)}
worst = max(float(np.abs(m[n] - stored[n]).max()) for n in rn)
print(f"Check A, {k} re-measured: max |difference| from stored measures {worst:.2e} nm", flush=True)
assert worst < 1e-3, worst

# check B
worst_ca = worst_unit = 0.0
for e in MAN:
    s = f"seed_{e['seed']:02d}"; c = []
    for ph in ("ph4", "ph7"):
        t = load_structure(str(RUNS / ph / "unit_off" / s / "protein.gro")); c.append(np.array([t.coord[(t.atom_name == "CA") & (t.res_id == i)][0] for i in range(2, 103)]))
    worst_ca = max(worst_ca, float(np.abs(c[0] - c[1]).max()))
    r0 = measures(c[0][None].astype(np.float64) / 10); worst_unit = max(worst_unit, abs(float(r0["unit_corefit"][0]) - e["unit_nm"]))
print(f"Check B, 12 seeds: max |CA difference| between pH values {worst_ca:.3f} (structure file units); max |unit RMSD - manifest| {worst_unit:.4f} nm", flush=True)
assert worst_ca < .05, "seeds are not paired"
assert worst_unit < .002, "seed structures do not match the manifest"

# check C and measures
runs = {}; max_bond = 0.0; warnings = 0
for ph in ("ph4", "ph7"):
    for e in MAN:
        s = f"seed_{e['seed']:02d}"; entry = f"{ph}/unit_off/{s}"; xyz, tim = read(entry, 1)
        assert len(xyz) == 10001 and abs(tim[-1] - 100000) < 1 and abs(tim[1] - tim[0] - 10) < 1e-3, (entry, len(xyz), tim[:2], tim[-1])
        max_bond = max(max_bond, float(np.linalg.norm(xyz[:, bonds[ph][:, 0]] - xyz[:, bonds[ph][:, 1]], axis=2).max()))
        warnings += sum(int(a) + int(b) for _, a, b in (l.split() for l in (RUNS / entry / "qc/lincs.txt").read_text().splitlines()))
        X = xyz[::STRIDE, idx[ph]].astype(np.float64); assert len(X) == 1001, len(X)
        runs[entry] = measures(X)
print(f"Check C, 24 runs of 1001 frames: LINCS and SETTLE warnings {warnings}; max bond {max_bond:.3f} nm", flush=True)
assert warnings == 0 and max_bond < .30, (warnings, max_bond)

seeds = [f"seed_{e['seed']:02d}" for e in MAN]; pairs = [(runs[f"ph4/unit_off/{s}"], runs[f"ph7/unit_off/{s}"]) for s in seeds]
R = compare(pairs, 10); P = {k: R[k] for k in PRIMARY}; bh(P); ratio = occ_ratio(pairs)
print(f"\nFixed tests, 12 pairs, 1 ns stays. Statistic pH 4 minus pH 7.\n{'measure':36s}{'pH4':>9s}{'pH7':>9s}{'diff':>9s}{'95% interval':>20s}{'p':>8s}{'q':>8s}")
for k, v in R.items():
    print(f"{k:36s}{v['ph4']:9.3f}{v['ph7']:9.3f}{v['diff']:9.3f}  [{v['lo']:8.3f},{v['hi']:8.3f}]{v['p']:8.4f}" + (f"{v['q']:8.4f}" if k in P else f"{'':8s}") + ("  primary" if k in P else ""), flush=True)
print(f"\npH 4 / pH 7 unit-off occupancy ratio {ratio['ratio']:.2f}, 95 % interval [{ratio['lo']:.2f}, {ratio['hi']:.2f}], undefined resamples {ratio['undefined_resamples']}", flush=True)
sup = any(v["q"] < .05 and v["diff"] > 0 for v in P.values()) and all(v["diff"] > 0 for v in P.values()); notsup = ratio["hi"] < 2
outcome = "both rules met, report as such" if sup and notsup else "supported" if sup else "not supported" if notsup else "inconclusive"
print(f"OUTCOME under the fixed rule: {outcome}", flush=True)

print("\nDescriptive from here, no claim.\n\nPer pair: seed source walker | occupancy % pH 4, pH 7 | unit RMSD pH 4, pH 7 | mean Folded-like % pH 4, pH 7 | unit-off stays pH 4, pH 7")
per = []
for e, s, (a, b) in zip(MAN, seeds, pairs):
    la, lb = labels(a, T0), labels(b, T0); sa, sb = stays(la, 8, 10), stays(lb, 8, 10); row = dict(seed=s, source=e["ph_source"], walker=e["walker"],
        occ=[100 * float((la == UNIT).mean()), 100 * float((lb == UNIT).mean())], unit=[float(a["unit_corefit"].mean()), float(b["unit_corefit"].mean())],
        folded=[100 * float((la == F).mean()), 100 * float((lb == F).mean())], stays=[sum(x[0] == UNIT for x in sa), sum(x[0] == UNIT for x in sb)]); per.append(row)
    print(f"  {s} {e['ph_source']} w{e['walker']} | {row['occ'][0]:5.1f} {row['occ'][1]:5.1f} | {row['unit'][0]:.3f} {row['unit'][1]:.3f} | {row['folded'][0]:5.1f} {row['folded'][1]:5.1f} | {row['stays'][0]:2d} {row['stays'][1]:2d}", flush=True)

print("\nBy seed source, no test: pH 4, pH 7")
strata = {}
for name in ("pH 4", "pH 7"):
    sel = [p for e, p in zip(MAN, pairs) if e["ph_source"] == name]; o = [[100 * (labels(x, T0) == UNIT).mean() for x in p] for p in sel]; u = [[x["unit_corefit"].mean() for x in p] for p in sel]
    strata[name] = dict(occ=np.mean(o, 0).tolist(), unit=np.mean(u, 0).tolist()); print(f"  source {name}, {len(sel)} pairs: occupancy {strata[name]['occ'][0]:.1f}, {strata[name]['occ'][1]:.1f} %; unit RMSD {strata[name]['unit'][0]:.3f}, {strata[name]['unit'][1]:.3f} nm", flush=True)

print("\nBy 10 ns bin, mean over 12 runs: unit-off % pH 4/pH 7, unit RMSD pH 4/pH 7, Folded-like % pH 4/pH 7")
bins = []
for b in range(10):
    sl = slice(b * 100, (b + 1) * 100); v = []
    for f in (lambda r: 100 * (labels(r, T0)[sl] == UNIT).mean(), lambda r: r["unit_corefit"][sl].mean(), lambda r: 100 * (labels(r, T0)[sl] == F).mean()):
        v.append([float(np.mean([f(x) for x, _ in pairs])), float(np.mean([f(y) for _, y in pairs]))])
    bins.append(v); print(f"  {b * 10:3d}-{b * 10 + 10:<4d} {v[0][0]:5.1f}/{v[0][1]:5.1f}   {v[1][0]:.3f}/{v[1][1]:.3f}   {v[2][0]:5.1f}/{v[2][1]:5.1f}", flush=True)

print("\nAll states, mean % of frames per run")
print("        " + "".join(f"{s:>7s}" for s in ST)); occ = {}
for i, ph in enumerate(("ph4", "ph7")):
    occ[ph] = [100 * float(np.mean([(labels(p[i], T0) == k).mean() for p in pairs])) for k in range(8)]; print(f"  {ph}  " + "".join(f"{x:7.1f}" for x in occ[ph]))
print("\nEvents between 1 ns stays (rows from, cols to)"); ev = {}
for i, ph in enumerate(("ph4", "ph7")):
    E = np.zeros((8, 8)); dw = np.zeros(8); ns = 0; first = []
    for p in pairs:
        f, d, e = events(labels(p[i], T0), 10); E += e; dw += d; ns += sum(x[0] == UNIT for x in f); first.append(ST[f[0][0]])
    ev[ph] = dict(events=E.astype(int).tolist(), dwell_ns=dw.tolist(), unit_stays=int(ns), first_state=first)
    print(f" {ph}  " + "".join(f"{s:>6s}" for s in ST) + "   dwell ns")
    for a, s in enumerate(ST):
        print(f"  {s:5s}" + "".join(f"{int(v):6d}" if v else f"{'.':>6s}" for v in E[a]) + f"  {dw[a]:8.1f}")
    print(f"  unit-off stays {ns}, mean length {dw[UNIT] / max(ns, 1):.1f} ns; first state per run {first}", flush=True)
print("\nStay-length sensitivity for the two rates: 0.5 ns, 2 ns: diff (p)")
sens = {"0.5 ns": compare(pairs, 5), "2 ns": compare(pairs, 20)}
for k in ("unit-off exit rate, /us", "Folded-like > unit-off, /us"):
    print(f"  {k:32s}" + "".join(f"{sens[n][k]['diff']:10.1f} ({sens[n][k]['p']:.3f})" for n in sens), flush=True)

json.dump(dict(check_a_max_nm=worst, check_b_max_ca=worst_ca, check_b_max_unit_nm=worst_unit, check_c=dict(warnings=warnings, max_bond_nm=max_bond), results=R, primary=P, occupancy_ratio=ratio,
               outcome=outcome, per_pair=per, by_source=strata, bins_10ns=bins, occupancy=occ, events=ev, sensitivity=sens, states=ST), open(out_json, "w"), indent=1)
np.savez_compressed(out_npz, rig_names=np.array(rn), **{k.replace("/", "__"): np.column_stack([v[n] for n in rn]).astype(np.float32) for k, v in runs.items()})
print("done", flush=True)
