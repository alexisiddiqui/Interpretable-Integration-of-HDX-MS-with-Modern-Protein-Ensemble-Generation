"""Paper-derived PUF variables on the PCA101 and dihedral planes. Bin colour = plain frame mean (or rule fraction) of the
frames in the bin, conditional on position; grey contours = MSM stationary free energy (1, 2, 3 kcal/mol, no MaxCal).
Usage: puf_plots.py <puf_cvs_tight.npz> <puf_final.json> <basins_seed.json> <out_prefix>"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap
from scipy.ndimage import gaussian_filter
from scipy.stats import binned_statistic_2d
Z = np.load(sys.argv[1]); TH = json.load(open(sys.argv[2]))["thresholds_nm"]; BAS = json.load(open(sys.argv[3])); prefix = sys.argv[4]
rn = [str(s) for s in Z["rig_names"]]; names = [str(s) for s in Z["set_names"]]
KT = 0.0019872043 * 298.15
INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "figure.facecolor": SURF, "axes.facecolor": "#f1f0ec",
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.labelcolor": INK2})
FOLD = {"ph4": (7.5, -27.5), "ph7": (12.5, -17.5)}
D = {}
for ph in ("ph4", "ph7"):
    d = dict(r={n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}, q={n: Z[f"{ph}_q"][:, i] for i, n in enumerate(names)}, x=Z[f"{ph}_x"], w=Z[f"{ph}_wp"])
    d["F"] = np.linalg.norm(d["x"][:, :2] - np.array(FOLD[ph]), axis=1) < 10
    D[ph] = d
PLANES = {"pca": (0, 1, np.arange(-30, 125, 5.0), np.arange(-100, 70, 5.0)),
          "dih": (2, 3, np.arange(-0.36, 0.04, 0.0125), np.arange(0.74, 2.08, 0.04))}
COLS = [("pca", "ph4"), ("pca", "ph7"), ("dih", "ph4"), ("dih", "ph7")]
qrel = lambda c: (lambda d: d["q"][c] / d["q"][c][d["F"]].mean())
rig = lambda c: (lambda d: d["r"][c])
qcm = ListedColormap(plt.get_cmap("Blues_r")(np.linspace(0.0, 0.9, 6))); qn = BoundaryNorm([0, .2, .4, .6, .8, .9, 1.05], 6)
dcm = ListedColormap(plt.get_cmap("Oranges")(np.linspace(0.15, 1.0, 6))); dn = BoundaryNorm([0, .3, .45, .6, .8, 1.0, 1.4], 6)
fcm = ListedColormap(plt.get_cmap("Purples")(np.linspace(0.15, 1.0, 6))); fn = BoundaryNorm([0, .02, .1, .25, .5, .75, 1.0], 6)


def panel(ax, plane, ph, val, cm, nm, minf=10):
    d = D[ph]; i, j, xe, ye = PLANES[plane]; x, y = d["x"][:, i], d["x"][:, j]
    n = np.histogram2d(x, y, bins=[xe, ye])[0]
    s = binned_statistic_2d(x, y, val, "mean", bins=[xe, ye]).statistic
    s[n < minf] = np.nan
    im = ax.pcolormesh(xe, ye, s.T, cmap=cm, norm=nm, rasterized=True)
    H = np.histogram2d(x, y, bins=[xe, ye], weights=d["w"])[0]
    G = -KT * np.log(np.maximum(gaussian_filter(H, 0.7), 1e-12) / gaussian_filter(H, 0.7).max())
    ax.contour(0.5 * (xe[1:] + xe[:-1]), 0.5 * (ye[1:] + ye[:-1]), G.T, levels=[1, 2, 3], colors=INK, linewidths=[.8, .55, .35], alpha=.7)
    if plane == "pca":
        for b in BAS:
            c = b["centre"]; ax.add_patch(plt.Circle(c, 10, fill=False, ec=INK, lw=.7, ls=(0, (3, 2))))
        ax.plot([87.5], [17.5], marker="+", ms=7, mew=1.2, color="#c0143c")
        ax.set_aspect("equal"); ax.set_xlim(-30, 120); ax.set_ylim(-100, 65)
    else:
        ax.set_xticks(np.log10([.5, .7, 1.0])); ax.set_xticklabels([".5", ".7", "1"])
        ax.set_yticks(np.log10([10, 30, 100])); ax.set_yticklabels(["10", "30", "100"]); ax.set_xlim(-.36, .03); ax.set_ylim(.74, 2.08)
    return im


def sheet(rows, title, out, h=2.35):
    fig, axes = plt.subplots(len(rows), 4, figsize=(11.4, h * len(rows) + .9), constrained_layout=True, squeeze=False)
    for r, (lab, f, cm, nm, unit) in enumerate(rows):
        for c, (plane, ph) in enumerate(COLS):
            ax = axes[r, c]; im = panel(ax, plane, ph, f(D[ph]), cm, nm)
            if r == 0:
                ax.set_title(("PCA101 plane" if plane == "pca" else "Dihedral plane") + f", run at pH {ph[2]}", loc="left", fontsize=8.5, color=INK, fontweight="bold")
            if r == len(rows) - 1:
                ax.set_xlabel("PC1" if plane == "pca" else "dRMSD (rad, log)")
            if c == 0:
                ax.set_ylabel("PC2")
            if c == 2:
                ax.set_ylabel("β1 dihedral dev. (°, log)")
        cb = fig.colorbar(im, ax=axes[r, :], shrink=.86, pad=.012, aspect=16); cb.set_label(f"{lab}\n{unit}", fontsize=7.5, color=INK); cb.ax.tick_params(labelsize=7)
    fig.suptitle(title, x=.01, ha="left", fontsize=9.5, color=INK)
    fig.savefig(out, dpi=150, facecolor=SURF); plt.close(fig)


QU, NM = "Q relative to Folded", "core-fit RMSD (nm)"
sheet([("β1 ↔ rest [PUF1]", qrel("b1_rest"), qcm, qn, QU), ("loop 133–143 ↔ α3 [PUF1]", qrel("loop_a3"), qcm, qn, QU), ("α3 C 217–223 [PUF1]", qrel("a3C217"), qcm, qn, QU),
       ("α1+β2 ↔ core [PUF2]", qrel("a1b2_core"), qcm, qn, QU), ("α1 N 144–148 [m_op 0.4]", rig("a1N_corefit"), dcm, dn, NM), ("α1C–β2 unit 144–167 [PUF2]", rig("unit_corefit"), dcm, dn, NM)],
      "Paper-derived PUF variables by position. Blue, native Cα contacts (macro_structure.py definitions), darker = contacts lost.\n"
      "Orange, displacement after superposing on the disulfide-proximal core (175–187, 201–216), darker = further from 2L39.\n"
      "Black contours, MSM free energy 1, 2, 3 kcal/mol. Dashed circles, historical basins. Red cross, pH 7 minimum (87.5, 17.5). Grey, fewer than 10 frames.", f"{prefix}_maps.png")
T = TH
def R(d):
    r = d["r"]; o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    return dict(b1=b1 & ~lp & ~a1n, m04=b1 & lp & a1n & ok, unit=un & ~b1 & ok, puf2=a1 & b2 & ok, a3=(o("a3C_corefit") | o("a3C_selffit")) & ~b1)
FU = "fraction of frames in bin"
sheet([("β1 alone displaced", lambda d: R(d)["b1"].astype(float), fcm, fn, FU), ("β1 + loop + α1 N (m_op 0.4 class)", lambda d: R(d)["m04"].astype(float), fcm, fn, FU),
       ("α1+β2 off, core intact (PUF2 text)", lambda d: R(d)["puf2"].astype(float), fcm, fn, FU), ("α1C–β2 unit off, β1 kept", lambda d: R(d)["unit"].astype(float), fcm, fn, FU),
       ("α3 C off or disordered, β1 kept", lambda d: R(d)["a3"].astype(float), fcm, fn, FU)],
      "Where each rule is met. A segment is displaced when beyond the 99th percentile of Folded frames (pooled over pH).\n"
      "The full PUF1 text rule (β1 + loop + α3 C) has no frames and is not shown.\n"
      "Black contours, MSM free energy 1, 2, 3 kcal/mol. Dashed circles, historical basins. Red cross, pH 7 minimum. Grey, fewer than 10 frames.", f"{prefix}_rules.png")
print("wrote", prefix)
