"""Two-constraint MaxCal redone on structural observables, from the published per-frame microstates (msm_weights.npz), so no
k-means is repeated. Functions tilt_obs, dg_open, kl_rate and maxcal_open are those of msm_build.py. Variant V0 rebuilds the
published model and must reproduce its weights before the new variants are trusted. pH 4 multipliers are carried to pH 7.

Usage: puf_maxcal.py <puf_cvs_tight.npz> <puf_final.json> <msm_weights.npz> <lag_ns> <out.json> <deeptime_site_dir>"""
import json, sys
sys.path.insert(0, sys.argv[6])
import numpy as np
from scipy.optimize import least_squares
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import BayesianMSM, MaximumLikelihoodMSM
Z = np.load(sys.argv[1]); T = json.load(open(sys.argv[2]))["thresholds_nm"]; W = np.load(sys.argv[3]); LAG_NS = float(sys.argv[4])
KT = 0.0019872043 * 298.15; DT = 0.1; LAG = int(round(LAG_NS / DT)); K = 100; NS = 200
rn = [str(s) for s in Z["rig_names"]]; qn = [str(s) for s in Z["set_names"]]
CL = ["Folded-like", "b1 alone", "PUF1 cand", "PUF2 cand", "b1+partial", "core distorted", "a3C off", "unit off"]


def tilt_obs(P, Fm, lam):
    M = P * np.exp(np.asarray(lam) @ Fm)[None, :]
    w, vr = np.linalg.eig(M); i = np.argmax(np.real(w)); mu = np.real(w[i]); v = np.abs(np.real(vr[:, i]))
    w2, vl = np.linalg.eig(M.T); u = np.abs(np.real(vl[:, np.argmax(np.real(w2))]))
    pi = u * v; pi /= pi.sum()
    Pn = M * v[None, :] / (mu * v[:, None])
    return Pn / Pn.sum(axis=1, keepdims=True), pi


def dg_open(pi, g):
    p = pi @ g
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(p > 0, -KT * np.log(p / (1 - p)), np.nan)


def kl_rate(Pn, pin, P):
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.nansum(pin[:, None] * np.where(Pn > 0, Pn * np.log(Pn / P), 0.0)))


def maxcal_open(P, g, targets):
    Fm = g.T

    def resid(lam):
        _, pi = tilt_obs(P, Fm, lam)
        return [(-dg_open(pi, g[:, [j]])[0] + t) / KT for j, t in enumerate(targets)]

    sol = least_squares(resid, np.zeros(g.shape[1]), xtol=1e-12, ftol=1e-12)
    Pn, pin = tilt_obs(P, Fm, sol.x)
    return sol, Pn, pin, kl_rate(Pn, pin, P), Fm


D = {}
for ph in ("ph4", "ph7"):
    r = {n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}; q = {n: Z[f"{ph}_q"][:, i] for i, n in enumerate(qn)}
    o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    lab = np.zeros(len(b1), int)
    lab[~b1 & un & ok] = 7; lab[~b1 & a3] = 6; lab[~b1 & ~ok] = 5; lab[b1] = 4
    lab[b1 & ~lp & ~a1n & ok] = 1; lab[b1 & lp & a1n & ok] = 2; lab[b1 & a1 & b2 & ok] = 3
    micro = W[f"{ph}_micro"].astype(int); run = Z[f"{ph}_run"]
    dtr = [micro[run == u] for u in np.unique(run)]
    cnt = np.bincount(micro, minlength=K).astype(float)
    avg = lambda m: np.bincount(micro, weights=m.astype(float), minlength=K) / np.maximum(cnt, 1)
    obs = dict(b1q=avg(q["b1_rest"] < .5), b2q=avg(q["b2_seg"] < .5), b1d=avg(b1), p1=avg(lab == 2), p2=avg(lab == 3), band=avg((lab == 2) | (lab == 3)), arm=avg(lab == 1))
    G = np.stack([avg(lab == k) for k in range(8)], 1)
    c = TransitionCountEstimator(LAG, "sliding").fit(dtr).fetch_model(); sub = c.submodel_largest(directed=True)
    m = MaximumLikelihoodMSM(reversible=True).fit(sub).fetch_model(); sym = m.count_model.state_symbols
    eff = TransitionCountEstimator(LAG, "effective").fit(dtr).fetch_model(); eff = eff.submodel(eff.symbols_to_states(sym))
    post = BayesianMSM(n_samples=NS, reversible=True).fit(eff).fetch_model()
    D[ph] = dict(micro=micro, cnt=cnt, obs=obs, G=G, P=m.transition_matrix, pi=m.stationary_distribution, sym=sym, samples=post.samples, esym=eff.state_symbols, lab=lab)
    full = np.zeros(K); full[sym] = m.stationary_distribution; w = full[micro] / np.maximum(cnt[micro], 1)
    print(f"{ph}: active {len(sym)}/{K}; rebuilt prior vs published frame weights, max |dw| {np.abs(w - W[f'{ph}_w_prior']).max():.2e}, sum|dw| {np.abs(w - W[f'{ph}_w_prior']).sum():.2e}")
    print("   max microstate fraction:", {k: round(float(v[sym].max()), 2) for k, v in obs.items()}, "| microstates with p2>0.05:", int((obs['p2'][sym] > .05).sum()), "p1>0.05:", int((obs['p1'][sym] > .05).sum()))

