"""TeaA landscapes: CA-PCA log-density and RMSD(open) vs RMSD(closed) maps for MD vs generated ensembles.

Usage (from the MaxENT-FK repo, login node is fine):
    OMP_NUM_THREADS=1 uv run --no-sync python $ROOT/_runtime/analysis/landscape_plots.py

Edit ENSEMBLES / PANELS / CURVES below to add panels (e.g. a second seed). Outputs go to OUT.
"""
from __future__ import annotations

import csv, glob, json, os, warnings
from pathlib import Path

import numpy as np

warnings.filterwarnings("ignore")
import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LogNorm, TwoSlopeNorm  # noqa: E402
from scipy.ndimage import gaussian_filter  # noqa: E402

RT = Path("/home/u6xq/hussain.u6xq/_runtime")
REPO = Path("/scratch/u6xq/hussain.u6xq/MaxENT-FK")
TRAJ = REPO / "examples/TeaA/raw_data/trajectories"
REFS = REPO / "examples/TeaA/cv/refs"
A = RT / "analysis/TeaA_cv"
FD = RT / "analysis/fiedler"
OUT = FD / "landscapes_F"
S = RT / "runs/TeaA_sdedit"
SF = RT / "runs/TeaA_sdedit_filt"
I = RT / "runs/TeaA_inState"
LAMBDA = 1000.0

# ---------------------------------------------------------------- ensembles (sources)
# md: xtc stem (topology TeaA_ref_closed_state.pdb); runs: run dirs with predictions/*/*_model_*.pdb;
# weights: MaxEnt CSV (lambda,label,path,weight,...) matched by realpath at lambda LAMBDA.
ENSEMBLES = {
    "md_open": {"md": "TeaA_open_sliced"},
    "md_closed": {"md": "TeaA_closed_sliced"},
    "md_intermediate": {"md": "TeaA_open_closed_intermediate_sliced"},
    "unguided": {"runs": [S / f"ung_noise_s{k}_s{k}_n50" for k in (43, 44, 45)]},
    "metad_union": {"runs": [S / f"metadF_r{k}_s52_n50" for k in (2, 3, 4)]
                    + [S / f"contF_c{k}_s50{k}_n50" for k in range(1, 9)],
                    "weights": FD / "metad_F_blind_weights.csv"},
    "refined_a025": {"runs": sorted(SF.glob("refa025F_k*_p70")),
                     "weights": FD / "sweep_F_a0.25_blind.csv"},
    "control": {"runs": sorted(SF.glob("ctlF_k*_p70")),
                "weights": FD / "step2_F_ctl_blind.csv"},
    "instate_open": {"runs": [I / "refopen_thr1_s42"]},
    "instate_closed": {"runs": [I / "closed_thr1_s42"]},
}
POP = {"open": 0.4, "closed": 0.6}  # target populations
# panel: label, ensembles, weighting = "uniform" | "maxent" | {ensemble: total mass}
PANELS = [
    ("MD open (15 fr)", ["md_open"], "uniform"),
    ("MD closed (332 fr)", ["md_closed"], "uniform"),
    ("MD combined 40:60", ["md_open", "md_closed"], {"md_open": POP["open"], "md_closed": POP["closed"]}),
    ("MD open-closed-intermediate (890 fr)", ["md_intermediate"], "uniform"),
    ("Unguided Boltz (150)", ["unguided"], "uniform"),
    ("Metad union, uniform (550)", ["metad_union"], "uniform"),
    ("Metad union, MaxEnt λ1000", ["metad_union"], "maxent"),
    ("Refined α0.25, uniform (236, pLDDT≥0.7)", ["refined_a025"], "uniform"),
    ("Refined α0.25, MaxEnt λ1000", ["refined_a025"], "maxent"),
    ("Control, uniform (236)", ["control"], "uniform"),
    ("Control, MaxEnt λ1000", ["control"], "maxent"),
    ("In-state pools (20 open + 20 closed)", ["instate_open", "instate_closed"], "uniform"),
]
# summary 1D curves: label, ensembles, weighting
CURVES = [
    ("MD 40:60 (per-state weighted)", ["md_open", "md_closed"], {"md_open": POP["open"], "md_closed": POP["closed"]}),
    ("Unguided Boltz", ["unguided"], "uniform"),
    ("Metad union, uniform", ["metad_union"], "uniform"),
    ("Refined α0.25, uniform", ["refined_a025"], "uniform"),
    ("Refined α0.25, MaxEnt λ1000", ["refined_a025"], "maxent"),
]
PCA_FIT = {"md_open": 0.5, "md_closed": 0.5}  # per-state equal weighting for the PCA fit (default)
SIGMA_PC = 1.5  # A (PC units = Euclidean norm over 309 CA), Gaussian smoothing of the 2D/1D PC densities
SIGMA_THETA = 1.5  # deg, 1D theta density
NGRID = 240
DECADES = 3.5  # colour range of log10 density
THR = {"open": 1.88, "closed": 1.82}  # lobe-II hinge-state thresholds (A)
C_OPEN, C_CLOSED = "#d95f02", "#1f78b4"


