"""msm_build.py's summary figure (ΔG vs F per macrostate), redrawn from a stored msm_report.json, because msm_build.py draws
the Bayesian intervals from unseeded samples and a rebuild would change them. Plot code copied from msm_build.py.

Usage: msm_summary_replot.py <msm_report.json> <out.png>"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

report = json.load(open(sys.argv[1])); MACROS = ["F", "PUF1", "PUF2", "PUF3", "PUF3L", "I"]; HDX_DG = {"PUF1": 2.2, "PUF2": 3.1}
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
fig.tight_layout(); fig.savefig(sys.argv[2], dpi=130); plt.close(fig)
