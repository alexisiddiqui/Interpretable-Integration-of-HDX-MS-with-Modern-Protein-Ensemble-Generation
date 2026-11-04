"""Markov state models of MoPrP per pH from the unbiased MD and the seeded runs, plus a MaxCal consistency test
against the pH 4 HDX opening free energies.

Data per target pH, all at 100 ps:
  unbiased MD   4 replicas x (100 + 400 ns) blocks (pca101_scores.npz <ph>_u*, dihedrals from the dihedral archive,
                which holds every 10th 10-ps frame); blocks are treated as separate trajectories
  seeded runs   the half-1 runs (12 seeds x 6 basins, 20 ns) with the extended seeds (3 x 6 basins, 100 ns)
                replacing their 20 ns copies
Features: PC1, PC2 (101-HDX-residue Cartesian PCA), log10 dRMSD and log10 beta1 dihedral deviation (JAX-ENT
definitions), z-scored on the pooled data of both pH; one k-means discretisation shared by both pH.
With MSM_FEATURES=<tica_features.npz> (tica_features.py: backbone phi/psi sin/cos + Ca-Ca distances) the clustering
space is instead TICA (lag MSM_TICA_LAG_NS, first MSM_TICA_DIM components, kinetic-map scaling, no per-feature
scaling) fitted on the long unbiased MD only (MSM_TICA_FIT=unbiased, default: 4 x 500 ns per pH, both pH pooled so
the two share one basis; the seeded runs are only transformed) or on everything (MSM_TICA_FIT=all); PCA and dihedral coordinates are still used for the macrostates and the maps.
Macrostates (PCA, user basin labels): within MACRO_R of a basin centre; both folded centres form F; everything
else is I (intermediate). Microstates take the macrostate of their mean PCA position.

Per pH:
  - implied timescales over LAGS; maximum-likelihood reversible MSM at LAG on the largest strongly connected set
    (fraction of frames kept is reported; basins outside it have no population estimate)
  - Bayesian MSM (posterior samples) for macrostate populations and dG = -kT ln(p_X / p_F)
  - MFPTs between macrostates; Chapman-Kolmogorov test on the macrostates
  - raw core-to-core transition counts (milestoning on the macrostate cores, independent of the MSM): events,
    dwell time, rates; with zero events the 95 % upper bound 3/T
pH 4 only, MaxCal: minimum-caliber change of the MSM (exponential tilting of the transition matrix, Doob transform)
that makes p_PUF1/p_F and p_PUF2/p_F match the HDX dG_op (Moulick et al. 2015: 2.2 and 3.1 kcal/mol); reports
the Lagrange multipliers, the path KL divergence rate, and the opening/closing MFPTs before and after.
MaxCal uncertainty (MSM_MAXCAL_SAMPLES, default 200): the tilt repeated on each Bayesian sample with targets drawn
from the HDX values and errors (2.2 +/- 0.2, 3.1 +/- 0.5), and from their inverse-variance combination with the
MSM posterior; the pH 4 multipliers carried to the pH 7 samples (pH 7 has no HDX data).
Segment-opening MaxCal (MSM_OPEN_OBS = segment_contacts.py output): the same, but the constraint is the HDX
opening free energy of a segment, dG_op = -kT ln(P_open / P_closed) with P_open the MSM-weighted fraction of frames
whose native-contact fraction is below MSM_OPEN_Q (default 0.5); MSM_OPEN_TARGETS (default b1_rest:2.2:0.2, i.e.
beta1 opening = HDX PUF1). Other columns are reported as predictions.

Usage: msm_build.py <half1_qc.npz> <half1_dih.npz> <ext_qc.npz[,ext_qc2.npz]> <ext_dih.npz[,ext_dih2.npz]> <pca101_scores.npz> <basins_seed.json>
                    <out_dir>     env: MSM_K (150), MSM_LAG_NS (2), MSM_MACRO_R (15), MSM_SAMPLES (200),
                                  MSM_FEATURES, MSM_TICA_LAG_NS (2), MSM_TICA_DIM (10)
"""
import json
import os
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from deeptime.clustering import KMeans
from deeptime.decomposition import TICA
from deeptime.markov import TransitionCountEstimator
from deeptime.markov.msm import BayesianMSM, MaximumLikelihoodMSM
from deeptime.markov.tools.analysis import mfpt

h_qc, h_dih, e_qc, e_dih, scores_path, basins_path, out = sys.argv[1:8]
out = Path(out); out.mkdir(parents=True, exist_ok=True)
K = int(os.environ.get("MSM_K", 150))
LAG_NS = float(os.environ.get("MSM_LAG_NS", 2.0))
MACRO_R = float(os.environ.get("MSM_MACRO_R", 15.0))
N_SAMPLES = int(os.environ.get("MSM_SAMPLES", 200))
FEATURES = os.environ.get("MSM_FEATURES") or None
TICA_LAG_NS = float(os.environ.get("MSM_TICA_LAG_NS", 2.0))
TICA_DIM = int(os.environ.get("MSM_TICA_DIM", 10))
TICA_FIT = os.environ.get("MSM_TICA_FIT", "unbiased")  # unbiased | all
FEATURE_SET = os.environ.get("MSM_FEATURE_SET", "tors")   # all | dist (Ca-Ca distances) | tors (phi/psi sin/cos)
# embedding of the features used for clustering: tica (time-lagged) or phate (geometric diffusion embedding, Moon et
# al. 2019; fitted on MSM_PHATE_FIT = all frames of unbiased dynamics, or unbiased MD only + Nystrom extension)
EMBED = os.environ.get("MSM_EMBED", "tica")
PHATE_DIM = int(os.environ.get("MSM_PHATE_DIM", 3))
PHATE_FIT = os.environ.get("MSM_PHATE_FIT", "all")
PHATE_KNN = int(os.environ.get("MSM_PHATE_KNN", 5))
PHATE_LANDMARKS = int(os.environ.get("MSM_PHATE_LANDMARKS", 2000))
# per-feature z-scoring with the mean/SD of the fit set (PHATE's kNN graph is distance based; TICA whitens itself)
FEATURE_NORM = os.environ.get("MSM_FEATURE_NORM", "none")    # none | zscore
# MSM_EMBED=none clusters directly on the features; MSM_KMEANS_FIT picks the frames the k-means centres come from
KMEANS_FIT = os.environ.get("MSM_KMEANS_FIT", "all")         # all | unbiased
DT_NS = 0.1                                            # analysis resolution
LAGS_NS = [0.2, 0.5, 1, 2, 3, 5, 7.5, 10]
KT = 0.0019872043 * 298.15                             # kcal/mol
HDX_DG = {"PUF1": 2.2, "PUF2": 3.1}                    # pH 4, EX2, Moulick et al. 2015
HDX_ERR = {"PUF1": 0.2, "PUF2": 0.5}                   # their reported errors (Fig. 8 legend / Discussion)
MC_SAMPLES = int(os.environ.get("MSM_MAXCAL_SAMPLES", 200))
# segment-opening MaxCal: per-frame native-contact fractions (segment_contacts.py); a segment is open in a frame when
# its fraction is below MSM_OPEN_Q; MSM_OPEN_TARGETS = column:dG:sd[,...] are the HDX dG_op constraints (pH 4)
OPEN_OBS = os.environ.get("MSM_OPEN_OBS") or None
OPEN_Q = float(os.environ.get("MSM_OPEN_Q", 0.5))
OPEN_TARGETS = {c.split(":")[0]: (float(c.split(":")[1]), float(c.split(":")[2]))
                for c in os.environ.get("MSM_OPEN_TARGETS", "b1_rest:2.2:0.2").split(",") if c}
