"""Figures for the segment-opening MaxCal (msm_build.py with MSM_OPEN_OBS).

  <prefix>_dGop.png   HDX-style opening free energies per segment (median, 95 % interval over Bayesian samples):
                      MSM alone, MaxCal fitted to HDX ± error, MaxCal fitted to the HDX/MSM combination; pH 4 and pH 7
                      (pH 7 = the pH 4 correction carried over); one row per model directory, HDX values as lines
  <prefix>_states.png the same for the PCA macrostates (ΔG vs F) and the opening / closing MFPTs, for one model

Usage: python segment_maxcal_plots.py <out_prefix> <state_model_dir> <model_dir> [<model_dir> ...]
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

prefix, state_dir, *dirs = sys.argv[1:]
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
VAR = {"prior": ("MSM only", "#8a8985"), "hdx": ("MaxCal → HDX ± error", "#d6604d"),
       "combined": ("MaxCal → HDX/MSM combined", "#2166ac")}
SEG = {"b1_rest": "β1 (127–132) opening\n[HDX PUF1 2.2 ± 0.2, constrained]",
       "b2_seg": "β2 region (154–167) opening\n[HDX PUF2 3.1 ± 0.5, prediction]",
       "loop_a3": "β1–α1 loop ↔ α3 opening\n[part of HDX PUF1, prediction]",
       "a1b2_core": "α1 + β2 off the α2–α3 core\n[HDX PUF2 picture, prediction]"}
HDX_LINE = {"b1_rest": (2.2, 0.2), "b2_seg": (3.1, 0.5), "loop_a3": (2.2, 0.2), "a1b2_core": (3.1, 0.5)}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})


def name(d):
    r = json.load(open(Path(d) / "msm_report.json"))
    q = r["ph"]["ph4"]["segment_maxcal"]["open_q"]
    return f"K={r['K']}, lag {r['lag_ns']:g} ns, open if Q < {q:g}"


def series(seg, ph, variant):
    """{column: [lo, med, hi]} of dG_op for one variant at one pH."""
    if variant == "prior":
        return seg["prior_dG_op"]
    key = variant if ph == "ph4" else f"transfer_{variant}"
    d = seg.get(key, {}).get("dG", {})
    return {k.split(":", 1)[1]: v for k, v in d.items() if k.startswith("open:")}


reports = {d: json.load(open(Path(d) / "msm_report.json")) for d in dirs}
cols = [c for c in SEG if c in reports[dirs[0]]["ph"]["ph4"]["segment_maxcal"]["prior_dG_op"]]
fig, axes = plt.subplots(2, len(cols), figsize=(4.6 * len(cols), 1.0 * len(dirs) + 5.2), sharey=True)
ys = np.arange(len(dirs))[::-1]
for row, ph in enumerate(("ph4", "ph7")):
    for ax, c in zip(axes[row], cols):
        for k, d in enumerate(dirs):
            seg = reports[d]["ph"][ph]["segment_maxcal"]
            for off, v in zip((0.22, 0.0, -0.22), VAR):
                ci = series(seg, ph, v).get(c)
                if ci is None or not np.all(np.isfinite(ci)):
                    continue
                ax.errorbar(ci[1], ys[k] + off, xerr=[[ci[1] - ci[0]], [ci[2] - ci[1]]], fmt="o", ms=4, capsize=2,
                            color=VAR[v][1], label=VAR[v][0] if k == 0 else None)
        if not ax.lines:
            ax.text(0.5, 0.5, "never open in any frame\n(not sampled: no ΔG_op)", transform=ax.transAxes, ha="center",
                    va="center", fontsize=9, color=INK2)
            ax.set_xticks([])
        if ph == "ph4":
            t, e = HDX_LINE[c]
            ax.axvspan(t - e, t + e, color="#d6604d", alpha=0.12, lw=0)
            ax.axvline(t, color="#d6604d", ls="--", lw=1.1)
        ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
        ax.set_title(("pH 4: " if ph == "ph4" else "pH 7 (pH 4 correction carried over): ") + SEG[c], loc="left",
                     fontsize=8.5, color=INK)
        ax.set_xlabel("ΔG_op = −kT ln(P_open / P_closed)  (kcal/mol)")
    axes[row, 0].set_yticks(ys); axes[row, 0].set_yticklabels([name(d) for d in dirs], fontsize=8)
axes[0, 0].legend(frameon=False, fontsize=7.5, loc="upper left")
fig.suptitle("Segment-opening MaxCal (direct Cartesian 10-PC MSMs, ext12): opening free energies of the HDX segments "
             "(median and 95 % interval over Bayesian MSM samples; red band = HDX value ± error, Moulick et al. 2015)",
             x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(f"{prefix}_dGop.png", dpi=130)
plt.close(fig)

# ---------- macrostates and MFPTs for one model ----------
r = json.load(open(Path(state_dir) / "msm_report.json"))
MAC = ["PUF1", "PUF2", "PUF3", "PUF3L"]
LAB = {"PUF1": "'PUF1' (α2–α3 loop)", "PUF2": "'PUF2' (β1 off)", "PUF3": "'PUF3' (β1 off, far)",
       "PUF3L": "'PUF3-like' (β1 off)"}
fig, axes = plt.subplots(1, 3, figsize=(17, 4.8))
for j, ph in enumerate(("ph4", "ph7")):
    ax = axes[j]
    seg = r["ph"][ph]["segment_maxcal"]
    for off, v in zip((0.22, 0.0, -0.22), VAR):
        if v == "prior":
            d = r["ph"][ph]["dG_ci95"] if ph == "ph4" else seg["prior"]["dG"]
        else:
            d = seg[v if ph == "ph4" else f"transfer_{v}"]["dG"]
        for i, m in enumerate(MAC):
            ci = d.get(m)
            if ci is not None and np.all(np.isfinite(ci)):
                ax.errorbar(ci[1], len(MAC) - 1 - i + off, xerr=[[ci[1] - ci[0]], [ci[2] - ci[1]]], fmt="o", ms=4,
                            capsize=2, color=VAR[v][1], label=VAR[v][0] if i == 0 else None)
    ax.set_yticks(range(len(MAC))); ax.set_yticklabels([LAB[m] for m in MAC][::-1])
    ax.grid(axis="x", color=GRID, lw=0.6); ax.set_axisbelow(True)
    ax.set_xlabel("ΔG vs Folded (kcal/mol)")
    ax.set_title(f"pH {ph[2]}: PCA macrostates" + (" (pH 4 correction carried over)" if ph == "ph7" else ""),
                 loc="left", fontsize=9.5, color=INK)
axes[0].legend(frameon=False, fontsize=7.5, loc="lower right")
ax = axes[2]
pairs = [f"F->{m}" for m in MAC] + [f"{m}->F" for m in MAC]
xs = np.arange(len(pairs))
for j, (ph, v, col, off) in enumerate([("ph4", "hdx", "#2166ac", -0.2), ("ph7", "transfer_hdx", "#b2182b", 0.2)]):
    d = r["ph"][ph]["segment_maxcal"][v]["mfpt_ns"]
    med = [d[p][1] if d.get(p) else np.nan for p in pairs]
    lo = [d[p][1] - d[p][0] if d.get(p) else 0 for p in pairs]
    hi = [d[p][2] - d[p][1] if d.get(p) else 0 for p in pairs]
    ax.errorbar(xs + off, med, yerr=[lo, hi], fmt="o", ms=4, capsize=2, color=col,
                label=f"pH {ph[2]}, MaxCal → HDX" + (" (carried over)" if ph == "ph7" else ""))
ax.set_yscale("log"); ax.set_xticks(xs); ax.set_xticklabels([p.replace("->", "→") for p in pairs], rotation=40, ha="right")
ax.set_ylabel("MFPT (ns)"); ax.grid(axis="y", color=GRID, lw=0.6); ax.set_axisbelow(True)
ax.legend(frameon=False, fontsize=7.5)
ax.set_title("opening / closing MFPTs after MaxCal", loc="left", fontsize=9.5, color=INK)
fig.suptitle(f"Segment-opening MaxCal, {name(state_dir)}: PCA macrostate free energies and kinetics",
             x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(f"{prefix}_states.png", dpi=130)
plt.close(fig)
print("wrote", f"{prefix}_dGop.png", f"{prefix}_states.png")
