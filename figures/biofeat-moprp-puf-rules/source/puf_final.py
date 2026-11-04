"""Final rule table (tight disulfide-proximal core), seed-independent and paired checks.
Usage: puf_final.py <puf_cvs_tight.npz> <cartesian_features.npz> <out.json>"""
import json, sys, zipfile
import numpy as np
from scipy.stats import wilcoxon, binomtest
Z = np.load(sys.argv[1]); rn = [str(s) for s in Z["rig_names"]]; names = [str(s) for s in Z["set_names"]]
keys = [n[:-4] for n in zipfile.ZipFile(sys.argv[2]).namelist() if n != "feature_names.npy"]
KT = 0.0019872043 * 298.15
dg = lambda p: float("inf") if p <= 0 else float(-KT * np.log(p / (1 - p)))
FOLD = {"ph4": (7.5, -27.5), "ph7": (12.5, -17.5)}
D = {}
for ph in ("ph4", "ph7"):
    d = dict(r={n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}, q={n: Z[f"{ph}_q"][:, i] for i, n in enumerate(names)}, x=Z[f"{ph}_x"], wp=Z[f"{ph}_wp"], wm=Z[f"{ph}_wm"], src=Z[f"{ph}_src"], run=Z[f"{ph}_run"])
    d["F"] = np.linalg.norm(d["x"][:, :2] - np.array(FOLD[ph]), axis=1) < 10
    d["keys"] = [k for k in keys if k.startswith(ph + "__")]
    D[ph] = d
T = {n: float(np.percentile(np.concatenate([D[p]["r"][n][D[p]["F"]] for p in D]), 99)) for n in rn}
print("thresholds nm:", {k: round(T[k], 2) for k in ("core","b1_corefit","loop_corefit","a1_corefit","a1N_corefit","a1C_corefit","b2_corefit","a3C_corefit","a3C_selffit","unit_corefit")})
def rules(d):
    r = d["r"]; o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    return {"b1 only": b1 & ~lp & ~a1n, "b1+loop": b1 & lp & ok, "b1+loop+a1N": b1 & lp & a1n & ok, "b1+loop+a3C (PUF1 text)": b1 & lp & a3 & ok,
            "b1+loop+a1N+a3C": b1 & lp & a1n & a3 & ok, "a3C, b1 kept": a3 & ~b1, "unit off, b1 kept": un & ~b1 & ok, "unit off, b1 off": un & b1 & ok,
            "a1+b2 off, core ok (PUF2 text)": a1 & b2 & ok, "PUF2 seq (+b1+loop+a3C)": a1 & b2 & b1 & lp & a3 & ok, "core distorted": ~ok}
out = {"thresholds_nm": T}
print(f"{'rule':32s}   MSM/MaxCal frames runs r80 PCmedian  (pH4 | pH7)")
for n in rules(D["ph4"]):
    s = f"{n:32s}"
    for ph, d in D.items():
        m = rules(d)[n]; c = int(m.sum()); rc = np.sort(np.bincount(d["run"][m]))[::-1] if c else np.array([0])
        r80 = int(np.searchsorted(np.cumsum(rc), .8 * c) + 1) if c else 0
        med = np.median(d["x"][m, :2], axis=0).round(0) if c else [np.nan, np.nan]
        srcs = {str(k): int((d["src"][m] == k).sum()) for k in np.unique(d["src"][m])}
        top = max(srcs, key=srcs.get) if c else "-"
        s += f" | {dg(d['wp'][m].sum()):5.2f}/{dg(d['wm'][m].sum()):5.2f} n={c:5d} r={int((rc>0).sum()):3d} r80={r80:2d} ({med[0]:4.0f},{med[1]:4.0f}) {top}:{(srcs.get(top,0)/max(c,1)):.2f}"
        out[f"{n}|{ph}"] = dict(dG_msm=dg(d['wp'][m].sum()), dG_maxcal=dg(d['wm'][m].sum()), frames=c, runs=int((rc > 0).sum()), runs80=r80, top_source=top)
    print(s)