rng = np.random.default_rng(1)

S = np.load(scores_path, allow_pickle=True)
basins = json.load(open(basins_path))
CENTRES = {"F": [np.array(b["centre"]) for b in basins if b["label"] == "Folded"]}
for b in basins:
    if b["label"] != "Folded":
        CENTRES[b["label"].replace("-like", "L")] = [np.array(b["centre"])]
MACROS = ["F", "PUF1", "PUF2", "PUF3", "PUF3L", "I"]


# ---------------------------------------------------------------- data
def seeded():
    """{entry: (time_ns, (n, 4) features raw)} at DT_NS, extended runs replacing their 20 ns copies."""
    trajs = {}
    # extension archives (comma-separated lists, in matching order) come after half 1: they overwrite its 20 ns copies
    for qc, dih in [(h_qc, h_dih)] + list(zip(e_qc.split(","), e_dih.split(","), strict=True)):
        Q, D = np.load(qc), np.load(dih)
        runs = json.loads(str(Q["runs"]))
        assert json.loads(str(D["entries"])) == [r["entry"] for r in runs]
        for i, r in enumerate(runs):
            t = Q[f"r{i:03d}_time_ps"].astype(float) / 1000.0
            step = int(round(DT_NS / np.median(np.diff(t))))
            x = np.column_stack([Q[f"r{i:03d}_pc"], np.log10(D[f"r{i:03d}_drmsd_rad"]),
                                 np.log10(D[f"r{i:03d}_b1_dih_dev_deg"])]).astype(float)
            trajs[r["entry"]] = (t[::step], x[::step])
    return trajs


def unbiased(ph):
    """Unbiased blocks as separate trajectories at 100 ps (every 10th 10-ps frame, matching the dihedral archive)."""
    D = np.load(e_dih.split(",")[0])                         # every dihedral archive holds the same u_<ph> arrays
    pc, seg, frame = S[f"{ph}_u"], S[f"{ph}_u_seg"], S[f"{ph}_u_frame"]
    drmsd, b1 = D[f"u_{ph}_drmsd_rad"], D[f"u_{ph}_b1_dih_dev_deg"]
    out_, k = [], 0
    for s in np.unique(seg):                                 # segments in the archive order = dihedral order
        m = (seg == s) & (frame % 10 == 0)
        idx = np.flatnonzero(m)[np.argsort(frame[m])]
        n = len(idx)
        x = np.column_stack([pc[idx], np.log10(drmsd[k:k + n]), np.log10(b1[k:k + n])]).astype(float)
        out_.append((f"{ph}/unbiased/seg{s}", np.arange(n) * DT_NS, x))
        k += n
    assert k == len(drmsd), (ph, k, len(drmsd))
    return out_


SEEDED = seeded()
# MSM_DATA=unbiased builds the MSM from the long unbiased MD alone (diagnostic: are the seeded runs what breaks it?)
MSM_DATA = os.environ.get("MSM_DATA", "all")
TRAJ = {ph: ([(e, t, x) for e, (t, x) in SEEDED.items() if e.startswith(ph + "/")] if MSM_DATA == "all" else [])
        + unbiased(ph) for ph in ("ph4", "ph7")}
allx = np.concatenate([x for ph in TRAJ for _, _, x in TRAJ[ph]])
MU, SD = allx.mean(axis=0), allx.std(axis=0)


def macro_of_pc(pc):
    lab = np.full(len(pc), "I", dtype=object)
    for name, cs in CENTRES.items():
        for c in cs:
            lab[np.linalg.norm(pc - c, axis=1) < MACRO_R] = name
    return lab


# ---------------------------------------------------------------- discretisation
TICA_INFO = None
if FEATURES:
    Fz = np.load(FEATURES)
    fnames = Fz["feature_names"]
    cols = {"all": np.ones(len(fnames), bool), "dist": np.char.startswith(fnames.astype(str), "dCA_"),
            "tors": ~np.char.startswith(fnames.astype(str), "dCA_")}[FEATURE_SET]
    FEAT = {ph: [Fz[e.replace("/", "__")][:, cols] for e, _, _ in TRAJ[ph]] for ph in TRAJ}
    for ph in TRAJ:
        for (e, _, x), f in zip(TRAJ[ph], FEAT[ph]):
            assert len(f) == len(x), (e, len(f), len(x))
