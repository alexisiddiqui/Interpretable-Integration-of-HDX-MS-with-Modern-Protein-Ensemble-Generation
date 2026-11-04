"""Frame-based pH comparison of the band runs, replacing the yes/no return tests of puf_stage1.py, which discard most of the information for
transient states. The measures below were fixed before any of them was computed.

Unit of analysis: the seed pair. Seed NN at pH 4 and at pH 7 start from the same MI+PB frame (checked here), so pH is compared within pairs.
Run-to-run correlation in time is never assumed away, because every uncertainty resamples whole pairs.

Family, 22 measures, statistic pH 4 minus pH 7 over the pooled runs:
  occupancy of b1 alone, PUF1 candidate, PUF2 candidate, b1+partial (4)
  exit rate of the same four states, exits / committed time, the estimator that allows for stays cut off by the run ends (4)
  band -> b1 alone and b1 alone -> band rates, coarse states (2)
  PUF1 -> PUF2 and PUF2 -> PUF1 rates (2)
  mean core-fit RMSD of b1, loop, a1N, a1C, b2 over the whole run and over 50-100 ns (10)

Primary set: the 12 held-out pairs, exact sign-flip test (4096 relabellings), Benjamini-Hochberg at 0.05 over the family. Half 1 suggested the
earlier hypothesis, so it is shown for direction and the 24 pairs together are supporting evidence only (20000 random relabellings).
Sensitivity, primary set: stays of 0.5 and 2 ns, and the PUF2 candidate at b2 > 0.30 nm.

Usage: puf_stage1b.py <puf_final.json> <puf_cvs_tight.npz> <cartesian_features.npz> <puf_stage1_rig.npz> <runs_root> <out.json>"""
import json, sys, zipfile
from pathlib import Path
import numpy as np
from biotite.structure.io import load_structure

thr_file, cvs, feats, rig, runs_root, out_json = sys.argv[1:7]
T0 = json.load(open(thr_file))["thresholds_nm"]; Z = np.load(cvs); H = np.load(rig)
keys = [n[:-4] for n in zipfile.ZipFile(feats).namelist() if n != "feature_names.npy"]
rn = [str(s) for s in Z["rig_names"]]; DT = 0.1; RUNS = Path(runs_root); rng = np.random.default_rng(20261104)
ST = ["F", "ARM", "P1", "P2", "B1X", "CORE", "A3", "UNIT"]; CS = ["F", "ARM", "BAND", "LOBE", "A3", "UNIT"]
CMAP = np.array([0, 1, 2, 2, 2, 3, 4, 5]); SEGS = ["b1", "loop", "a1N", "a1C", "b2"]; A, P1, P2, BX = 1, 2, 3, 4


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


def metrics(r, w, b2):
    """Numerator and denominator of each measure for one run, so that pooled values are sums over runs."""
    T = dict(T0, b2_corefit=b2); lab = labels(r, T); f = stays(lab, 8, w); c = stays(CMAP[lab], len(CS), w); m = {}
    dw = np.zeros(8); ex = np.zeros(8); E = np.zeros((8, 8))
    for s in f:
        dw[s[0]] += s[2] * DT
    for a, b in zip(f, f[1:]):
        ex[a[0]] += 1; E[a[0], b[0]] += 1
    cdw = np.zeros(len(CS)); cE = np.zeros((len(CS), len(CS)))
    for s in c:
        cdw[s[0]] += s[2] * DT
    for a, b in zip(c, c[1:]):
        cE[a[0], b[0]] += 1
    for i, n in ((A, "b1 alone"), (P1, "PUF1 cand"), (P2, "PUF2 cand"), (BX, "b1+partial")):
        m[f"occupancy {n}, %"] = (100 * (lab == i).mean(), 1.0)
    for i, n in ((A, "b1 alone"), (P1, "PUF1 cand"), (P2, "PUF2 cand"), (BX, "b1+partial")):
        m[f"exit rate {n}, /us"] = (1000 * ex[i], dw[i])
    m["band > b1 alone, /us"] = (1000 * cE[2, 1], cdw[2]); m["b1 alone > band, /us"] = (1000 * cE[1, 2], cdw[1])
    m["PUF1 > PUF2, /us"] = (1000 * E[P1, P2], dw[P1]); m["PUF2 > PUF1, /us"] = (1000 * E[P2, P1], dw[P2])
    for s in SEGS:
        x = r[s + "_corefit"]; m[f"{s} RMSD all, nm"] = (x.mean(), 1.0)
    for s in SEGS:
        x = r[s + "_corefit"]; m[f"{s} RMSD 50-100 ns, nm"] = (x[500:].mean(), 1.0)
    return m


def compare(pairs, w, b2, n_perm=20000):
    """pairs: list of (run at pH 4, run at pH 7). Returns measure -> pH 4, pH 7, difference, 95 % interval, p."""
    M4 = [metrics(a, w, b2) for a, _ in pairs]; M7 = [metrics(b, w, b2) for _, b in pairs]; n = len(pairs); res = {}
    if n <= 14:
        flips = ((np.arange(2 ** n)[:, None] >> np.arange(n)) & 1).astype(bool)
    else:
        flips = rng.random((n_perm, n)) < .5; flips[0] = False
    boot = rng.integers(0, n, (5000, n))
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