print("\n== unbiased MD only (no seeds, no weights): beta1-closed frames, a1N/unit/loop/a3C core-fit")
for ph, d in D.items():
    m = (d["src"] == "unbiased"); c = m & (d["q"]["b1_rest"] >= .5)
    print(f"  {ph} frames {m.sum()} b1-open {(d['q']['b1_rest'][m]<.5).mean():.3f}; closed: a1N mean {d['r']['a1N_corefit'][c].mean():.2f} P(>0.6) {(d['r']['a1N_corefit'][c]>.6).mean():.3f} unit P(>{T['unit_corefit']:.2f}) {(d['r']['unit_corefit'][c]>T['unit_corefit']).mean():.3f} loop mean {d['r']['loop_corefit'][c].mean():.2f}")
    per = []
    for u in np.unique(d["run"][m]):
        k = c & (d["run"] == u); per.append((d['keys'][u].split('__')[-1], int(k.sum()), round(float((d['r']['a1N_corefit'][k] > .6).mean()), 3) if k.sum() else None))
    print("    per block:", per)

print("\n== paired, same seed at both target pH, ph7_3 source, last 20 ns (pH 7 minus pH 4)")
def tail(d, key, n=200):
    u = d["keys"].index(key); ii = np.flatnonzero(d["run"] == u)[-n:]
    return [*d["x"][ii, :2].mean(0)] + [d["r"][c][ii].mean() for c in ("b1_corefit", "loop_corefit", "a1N_corefit", "unit_corefit")]
for src in ("ph7_3", "ph4_3", "ph4_2", "ph7_2"):
    pairs = [k.split("__", 1)[1] for k in D["ph4"]["keys"] if k.split("__")[1] == src and f"ph7__{k.split('__',1)[1]}" in D["ph7"]["keys"]]
    pairs = [p for p in pairs if (D["ph4"]["run"] == D["ph4"]["keys"].index("ph4__" + p)).sum() > 500 and (D["ph7"]["run"] == D["ph7"]["keys"].index("ph7__" + p)).sum() > 500]
    A = np.array([tail(D["ph4"], "ph4__" + p) for p in pairs]); B = np.array([tail(D["ph7"], "ph7__" + p) for p in pairs]); df = B - A
    print(f" {src}: {len(pairs)} pairs")
    for j, c in enumerate(("PC1", "PC2", "b1", "loop", "a1N", "unit")):
        print(f"   {c:5s} pH4 {A[:,j].mean():7.2f} pH7 {B[:,j].mean():7.2f} diff {df[:,j].mean():7.2f}  pos {int((df[:,j]>0).sum())}/{len(pairs)}  Wilcoxon p {wilcoxon(df[:,j]).pvalue:.3f}")

print("\n== who holds the pH 7 minimum bin (87.5,17.5) +- 5 box")
for ph, d in D.items():
    m = (np.abs(d["x"][:, 0] - 87.5) < 5) & (np.abs(d["x"][:, 1] - 17.5) < 5)
    rc = np.bincount(d["run"][m]); order = np.argsort(rc)[::-1][:5]
    print(f"  {ph}: frames {m.sum()} runs {(rc>0).sum()} weight {d['wp'][m].sum():.4f}; top " + ", ".join(f"{d['keys'][u].split('__',1)[1]}:{rc[u]}" for u in order if rc[u]))
    print("     by source", {str(s): (int((d['src'][m]==s).sum()), round(float(d['wp'][m & (d['src']==s)].sum()), 4)) for s in np.unique(d['src'][m])})
print("ranges", D["ph4"]["x"][:, 2].min(), D["ph4"]["x"][:, 2].max(), D["ph4"]["x"][:, 3].min(), D["ph4"]["x"][:, 3].max())
json.dump(out, open(sys.argv[3], "w"), indent=1)
