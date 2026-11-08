"""Combine the basin renders with their location in the Cartesian PCA.

Usage: python compose.py <frames_dir> <renders_dir> <pca_scores.npz> <rmsd_min> <rmsd_max> <out.png>
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap, Normalize

frames_dir, renders_dir, scores_path = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
lo, hi, out = float(sys.argv[4]), float(sys.argv[5]), sys.argv[6]
TITLE = sys.argv[7] if len(sys.argv) > 7 else "MoPrP Cartesian-PCA basins (mi-v2): representative frames"
ALL_LABEL = sys.argv[8] if len(sys.argv) > 8 else ("all 101" if len(sys.argv) > 7 else "all")

SURF, INK, INK2 = "#fcfcfb", "#0b0b0b", "#52514e"
# PyMOL's paleyellow -> orange -> pink -> red -> black, as used in the render
pymol_rgb = [(1.0, 1.0, 0.5), (1.0, 0.5, 0.0), (1.0, 0.65, 0.85), (1.0, 0.0, 0.0), (0.0, 0.0, 0.0)]
cmap = LinearSegmentedColormap.from_list("pymol_spectrum", pymol_rgb)

basins = json.loads((frames_dir / "basins.json").read_text())
S = np.load(scores_path)
by_ph = {}
for b in basins:
    by_ph.setdefault(b["ph"], []).append(b)

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.labelcolor": INK2})
ncol = 1 + max(len(v) for v in by_ph.values())
fig = plt.figure(figsize=(4.2 * ncol, 4.9 * len(by_ph) + 0.8), facecolor=SURF)
gs = fig.add_gridspec(len(by_ph), ncol, width_ratios=[1.15] + [1] * (ncol - 1), wspace=0.06, hspace=0.32)

edges = np.linspace(-120, 150, 70)

# one crop box for every render (union of non-white pixels) so all panels keep the same scale
def _ink(path):
    im = plt.imread(path)[..., :3]
    rows, cols = np.nonzero((im < 0.97).any(axis=2))
    return rows.min(), rows.max(), cols.min(), cols.max()
boxes = np.array([_ink(renders_dir / b["file"].replace(".pdb", ".png")) for b in basins])
PAD = 20
CROP = (max(boxes[:, 0].min() - PAD, 0), boxes[:, 1].max() + PAD, max(boxes[:, 2].min() - PAD, 0), boxes[:, 3].max() + PAD)
for row, (ph, items) in enumerate(by_ph.items()):
    tag = ph.replace(" ", "").lower()
    ax = fig.add_subplot(gs[row, 0])
    ax.set_facecolor(SURF)
    pooled = np.concatenate([S[f"{tag}_mi"], S[f"{tag}_mmpb"]])
    H, _, _ = np.histogram2d(pooled[:, 0], pooled[:, 1], bins=(edges, edges))
    ax.pcolormesh(edges, edges, np.ma.masked_invalid(np.log10(np.where(H > 0, H, np.nan))).T,
                  cmap="Greys", vmin=-0.5, vmax=4.2)
    ref = S[f"{tag}_reference"]
    ax.scatter(ref[:, 0], ref[:, 1], s=6, c=INK, zorder=3, label="2L39 models")
    ax.scatter(*S[f"{tag}_af3"], marker="*", s=140, c="#e34948", edgecolors="white", zorder=4, label="AF3 start")
    for k, b in enumerate(items, 1):
        cx, cy = b["centre"]
        ax.add_patch(plt.Circle((cx, cy), b["radius"], fill=False, lw=1.6, ec="#2a78d6", zorder=5))
        # MI-native sits on top of MI+PB-native at pH 7: put that label below-left
        dx, dy = (-1.6, -1.6) if b["condition"] == "mi" and b["basin"] == "native" else (0.8, 0.8)
        ax.text(cx + b["radius"] * dx, cy + b["radius"] * dy, str(k), color="#2a78d6", fontsize=11,
                fontweight="bold", zorder=6, ha="center", va="center")
    lo_xy, hi_xy = np.percentile(pooled, 0.05, axis=0) - 10, np.percentile(pooled, 99.95, axis=0) + 10
    ax.set_xlim(lo_xy[0], hi_xy[0]); ax.set_ylim(lo_xy[1], hi_xy[1]); ax.set_aspect("equal")
    ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    ax.set_title(f"{ph}: MI + MI+PB frames (raw counts)", loc="left", fontsize=10, color=INK)
    if row == 0:
        ax.legend(loc="lower right", fontsize=7.5, frameon=False)

    for k, b in enumerate(items, 1):
        ax = fig.add_subplot(gs[row, k])
        img = plt.imread(renders_dir / b["file"].replace(".pdb", ".png"))
        ax.imshow(img[CROP[0]:CROP[1], CROP[2]:CROP[3]])
        ax.set_xticks([]); ax.set_yticks([])
        for s in ax.spines.values():
            s.set_visible(False)
        src = "MI+PB" if b["condition"] == "mmpb" else "MI"
        ax.set_title(f"{k}  {b['basin']}  ({src})", loc="left", fontsize=10.5, color=INK, fontweight="bold")
        rms_all = np.mean([f.get("ca_rmsd_all", f.get("ca_rmsd_101")) for f in b["frames"]])
        rms_core = np.mean([f["ca_rmsd_core"] for f in b["frames"]])
        reps = ", ".join(f"w{i+1} {n / b['frames_in_basin']:.0%}" for i, n in enumerate(b["by_replica"]) if n)
        wf = "\nmi.weight share: n/a (MI run)" if b["weight_fraction"] is None else \
            f"\nmi.weight share: {b['weight_fraction']:.1%}"
        ax.text(0.0, -0.02,
                f"{b['frames_in_basin']:,} frames in circle; {len(b['frames'])} shown\n"
                f"walkers: {reps}{wf}\n"
                f"Cα RMSD to minimised: {rms_all:.1f} Å {ALL_LABEL}, {rms_core:.1f} Å core",
                transform=ax.transAxes, va="top", fontsize=8, color=INK2)

cax = fig.add_axes([0.40, 0.035, 0.3, 0.012])
cb = fig.colorbar(plt.cm.ScalarMappable(norm=Normalize(lo, hi), cmap=cmap), cax=cax, orientation="horizontal")
cb.set_label("per-residue backbone RMSD from minimised AF3 start (Å); putty width scales with it; "
             "grey tube = minimised structure", fontsize=8.5, color=INK2)
fig.suptitle(TITLE, x=0.06, ha="left",
             fontsize=13, color=INK, y=0.995)
fig.savefig(out, dpi=130, bbox_inches="tight", facecolor=SURF)
print("wrote", out)