def rng(s):
    return [i for part in s.split(",") for i in range(int(part.split("-")[0]), int(part.split("-")[1]) + 1)]


LOBE_I, LOBE_II = set(rng("1-122,207-249,284-309")), set(rng("123-206,250-283"))
RES = list(range(1, 310))  # project convention (hinge_eval/theta_eval): residues 1-309
FIT = np.array([i for i, r in enumerate(RES) if r in LOBE_I])
MEAS = np.array([i for i, r in enumerate(RES) if r in LOBE_II])
ALL = np.arange(len(RES))


def ca(path):
    d = {}
    for line in open(path):
        if line.startswith("ATOM") and line[12:16].strip() == "CA":
            d.setdefault(int(line[22:26]), np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])]))
    return d


def ca_arr(path):
    c = ca(path)
    return np.stack([c[r] for r in RES]) if all(r in c for r in RES) else None


def kabsch(P, Q):  # R, t with P @ R.T + t ~ Q
    pc, qc = P.mean(0), Q.mean(0)
    u, _, vt = np.linalg.svd((P - pc).T @ (Q - qc))
    d = np.sign(np.linalg.det(vt.T @ u.T))
    R = vt.T @ np.diag([1, 1, d]) @ u.T
    return R, qc - R @ pc


def fit_rmsd(x, ref, fit, meas):
    R, t = kabsch(x[fit], ref[fit])
    y = x @ R.T + t
    return float(np.sqrt(((y[meas] - ref[meas]) ** 2).sum(-1).mean()))


def superpose(x, ref):
    R, t = kabsch(x, ref)
    return x @ R.T + t


# blind theta (copied from theta_eval.py)
_info = json.load(open(FD / "blind_axis_fiedler.json"))
THFIT = np.array([i for i, r in enumerate(RES) if r in set(_info["lobe_I"])])
THMEAS = np.array([i for i, r in enumerate(RES) if r in set(_info["lobe_II"])])
_axis = np.array(_info["axis"])
_B = ca_arr(_info["base"])


def logmap(R):
    c = np.clip((np.trace(R) - 1) / 2, -1, 1)
    ang = np.arccos(c)
    if ang < 1e-8:
        return np.zeros(3)
    return np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]]) / (2 * np.sin(ang)) * ang


def theta(X):
    R1, t1 = kabsch(X[THFIT], _B[THFIT])
    Y = X @ R1.T + t1
    R2, _ = kabsch(_B[THMEAS], Y[THMEAS])
    return float(np.degrees(logmap(R2) @ _axis))


REF = {s: ca_arr(REFS / f"TeaA_ref_{s}_boltznames.pdb") for s in ("open", "closed")}


def load_md(stem):
    import MDAnalysis as mda
    u = mda.Universe(str(TRAJ / "TeaA_ref_closed_state.pdb"), str(TRAJ / f"{stem}.xtc"))
    sel = u.select_atoms("name CA")
    pos = {r: i for i, r in enumerate(sel.resids)}
    idx = np.array([pos[r] for r in RES])
    X = np.stack([sel.positions[idx].astype(float) for _ in u.trajectory])
    return X, [f"{TRAJ / stem}.xtc#{i}" for i in range(len(X))]


def load_weights(path):
    w = {}
    with open(path) as f:
        for row in csv.DictReader(f):
            if float(row["lambda"]) == LAMBDA:
                w[os.path.realpath(row["path"])] = (float(row["weight"]), float(row["lobeII_rmsd_open"]),
                                                    float(row["lobeII_rmsd_closed"]))
    return w


