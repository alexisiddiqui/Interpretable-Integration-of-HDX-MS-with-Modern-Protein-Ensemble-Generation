"""MaxCal variant C (beta1 displaced 2.2, PUF1 candidate 2.2, PUF2 candidate 3.1, pH 4 only) and MSM cluster populations at both
pH, with the structural heatmap (macro_structure.py layout) and the free-energy maps (fes_maxcal_plots.py layout).
C has no exact solution, so every fit is kept as the best compromise: a tilt is the exact MaxCal solution for the values it
achieves. Bayesian intervals use all 200 samples. No MaxCal at pH 7. Published microstates are reused.

Usage: puf_c_heatmap.py <puf_cvs_tight.npz> <puf_final.json> <msm_weights.npz> <lag_ns> <cartesian_features.npz> <pca101_scores.npz>
                        <basins_seed.json> <out_prefix>"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import least_squares
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import BayesianMSM, MaximumLikelihoodMSM
cvs, thr, wts, lag_s, feat, scores, basins_p, prefix = sys.argv[1:9]
Z = np.load(cvs); T = json.load(open(thr))["thresholds_nm"]; W = np.load(wts); LAG_NS = float(lag_s); F = np.load(feat); S = np.load(scores, allow_pickle=True)
BAS = json.load(open(basins_p))
KT = 0.0019872043 * 298.15; LAG = int(round(LAG_NS / 0.1)); K = 100; NS = int(os.environ.get("PUF_NS", 200))   # PUF_NS < 200 redraws figures only, leaving the populations file
rn = [str(s) for s in Z["rig_names"]]
ORDER = [0, 1, 4, 2, 3, 5, 6, 7]                     # label ids in display order
NAME = {0: "Folded-like", 1: "β1 alone", 2: "PUF1 candidate", 3: "PUF2 candidate", 4: "β1 + partial", 5: "β1 kept, core distorted", 6: "β1 kept, α3 C off", 7: "β1 kept, unit off"}
TG, SD = [2.2, 2.2, 3.1], [.2, .2, .5]


def tilt_obs(P, Fm, lam):
    M = P * np.exp(np.asarray(lam) @ Fm)[None, :]
    w, vr = np.linalg.eig(M); i = np.argmax(np.real(w)); mu = np.real(w[i]); v = np.abs(np.real(vr[:, i]))
    w2, vl = np.linalg.eig(M.T); u = np.abs(np.real(vl[:, np.argmax(np.real(w2))]))
    pi = u * v; pi /= pi.sum()
    Pn = M * v[None, :] / (mu * v[:, None])
    return Pn / Pn.sum(axis=1, keepdims=True), pi


def dg_open(pi, g):
    p = pi @ g
    return -KT * np.log(p / (1 - p))


def fit(P, g, t):
    def resid(lam):
        _, pi = tilt_obs(P, g.T, lam)
        return [(-dg_open(pi, g[:, j]) + t[j]) / KT for j in range(g.shape[1])]
    s = least_squares(resid, np.zeros(g.shape[1]), xtol=1e-12, ftol=1e-12)
    return s, tilt_obs(P, g.T, s.x)


D = {}
for ph in ("ph4", "ph7"):
    r = {n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}
    o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    lab = np.zeros(len(b1), int)
    lab[~b1 & un & ok] = 7; lab[~b1 & a3] = 6; lab[~b1 & ~ok] = 5; lab[b1] = 4
    lab[b1 & ~lp & ~a1n & ok] = 1; lab[b1 & lp & a1n & ok] = 2; lab[b1 & a1 & b2 & ok] = 3
    micro = W[f"{ph}_micro"].astype(int); run = Z[f"{ph}_run"]
    cnt = np.bincount(micro, minlength=K).astype(float)
    avg = lambda m: np.bincount(micro, weights=m.astype(float), minlength=K) / np.maximum(cnt, 1)
    dtr = [micro[run == u] for u in np.unique(run)]
    c = TransitionCountEstimator(LAG, "sliding").fit(dtr).fetch_model(); sub = c.submodel_largest(directed=True)
    m = MaximumLikelihoodMSM(reversible=True).fit(sub).fetch_model(); sym = m.count_model.state_symbols
    eff = TransitionCountEstimator(LAG, "effective").fit(dtr).fetch_model(); eff = eff.submodel(eff.symbols_to_states(sym))
    post = BayesianMSM(n_samples=NS, reversible=True).fit(eff).fetch_model()
    D[ph] = dict(r=r, lab=lab, micro=micro, cnt=cnt, obs=np.stack([avg(b1), avg(lab == 2), avg(lab == 3)], 1), G=np.stack([avg(lab == k) for k in range(8)], 1), P=m.transition_matrix, pi=m.stationary_distribution,
                 sym=sym, esym=eff.state_symbols, samples=post.samples, x=W[f"{ph}_x"].astype(float), wp=W[f"{ph}_w_prior"])


def fw(d, pi):
    full = np.zeros(K); full[d["sym"]] = pi
    return full[d["micro"]] / np.maximum(d["cnt"][d["micro"]], 1)


d4, d7 = D["ph4"], D["ph7"]
g4 = d4["obs"][d4["sym"]]
sol, (Pc, pc) = fit(d4["P"], g4, TG)
print("C ML: lambda", np.round(sol.x, 3), "achieved dG_op", [round(float(dg_open(pc, g4[:, j])), 3) for j in range(3)], flush=True)
wC = fw(d4, pc)
stats = lambda a: [float(np.percentile(a, q)) for q in (2.5, 50, 97.5)]
rel = lambda p: -KT * np.log(np.maximum(p, 1e-12) / p[..., [0]])
out = {"lag_ns": LAG_NS, "lambda": sol.x.tolist(), "achieved_dG_op": [float(dg_open(pc, g4[:, j])) for j in range(3)], "clusters": {}}
Pm = {ph: D[ph]["pi"] @ D[ph]["G"][D[ph]["sym"]] for ph in D}; Pcl = pc @ d4["G"][d4["sym"]]
B = {ph: np.array([s.stationary_distribution @ D[ph]["G"][D[ph]["esym"]] for s in D[ph]["samples"]]) for ph in D}
rng = np.random.default_rng(7); gb = d4["obs"][d4["esym"]]; Gb = d4["G"][d4["esym"]]; BC, AO = [], []
for s in d4["samples"]:
    t = [rng.normal(a, b) for a, b in zip(TG, SD)]
    _, (_, p) = fit(s.transition_matrix, gb, t)
    BC.append(p @ Gb); AO.append([dg_open(p, gb[:, j]) for j in range(3)])
BC = np.array(BC); AO = np.array(AO)
out["achieved_dG_op_bayes"] = [stats(AO[:, j]) for j in range(3)]
for k in range(8):
    out["clusters"][NAME[k]] = dict(msm_ph4_pct=100 * float(Pm["ph4"][k]), msm_ph4_ci=[100 * v for v in stats(B["ph4"][:, k])], msm_ph7_pct=100 * float(Pm["ph7"][k]), msm_ph7_ci=[100 * v for v in stats(B["ph7"][:, k])],
                                    maxcal_ph4_pct=100 * float(Pcl[k]), maxcal_ph4_ci=[100 * v for v in stats(BC[:, k])],
                                    dG_msm_ph4=float(rel(Pm["ph4"])[k]), dG_msm_ph4_ci=stats(rel(B["ph4"])[:, k]), dG_msm_ph7=float(rel(Pm["ph7"])[k]), dG_msm_ph7_ci=stats(rel(B["ph7"])[:, k]),
                                    dG_maxcal_ph4=float(rel(Pcl)[k]), dG_maxcal_ph4_ci=stats(rel(BC)[:, k]))
grp = {"β1 displaced, all": [1, 2, 3, 4], "band (PUF1 + PUF2 + partial)": [2, 3, 4], "β1 kept, perturbed": [5, 6, 7]}
out["groups"] = {n: dict(msm_ph4=[100 * v for v in stats(B["ph4"][:, i].sum(1))], msm_ph7=[100 * v for v in stats(B["ph7"][:, i].sum(1))], maxcal_ph4=[100 * v for v in stats(BC[:, i].sum(1))]) for n, i in grp.items()}
if NS == 200:
    json.dump(out, open(prefix + "_populations.json", "w"), indent=1)
print(f"{'cluster':26s} MSM pH4 %  [95%]        MSM pH7 % [95%]        C pH4 % [95%]")
for k in ORDER:
    c = out["clusters"][NAME[k]]; f = lambda a: f"[{a[0]:.2f}, {a[2]:.2f}]"
    print(f"{NAME[k]:26s} {c['msm_ph4_pct']:6.2f} {f(c['msm_ph4_ci']):16s} {c['msm_ph7_pct']:6.2f} {f(c['msm_ph7_ci']):16s} {c['maxcal_ph4_pct']:6.2f} {f(c['maxcal_ph4_ci'])}  dG {c['dG_msm_ph4']:.2f}/{c['dG_msm_ph7']:.2f}/{c['dG_maxcal_ph4']:.2f}", flush=True)
print(out["groups"]); print("achieved bayes", out["achieved_dG_op_bayes"], flush=True)

# native contacts as macro_structure.py
RES = np.arange(123, 224); centre, scale = S["ph4_center"], S["ph4_scale"]
nat = (centre * scale).reshape(101, 3); D0 = np.linalg.norm(nat[:, None] - nat[None], axis=-1)
I, J = np.triu_indices(101, 4); keep = D0[I, J] < 0.8; I, J, d0 = I[keep], J[keep], D0[I, J][keep]; ri, rj = RES[I], RES[J]
in_ = lambda r, a, b: (r >= a) & (r <= b)
SEG = [("β1 127–132", 127, 132), ("β1–α1 loop 133–143", 133, 143), ("α1 144–153", 144, 153), ("β2 region 154–167", 154, 167), ("α2 172–193", 172, 193), ("α2–α3 loop 194–199", 194, 199), ("α3 N 200–211", 200, 211), ("α3 C 212–223", 212, 223)]
GRP = [("α1+β2 ↔ α2–α3 core", (144, 167), (172, 223)), ("β1 ↔ rest", (127, 132), (133, 223)), ("β1–α1 loop ↔ α3", (133, 143), (200, 223))]
masks = [in_(ri, a, b) | in_(rj, a, b) for _, a, b in SEG] + [(in_(ri, *a) & in_(rj, *b)) | (in_(rj, *a) & in_(ri, *b)) for _, a, b in GRP]
cols = [s[0] for s in SEG] + [g[0] for g in GRP]
acc = {ph: np.zeros((8, len(cols))) for ph in D}; pos = {ph: 0 for ph in D}; nfr = {ph: np.zeros(8) for ph in D}
for k in F.files:
    if k == "feature_names":
        continue
    ph = k.split("__")[0]; z = F[k].astype(np.float64); X = ((z + centre) * scale).reshape(len(z), 101, 3)
    formed = np.linalg.norm(X[:, I] - X[:, J], axis=-1) < 1.2 * d0
    q = np.column_stack([formed[:, m].mean(1) for m in masks]); lb = D[ph]["lab"][pos[ph]:pos[ph] + len(z)]; pos[ph] += len(z)
    for c in range(8):
        s = lb == c; acc[ph][c] += q[s].sum(0); nfr[ph][c] += s.sum()
Qr = {ph: (acc[ph] / np.maximum(nfr[ph], 1)[:, None]) / (acc[ph][0] / nfr[ph][0]) for ph in D}
RC = [("β1", "b1_corefit"), ("loop", "loop_corefit"), ("α1 N", "a1N_corefit"), ("α1 C", "a1C_corefit"), ("β2", "b2_corefit"), ("α3 C", "a3C_corefit"), ("core", "core")]
Rm = {ph: np.array([[D[ph]["r"][n][D[ph]["lab"] == c].mean() for _, n in RC] for c in range(8)]) for ph in D}

INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "figure.facecolor": SURF, "axes.facecolor": SURF, "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
ROLE = {"β1 127–132": "PUF1", "β1–α1 loop 133–143": "PUF1", "α3 C 212–223": "PUF1", "α1 144–153": "PUF1/2", "β2 region 154–167": "PUF2"}
fig, axes = plt.subplots(2, 2, figsize=(19, 11), gridspec_kw=dict(wspace=.5, hspace=.42, height_ratios=[1, 1]), sharey=True)
for c_, ph in enumerate(("ph4", "ph7")):
    ax = axes[0, c_]; M = Qr[ph][ORDER]
    im = ax.imshow(M, cmap="RdBu", vmin=.4, vmax=1.6, aspect="auto")
    for (a, b), v in np.ndenumerate(M):
        ax.text(b, a, f"{v:.2f}", ha="center", va="center", fontsize=7.5, color="w" if abs(v - 1) > .4 else INK)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels([f"{c}\n[HDX {ROLE[c]}]" if c in ROLE else c for c in cols], rotation=40, ha="right", fontsize=7.5)
    ax.axvline(len(SEG) - .5, color=INK, lw=1.2); ax.set_yticks(range(8)); ax.set_yticklabels([NAME[k] for k in ORDER], fontsize=8.5)
    ax.set_title(f"Native Cα contacts, run at pH {ph[2]}", loc="left", fontsize=10.5, color=INK, fontweight="bold")
    x0 = len(cols) - .5 + .25
    ax.text(x0, -.6, "ΔG (kcal/mol)\nMSM → MaxCal C" if ph == "ph4" else "ΔG (kcal/mol)\nMSM", fontsize=7.5, color=INK2, va="bottom")
    for i, k in enumerate(ORDER):
        e = out["clusters"][NAME[k]]
        t = "—" if k == 0 else (f"{e['dG_msm_ph4']:.1f} → {e['dG_maxcal_ph4']:.1f}" if ph == "ph4" else f"{e['dG_msm_ph7']:.1f}")
        ax.text(x0, i, t, fontsize=9, color=INK, va="center", clip_on=False)
    ax = axes[1, c_]; M = Rm[ph][ORDER]
    im2 = ax.imshow(M, cmap="Oranges", vmin=.1, vmax=1.4, aspect="auto")
    for (a, b), v in np.ndenumerate(M):
        ax.text(b, a, f"{v:.2f}", ha="center", va="center", fontsize=8, color="w" if v > .85 else INK)
    ax.set_xticks(range(len(RC))); ax.set_xticklabels([n for n, _ in RC], fontsize=8.5); ax.set_yticks(range(8)); ax.set_yticklabels([NAME[k] for k in ORDER], fontsize=8.5)
    ax.set_title(f"Displacement from 2L39 (core-fit), run at pH {ph[2]}", loc="left", fontsize=10.5, color=INK, fontweight="bold")
fig.colorbar(im, ax=axes[0, :], shrink=.8, pad=.09, label="native-contact fraction relative to Folded-like")
fig.colorbar(im2, ax=axes[1, :], shrink=.8, pad=.03, label="core-fit RMSD (nm)")
a = out["achieved_dG_op"]
fig.suptitle(f"What each structural cluster is, with free energies from the MSM alone and after MaxCal C at pH 4 (lag {LAG_NS:g} ns). Targets β1 displaced 2.2, PUF1 candidate 2.2, PUF2 candidate 3.1; "
             f"best compromise reached {a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f} kcal/mol.\nΔG against Folded-like. No MaxCal at pH 7. Plain frame averages per cluster. Displacement: superposed on the disulfide-proximal core (175–187, 201–216).", x=.01, ha="left", fontsize=10.5, color=INK)
fig.savefig(f"{prefix}_heatmap.png", dpi=130, bbox_inches="tight"); plt.close(fig)

LBL = {"Folded": "Folded", "PUF1": "α2–α3 lobe", "PUF2": "β1 arm", "PUF3": "β1 arm", "PUF3-like": "β1–loop–α1\nband"}
PL = {"pca": dict(c=(0, 1), rng=[[-50, 140], [-100, 70]], xl="PC1", yl="PC2", log=False), "dih": dict(c=(2, 3), rng=[[np.log10(.42), np.log10(1.6)], [np.log10(7), np.log10(120)]], xl="dRMSD vs 2L39 (rad)", yl="β1 dihedral deviation (°)", log=True)}
hist = lambda x, w, P: np.histogram2d(x[:, P["c"][0]], x[:, P["c"][1]], bins=60, range=P["rng"], weights=w)


def free(H):
    with np.errstate(divide="ignore"):
        G = -KT * np.log(H / H.sum())
    G[~np.isfinite(G)] = np.nan
    return G - np.nanmin(G)


def deco(ax, P, plane):
    if plane == "pca":
        for b in BAS:
            if b["label"] == "Folded" and b["ph"] == "pH 7":
                continue
            ax.add_patch(plt.Circle(b["centre"], 15, fill=False, ec="w", ls="--", lw=1.1))
            ax.text(b["centre"][0], b["centre"][1] + 17, LBL[b["label"]], color="w", fontsize=7, ha="center", va="bottom", fontweight="bold")
    if P["log"]:
        xt, yt = [.5, .6, .8, 1., 1.5], [10, 15, 20, 30, 40, 60, 100]
        ax.set_xticks(np.log10(xt)); ax.set_xticklabels([f"{v:g}" for v in xt]); ax.set_yticks(np.log10(yt)); ax.set_yticklabels([f"{v:g}" for v in yt])
    ax.set_xlabel(P["xl"]); ax.set_ylabel(P["yl"])


fig, axes = plt.subplots(2, 4, figsize=(21, 9.6))
for r_, (plane, P) in enumerate(PL.items()):
    H4, xe, ye = hist(d4["x"], d4["wp"], P); Hc, _, _ = hist(d4["x"], wC, P); H7, _, _ = hist(d7["x"], d7["wp"], P)
    with np.errstate(divide="ignore", invalid="ignore"):
        Dl = -KT * np.log((Hc / Hc.sum()) / (H4 / H4.sum())); Dl[~np.isfinite(Dl)] = np.nan
    for c_, (Zm, cm, lo, hi, cl, ti) in enumerate([(free(H4), "viridis", 0, 6, "free energy (kcal/mol)", "pH 4, MSM alone"), (free(Hc), "viridis", 0, 6, "free energy (kcal/mol)", "pH 4, after MaxCal C"),
                                                   (Dl, "RdBu_r", -3, 3, "−kT ln(p_MaxCal / p_MSM)  (kcal/mol)", "pH 4, change: red = population removed, blue = gained"), (free(H7), "viridis", 0, 6, "free energy (kcal/mol)", "pH 7, MSM alone")]):
        ax = axes[r_, c_]; im = ax.pcolormesh(xe, ye, np.ma.masked_invalid(Zm).T, cmap=cm, vmin=lo, vmax=hi, shading="flat"); fig.colorbar(im, ax=ax, label=cl, shrink=.85); deco(ax, P, plane)
        ax.set_title(ti, loc="left", fontsize=9.5, color=INK)
fig.suptitle(f"MSM free energy before and after MaxCal C at pH 4 (targets β1 displaced 2.2, PUF1 candidate 2.2, PUF2 candidate 3.1; reached {a[0]:.2f}, {a[1]:.2f}, {a[2]:.2f}; K = 100, lag {LAG_NS:g} ns, maximum-likelihood models). No MaxCal at pH 7.", x=.01, ha="left", fontsize=11.5, color=INK)
fig.tight_layout(rect=(0, 0, 1, .95)); fig.savefig(f"{prefix}_fes.png", dpi=125); plt.close(fig)
print("wrote", prefix, flush=True)