if FEATURES and EMBED == "phate":
    import phate
    keys = [(ph, k) for ph in FEAT for k in range(len(FEAT[ph]))]
    fit_keys = [(ph, k) for ph, k in keys if PHATE_FIT == "all" or "/unbiased/" in TRAJ[ph][k][0]]
    Xfit = np.concatenate([FEAT[ph][k] for ph, k in fit_keys]).astype(np.float64)
    if FEATURE_NORM == "zscore":
        f_mu, f_sd = Xfit.mean(axis=0), np.maximum(Xfit.std(axis=0), 1e-3)
        Xfit = (Xfit - f_mu) / f_sd
        FEAT = {ph: [((f - f_mu) / f_sd).astype(np.float32) for f in FEAT[ph]] for ph in FEAT}
    op = phate.PHATE(n_components=PHATE_DIM, knn=PHATE_KNN, n_landmark=PHATE_LANDMARKS, t="auto",
                     n_jobs=os.cpu_count(), random_state=1, verbose=1)
    Efit = op.fit_transform(Xfit)
    del Xfit
    SPACE = {ph: [None] * len(FEAT[ph]) for ph in FEAT}
    i = 0
    for ph, k in fit_keys:
        n = len(FEAT[ph][k]); SPACE[ph][k] = Efit[i:i + n]; i += n
    for ph, k in keys:
        if SPACE[ph][k] is None:                                 # Nystrom extension onto the fitted graph
            SPACE[ph][k] = op.transform(FEAT[ph][k].astype(np.float64))
    TICA_INFO = dict(embed="phate", dim=PHATE_DIM, feature_set=FEATURE_SET, feature_norm=FEATURE_NORM, fit_on=PHATE_FIT, knn=PHATE_KNN,
                     n_landmark=PHATE_LANDMARKS, t=int(op.optimal_t) if getattr(op, "optimal_t", None) else None,
                     fit_frames=int(len(Efit)), n_features=int(FEAT["ph4"][0].shape[1]))
elif FEATURES and EMBED == "none":
    SPACE = {ph: [f.astype(np.float64) for f in FEAT[ph]] for ph in FEAT}
    TICA_INFO = dict(embed="none", feature_set=FEATURE_SET, n_features=int(FEAT["ph4"][0].shape[1]), kmeans_fit=KMEANS_FIT)
elif FEATURES:
    if FEATURE_NORM == "zscore":                        # no effect on TICA in exact arithmetic (it whitens itself)
        fit = np.concatenate([f for ph in FEAT for (e, _, _), f in zip(TRAJ[ph], FEAT[ph])
                              if TICA_FIT == "all" or "/unbiased/" in e]).astype(np.float64)
        f_mu, f_sd = fit.mean(axis=0), np.maximum(fit.std(axis=0), 1e-6)
        del fit
        FEAT = {ph: [((f - f_mu) / f_sd).astype(np.float32) for f in FEAT[ph]] for ph in FEAT}
    tl = int(round(TICA_LAG_NS / DT_NS))
    # fit on the long unbiased MD only: seeded (short APO) runs start out of equilibrium and are only projected
    pairs = [(f[:-tl], f[tl:]) for ph in FEAT for (e, _, _), f in zip(TRAJ[ph], FEAT[ph])
             if len(f) > tl and (TICA_FIT == "all" or "/unbiased/" in e)]
    X0 = np.concatenate([a for a, _ in pairs]).astype(np.float64); X1 = np.concatenate([b for _, b in pairs]).astype(np.float64)
    tica = TICA(dim=TICA_DIM, scaling="kinetic_map").fit((X0, X1)).fetch_model()
    del X0, X1
    sv = np.asarray(tica.singular_values)
    TICA_INFO = dict(lag_ns=TICA_LAG_NS, dim=TICA_DIM, feature_set=FEATURE_SET, feature_norm=FEATURE_NORM, fit_on=TICA_FIT,
                     fit_pairs=int(sum(len(a) for a, _ in pairs)), n_features=int(FEAT["ph4"][0].shape[1]),
                     singular_values=[float(v) for v in sv[:20]],
                     timescales_ns=[float(-TICA_LAG_NS / np.log(abs(v))) for v in sv[:20] if 0 < abs(v) < 1],
                     cumulative_kinetic_variance=[float(v) for v in (np.cumsum(sv ** 2) / np.sum(sv ** 2))[:20]])
    SPACE = {ph: [tica.transform(f.astype(np.float64)) for f in FEAT[ph]] for ph in FEAT}
else:
    SPACE = {ph: [(x - MU) / SD for _, _, x in TRAJ[ph]] for ph in TRAJ}
z = np.concatenate([s for ph in SPACE for (e, _, _), s in zip(TRAJ[ph], SPACE[ph])
                    if KMEANS_FIT == "all" or "/unbiased/" in e])