def collect():
    recs = {}
    for name, spec in ENSEMBLES.items():
        if "md" in spec:
            X, paths = load_md(spec["md"])
        else:
            paths = [p for r in spec["runs"] for p in sorted(glob.glob(f"{r}/predictions/*/*_model_*.pdb"))]
            arrs = [ca_arr(p) for p in paths]
            miss = [p for p, a in zip(paths, arrs) if a is None]
            if miss:
                print(f"[{name}] skipped {len(miss)} PDBs with missing CA")
            paths = [p for p, a in zip(paths, arrs) if a is not None]
            X = np.stack([a for a in arrs if a is not None])
        d = {"X": X, "paths": paths, "n": len(X)}
        d["rmsd_open"] = np.array([fit_rmsd(x, REF["open"], ALL, ALL) for x in X])
        d["rmsd_closed"] = np.array([fit_rmsd(x, REF["closed"], ALL, ALL) for x in X])
        d["lobeII_rmsd_open"] = np.array([fit_rmsd(x, REF["open"], FIT, MEAS) for x in X])
        d["lobeII_rmsd_closed"] = np.array([fit_rmsd(x, REF["closed"], FIT, MEAS) for x in X])
        d["theta"] = np.array([theta(x) for x in X])
        d["w"] = np.full(len(X), np.nan)
        if "weights" in spec:
            W = load_weights(spec["weights"])
            keys = [os.path.realpath(p) for p in paths]
            hit = [k in W for k in keys]
            d["w"] = np.array([W[k][0] if k in W else 0.0 for k in keys])
            dl = [max(abs(W[k][1] - a), abs(W[k][2] - b)) for k, a, b in
                  zip(keys, d["lobeII_rmsd_open"], d["lobeII_rmsd_closed"]) if k in W]
            print(f"[{name}] weights matched {sum(hit)}/{len(keys)} (csv rows {len(W)}), sum {d['w'].sum():.6f}, "
                  f"max |lobeII rmsd - csv| {max(dl):.4f} A, n_eff {1 / np.sum((d['w'] / d['w'].sum()) ** 2):.1f}")
        recs[name] = d
        print(f"[{name}] n={len(X)}")
    return recs


def panel_data(recs, ens, weighting, key):
    vals, ws = [], []
    for e in ens:
        v = recs[e][key]
        if weighting == "uniform":
            w = np.ones(len(v))
        elif weighting == "maxent":
            w = recs[e]["w"].copy()
        else:
            w = np.full(len(v), weighting[e] / len(v))
        vals.append(v)
        ws.append(w)
    v, w = np.concatenate(vals), np.concatenate(ws)
    return v, w / w.sum()


def wpca(X, w):
    mu = (w[:, None] * X).sum(0)
    Z = X - mu
    C = (w[:, None] * Z).T @ Z
    ev, V = np.linalg.eigh(C)
    o = np.argsort(ev)[::-1]
    return mu, ev[o], V[:, o]


def wcorr(a, b, w=None):
    w = np.ones(len(a)) / len(a) if w is None else w / w.sum()
    ma, mb = (w * a).sum(), (w * b).sum()
    return float((w * (a - ma) * (b - mb)).sum() / np.sqrt((w * (a - ma) ** 2).sum() * (w * (b - mb) ** 2).sum()))


def density2d(x, y, w, ex, ey, sig_bins):
    H, _, _ = np.histogram2d(x, y, bins=[ex, ey], weights=w)
    H = gaussian_filter(H, sig_bins, mode="constant")
    area = (ex[1] - ex[0]) * (ey[1] - ey[0])
    return H / (H.sum() * area)


def hpd_level(D, area, mass=0.95):
    f = np.sort(D.ravel())[::-1]
    c = np.cumsum(f) * area
    return f[min(np.searchsorted(c, mass), len(f) - 1)]


def lookup(D, ex, ey, x, y):
    i = np.clip(np.searchsorted(ex, x) - 1, 0, len(ex) - 2)
    j = np.clip(np.searchsorted(ey, y) - 1, 0, len(ey) - 2)
    return D[i, j]


def kde1d(v, w, grid, sig):
    z = (grid[:, None] - v[None, :]) / sig
    return (np.exp(-0.5 * z ** 2) * w[None, :]).sum(1) / (sig * np.sqrt(2 * np.pi))


