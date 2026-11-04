"""Transitions between structurally defined states, and the order in which segments return to native, per run and pH.
No PCA position enters: a frame's state comes from the rule labels (same definitions at both pH), so a state means the same
thing wherever it sits on the plane. Raw trajectories at 100 ps, not the MSM, because the MSM microstates are shared between
pH values and mix structures. Labels are smoothed by a rolling majority over W ns; a stay counts when it lasts at least W ns;
the frames between stays are ignored (milestoning). Zero events: 95 % upper bound 3/T.

Usage: puf_transitions.py <puf_cvs_tight.npz> <puf_final.json> <cartesian_features.npz> <out.json>"""
import json, sys, zipfile
from collections import Counter
import numpy as np
from scipy.stats import fisher_exact
Z = np.load(sys.argv[1]); T = json.load(open(sys.argv[2]))["thresholds_nm"]
keys = [n[:-4] for n in zipfile.ZipFile(sys.argv[3]).namelist() if n != "feature_names.npy"]
rn = [str(s) for s in Z["rig_names"]]; DT = 0.1
S = ["F", "ARM", "P1", "P2", "B1X", "CORE", "A3", "UNIT"]
NAME = dict(F="Folded-like", ARM="b1 alone", P1="PUF1 cand", P2="PUF2 cand", B1X="b1+partial", CORE="core distorted", A3="a3C off", UNIT="unit off")
COARSE = dict(F="F", ARM="ARM", P1="BAND", P2="BAND", B1X="BAND", CORE="LOBE", A3="A3", UNIT="UNIT"); CS = ["F", "ARM", "BAND", "LOBE", "A3", "UNIT"]


def labels(r):
    o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    lab = np.zeros(len(b1), int)
    lab[~b1 & un & ok] = 7; lab[~b1 & a3] = 6; lab[~b1 & ~ok] = 5; lab[b1] = 4
    lab[b1 & ~lp & ~a1n & ok] = 1; lab[b1 & lp & a1n & ok] = 2; lab[b1 & a1 & b2 & ok] = 3
    return lab


def stays(lab, n_state, w):
    """Rolling majority over w frames, then runs of at least w frames. Returns [(state, start, length)]."""
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


D = {}
for ph in ("ph4", "ph7"):
    r = {n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}
    D[ph] = dict(r=r, lab=labels(r), run=Z[f"{ph}_run"], src=Z[f"{ph}_src"], keys=[k for k in keys if k.startswith(ph + "__")])
res = {}
for w_ns in (0.5, 1.0, 2.0):
    w = int(round(w_ns / DT))
    for scheme, names, mp in (("fine", S, {i: i for i in range(8)}), ("coarse", CS, {i: CS.index(COARSE[S[i]]) for i in range(8)})):
        if scheme == "fine" and w_ns != 1.0:
            continue
        print(f"\n===== {scheme} states, window {w_ns} ns: events a->b (rows from, cols to), last col dwell ns")
        for ph, d in D.items():
            E = np.zeros((len(names), len(names)), int); dw = np.zeros(len(names)); runs_ab = {}
            paths = Counter()
            for u in np.unique(d["run"]):
                ii = np.flatnonzero(d["run"] == u); lab = np.vectorize(mp.get)(d["lab"][ii]); ss = stays(lab, len(names), w)
                for s in ss:
                    dw[s[0]] += s[2] * DT
                for a, b in zip(ss, ss[1:]):
                    E[a[0], b[0]] += 1; runs_ab.setdefault((a[0], b[0]), set()).add(u)
                if str(d["src"][ii[0]]) == "ph7_3" and scheme == "coarse" and w_ns == 1.0:
                    seq = [names[s[0]] for s in ss]; paths[">".join(seq[:1] + [seq[-1]])] += 1
            print(f" {ph}  " + "".join(f"{n[:6]:>7s}" for n in names) + "   dwell")
            for i, n in enumerate(names):
                print(f"  {n[:6]:6s}" + "".join(f"{v:7d}" if v else f"{'.':>7s}" for v in E[i]) + f"  {dw[i]:8.0f}")
            res[f"{scheme}|{w_ns}|{ph}"] = dict(states=names, events=E.tolist(), dwell_ns=dw.tolist(), runs={f"{names[a]}>{names[b]}": len(v) for (a, b), v in runs_ab.items()})
            if paths:
                print("   pH 7 #3 seeds, first state > last state:", dict(paths))
            if scheme == "fine":
                print("   runs per pair:", {f"{names[a]}>{names[b]}": len(v) for (a, b), v in sorted(runs_ab.items()) if a in (2, 3) or b in (2, 3)})
                print(f"   P1<->P2 upper bound none needed if events; F->P1 {E[0,2]}, F->P2 {E[0,3]}, bound from F dwell {3/dw[0]*1e3:.3f} /us")

