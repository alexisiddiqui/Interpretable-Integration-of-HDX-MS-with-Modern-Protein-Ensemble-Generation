"""Free-energy heatmaps of an MSM before and after the segment-opening MaxCal (msm_build.py msm_weights.npz).

One figure per plane (PCA101 PC1-PC2; dRMSD - beta1 dihedral deviation), rows = run at pH 4 / pH 7, columns:
  MSM alone          -kT ln p, p = density of the ML MSM's stationary distribution (0 at the minimum)
  after MaxCal       the same for the tilted model (pH 4: beta1 opening matched to HDX PUF1 2.2 kcal/mol;
                     pH 7: the pH 4 multipliers carried over)
  change             -kT ln(p_MaxCal / p_MSM) per bin: red = population removed, blue = gained
  beta1 open         fraction of frames whose microstate has beta1 open (the observable MaxCal acts on)
PCA panels carry the macrostate circles with their structural meaning (macro_structure.py).

Usage: python fes_maxcal_plots.py <model_dir> <basins_seed.json> <out_prefix>
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

model, basins_path, prefix = sys.argv[1:4]
W = np.load(Path(model) / "msm_weights.npz")
rep = json.load(open(Path(model) / "msm_report.json"))
KT = rep["kT_kcal"]
cols = [str(c) for c in W["open_cols"]]
jb1 = cols.index("b1_rest")
q = rep["ph"]["ph4"]["segment_maxcal"]["open_q"]
TG = rep["ph"]["ph4"]["segment_maxcal"]["targets"]
SEGNAME = {"b1_rest": "β1", "b2_seg": "β2 region", "loop_a3": "loop–α3", "a1b2_core": "α1+β2 off core"}
TGT = ", ".join(f"{SEGNAME.get(c, c)} {t['dG']:g}" for c, t in TG.items())
basins = json.load(open(basins_path))
NAME = {"Folded": "Folded", "PUF1": "'PUF1'\nα2–α3 loop", "PUF2": "'PUF2'\nβ1 off", "PUF3": "'PUF3'\nβ1 off",
        "PUF3-like": "'PUF3-like'\nβ1 off"}
INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "figure.facecolor": SURF, "axes.facecolor": SURF})
PLANES = {"pca": dict(c=(0, 1), rng=[[-50, 140], [-100, 70]], xl="PC1", yl="PC2", log=False),
          "dih": dict(c=(2, 3), rng=[[np.log10(0.42), np.log10(1.6)], [np.log10(7), np.log10(120)]],
                      xl="dRMSD vs 2L39 (rad)", yl="β1 dihedral deviation (°)", log=True)}
BINS = 60


def hist(x, w, P):
    H, xe, ye = np.histogram2d(x[:, P["c"][0]], x[:, P["c"][1]], bins=BINS, range=P["rng"], weights=w)
    return H, xe, ye


def free(H):
    with np.errstate(divide="ignore"):
        G = -KT * np.log(H / H.sum())
    G[~np.isfinite(G)] = np.nan
    return G - np.nanmin(G)


def decorate(ax, P, plane):
    if plane == "pca":
        for b in basins:
            if b["label"] == "Folded" and b["ph"] == "pH 7":
                continue
            ax.add_patch(plt.Circle(b["centre"], 15, fill=False, ec="w", ls="--", lw=1.1))
            ax.text(b["centre"][0], b["centre"][1] + 17, NAME[b["label"]], color="w", fontsize=7, ha="center",
                    va="bottom", fontweight="bold")
    if P["log"]:
        xt, yt = [0.5, 0.6, 0.8, 1.0, 1.5], [10, 15, 20, 30, 40, 60, 100]
        ax.set_xticks(np.log10(xt)); ax.set_xticklabels([f"{v:g}" for v in xt])
        ax.set_yticks(np.log10(yt)); ax.set_yticklabels([f"{v:g}" for v in yt])
    ax.set_xlabel(P["xl"]); ax.set_ylabel(P["yl"])


for plane, P in PLANES.items():
    fig, axes = plt.subplots(2, 4, figsize=(21, 9.6))
    for row, ph in enumerate(("ph4", "ph7")):
        x = W[f"{ph}_x"].astype(float)
        Hp, xe, ye = hist(x, W[f"{ph}_w_prior"], P)
        Hm, _, _ = hist(x, W[f"{ph}_w_maxcal"], P)
        open_frame = W[f"{ph}_open_frac_micro"][W[f"{ph}_micro"].astype(int), jb1]
        Hn, _, _ = hist(x, None, P)
        Ho, _, _ = hist(x, open_frame, P)
        with np.errstate(divide="ignore", invalid="ignore"):
            pp, pm = Hp / Hp.sum(), Hm / Hm.sum()
            D = -KT * np.log(pm / pp)
            D[~np.isfinite(D)] = np.nan
            O = np.where(Hn > 0, Ho / Hn, np.nan)
        def dgop(w):                                          # ML beta1 opening free energy of the weighted frames
            po = np.sum(w * open_frame) / np.sum(w)
            return -KT * np.log(po / (1 - po))
        pre, post = dgop(W[f"{ph}_w_prior"]), dgop(W[f"{ph}_w_maxcal"])
        panels = [(free(Hp), "viridis", 0, 6, "free energy (kcal/mol)",
                   f"MSM alone: β1 opening ΔG_op {pre:.2f} kcal/mol"),
                  (free(Hm), "viridis", 0, 6, "free energy (kcal/mol)",
                   (f"after MaxCal (HDX: {TGT})" if ph == "ph4" else "pH 4 correction carried over")
                   + f": β1 ΔG_op {post:.2f}"),
                  (D, "RdBu_r", -3, 3, "−kT ln(p_MaxCal / p_MSM)  (kcal/mol)", "change: red = population removed, "
                   "blue = gained"),
                  (O, "magma", 0, 1, f"fraction of frames with β1 open (Q < {q:g})", "where β1 is open")]
        for col, (Z, cmap, lo, hi, cl, title) in enumerate(panels):
            ax = axes[row, col]
            im = ax.pcolormesh(xe, ye, np.ma.masked_invalid(Z).T, cmap=cmap, vmin=lo, vmax=hi, shading="flat")
            fig.colorbar(im, ax=ax, label=cl, shrink=0.85)
            decorate(ax, P, plane)
            ax.set_title(f"pH {ph[2]}: {title}", loc="left", fontsize=9, color=INK)
    lag = rep["lag_ns"]
    fig.suptitle(f"MSM free energy before and after MaxCal ({'PCA101 plane' if plane == 'pca' else 'dihedral plane'}; "
                 f"direct Cartesian 10-PC MSM, K={rep['K']}, lag {lag:g} ns, ext12; maximum-likelihood models)",
                 x=0.01, ha="left", fontsize=11.5, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(f"{prefix}_{plane}.png", dpi=125)
    plt.close(fig)
    print("wrote", f"{prefix}_{plane}.png")
