"""PUF1 <-> PUF2 candidate interconversion at each pH, from the structural labels on the raw trajectories (100 ps).
The 100-microstate MSM cannot do this because its microstates mix the two labels. Three measures:
  raw        direct adjacent stays (rolling majority over W ns, stays of at least W ns)
  milestone  only stays in P1 or P2 count; time is assigned to the last of the two visited; rate = events / committed time
  core MSM   8 labels, each frame takes the last stay visited; reversible ML MSM at several lags; MFPT and pi(P2)/pi(P1)
Bootstrap resamples whole runs within source groups, because a run is the independent unit.
Usage: puf_interconvert.py <puf_cvs_tight.npz> <puf_final.json> <out.json>"""
import json, sys
import numpy as np
from scipy.stats import chi2
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import MaximumLikelihoodMSM
Z = np.load(sys.argv[1]); T = json.load(open(sys.argv[2]))["thresholds_nm"]; rn = [str(s) for s in Z["rig_names"]]
KT = 0.0019872043 * 298.15; DT = 0.1; NB = 500; P1, P2 = 2, 3


def labels(r, tb2):
    o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("unit_corefit"); b2 = r["b2_corefit"] > tb2
    a3 = o("a3C_corefit") | o("a3C_selffit")
    lab = np.zeros(len(b1), int)
    lab[~b1 & un & ok] = 7; lab[~b1 & a3] = 6; lab[~b1 & ~ok] = 5; lab[b1] = 4
    lab[b1 & ~lp & ~a1n & ok] = 1; lab[b1 & lp & a1n & ok] = 2; lab[b1 & a1 & b2 & ok] = 3
    return lab


def stays(lab, w):
    c = np.stack([np.convolve(lab == k, np.ones(w), "same") for k in range(8)]); m = c.argmax(0)
    e = np.flatnonzero(np.diff(m)) + 1; st = np.r_[0, e]; ln = np.diff(np.r_[st, len(m)])
    out = []
    for a, l in zip(st, ln):
        if l >= w:
            s = int(m[a])
            if out and out[-1][0] == s:
                out[-1] = (s, out[-1][1], int(a) + int(l) - out[-1][1])
            else:
                out.append((s, int(a), int(l)))
    return out


def per_run(lab, w):
    """Events and times for one run; core-set dtraj (last stay visited; frames before the first stay dropped)."""
    ss = stays(lab, w); n = len(lab)
    raw12 = sum(a[0] == P1 and b[0] == P2 for a, b in zip(ss, ss[1:])); raw21 = sum(a[0] == P2 and b[0] == P1 for a, b in zip(ss, ss[1:]))
    d1 = sum(s[2] for s in ss if s[0] == P1) * DT; d2 = sum(s[2] for s in ss if s[0] == P2) * DT
    core = [s for s in ss if s[0] in (P1, P2)]; m12 = m21 = 0; t1 = t2 = 0.0
    for a, b in zip(core, core[1:]):
        if a[0] == P1 and b[0] == P2:
            m12 += 1
        if a[0] == P2 and b[0] == P1:
            m21 += 1
    for i, a in enumerate(core):
        end = core[i + 1][1] if i + 1 < len(core) else n
        t = (end - a[1]) * DT
        if a[0] == P1:
            t1 += t
        else:
            t2 += t
    dtr = None
    if ss:
        dtr = np.empty(n - ss[0][1], int); o = ss[0][1]
        for i, s in enumerate(ss):
            end = ss[i + 1][1] if i + 1 < len(ss) else n
            dtr[s[1] - o:end - o] = s[0]
    return dict(raw12=raw12, raw21=raw21, d1=d1, d2=d2, m12=m12, m21=m21, t1=t1, t2=t2, dtr=dtr)


def pois(n, t):
    """Events per us with exact 95 % interval."""
    if t <= 0:
        return None
    lo = chi2.ppf(.025, 2 * n) / 2 if n else 0.0; hi = chi2.ppf(.975, 2 * n + 2) / 2
    return [n / t * 1e3, lo / t * 1e3, hi / t * 1e3]