VAR = {"V0 published (b1_rest 2.2, b2_seg 3.1)": (["b1q", "b2q"], [2.2, 3.1], [.2, .5]),
       "A: b1 displaced 2.2, PUF2 cand 3.1": (["b1d", "p2"], [2.2, 3.1], [.2, .5]),
       "B: PUF1 cand 2.2, PUF2 cand 3.1": (["p1", "p2"], [2.2, 3.1], [.2, .5]),
       "C: b1 displaced 2.2, PUF1 cand 2.2, PUF2 cand 3.1": (["b1d", "p1", "p2"], [2.2, 2.2, 3.1], [.2, .2, .5])}
out = {}
d4, d7 = D["ph4"], D["ph7"]
dgF = lambda pi, G: (lambda p: [float(-KT * np.log(x / p[0])) if x > 0 else float("inf") for x in p])(pi @ G)
print("\nprior ML pH 4 %:", dict(zip(CL, np.round(100 * d4["pi"] @ d4["G"][d4["sym"]], 1))))
print("prior ML pH 7 %:", dict(zip(CL, np.round(100 * d7["pi"] @ d7["G"][d7["sym"]], 1))))
for name, (cols, tg, sd) in VAR.items():
    g4 = np.stack([d4["obs"][c][d4["sym"]] for c in cols], 1); g7 = np.stack([d7["obs"][c][d7["sym"]] for c in cols], 1)
    so, Pn, pin, kl, Fm = maxcal_open(d4["P"], g4, tg)
    res = float(np.max(np.abs(so.fun)))
    conv = bool(so.success and res <= 1e-6)
    print(f"\n=== {name}\n  ML converged {conv} (max residual {res:.1e}); lambda {np.round(so.x, 3)}; KL {kl / LAG_NS:.5f} /ns; achieved dG_op {np.round(dg_open(pin, g4), 2)}")
    if name.startswith("V0"):
        full = np.zeros(K); full[d4["sym"]] = pin; w = full[d4["micro"]] / np.maximum(d4["cnt"][d4["micro"]], 1)
        print(f"  reproduction vs published w_maxcal, pH 4: max |dw| {np.abs(w - W['ph4_w_maxcal']).max():.2e}, sum|dw| {np.abs(w - W['ph4_w_maxcal']).sum():.2e}")
    P7, pi7 = tilt_obs(d7["P"], g7.T, so.x)
    if name.startswith("V0"):
        full = np.zeros(K); full[d7["sym"]] = pi7; w = full[d7["micro"]] / np.maximum(d7["cnt"][d7["micro"]], 1)
        print(f"  reproduction vs published w_maxcal, pH 7: sum|dw| {np.abs(w - W['ph7_w_maxcal']).sum():.2e}")
    a4 = pin @ d4["G"][d4["sym"]]; a7 = pi7 @ d7["G"][d7["sym"]]
    print("  cluster        pH4 %   dG/Folded | pH7 % (transfer) dG/Folded")
    e4, e7 = dgF(pin, d4["G"][d4["sym"]]), dgF(pi7, d7["G"][d7["sym"]])
    for k, n in enumerate(CL):
        print(f"   {n:15s}{100 * a4[k]:6.2f}  {e4[k]:6.2f}   | {100 * a7[k]:6.2f}  {e7[k]:6.2f}")
    rng = np.random.default_rng(7); rows, fails, rows7 = [], 0, []
    gb4 = np.stack([d4["obs"][c][d4["esym"]] for c in cols], 1); Gb4 = d4["G"][d4["esym"]]
    gb7 = np.stack([d7["obs"][c][d7["esym"]] for c in cols], 1); Gb7 = d7["G"][d7["esym"]]
    for s4, s7 in zip(d4["samples"], d7["samples"]):
        t = [rng.normal(a, b) for a, b in zip(tg, sd)]
        s, Pb, pb, klb, _ = maxcal_open(s4.transition_matrix, gb4, t)
        if not s.success or np.max(np.abs(s.fun)) > 1e-6:
            fails += 1; continue
        rows.append(dgF(pb, Gb4) + [klb / LAG_NS]); _, p7 = tilt_obs(s7.transition_matrix, gb7.T, s.x); rows7.append(dgF(p7, Gb7))
    rows = np.array(rows); rows7 = np.array(rows7)
    q = lambda a, k: tuple(np.round(np.percentile(a[np.isfinite(a[:, k]), k], [2.5, 50, 97.5]), 2)) if np.isfinite(a[:, k]).any() else None
    print(f"  Bayesian: failed {fails}/{NS}; pH 4 dG/Folded PUF1 {q(rows, 2)}, PUF2 {q(rows, 3)}, b1 alone {q(rows, 1)}; KL/ns median {np.median(rows[:, 8]):.5f}; pH 7 transfer PUF1 {q(rows7, 2)}, PUF2 {q(rows7, 3)}, b1 alone {q(rows7, 1)}")
    out[name] = dict(ml_converged=conv, lam=so.x.tolist(), kl_per_ns=kl / LAG_NS, ph4_pct=dict(zip(CL, (100 * a4).tolist())), ph7_pct=dict(zip(CL, (100 * a7).tolist())), ph4_dG=dict(zip(CL, e4)), ph7_dG=dict(zip(CL, e7)), failed=fails, n=NS,
                     bayes=dict(ph4_PUF1=q(rows, 2), ph4_PUF2=q(rows, 3), ph4_b1=q(rows, 1), ph7_PUF1=q(rows7, 2), ph7_PUF2=q(rows7, 3), ph7_b1=q(rows7, 1)))
json.dump(out, open(sys.argv[5], "w"), indent=1, default=float)