km = KMeans(n_clusters=K, init_strategy="kmeans++", max_iter=200, fixed_seed=7, n_jobs=os.cpu_count()).fit(z).fetch_model()
DTRAJ = {ph: [km.transform(s).astype(int) for s in SPACE[ph]] for ph in SPACE}
if FEATURES and EMBED != "none":
    # embedding (first two components): unbiased MD grey, seeded frames coloured by source basin
    colours = dict(zip(["ph4_1", "ph4_2", "ph4_3", "ph7_1", "ph7_2", "ph7_3"],
                       ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#4a3aa7"]))
    names_ = {f"{b['ph'].replace(' ', '').lower()}_{b['id']}": f"{b['ph']} #{b['id']} {b['label']}" for b in basins}
    fig, axes = plt.subplots(1, 2, figsize=(14, 6.2), sharex=True, sharey=True)
    for ax, ph in zip(axes, ("ph4", "ph7")):
        for (e, _, _), s in zip(TRAJ[ph], SPACE[ph]):
            if "/unbiased/" in e:
                ax.scatter(s[::2, 0], s[::2, 1], s=2, color="#b8b8b8", alpha=0.3, lw=0, rasterized=True)
        for (e, _, _), s in zip(TRAJ[ph], SPACE[ph]):
            if "/unbiased/" not in e:
                b = e.split("/")[1]
                ax.scatter(s[:, 0], s[:, 1], s=2, color=colours[b], alpha=0.35, lw=0, rasterized=True)
        for b, c in colours.items():
            ax.scatter([], [], s=25, color=c, label=names_[b])
        ax.scatter([], [], s=25, color="#b8b8b8", label="unbiased MD")
        ax.set(title=f"run at pH {ph[2]}: {EMBED.upper()} embedding ({FEATURE_SET}), seeded frames by source basin",
               xlabel=f"{EMBED.upper()} 1", ylabel=f"{EMBED.upper()} 2")
    axes[1].legend(frameon=False, fontsize=8, markerscale=1.0, loc="best")
    fig.tight_layout(); fig.savefig(out / "msm_embedding.png", dpi=130); plt.close(fig)
# microstate mean PCA position (both pH pooled) -> macrostate
counts_all = np.zeros(K); pc_sum = np.zeros((K, 2))
for ph in TRAJ:
    for d, (_, _, x) in zip(DTRAJ[ph], TRAJ[ph]):
        np.add.at(counts_all, d, 1); np.add.at(pc_sum, d, x[:, :2])
MICRO_PC = pc_sum / np.maximum(counts_all, 1)[:, None]
MICRO_MACRO = macro_of_pc(MICRO_PC)
# how well microstates resolve the PCA basins: of the frames inside each basin core, the fraction whose microstate is
# mapped to that basin
_lab = np.concatenate([macro_of_pc(x[:, :2]) for ph in TRAJ for _, _, x in TRAJ[ph]])
_mic = np.concatenate([d for ph in DTRAJ for d in DTRAJ[ph]])
MAPPING_RECALL = {m: (float(np.mean(MICRO_MACRO[_mic[_lab == m]] == m)) if np.any(_lab == m) else None) for m in MACROS}
print("frames in each basin core whose microstate maps to it:", {m: (None if v is None else round(v, 3)) for m, v in MAPPING_RECALL.items()})
# fraction of each microstate's frames in which each segment is open (per pH)
OPEN_COLS, OPEN_G = [], {}
if OPEN_OBS:
    _Z = np.load(OPEN_OBS)
    OPEN_COLS = [str(c) for c in _Z["columns"]]
    for ph in TRAJ:
        num, den, trimmed = np.zeros((K, len(OPEN_COLS))), np.zeros(K), 0
        for d, (name, _, x) in zip(DTRAJ[ph], TRAJ[ph]):
            q = _Z[name.replace("/", "__")].astype(float)
            if abs(len(q) - len(d)) > 1:
                raise SystemExit(f"{name}: {len(q)} contact frames vs {len(d)} MSM frames")
            n = min(len(q), len(d)); trimmed += abs(len(q) - len(d))
            np.add.at(num, d[:n], (q[:n] < OPEN_Q).astype(float)); np.add.at(den, d[:n], 1.0)
        OPEN_G[ph] = num / np.maximum(den, 1)[:, None]
        print(f"{ph}: open fractions (Q < {OPEN_Q:g}) over frames:",
              {c: round(float(num[:, j].sum() / den.sum()), 4) for j, c in enumerate(OPEN_COLS)}, "trimmed frames", trimmed)

report = {"msm_data": MSM_DATA, "tica": TICA_INFO, "K": K, "lag_ns": LAG_NS, "macro_radius": MACRO_R, "dt_ns": DT_NS, "kT_kcal": KT, "hdx_dG_pH4": HDX_DG,
          "micro_macro_counts": {m: int(np.sum(MICRO_MACRO == m)) for m in MACROS}, "mapping_recall": MAPPING_RECALL,
          "ph": {}}


def lag_steps(lag_ns):
    return int(round(lag_ns / DT_NS))


def ml_msm(dtrajs, lag_ns):
    counts = TransitionCountEstimator(lag_steps(lag_ns), "sliding").fit(dtrajs).fetch_model()
    sub = counts.submodel_largest(directed=True)
    return MaximumLikelihoodMSM(reversible=True).fit(sub).fetch_model(), sub, counts


def macro_sets(msm):
    """Indices (in the MSM's active set) of each macrostate's microstates."""
    sym = msm.count_model.state_symbols
    return {m: np.flatnonzero(MICRO_MACRO[sym] == m) for m in MACROS}


def macro_pops(pi, sets):
    return {m: float(pi[s].sum()) for m, s in sets.items()}


def dG(p, ref="F"):
    return {m: (float(-KT * np.log(p[m] / p[ref])) if p[m] > 0 and p[ref] > 0 else None) for m in p if m != ref}


def mfpt_ns(P, sets, a, b, lag_ns):
    if len(sets[a]) == 0 or len(sets[b]) == 0:
        return None
    # origin set weighted by the stationary distribution within it
    return float(mfpt(P, target=sets[b], origin=sets[a], tau=1, mu=stationary(P)) * lag_ns)


def stationary(P):
    w, v = np.linalg.eig(P.T)
    p = np.abs(np.real(v[:, np.argmax(np.real(w))]))
    return p / p.sum()


def raw_events(ph):
    """Core-to-core milestoning on the macrostate cores (F, PUF*), non-core frames keep the last core label."""
    ev, dwell = {}, {}
    for _, t, x in TRAJ[ph]:
        lab = macro_of_pc(x[:, :2])
        last = None
        for l in lab:
            if l != "I":
                if last is not None and l != last:
                    ev[(last, l)] = ev.get((last, l), 0) + 1
                last = l
            if last is not None:
                dwell[last] = dwell.get(last, 0.0) + DT_NS
    rows = []
    for a in MACROS[:-1]:
        for b in MACROS[:-1]:
            if a == b or a not in dwell:
                continue
            n, T = ev.get((a, b), 0), dwell[a]
            rows.append(dict(origin=a, target=b, events=n, dwell_ns=round(T, 1),
                             rate_per_us=round(1000 * n / T, 3), rate_upper95_per_us=round(1000 * max(n, 3.0) / T, 3)
                             if n == 0 else None))
    return rows


def tilt(P, sets, names, lam):
    """Doob-transformed exponential tilt P'_ij = P_ij e^{sum_k lam_k f_k(j)} v_j / (mu v_i), f_k = indicator of
    macrostate names[k]; returns the tilted transition matrix and its stationary distribution."""
    F = np.zeros((len(names), len(P)))
    for k, m in enumerate(names):
        F[k, sets[m]] = 1.0
    M = P * np.exp(np.asarray(lam) @ F)[None, :]
    w, vr = np.linalg.eig(M); i = np.argmax(np.real(w)); mu = np.real(w[i]); v = np.abs(np.real(vr[:, i]))
    w2, vl = np.linalg.eig(M.T); u = np.abs(np.real(vl[:, np.argmax(np.real(w2))]))
    pi = u * v; pi /= pi.sum()
    Pn = M * v[None, :] / (mu * v[:, None])
    return Pn / Pn.sum(axis=1, keepdims=True), pi


def kl_rate(Pn, pin, P):
    with np.errstate(divide="ignore", invalid="ignore"):
        return float(np.nansum(pin[:, None] * np.where(Pn > 0, Pn * np.log(Pn / P), 0.0)))


def maxcal(P, sets, targets):
    """Minimum-caliber tilt P'_ij = P_ij e^{sum_k lam_k f_k(j)} v_j / (mu v_i) matching log(p'_X / p'_F) = -dG_X / kT."""
    names = [m for m in targets if len(sets[m])]

    def tilted(lam):
        return tilt(P, sets, names, lam)

    def resid(lam):
        _, pi = tilted(lam)
        pf = pi[sets["F"]].sum()
        return [np.log(pi[sets[m]].sum() / pf) + targets[m] / KT for m in names]

    sol = least_squares(resid, np.zeros(len(names)), xtol=1e-12, ftol=1e-12)
    Pn, pin = tilted(sol.x)
    return names, sol, Pn, pin, kl_rate(Pn, pin, P)


def tilt_obs(P, Fm, lam):
    """tilt() with arbitrary per-state observables Fm (n_constraints, n_states) instead of macrostate indicators."""
    M = P * np.exp(np.asarray(lam) @ Fm)[None, :]
    w, vr = np.linalg.eig(M); i = np.argmax(np.real(w)); mu = np.real(w[i]); v = np.abs(np.real(vr[:, i]))
    w2, vl = np.linalg.eig(M.T); u = np.abs(np.real(vl[:, np.argmax(np.real(w2))]))
    pi = u * v; pi /= pi.sum()
    Pn = M * v[None, :] / (mu * v[:, None])
    return Pn / Pn.sum(axis=1, keepdims=True), pi


def dg_open(pi, g):
    """HDX-style opening free energy of each observable: -kT ln(P_open / P_closed) (EX2)."""
    p = pi @ g
    with np.errstate(divide="ignore", invalid="ignore"):
        return np.where(p > 0, -KT * np.log(p / (1 - p)), np.nan)     # nan: never open in the data (not sampled)


def maxcal_open(P, g, cols, targets):
    """Minimum-caliber tilt on the open fractions g (n_states, n_cols) matching dG_op of the target columns."""
    idx = [cols.index(c) for c in targets]
    Fm = g[:, idx].T

    def resid(lam):
        _, pi = tilt_obs(P, Fm, lam)
        return [-dg_open(pi, g[:, [j]])[0] / KT + targets[c] / KT for j, c in zip(idx, targets)]

    sol = least_squares(resid, np.zeros(len(idx)), xtol=1e-12, ftol=1e-12)
    Pn, pin = tilt_obs(P, Fm, sol.x)
    return sol, Pn, pin, kl_rate(Pn, pin, P), Fm


def ci95(v):
    v = np.asarray([x for x in v if x is not None and np.isfinite(x)], float)
    return [float(np.percentile(v, q)) for q in (2.5, 50, 97.5)] if len(v) else None


def summarise(rows):
    """Percentile summary of per-sample MaxCal results (dicts of dG, mfpt, kl, lagrange)."""
    keys_dg = sorted({k for r in rows for k in r["dG"]}); keys_mf = sorted({k for r in rows for k in r["mfpt"]})
    return dict(n=len(rows), dG={m: ci95([r["dG"].get(m) for r in rows]) for m in keys_dg},
                mfpt_ns={k: ci95([r["mfpt"].get(k) for r in rows]) for k in keys_mf},
                kl_rate_per_ns=ci95([r["kl"] for r in rows]) if rows and "kl" in rows[0] else None,
                lagrange={m: ci95([r["lam"][m] for r in rows]) for m in (rows[0]["lam"] if rows and "lam" in rows[0] else [])})


def state_summary(P, sets, lag_ns, pi=None):
    pi = stationary(P) if pi is None else pi
    pops = macro_pops(pi, sets)
    pairs = [f"F->{m}" for m in MACROS[1:-1]] + [f"{m}->F" for m in MACROS[1:-1]]
    return dict(dG=dG(pops), mfpt={k: mfpt_ns(P, sets, *k.split("->"), lag_ns) for k in pairs})


# ---------------------------------------------------------------- per pH
fig_its, ax_its = plt.subplots(1, 2, figsize=(12, 4.5), sharey=True)
MSMS = {}
PI_MC = {}                                             # MaxCal-tilted ML stationary distributions (segment MaxCal)
for col, ph in enumerate(("ph4", "ph7")):
    dtrajs = DTRAJ[ph]
    n_frames = sum(len(d) for d in dtrajs)
    # implied timescales
    its = []
    for lag in LAGS_NS:
        m, _, _ = ml_msm(dtrajs, lag)
        its.append(m.timescales(5) * DT_NS)              # deeptime timescales are in steps, lag included
    its = np.array(its)
    for k in range(its.shape[1]):
        ax_its[col].plot(LAGS_NS, its[:, k], "-o", ms=3, lw=1.3)
    ax_its[col].fill_between(LAGS_NS, LAGS_NS, 1e-3, color="#cccccc", alpha=0.6)
    ax_its[col].axvline(LAG_NS, color="k", ls=":", lw=1)
    ax_its[col].set(xscale="log", yscale="log", xlabel="lag (ns)", title=f"run at pH {ph[2]}: implied timescales")
    # model at LAG
    msm, sub, full = ml_msm(dtrajs, LAG_NS)
    MSMS[ph] = msm
    sym = sub.state_symbols
    kept = sum(np.isin(d, sym).sum() for d in dtrajs) / n_frames
    sets = macro_sets(msm)
    pops = macro_pops(msm.stationary_distribution, sets)
    # macrostates whose microstates are visited but fall outside the active set
    visited = np.unique(np.concatenate(dtrajs))
    dropped = {m: int(np.sum((MICRO_MACRO[visited] == m) & ~np.isin(visited, sym))) for m in MACROS}
    # Bayesian posterior
    # Bayesian posterior on statistically effective counts (sliding counts are correlated and give overconfident
    # posteriors), restricted to the same active set as the ML model
    eff = TransitionCountEstimator(lag_steps(LAG_NS), "effective").fit(dtrajs).fetch_model()
    eff = eff.submodel(eff.symbols_to_states(sym))
    post = BayesianMSM(n_samples=N_SAMPLES, reversible=True).fit(eff).fetch_model()
    samp_pops = [macro_pops(s.stationary_distribution, sets) for s in post.samples]
    samp_dG = {m: np.array([-KT * np.log(sp[m] / sp["F"]) for sp in samp_pops if sp[m] > 0]) for m in MACROS if m != "F"}
    ci = {m: ([float(np.percentile(v, q)) for q in (2.5, 50, 97.5)] if len(v) else None) for m, v in samp_dG.items()}
    pop_ci = {m: [float(np.percentile([sp[m] for sp in samp_pops], q)) for q in (2.5, 50, 97.5)] for m in MACROS}
    # MFPTs (ns) between macrostates with microstates in the active set
    P = msm.transition_matrix
    mf = {f"{a}->{b}": mfpt_ns(P, sets, a, b, LAG_NS) for a in MACROS[:-1] for b in MACROS[:-1] if a != b}
    # CK test on macrostates with population (stationary-weighted start within the macrostate)
    ck = {}
    for m in [x for x in MACROS if len(sets[x])]:
        pi = msm.stationary_distribution
        p0 = np.zeros(len(P)); p0[sets[m]] = pi[sets[m]] / pi[sets[m]].sum()
        pred, est = [], []
        for kk in range(1, 6):
            pred.append(float((p0 @ np.linalg.matrix_power(P, kk))[sets[m]].sum()))
            mk, subk, _ = ml_msm(dtrajs, LAG_NS * kk)
            symk = subk.state_symbols
            setk = np.flatnonzero(MICRO_MACRO[symk] == m)
            if len(setk) == 0:
                est.append(None); continue
            pik = mk.stationary_distribution
            q0 = np.zeros(len(symk)); q0[setk] = pik[setk] / pik[setk].sum()
            est.append(float((q0 @ mk.transition_matrix)[setk].sum()))
        ck[m] = dict(predicted=pred, estimated=est)
    res = dict(frames=n_frames, trajectories=len(dtrajs), active_states=int(len(sym)), visited_states=int(len(visited)),
               frames_in_active_set=float(kept), macro_states_in_active={m: int(len(s)) for m, s in sets.items()},
               macro_states_dropped=dropped, populations_ml=pops, dG_ml=dG(pops), populations_ci95=pop_ci, dG_ci95=ci,
               timescales_ns=[float(v) for v in msm.timescales(5) * DT_NS], mfpt_ns=mf, ck_test=ck,
               raw_core_events=raw_events(ph))
    # MaxCal against HDX (pH 4)
    if ph == "ph4":
        names, sol, Pn, pin, kl = maxcal(P, sets, HDX_DG)
        pops_mc = macro_pops(pin, sets)
        res["maxcal"] = dict(constrained=names, lagrange=[float(v) for v in sol.x], residual=[float(v) for v in sol.fun],
                             populations=pops_mc, dG=dG(pops_mc), kl_rate_per_lag=kl, kl_rate_per_ns=kl / LAG_NS,
                             mfpt_ns={f"{a}->{b}": mfpt_ns(Pn, sets, a, b, LAG_NS) for a in MACROS[:-1] for b in MACROS[:-1]
                                      if a != b},
                             hdx_within_posterior95={m: (ci[m] is not None and ci[m][0] <= HDX_DG[m] <= ci[m][2])
                                                     for m in HDX_DG})
    # MaxCal with uncertainty: one tilt per Bayesian MSM sample (statistical error of the simulations) with targets
    # drawn from  hdx      the HDX dG_op and its reported error, or
    #             combined the inverse-variance combination of HDX and this pH-4 MSM posterior (the correction stops
    #                      short of HDX where the simulations are more certain than the experiment)
    # pH 7 has no HDX data: the per-sample pH 4 multipliers are applied unchanged to pH 7 samples (same lag, same
    # macrostate indicators), i.e. the correction is assumed to be pH independent; the untilted pH 7 posterior is the
    # reference.
    sets_b = {m: np.flatnonzero(MICRO_MACRO[eff.state_symbols] == m) for m in MACROS}
    samples = post.samples[:MC_SAMPLES]
    rng_mc = np.random.default_rng(7)
    if ph == "ph4":
        comb = {}
        for m in HDX_DG:
            v = samp_dG[m]; mu_s, sd_s = float(np.median(v)), float((np.percentile(v, 97.5) - np.percentile(v, 2.5)) / 3.92)
            w_e, w_s = 1 / HDX_ERR[m] ** 2, 1 / sd_s ** 2
            comb[m] = ((w_e * HDX_DG[m] + w_s * mu_s) / (w_e + w_s), (w_e + w_s) ** -0.5, mu_s, sd_s)
        LAMS = {}
        unc = {}
        for variant in ("hdx", "combined"):
            rows, lams, fails = [], [], 0
            for smp in samples:
                if variant == "hdx":
                    tg = {m: rng_mc.normal(HDX_DG[m], HDX_ERR[m]) for m in HDX_DG}
                else:
                    tg = {m: rng_mc.normal(comb[m][0], comb[m][1]) for m in HDX_DG}
                Ps = smp.transition_matrix
                nm, so, Pn_s, pin_s, kl_s = maxcal(Ps, sets_b, tg)
                if not so.success or np.max(np.abs(so.fun)) > 1e-6:
                    fails += 1; lams.append(None); continue
                st = state_summary(Pn_s, sets_b, LAG_NS, pin_s)
                rows.append(dict(**st, kl=kl_s / LAG_NS, lam=dict(zip(nm, map(float, so.x)))))
                lams.append((nm, so.x))
            unc[variant] = dict(summarise(rows), failed=fails)
            LAMS[variant] = lams
        unc["combined_targets"] = {m: dict(dG=c[0], sd=c[1], msm_median=c[2], msm_sd=c[3]) for m, c in comb.items()}
        unc["hdx_targets"] = {m: dict(dG=HDX_DG[m], sd=HDX_ERR[m]) for m in HDX_DG}
        res["maxcal_uncertainty"] = unc
    else:
        tr = {"prior": summarise([state_summary(smp.transition_matrix, sets_b, LAG_NS) for smp in samples])}
        for variant, lams in LAMS.items():
            rows = []
            for smp, lm in zip(samples, lams):
                if lm is None:
                    continue
                Pn_s, pin_s = tilt(smp.transition_matrix, sets_b, lm[0], lm[1])
                rows.append(dict(**state_summary(Pn_s, sets_b, LAG_NS, pin_s), kl=kl_rate(Pn_s, pin_s, smp.transition_matrix) / LAG_NS))
            tr[variant] = summarise(rows)
        res["maxcal_transfer_from_ph4"] = tr
    # segment-opening MaxCal: constraints on HDX segment opening (EX2: dG_op = -kT ln P_open/P_closed) instead of the
    # PCA macrostates; per Bayesian sample, targets drawn from HDX +/- error ("hdx") or the inverse-variance
    # combination with this MSM's posterior ("combined"); pH 4 multipliers carried to pH 7
    if OPEN_COLS:
        g_b = OPEN_G[ph][eff.state_symbols]
        prior_rows = []
        for smp in samples:
            pi_s = stationary(smp.transition_matrix)
            prior_rows.append(dict(dG_op=dict(zip(OPEN_COLS, map(float, dg_open(pi_s, g_b))))))
        seg = {"open_q": OPEN_Q, "targets": {c: dict(dG=t[0], sd=t[1]) for c, t in OPEN_TARGETS.items()},
               "prior_dG_op": {c: ci95([r["dG_op"][c] for r in prior_rows]) for c in OPEN_COLS},
               "open_fraction_frames": {c: float(np.mean(g_b[:, j])) for j, c in enumerate(OPEN_COLS)}}
        if ph == "ph4":
            comb = {}
            for c, (t, e) in OPEN_TARGETS.items():
                v = np.array([r["dG_op"][c] for r in prior_rows]); v = v[np.isfinite(v)]
                mu_s, sd_s = float(np.median(v)), float((np.percentile(v, 97.5) - np.percentile(v, 2.5)) / 3.92)
                w_e, w_s = 1 / e ** 2, 1 / max(sd_s, 1e-3) ** 2
                comb[c] = ((w_e * t + w_s * mu_s) / (w_e + w_s), (w_e + w_s) ** -0.5, mu_s, sd_s)
            seg["combined_targets"] = {c: dict(dG=v[0], sd=v[1], msm_median=v[2], msm_sd=v[3]) for c, v in comb.items()}
            SEG_LAMS = {}
            for variant in ("hdx", "combined"):
                rows, lams, fails = [], [], 0
                for smp in samples:
                    tg = {c: rng_mc.normal(*(OPEN_TARGETS[c] if variant == "hdx" else comb[c][:2])) for c in OPEN_TARGETS}
                    so, Pn_s, pin_s, kl_s, Fm = maxcal_open(smp.transition_matrix, g_b, OPEN_COLS, tg)
                    if not so.success or np.max(np.abs(so.fun)) > 1e-6:
                        fails += 1; lams.append(None); continue
                    st = state_summary(Pn_s, sets_b, LAG_NS, pin_s)
                    st["dG"].update({f"open:{c}": float(v) for c, v in zip(OPEN_COLS, dg_open(pin_s, g_b))})
                    rows.append(dict(**st, kl=kl_s / LAG_NS, lam=dict(zip(OPEN_TARGETS, map(float, so.x)))))
                    lams.append(so.x)
                seg[variant] = dict(summarise(rows), failed=fails)
                SEG_LAMS[variant] = lams
        else:
            idx = [OPEN_COLS.index(c) for c in OPEN_TARGETS]
            Fm7 = g_b[:, idx].T
            st0 = []
            for smp in samples:
                st = state_summary(smp.transition_matrix, sets_b, LAG_NS)
                st["dG"].update({f"open:{c}": float(v) for c, v in zip(OPEN_COLS, dg_open(stationary(smp.transition_matrix), g_b))})
                st0.append(st)
            seg["prior"] = summarise(st0)
            for variant, lams in SEG_LAMS.items():
                rows = []
                for smp, lm in zip(samples, lams):
                    if lm is None:
                        continue
                    Pn_s, pin_s = tilt_obs(smp.transition_matrix, Fm7, lm)
                    st = state_summary(Pn_s, sets_b, LAG_NS, pin_s)
                    st["dG"].update({f"open:{c}": float(v) for c, v in zip(OPEN_COLS, dg_open(pin_s, g_b))})
                    rows.append(dict(**st, kl=kl_rate(Pn_s, pin_s, smp.transition_matrix) / LAG_NS))
                seg[f"transfer_{variant}"] = summarise(rows)
        # maximum-likelihood model tilted to the central HDX values (pH 4) / with the pH 4 multipliers (pH 7)
        g_ml = OPEN_G[ph][sym]
        if ph == "ph4":
            so, Pn_ml, pin_ml, _, _ = maxcal_open(P, g_ml, OPEN_COLS, {c: t[0] for c, t in OPEN_TARGETS.items()})
            LAM_ML = so.x
        else:
            Pn_ml, pin_ml = tilt_obs(P, g_ml[:, [OPEN_COLS.index(c) for c in OPEN_TARGETS]].T, LAM_ML)
        PI_MC[ph] = pin_ml
        seg["ml_lagrange"] = [float(v) for v in LAM_ML]
        res["segment_maxcal"] = seg
    report["ph"][ph] = res
ax_its[0].set_ylabel("implied timescale (ns)")
fig_its.tight_layout(); fig_its.savefig(out / "msm_its.png", dpi=130); plt.close(fig_its)

# ---------------------------------------------------------------- per-frame weights (for re-plotting the maps)
# w reproduces the stationary density of the ML MSM (prior) and of its segment-MaxCal tilt; frames outside the
# active set get weight 0; x = PC1, PC2, log10 dRMSD, log10 beta1 dihedral deviation
_wf = {}
for ph in TRAJ:
    sym_ = MSMS[ph].count_model.state_symbols
    cnt_ = np.zeros(K)
    for d in DTRAJ[ph]:
        np.add.at(cnt_, d, 1)
    ds_ = np.concatenate(DTRAJ[ph])
    _wf[f"{ph}_x"] = np.concatenate([x for _, _, x in TRAJ[ph]]).astype(np.float32)
    _wf[f"{ph}_micro"] = ds_.astype(np.int16)
    for tag, pi_ in (("prior", MSMS[ph].stationary_distribution), ("maxcal", PI_MC.get(ph))):
        if pi_ is None:
            continue
        full = np.zeros(K); full[sym_] = pi_
        _wf[f"{ph}_w_{tag}"] = (full[ds_] / np.maximum(cnt_[ds_], 1)).astype(np.float64)
    if OPEN_G:
        _wf[f"{ph}_open_frac_micro"] = OPEN_G[ph].astype(np.float32)
np.savez_compressed(out / "msm_weights.npz", open_cols=np.array(OPEN_COLS), **_wf)

# ---------------------------------------------------------------- MSM free-energy maps
fig, axes = plt.subplots(2, 2, figsize=(13, 10.5))
for row, ph in enumerate(("ph4", "ph7")):
    msm = MSMS[ph]
    sym = msm.count_model.state_symbols
    pi_full = np.zeros(K); pi_full[sym] = msm.stationary_distribution
    cnt = np.zeros(K)
    for d in DTRAJ[ph]:
        np.add.at(cnt, d, 1)
    xs = np.concatenate([x for _, _, x in TRAJ[ph]]); ds = np.concatenate(DTRAJ[ph])
    w = pi_full[ds] / np.maximum(cnt[ds], 1)                 # per-frame weight reproducing the MSM stationary density
    for col, (cols, xl, yl, rng_) in enumerate([((0, 1), "PC1", "PC2", [[-50, 140], [-100, 70]]),
                                                ((2, 3), "dRMSD (rad, log)", "β1 dihedral dev. (°, log)",
                                                 [[np.log10(0.42), np.log10(1.6)], [np.log10(7), np.log10(120)]])]):
        ax = axes[row, col]
        H, xe, ye = np.histogram2d(xs[:, cols[0]], xs[:, cols[1]], bins=60, range=rng_, weights=w)
        with np.errstate(divide="ignore"):
            G = -KT * np.log(H / H.sum()); G -= np.nanmin(G[np.isfinite(G)])
        im = ax.pcolormesh(xe, ye, np.ma.masked_invalid(np.where(np.isfinite(G), G, np.nan)).T, cmap="viridis",
                           vmin=0, vmax=6, shading="flat")
        fig.colorbar(im, ax=ax, label="MSM free energy (kcal/mol)")
        if col == 0:
            for name, cs in CENTRES.items():
                for c in cs:
                    ax.add_patch(plt.Circle(c, MACRO_R, fill=False, ec="w", ls="--", lw=1.2))
                    ax.text(*c, name, color="w", ha="center", va="center", fontsize=8, fontweight="bold")
        else:
            xt, yt = [0.5, 0.6, 0.8, 1.0, 1.5], [10, 15, 20, 30, 40, 60, 100]
            ax.set_xticks(np.log10(xt)); ax.set_xticklabels([f"{v:g}" for v in xt])
            ax.set_yticks(np.log10(yt)); ax.set_yticklabels([f"{v:g}" for v in yt])
        ax.set(xlabel=xl, ylabel=yl, title=f"run at pH {ph[2]}: MSM stationary free energy (lag {LAG_NS:g} ns, K={K})")
fig.tight_layout(); fig.savefig(out / "msm_fes.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- summary figure
fig, axes = plt.subplots(1, 2, figsize=(14, 4.8), sharey=True)
for ax, ph in zip(axes, ("ph4", "ph7")):
    r = report["ph"][ph]
    names = [m for m in MACROS if m != "F"]
    xs_ = np.arange(len(names))
    for i, m in enumerate(names):
        c = r["dG_ci95"][m]
        if c:
            ax.errorbar(i, c[1], yerr=[[c[1] - c[0]], [c[2] - c[1]]], fmt="o", color="#2a78d6", capsize=3,
                        label="MSM (Bayesian median, 95 %)" if i == 0 else None)
        if ph == "ph4" and m in HDX_DG:
            ax.scatter(i + 0.15, HDX_DG[m], marker="*", s=120, color="#d6604d", zorder=4,
                       label="HDX ΔG_op (Moulick 2015)" if m == "PUF1" else None)
            if "maxcal" in r and r["maxcal"]["dG"].get(m) is not None:
                ax.scatter(i - 0.15, r["maxcal"]["dG"][m], marker="D", s=30, color="#1baf7a", zorder=4,
                           label="MaxCal-tilted MSM" if m == "PUF1" else None)
    ax.axhline(0, color="k", lw=0.7)
    ax.set_xticks(xs_); ax.set_xticklabels(names)
    ax.set_title(f"run at pH {ph[2]}: ΔG vs F (active set keeps {r['frames_in_active_set']:.1%} of frames)", loc="left")
    ax.legend(frameon=False, fontsize=8)
axes[0].set_ylabel("ΔG relative to Folded (kcal/mol)")
fig.tight_layout(); fig.savefig(out / "msm_summary.png", dpi=130); plt.close(fig)

(out / "msm_report.json").write_text(json.dumps(report, indent=1, default=float))
for ph, r in report["ph"].items():
    print(f"== {ph}: {r['frames']} frames, {r['trajectories']} trajectories; active {r['active_states']}/{r['visited_states']} "
          f"states, {r['frames_in_active_set']:.1%} of frames; macro states in active set {r['macro_states_in_active']}, "
          f"dropped {r['macro_states_dropped']}")
    print("   timescales (ns):", [round(v, 1) for v in r["timescales_ns"]])
    print("   populations (ML):", {m: f"{v:.3g}" for m, v in r["populations_ml"].items()})
    print("   dG vs F, Bayesian 95 %:", {m: (None if c is None else [round(v, 2) for v in c]) for m, c in r["dG_ci95"].items()})
    print("   MFPT (ns):", {k: (None if v is None else round(v, 1)) for k, v in r["mfpt_ns"].items()})
    print("   raw core events:", [(e["origin"], e["target"], e["events"], e["dwell_ns"]) for e in r["raw_core_events"] if e["events"]])
    if "maxcal" in r:
        mc = r["maxcal"]
        print("   MaxCal:", "constrained", mc["constrained"], "lambda", [round(v, 3) for v in mc["lagrange"]],
              "KL/ns", f"{mc['kl_rate_per_ns']:.3g}", "dG", {m: (None if v is None else round(v, 2)) for m, v in mc["dG"].items()},
              "HDX in MSM 95 %:", mc["hdx_within_posterior95"])
if TICA_INFO and "timescales_ns" in TICA_INFO:
    print("TICA:", TICA_INFO["n_features"], "features, lag", TICA_LAG_NS, "ns; timescales (ns)",
          [round(v, 1) for v in TICA_INFO["timescales_ns"][:10]])
print("wrote", out)