def core_msm(dtrs, lag):
    """pi ratio and MFPTs (ns) between P1 and P2, or None when they are not both in the connected set."""
    d = [x for x in dtrs if x is not None and len(x) > lag]
    c = TransitionCountEstimator(lag, "sliding").fit(d).fetch_model(); sub = c.submodel_largest(directed=True)
    sym = list(sub.state_symbols)
    if P1 not in sym or P2 not in sym:
        return None
    m = MaximumLikelihoodMSM(reversible=True).fit(sub).fetch_model(); P = m.transition_matrix; pi = m.stationary_distribution; n = len(sym)
    i, j = sym.index(P1), sym.index(P2)

    def mfpt(a, b):
        idx = [k for k in range(n) if k != b]
        t = np.linalg.solve(np.eye(n - 1) - P[np.ix_(idx, idx)], np.ones(n - 1))
        return float(t[idx.index(a)] * lag * DT)
    return dict(ddG=float(-KT * np.log(pi[j] / pi[i])), p1=float(pi[i]), p2=float(pi[j]), mfpt12=mfpt(i, j), mfpt21=mfpt(j, i))


res = {}
rng = np.random.default_rng(11)
for ph in ("ph4", "ph7"):
    r = {n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}; run = Z[f"{ph}_run"]; src = Z[f"{ph}_src"]
    runs = np.unique(run); rs = np.array([src[run == u][0] for u in runs])
    for tb2 in (T["b2_corefit"], 0.30, 0.35):
        lab = labels(r, tb2)
        for w_ns in (0.5, 1.0, 2.0):
            w = int(round(w_ns / DT)); R = [per_run(lab[run == u], w) for u in runs]
            tot = {k: sum(x[k] for x in R) for k in ("raw12", "raw21", "d1", "d2", "m12", "m21", "t1", "t2")}
            ev_runs = sum(1 for x in R if x["m12"] + x["m21"] > 0); p2_runs = sum(1 for x in R if x["d2"] > 0); p1_runs = sum(1 for x in R if x["d1"] > 0)
            key = f"{ph}|b2>{tb2:.2f}|W{w_ns}"
            res[key] = dict(**{k: float(v) for k, v in tot.items()}, runs_with_events=ev_runs, runs_P1=p1_runs, runs_P2=p2_runs, k12_raw=pois(tot["raw12"], tot["d1"]), k21_raw=pois(tot["raw21"], tot["d2"]), k12_ms=pois(tot["m12"], tot["t1"]), k21_ms=pois(tot["m21"], tot["t2"]))
            print(f"{key:24s} raw {tot['raw12']:2d}/{tot['raw21']:2d} dwell {tot['d1']:6.1f}/{tot['d2']:6.1f} ns | milestone {tot['m12']:2d}/{tot['m21']:2d} committed {tot['t1']:7.1f}/{tot['t2']:7.1f} ns runs(ev/P1/P2) {ev_runs}/{p1_runs}/{p2_runs}", flush=True)
            if tb2 == T["b2_corefit"] and w_ns == 1.0:
                print("   k12, k21 milestone per us [95%]:", np.round(res[key]["k12_ms"], 2) if res[key]["k12_ms"] else None, np.round(res[key]["k21_ms"], 2) if res[key]["k21_ms"] else None, flush=True)
                for lag_ns in (1, 2, 5, 10):
                    lag = int(lag_ns / DT); c = core_msm([x["dtr"] for x in R], lag); B = []
                    groups = {s: np.flatnonzero(rs == s) for s in np.unique(rs)}
                    for _ in range(NB):
                        pick = np.concatenate([rng.choice(ix, len(ix)) for ix in groups.values()])
                        try:
                            b = core_msm([R[i]["dtr"] for i in pick], lag)
                        except Exception:
                            b = None
                        B.append(b)
                    ok = [b for b in B if b]
                    q = lambda f: [float(v) for v in np.percentile([b[f] for b in ok], [2.5, 50, 97.5])] if ok else None
                    res[f"{key}|coreMSM lag{lag_ns}"] = dict(ml=c, bootstrap_ok=len(ok), n=NB, ddG=q("ddG"), mfpt12=q("mfpt12"), mfpt21=q("mfpt21"))
                    print(f"   core MSM lag {lag_ns} ns: ML {None if c is None else {k: round(v, 3) for k, v in c.items()}}; boot ok {len(ok)}/{NB} ddG {None if not ok else np.round(q('ddG'), 2)} MFPT12 {None if not ok else np.round(q('mfpt12'), 0)} MFPT21 {None if not ok else np.round(q('mfpt21'), 0)}", flush=True)
json.dump(res, open(sys.argv[3], "w"), indent=1)
print("done", flush=True)