def grid_axes(n):
    nc = 4
    nr = int(np.ceil(n / nc))
    fig, axs = plt.subplots(nr, nc, figsize=(4.1 * nc, 3.7 * nr), sharex=True, sharey=True, squeeze=False)
    for ax in axs.ravel()[n:]:
        ax.set_visible(False)
    return fig, axs.ravel()


def save(fig, stem):
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{stem}.{ext}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("wrote", OUT / f"{stem}.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    recs = collect()
    ref_cl = REF["closed"]
    for d in recs.values():
        d["Xa"] = np.stack([superpose(x, ref_cl).ravel() for x in d["X"]])
    refa = {s: superpose(REF[s], ref_cl).ravel() for s in REF}
    print("residues used: %d CA (1-309); MD topology and Boltz PDBs both have 310" % len(RES))

    # ---------------- PCA on MD frames only
    Xmd = np.concatenate([recs[e]["Xa"] for e in PCA_FIT])
    th_md = np.concatenate([recs[e]["theta"] for e in PCA_FIT])
    w_state = np.concatenate([np.full(recs[e]["n"], PCA_FIT[e] / recs[e]["n"]) for e in PCA_FIT])
    w_frame = np.full(len(Xmd), 1.0 / len(Xmd))
    fits = {}
    for nm, w in (("per-state", w_state), ("per-frame", w_frame)):
        mu, ev, V = wpca(Xmd, w)
        V = V[:, :2].copy()
        if wcorr((Xmd - mu) @ V[:, 0], th_md) < 0:
            V[:, 0] *= -1
        if ((refa["closed"] - mu) @ V[:, 1]) < 0:
            V[:, 1] *= -1
        fits[nm] = (mu, ev, V)
        p = (Xmd - mu) @ V
        print(f"PCA {nm}: var explained PC1 {ev[0] / ev.sum():.4f} PC2 {ev[1] / ev.sum():.4f}; "
              f"corr(PC1, theta) MD frames unweighted {wcorr(p[:, 0], th_md):.4f} weighted {wcorr(p[:, 0], th_md, w):.4f}; "
              f"PC1 open ref {(refa['open'] - mu) @ V[:, 0]:.2f} closed ref {(refa['closed'] - mu) @ V[:, 0]:.2f}")
    print(f"|cos(PC1 per-state, PC1 per-frame)| = {abs(fits['per-state'][2][:, 0] @ fits['per-frame'][2][:, 0]):.4f}; "
          f"|cos PC2| = {abs(fits['per-state'][2][:, 1] @ fits['per-frame'][2][:, 1]):.4f}")
    mu, ev, V = fits["per-state"]
    for d in recs.values():
        d["pc"] = (d["Xa"] - mu) @ V
        d["PC1"], d["PC2"] = d["pc"][:, 0], d["pc"][:, 1]
    refpc = {s: (refa[s] - mu) @ V for s in refa}
    gen = [e for e in recs if not e.startswith("md_")]
    allpc = np.concatenate([recs[e]["pc"] for e in recs])
    allth = np.concatenate([recs[e]["theta"] for e in recs])
    allpc1 = np.concatenate([recs[e]["PC1"] for e in recs])
    print(f"corr(PC1, theta): all structures {wcorr(allpc1, allth):.4f}; generated only "
          f"{wcorr(np.concatenate([recs[e]['PC1'] for e in gen]), np.concatenate([recs[e]['theta'] for e in gen])):.4f}; "
          f"MD incl. intermediates {wcorr(recs['md_intermediate']['PC1'], recs['md_intermediate']['theta']):.4f}")
    for e in recs:
        print(f"  corr(PC1, theta) {e:16s} {wcorr(recs[e]['PC1'], recs[e]['theta']):.4f}")

    # ---------------- common grid + densities
    lo, hi = allpc.min(0), allpc.max(0)
    pad = 0.08 * (hi - lo)
    lo, hi = lo - pad, hi + pad
    ex, ey = np.linspace(lo[0], hi[0], NGRID + 1), np.linspace(lo[1], hi[1], NGRID + 1)
    sig = (SIGMA_PC / (ex[1] - ex[0]), SIGMA_PC / (ey[1] - ey[0]))
    area = (ex[1] - ex[0]) * (ey[1] - ey[0])
    dens = []
    for label, ens, wt in PANELS:
        x, w = panel_data(recs, ens, wt, "PC1")
        y, _ = panel_data(recs, ens, wt, "PC2")
        dens.append(density2d(x, y, w, ex, ey, sig))
    Dst, lvl = {}, {}
    for s in ("open", "closed"):
        e = f"md_{s}"
        Dst[s] = density2d(recs[e]["PC1"], recs[e]["PC2"], np.full(recs[e]["n"], 1 / recs[e]["n"]), ex, ey, sig)
        lvl[s] = hpd_level(Dst[s], area)
    for d in recs.values():
        for s in Dst:
            d[f"in95_{s}"] = lookup(Dst[s], ex, ey, d["PC1"], d["PC2"]) >= lvl[s]

    vmax = max(np.log10(D.max()) for D in dens)
    vmin = vmax - DECADES
    xc, yc = 0.5 * (ex[1:] + ex[:-1]), 0.5 * (ey[1:] + ey[:-1])

    def refs_pc(ax):
        ax.plot(*refpc["open"], marker="*", ms=13, mfc=C_OPEN, mec="k", mew=0.8, ls="none", label="open ref", zorder=5)
        ax.plot(*refpc["closed"], marker="P", ms=11, mfc=C_CLOSED, mec="k", mew=0.8, ls="none", label="closed ref", zorder=5)
        for s, c in (("open", C_OPEN), ("closed", C_CLOSED)):
            ax.contour(xc, yc, Dst[s].T, levels=[lvl[s]], colors=[c], linewidths=0.9, linestyles="--", zorder=4)

    fig, axs = grid_axes(len(PANELS))
    for ax, (label, ens, wt), D in zip(axs, PANELS, dens):
        L = np.log10(np.where(D > 0, D, np.nan))
        L = np.ma.masked_where(~np.isfinite(L) | (L < vmin), L)
        im = ax.pcolormesh(ex, ey, L.T, cmap="Greens", vmin=vmin, vmax=vmax, shading="flat", rasterized=True)
        refs_pc(ax)
        ax.set_title(label, fontsize=9.5)
        ax.grid(alpha=0.25, lw=0.5)
    for ax in axs[len(PANELS) - 4:len(PANELS)]:
        ax.set_xlabel(f"PC1 (Å)  [{100 * ev[0] / ev.sum():.1f}% MD var]")
    for ax in axs[::4]:
        ax.set_ylabel(f"PC2 (Å)  [{100 * ev[1] / ev.sum():.1f}%]")
    axs[0].legend(fontsize=7.5, loc="lower left", framealpha=0.8)
    fig.suptitle("TeaA Fiedler lobes (corrected amide H), CA PCA (fit on MD open+closed, per-state equal weights; all structures superposed on closed ref)\n"
                 f"log10 density, Gaussian σ={SIGMA_PC} Å; dashed = MD open / closed 95% HPD regions", fontsize=10.5)
    fig.tight_layout(rect=(0, 0, 0.93, 0.95))
    cax = fig.add_axes([0.945, 0.25, 0.012, 0.5])
    fig.colorbar(im, cax=cax, label="log10 density (Å$^{-2}$)")
    save(fig, "pca_logdensity")

    # ---------------- RMSD landscapes
    d_oc = fit_rmsd(REF["open"], REF["closed"], ALL, ALL)
    d_oc_l = fit_rmsd(REF["open"], REF["closed"], FIT, MEAS)
    print(f"open-closed ref RMSD: all-CA {d_oc:.3f} A, lobe II after lobe-I fit {d_oc_l:.3f} A")
    gth = np.concatenate([recs[e]["theta"] for e in recs])
    tlim = (np.percentile(gth, 1), np.percentile(gth, 99))
    tnorm = TwoSlopeNorm(vcenter=-5.0, vmin=min(tlim[0], -20.5), vmax=max(tlim[1], 10.5))
    allw = np.concatenate([recs[e]["w"] for e in recs if np.isfinite(recs[e]["w"]).all()])
    wnorm = LogNorm(vmin=1e-6, vmax=allw.max())
    sc_t = sc_w = None
    for kind, kx, ky, dd, xl, yl, thr in (
            ("allCA", "rmsd_open", "rmsd_closed", d_oc, "all-CA RMSD to open ref (Å)", "all-CA RMSD to closed ref (Å)", False),
            ("lobeII", "lobeII_rmsd_open", "lobeII_rmsd_closed", d_oc_l, "lobe-II RMSD to open (lobe-I fit, Å)",
             "lobe-II RMSD to closed (lobe-I fit, Å)", True)):
        mx = max(max(recs[e][kx].max(), recs[e][ky].max()) for e in recs) * 1.04
        fig, axs = grid_axes(len(PANELS))
        for ax, (label, ens, wt) in zip(axs, PANELS):
            md_panel = all(e.startswith("md_") for e in ens)
            if not md_panel:  # MD frames as faint background
                for e, c in (("md_open", C_OPEN), ("md_closed", C_CLOSED)):
                    ax.scatter(recs[e][kx], recs[e][ky], s=5, c=c, alpha=0.25, lw=0, zorder=1)
            for e in ens:
                r = recs[e]
                if e in ("md_open", "md_closed"):
                    c = C_OPEN if e == "md_open" else C_CLOSED
                    ax.scatter(r[kx], r[ky], s=10, c=c, alpha=0.6, lw=0, zorder=2, label=e.replace("md_", "MD "))
                elif wt == "maxent":
                    o = np.argsort(r["w"])
                    w = r["w"][o]
                    sc_w = ax.scatter(r[kx][o], r[ky][o], s=8 + 70 * w / r["w"].max(), c=np.clip(w, 1e-6, None),
                                      cmap="Purples", norm=wnorm, lw=0.3, edgecolors="k", zorder=3)
                else:
                    sc_t = ax.scatter(r[kx], r[ky], s=12, c=r["theta"], cmap="coolwarm", norm=tnorm, lw=0.2,
                                      edgecolors="k", zorder=3)
            ax.plot([0, mx], [0, mx], color="0.5", lw=0.7, ls=":")
            ax.plot(0, dd, marker="*", ms=13, mfc=C_OPEN, mec="k", ls="none", zorder=5, label="open ref")
            ax.plot(dd, 0, marker="P", ms=11, mfc=C_CLOSED, mec="k", ls="none", zorder=5, label="closed ref")
            if thr:
                ax.axvline(THR["open"], color=C_OPEN, ls="--", lw=0.9)
                ax.axhline(THR["closed"], color=C_CLOSED, ls="--", lw=0.9)
            ax.set_xlim(-0.2, mx)
            ax.set_ylim(-0.2, mx)
            ax.set_aspect("equal")
            ax.set_title(label, fontsize=9.5)
            ax.grid(alpha=0.25, lw=0.5)
        for ax in axs[len(PANELS) - 4:len(PANELS)]:
            ax.set_xlabel(xl)
        for ax in axs[::4]:
            ax.set_ylabel(yl)
        axs[2].legend(fontsize=7.5, loc="upper right", framealpha=0.8)
        extra = f"; dashed = hinge thresholds {THR['open']} Å (open) / {THR['closed']} Å (closed)" if thr else ""
        fig.suptitle(f"TeaA Fiedler lobes (corrected amide H), {kind} RMSD landscape (residues 1-309). Uniform panels coloured by blind θ, MaxEnt panels "
                     f"by λ{LAMBDA:g} weight (size ∝ weight); faint dots = MD frames{extra}", fontsize=10)
        fig.tight_layout(rect=(0, 0, 0.92, 0.95))
        if sc_t is not None:
            fig.colorbar(sc_t, cax=fig.add_axes([0.93, 0.55, 0.01, 0.33]), label="blind θ (deg)")
        if sc_w is not None:
            fig.colorbar(sc_w, cax=fig.add_axes([0.93, 0.12, 0.01, 0.33]), label=f"MaxEnt weight λ{LAMBDA:g}")
        save(fig, f"rmsd_{kind}")

    # ---------------- 1D summary
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.8))
    colors = ["0.15", "#7570b3", "#e7298a", "#66a61e", "#e6ab02", "#a6761d"]
    for ax, key, sg, xlab in ((axs[0], "PC1", SIGMA_PC, "PC1 (Å)"), (axs[1], "theta", SIGMA_THETA, "blind θ (deg)")):
        allv = np.concatenate([recs[e][key] for e in recs])
        g = np.linspace(allv.min() - 3 * sg, allv.max() + 3 * sg, 600)
        top = 0.0
        for (label, ens, wt), c in zip(CURVES, colors):
            v, w = panel_data(recs, ens, wt, key)
            yk = kde1d(v, w, g, sg)
            top = max(top, yk.max())
            ax.semilogy(g, yk, color=c, lw=2.2 if label.startswith("MD") else 1.6,
                        ls="--" if wt == "maxent" else "-", label=label)
        rv = {"PC1": (refpc["open"][0], refpc["closed"][0]),
              "theta": (theta(REF["open"]), theta(REF["closed"]))}[key]
        ax.axvline(rv[0], color=C_OPEN, lw=1, ls=":", label="open ref")
        ax.axvline(rv[1], color=C_CLOSED, lw=1, ls=":", label="closed ref")
        ax.set_ylim(top * 1e-4, top * 2)
        ax.set_xlabel(xlab)
        ax.set_ylabel("density (log scale)")
        ax.grid(alpha=0.25, lw=0.5)
    h, l = axs[0].get_legend_handles_labels()
    fig.legend(h, l, fontsize=8.5, loc="lower center", ncol=4, frameon=False)
    fig.suptitle(f"TeaA Fiedler lobes (corrected amide H), 1D densities (Gaussian KDE, σ={SIGMA_PC} Å on PC1, {SIGMA_THETA}° on θ)", fontsize=10.5)
    fig.tight_layout(rect=(0, 0.12, 1, 1))
    save(fig, "summary_1d")

    # ---------------- per-structure CSV
    with open(OUT / "per_structure.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["path", "ensemble", "PC1", "PC2", "rmsd_open", "rmsd_closed", "lobeII_rmsd_open",
                     "lobeII_rmsd_closed", "theta", "weight_l1000", "in_md_open_95", "in_md_closed_95"])
        for e, d in recs.items():
            for i in range(d["n"]):
                wr.writerow([d["paths"][i], e] + [f"{d[k][i]:.4f}" for k in
                            ("PC1", "PC2", "rmsd_open", "rmsd_closed", "lobeII_rmsd_open", "lobeII_rmsd_closed", "theta")]
                            + ["" if np.isnan(d["w"][i]) else f"{d['w'][i]:.6g}", int(d["in95_open"][i]),
                               int(d["in95_closed"][i])])

    # ---------------- summary table
    keys = ("PC1", "PC2", "theta", "rmsd_open", "rmsd_closed", "lobeII_rmsd_open", "lobeII_rmsd_closed",
            "in95_open", "in95_closed")
    rows = []
    for label, ens, wt in PANELS:
        v = {k: panel_data(recs, ens, wt, k)[0].astype(float) for k in keys}
        w = panel_data(recs, ens, wt, "PC1")[1]
        m = {k: float((w * v[k]).sum()) for k in keys}
        sd1 = float(np.sqrt((w * (v["PC1"] - m["PC1"]) ** 2).sum()))
        ho = float((w * (v["lobeII_rmsd_open"] <= THR["open"])).sum())
        hc = float((w * (v["lobeII_rmsd_closed"] <= THR["closed"])).sum())
        rows.append([label, len(w), 1 / np.sum(w ** 2), m["PC1"], sd1, m["PC2"], m["theta"], m["in95_open"],
                     m["in95_closed"], ho, hc, m["rmsd_open"], m["rmsd_closed"], m["lobeII_rmsd_open"],
                     m["lobeII_rmsd_closed"]])
    hdr = ["panel", "n", "n_eff", "PC1_mean", "PC1_sd", "PC2_mean", "theta_mean", "f_in_MDopen95", "f_in_MDclosed95",
           "f_hinge_open", "f_hinge_closed", "rmsd_open", "rmsd_closed", "lobeII_open", "lobeII_closed"]
    with open(OUT / "summary.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(hdr)
        for r in rows:
            wr.writerow([r[0], r[1]] + [f"{x:.4f}" for x in r[2:]])
    print("\n" + " | ".join(hdr))
    for r in rows:
        print(f"{r[0]:38s} | {r[1]:4d} | " + " | ".join(f"{x:7.3f}" for x in r[2:]))
    print(f"\nMD 95% HPD levels (density): open {lvl['open']:.4g}, closed {lvl['closed']:.4g}; "
          f"grid {NGRID}x{NGRID}, PC1 [{lo[0]:.1f},{hi[0]:.1f}] PC2 [{lo[1]:.1f},{hi[1]:.1f}]")
    print(f"ref PCs: open {refpc['open'].round(2)}, closed {refpc['closed'].round(2)}; ref theta open "
          f"{theta(REF['open']):.2f} closed {theta(REF['closed']):.2f}")


if __name__ == "__main__":
    main()