print("\n===== return order, 100 ns runs, segment first stays below threshold for 5 ns")
F95 = {}
for ph in D:
    pass
SEG = [("b1", "b1_corefit"), ("loop", "loop_corefit"), ("a1N", "a1N_corefit")]
fold = {n: np.concatenate([D[p]["r"][n][D[p]["lab"] == 0] for p in D]) for _, n in SEG}
for tag, thr in (("Folded-like 99th pct", {n: float(np.percentile(fold[n], 99)) for _, n in SEG}), ("Folded-like 90th pct", {n: float(np.percentile(fold[n], 90)) for _, n in SEG})):
    print(f"\n -- {tag}:", {k: round(v, 2) for k, v in thr.items()})
    for src in ("ph7_3",):
        tab = {}
        for ph, d in D.items():
            rows = []
            for u in np.unique(d["run"][d["src"] == src]):
                ii = np.flatnonzero(d["run"] == u)
                if len(ii) < 500:
                    continue
                t = {}
                for s, n in SEG:
                    x = np.convolve(d["r"][n][ii], np.ones(10) / 10, "same"); below = x < thr[n]; hold = 50; ret = None
                    if x[:20].mean() < thr[n]:
                        t[s] = "start"; continue
                    run_len = 0
                    for i, b in enumerate(below):
                        run_len = run_len + 1 if b else 0
                        if run_len >= hold:
                            ret = (i - hold + 1) * DT; break
                    t[s] = ret
                rows.append((d["keys"][u].split("__")[-1], t))
            tab[ph] = rows
            print(f"  {src} {ph}: " + " ".join(f"{k[-2:]}:" + "/".join("s" if v[x] == "start" else "-" if v[x] is None else f"{v[x]:.0f}" for x in ("b1", "loop", "a1N")) for k, v in rows))
            cat = Counter()
            for _, v in rows:
                b, a = v["b1"], v["a1N"]
                bb = None if b == "start" else b; aa = None if a == "start" else a
                if a == "start" or b == "start":
                    cat["started below"] += 1
                elif bb is None and aa is None:
                    cat["neither"] += 1
                elif aa is None or (bb is not None and bb < aa):
                    cat["b1 first"] += 1
                else:
                    cat["a1N first"] += 1
            print("    order b1 vs a1N:", dict(cat), "| b1 returned", sum(v["b1"] not in (None, "start") for _, v in rows), "| loop", sum(v["loop"] not in (None, "start") for _, v in rows), "| a1N", sum(v["a1N"] not in (None, "start") for _, v in rows))
            res[f"order|{tag}|{ph}"] = dict(counts=dict(cat), runs={k: v for k, v in rows})
        c = [[sum(1 for _, v in tab[p] if v["b1"] not in (None, "start") and (v["a1N"] in (None,) or (v["a1N"] != "start" and v["b1"] < v["a1N"]))),
              sum(1 for _, v in tab[p] if v["a1N"] not in (None, "start") and (v["b1"] in (None,) or (v["b1"] != "start" and v["a1N"] < v["b1"])))] for p in ("ph4", "ph7")]
        print("    2x2 [b1 first, a1N first] pH4, pH7:", c, "Fisher p", round(float(fisher_exact(c)[1]), 3))
json.dump(res, open(sys.argv[4], "w"), indent=1, default=str)
