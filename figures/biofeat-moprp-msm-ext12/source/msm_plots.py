"""Summary figures for a set of msm_build.py runs.

  <prefix>_dG_compare.png  ΔG vs F (Bayesian median, 95 % interval) of every PUF macrostate in every model, pH 4 and
                           pH 7 side by side, with the pH 4 HDX ΔG_op (Moulick et al. 2015) as stars
  <prefix>_ck.png          Chapman-Kolmogorov test of one model: probability of staying in each macrostate after
                           k lags, predicted from the lag-τ model (T^k) vs estimated with a model at lag kτ
  <prefix>_mfpt.png        MFPTs F -> X and X -> F of that model, both pH (log scale)

Usage: python msm_plots.py <out_prefix> <ck_model_dir> <model_dir> [<model_dir> ...]
       env MSM_PLOTS_DATA: the seeded data set named in the ΔG title (default: the ext6 set)
"""
import json
import os
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

prefix, ck_dir, *dirs = sys.argv[1:]
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
PH_COL = {"ph4": "#2166ac", "ph7": "#b2182b"}
MAC_COL = {"F": "#52514e", "PUF1": "#e87ba4", "PUF2": "#eb6834", "PUF3": "#1baf7a", "PUF3L": "#4a3aa7", "I": "#b8b8b8"}
LABEL = {"F": "Folded", "PUF1": "PUF1", "PUF2": "PUF2", "PUF3": "PUF3", "PUF3L": "PUF3-like", "I": "intermediate"}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})


def name(d):
    r = json.load(open(Path(d) / "msm_report.json"))
    t = r.get("tica") or {}
    feat = "Cartesian 10 PCs" if "cartpca10" in d else ("distance 10 PCs" if "distpca10" in d else "features")
    emb = "direct k-means" if t.get("embed") == "none" else f"TICA {t.get('dim')}"
    tag = re.match(r"(ext\d+)_", Path(d).name)
    return (f"{tag.group(1)}: " if tag else "") + f"{feat}, {emb}, K={r['K']}, lag {r['lag_ns']:g} ns"


reports = {d: json.load(open(Path(d) / "msm_report.json")) for d in dirs}
HDX = next(iter(reports.values()))["hdx_dG_pH4"]

# ---------- ΔG comparison ----------
macros = ["PUF1", "PUF2", "PUF3", "PUF3L"]
fig, axes = plt.subplots(1, len(macros), figsize=(4.4 * len(macros), 0.55 * len(dirs) + 2.2), sharey=True)
ys = np.arange(len(dirs))[::-1]
for ax, m in zip(axes, macros):
    for k, d in enumerate(dirs):
        for off, ph in ((0.13, "ph4"), (-0.13, "ph7")):
            c = reports[d]["ph"][ph]["dG_ci95"].get(m)
            if c:
                ax.errorbar(c[1], ys[k] + off, xerr=[[c[1] - c[0]], [c[2] - c[1]]], fmt="o", ms=4.5, capsize=2,
                            color=PH_COL[ph], label=f"run at pH {ph[2]}" if k == 0 else None)
    if m in HDX:
        ax.axvline(HDX[m], color="#d6604d", ls="--", lw=1.2, label="HDX ΔG_op, pH 4")
    ax.axvline(0, color=INK2, lw=0.6)
    ax.set_title(f"{LABEL[m]} vs Folded", loc="left", fontsize=10, color=INK)
    ax.set_xlabel("ΔG (kcal/mol)")
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
axes[0].set_yticks(ys); axes[0].set_yticklabels([name(d) for d in dirs], fontsize=8)
handles, labels = [], []
for ax in axes:
    for h, l in zip(*ax.get_legend_handles_labels()):
        if l not in labels:
            handles.append(h); labels.append(l)
axes[-1].legend(handles, labels, frameon=False, fontsize=8, loc="lower right")
DATA = os.environ.get("MSM_PLOTS_DATA", "6 × 100 ns + 6 × 20 ns seeds per basin and pH")
fig.suptitle("MSM free energies of the PUF macrostates relative to Folded (Bayesian median and 95 % interval)\n"
             f"{DATA}; plus the unbiased MD", x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(f"{prefix}_dG_compare.png", dpi=130)
plt.close(fig)

# ---------- CK test ----------
r = json.load(open(Path(ck_dir) / "msm_report.json"))
lag = r["lag_ns"]
macs = [m for m in ["F", "PUF1", "PUF2", "PUF3", "PUF3L", "I"] if m in r["ph"]["ph4"]["ck_test"]]
fig, axes = plt.subplots(2, len(macs), figsize=(3.0 * len(macs), 6.2), sharex=True, sharey=True)
for row, ph in enumerate(("ph4", "ph7")):
    for col, m in enumerate(macs):
        ax = axes[row, col]
        ck = r["ph"][ph]["ck_test"].get(m)
        if ck:
            k = np.arange(1, len(ck["predicted"]) + 1) * lag
            est = [np.nan if v is None else v for v in ck["estimated"]]
            ax.plot(k, ck["predicted"], "--", color=INK2, lw=1.4, label=f"predicted (lag {lag:g} ns model)")
            ax.plot(k, est, "o-", color=MAC_COL[m], lw=1.6, ms=4, label="estimated (lag k·τ models)")
        ax.set_ylim(0, 1.02)
        ax.grid(color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.set_title(f"pH {ph[2]}: {LABEL[m]}", loc="left", fontsize=9.5, color=INK)
        if row == 1:
            ax.set_xlabel("time (ns)")
        if col == 0:
            ax.set_ylabel("P(still in macrostate)")
axes[0, 0].legend(frameon=False, fontsize=7.5, loc="lower left")
fig.suptitle(f"Chapman–Kolmogorov test: {name(ck_dir)} (agreement = Markovian at the macrostate level)",
             x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(f"{prefix}_ck.png", dpi=130)
plt.close(fig)

# ---------- MFPTs ----------
fig, ax = plt.subplots(figsize=(9.5, 4.6))
xs = np.arange(4)
for j, ph in enumerate(("ph4", "ph7")):
    mf = r["ph"][ph]["mfpt_ns"]
    opn = [mf.get(f"F->{m}") or np.nan for m in macros]
    cls = [mf.get(f"{m}->F") or np.nan for m in macros]
    ax.bar(xs + (j - 0.5) * 0.38, opn, width=0.17, color=PH_COL[ph], label=f"F → X, pH {ph[2]}")
    ax.bar(xs + (j - 0.5) * 0.38 + 0.18, cls, width=0.17, color=PH_COL[ph], alpha=0.45, label=f"X → F, pH {ph[2]}")
ax.set_yscale("log")
ax.set_xticks(xs + 0.09); ax.set_xticklabels([LABEL[m] for m in macros])
ax.set_ylabel("mean first-passage time (ns)")
ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=8, ncol=2)
ax.set_title(f"Opening (F → X) and closing (X → F) MFPTs: {name(ck_dir)}", loc="left", fontsize=10, color=INK)
fig.tight_layout()
fig.savefig(f"{prefix}_mfpt.png", dpi=130)
plt.close(fig)
print("wrote", f"{prefix}_dG_compare.png", f"{prefix}_ck.png", f"{prefix}_mfpt.png")