# runs
stored = {}
for ph in ("ph4", "ph7"):
    r = {n: Z[f"{ph}_rig"][:, i].astype(float) for i, n in enumerate(rn)}; run, src = Z[f"{ph}_run"], Z[f"{ph}_src"]
    ks = [k for k in keys if k.startswith(ph + "__")]
    for u in np.unique(run[src == "ph7_3"]):
        ii = np.flatnonzero(run == u)
        if len(ii) >= 500:
            stored[ks[u]] = {n: v[ii] for n, v in r.items()}
held = {k: {n: H[k][:, i].astype(float) for i, n in enumerate(rn)} for k in H.files if k != "rig_names"}
seeds = lambda d: sorted({k.split("__")[-1] for k in d if k.startswith("ph4__")})
pairs_of = lambda d: [(d[f"ph4__ph7_3__{s}"], d[f"ph7__ph7_3__{s}"]) for s in seeds(d)]
h1, h2 = pairs_of(stored), pairs_of(held); print("pairs: half 1", len(h1), "held out", len(h2), "frames", len(h1[0][0]["core"]), len(h2[0][0]["core"]), flush=True)
assert len(h1) == 12 and len(h2) == 12

# pairing check: the seed's backbone at the two pH values, from the seed structure written before any simulation
worst = 0.0
for s in seeds(stored) + seeds(held):
    c = []
    for ph in ("ph4", "ph7"):
        t = load_structure(str(RUNS / ph / "ph7_3" / s / "protein.gro")); c.append(t.coord[t.atom_name == "CA"])
    worst = max(worst, float(np.abs(c[0] - c[1]).max()))
print(f"pairing check, max |CA difference| between pH 4 and pH 7 protein.gro of the same seed, 24 seeds: {worst:.3f} (structure file units)", flush=True)
assert worst < 0.05, "seeds are not paired"

P = compare(h2, 10, T0["b2_corefit"]); bh(P); A1 = compare(h1, 10, T0["b2_corefit"]); ALL = compare(h1 + h2, 10, T0["b2_corefit"]); bh(ALL)
print("\nPrimary, 12 held-out pairs, 1 ns stays, b2 0.25 nm. Half 1 and all 24 alongside.")
print(f"{'measure':28s}{'pH4':>8s}{'pH7':>8s}{'diff':>8s}{'95% interval':>18s}{'p':>7s}{'q':>7s} |{'half-1 diff':>12s}{'p':>7s} |{'all-24 diff':>12s}{'p':>7s}{'q':>7s}")
for k, v in P.items():
    print(f"{k:28s}{v['ph4']:8.2f}{v['ph7']:8.2f}{v['diff']:8.2f}  [{v['lo']:7.2f},{v['hi']:7.2f}]{v['p']:7.3f}{v['q']:7.3f} |{A1[k]['diff']:12.2f}{A1[k]['p']:7.3f} |{ALL[k]['diff']:12.2f}{ALL[k]['p']:7.3f}{ALL[k]['q']:7.3f}", flush=True)
print("\nSensitivity, held-out pairs: diff (p)")
S = {"0.5 ns stays": compare(h2, 5, T0["b2_corefit"]), "2 ns stays": compare(h2, 20, T0["b2_corefit"]), "b2 0.30 nm": compare(h2, 10, .30)}
print(f"{'measure':28s}" + "".join(f"{n:>18s}" for n in S))
for k in P:
    print(f"{k:28s}" + "".join(f"{S[n][k]['diff']:11.2f} ({S[n][k]['p']:.3f})" for n in S), flush=True)

print("\nSegment core-fit RMSD by 10 ns bin, mean over runs, nm: pH 4 / pH 7")
curves = {}
for name, pr in (("held out", h2), ("half 1", h1)):
    print(f" {name}\n  {'bin ns':8s}" + "".join(f"{s:>13s}" for s in SEGS))
    for b in range(10):
        sl = slice(b * 100, (b + 1) * 100); row = []
        for s in SEGS:
            a = np.mean([x[s + "_corefit"][sl].mean() for x, _ in pr]); c = np.mean([y[s + "_corefit"][sl].mean() for _, y in pr]); row.append((a, c))
            curves.setdefault(name, {}).setdefault(s, []).append([float(a), float(c)])
        print(f"  {b * 10:3d}-{b * 10 + 10:<4d}" + "".join(f"  {a:5.2f}/{c:5.2f}" for a, c in row), flush=True)
json.dump(dict(primary=P, half1=A1, all24=ALL, sensitivity=S, curves=curves, pairing_check=worst), open(out_json, "w"), indent=1)
print("\nheld-out measures passing q < 0.05:", [k for k, v in P.items() if v["q"] < .05], flush=True)
print("done", flush=True)
