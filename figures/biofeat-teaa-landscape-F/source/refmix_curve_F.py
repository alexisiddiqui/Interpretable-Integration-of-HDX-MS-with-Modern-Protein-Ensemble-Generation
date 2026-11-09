"""Fit to the TeaA target for mixtures of the in-state open and closed pools, against open fraction.

Reads the two-pool grid and the MaxEnt floors (lambda 1000) from the Fiedler scoring logs on Isambard and writes
fiedler/landscapes_F/refmix_curve.{png,pdf}. The pools are 20 open and 20 closed Boltz structures (TeaA_inState),
scored with the guidance forward model (uniform inside each pool).
"""
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

H = Path.home()
LOG = H / "_logs"
OUT = H / "_runtime/analysis/fiedler/landscapes_F"

bins = (LOG / "F_bins_8050284.out").read_text()
grid_line = next(l for l in bins.splitlines() if l.strip().startswith("grid:"))
pts = [(float(a), float(b)) for a, b in re.findall(r"([0-9.]+):([0-9.]+)", grid_line)]
simplex = re.search(r"simplex fit: f in_open ([0-9.]+), in_closed [0-9.]+, MSE ([0-9.]+)", bins)
f_best, mse_best = float(simplex.group(1)), float(simplex.group(2))


def floor(job):
    txt = (LOG / job).read_text()
    return float(re.search(r"lambda 1000: floor ([0-9.]+)", txt).group(1))


fl = {"refined, MaxEnt": floor("F_blind_8050281.out"),
      "metadiffusion union, MaxEnt": floor("F_metad_8049979.out"),
      "control, MaxEnt": floor("F_ctl_8050283.out")}

ink, muted, accent = "#222222", "#6b6b6b", "#1f78b4"
fig, ax = plt.subplots(figsize=(5.2, 3.4))
x, y = zip(*pts)
ax.plot(x, y, color=accent, lw=2, marker="o", ms=4, zorder=3, label="open + closed in-state pools")
mse40 = dict(pts)[0.40]
ax.axvline(0.40, color=muted, lw=1, ls=":", zorder=1)
ax.annotate(f"target 0.40\nMSE {mse40:.5f}", (0.40, mse40), xytext=(0.13, 0.0090), color=ink, fontsize=8,
            arrowprops=dict(arrowstyle="-", color=muted, lw=0.8))
ax.annotate(f"best fit {f_best:.3f}\nMSE {mse_best:.5f}", (f_best, mse_best), xytext=(0.60, 0.0040), color=ink,
            fontsize=8, arrowprops=dict(arrowstyle="-", color=muted, lw=0.8))
for (lab, v), ls, va in zip(fl.items(), ["--", "-.", ":"], ["center", "top", "bottom"]):
    ax.axhline(v, color=ink if lab.startswith("refined") else muted, lw=1, ls=ls, zorder=2)
    ax.text(1.0, v, f" {lab} {v:.4f}", va=va, ha="left", fontsize=7.5, color=ink)
ax.set_xlim(0, 1)
ax.set_ylim(0, 0.0125)
ax.set_xlabel("open fraction of the mixture")
ax.set_ylabel("uptake MSE against target")
ax.grid(alpha=0.25, lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
ax.legend(fontsize=7.5, loc="upper center", frameon=False)
ax.set_title("TeaA, in-state pool mixtures against the HDX target (Fiedler run floors, λ 1000)", fontsize=8.5)
OUT.mkdir(parents=True, exist_ok=True)
for ext in ("png", "pdf"):
    fig.savefig(OUT / f"refmix_curve.{ext}", dpi=200, bbox_inches="tight")
print("grid", pts)
print("best", f_best, mse_best, "floors", fl)
print("wrote", OUT / "refmix_curve.png")
