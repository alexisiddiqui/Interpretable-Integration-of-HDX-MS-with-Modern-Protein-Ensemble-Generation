"""Mutually exclusive cluster identity of every frame from the paper-derived rules (priority order below), on the PCA101
and dihedral planes. Writes three figures: _clusters_overview (dominant cluster per bin, by frames and MSM weight; pale = share below
50 %), _clusters_candidates (PUF1 and PUF2 candidates) and _clusters_rules (remaining clusters), the last two as share of bin.

Usage: puf_clusters.py <puf_cvs_tight.npz> <puf_final.json> <basins_seed.json> <out_prefix>"""
import json, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import BoundaryNorm, ListedColormap, to_rgb
from matplotlib.patches import Patch
from scipy.ndimage import gaussian_filter
Z = np.load(sys.argv[1]); T = json.load(open(sys.argv[2]))["thresholds_nm"]; BAS = json.load(open(sys.argv[3])); prefix = sys.argv[4]
rn = [str(s) for s in Z["rig_names"]]
KT = 0.0019872043 * 298.15
INK, INK2, SURF, EMPTY = "#0b0b0b", "#52514e", "#fcfcfb", "#ffffff"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8, "figure.facecolor": SURF, "axes.facecolor": EMPTY, "axes.edgecolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.labelcolor": INK2})
# id, label, colour (hues = palette slots 1-3, validated all-pairs; the rest neutral)
CL = [("F", "Folded-like", "#e4e2dc"), ("B1", "β1 alone", "#2a78d6"), ("P1", "PUF1 candidate: β1 + loop + α1 N", "#eb6834"), ("P2", "PUF2 candidate: β1 + α1 + β2, core intact", "#1baf7a"),
      ("B1X", "β1 + partial (loop or α1 N, or core distorted)", "#8f8d86"), ("CORE", "β1 kept, core distorted", "#55534e"), ("A3", "β1 kept, α3 C off or disordered", "#55534e"), ("UNIT", "β1 kept, α1C–β2 unit off", "#55534e")]
IDS = [c[0] for c in CL]


def label(ph):
    r = {n: Z[f"{ph}_rig"][:, i] for i, n in enumerate(rn)}
    o = lambda n: r[n] > T[n]; ok = ~o("core")
    b1, lp, a1, a1n, b2, un = o("b1_corefit"), o("loop_corefit"), o("a1_corefit"), o("a1N_corefit"), o("b2_corefit"), o("unit_corefit")
    a3 = o("a3C_corefit") | o("a3C_selffit")
    lab = np.zeros(len(b1), int)                                   # F
    lab[~b1 & un & ok] = IDS.index("UNIT")
    lab[~b1 & a3] = IDS.index("A3")
    lab[~b1 & ~ok] = IDS.index("CORE")
    lab[b1] = IDS.index("B1X")
    lab[b1 & ~lp & ~a1n & ok] = IDS.index("B1")
    lab[b1 & lp & a1n & ok] = IDS.index("P1")
    lab[b1 & a1 & b2 & ok] = IDS.index("P2")
    return lab, dict(both_a3_core=int((~b1 & a3 & ~ok).sum()), both_a3_unit=int((~b1 & a3 & un & ok).sum()))


D = {}
for ph in ("ph4", "ph7"):
    lab, ov = label(ph)
    D[ph] = dict(lab=lab, x=Z[f"{ph}_x"], wp=Z[f"{ph}_wp"], wm=Z[f"{ph}_wm"], run=Z[f"{ph}_run"], src=Z[f"{ph}_src"], ov=ov)

out = {}
print(f"{'cluster':46s} | pH 4: frames runs top-source  MSM%  dG/Fl  MaxCal% dG/Fl | pH 7 same")
for k, (i, name, _) in enumerate(CL):
    s = f"{name[:46]:46s}"
    for ph, d in D.items():
        m = d["lab"] == k; f = d["lab"] == 0
        g = lambda w: -KT * np.log(w[m].sum() / w[f].sum()) if w[m].sum() > 0 else np.inf
        srcs, cnt = np.unique(d["src"][m], return_counts=True); top = srcs[cnt.argmax()] if len(srcs) else "-"; sh = cnt.max() / cnt.sum() if len(srcs) else 0
        s += f" | {m.sum():6d} {len(np.unique(d['run'][m])):3d} {top:8s}{sh:4.2f} {100*d['wp'][m].sum():5.1f} {g(d['wp']):5.2f}  {100*d['wm'][m].sum():5.1f} {g(d['wm']):5.2f}"
        out[f"{i}|{ph}"] = dict(frames=int(m.sum()), runs=int(len(np.unique(d['run'][m]))), top_source=str(top), top_share=float(sh), msm_pct=float(100 * d['wp'][m].sum()), dG_vs_folded_like_msm=float(g(d['wp'])), maxcal_pct=float(100 * d['wm'][m].sum()), dG_vs_folded_like_maxcal=float(g(d['wm'])))
    print(s)
print("overlaps resolved by priority:", {p: D[p]["ov"] for p in D})
json.dump(out, open(prefix + "_clusters.json", "w"), indent=1)

PLANES = {"pca": (0, 1, np.arange(-30, 125, 5.0), np.arange(-100, 70, 5.0)), "dih": (2, 3, np.arange(-0.36, 0.04, 0.0125), np.arange(0.74, 2.08, 0.04))}


def deco(ax, plane, d):
    i, j, xe, ye = PLANES[plane]
    H = np.histogram2d(d["x"][:, i], d["x"][:, j], bins=[xe, ye], weights=d["wp"])[0]; Hs = gaussian_filter(H, .7)
    G = -KT * np.log(np.maximum(Hs, 1e-12) / Hs.max())
    ax.contour(.5 * (xe[1:] + xe[:-1]), .5 * (ye[1:] + ye[:-1]), G.T, levels=[1, 2, 3], colors=INK, linewidths=[.8, .55, .35], alpha=.75)
    if plane == "pca":
        for b in BAS:
            ax.add_patch(plt.Circle(b["centre"], 10, fill=False, ec=INK, lw=.7, ls=(0, (3, 2))))
        ax.set_aspect("equal"); ax.set_xlim(-30, 120); ax.set_ylim(-100, 65); ax.set_xlabel("PC1"); ax.set_ylabel("PC2")
    else:
        ax.set_xticks(np.log10([.5, .7, 1.0])); ax.set_xticklabels([".5", ".7", "1"]); ax.set_yticks(np.log10([10, 30, 100])); ax.set_yticklabels(["10", "30", "100"])
        ax.set_xlim(-.36, .03); ax.set_ylim(.74, 2.08); ax.set_xlabel("dRMSD (rad, log)"); ax.set_ylabel("β1 dihedral dev. (°, log)")


def dominant(ax, plane, ph, by, minf=10):
    d = D[ph]; i, j, xe, ye = PLANES[plane]; x, y = d["x"][:, i], d["x"][:, j]
    n = np.histogram2d(x, y, bins=[xe, ye])[0]
    w = np.ones(len(x)) if by == "frames" else d["wp"]
    H = np.stack([np.histogram2d(x[d["lab"] == k], y[d["lab"] == k], bins=[xe, ye], weights=w[d["lab"] == k])[0] for k in range(len(CL))])
    tot = H.sum(0); top = H.argmax(0); share = np.divide(H.max(0), tot, out=np.zeros_like(tot), where=tot > 0)
    img = np.ones((*top.shape, 3))
    for k, c in enumerate(CL):
        rgb = np.array(to_rgb(c[2])); m = top == k
        img[m] = rgb; p = m & (share < .5); img[p] = .5 * rgb + .5 * np.array(to_rgb(SURF))
    img[(n < minf) | (tot <= 0)] = 1
    ax.imshow(img.transpose(1, 0, 2), origin="lower", extent=[xe[0], xe[-1], ye[0], ye[-1]], aspect="auto", interpolation="nearest")
    deco(ax, plane, d)


COLS = [("pca", "ph4"), ("dih", "ph4"), ("pca", "ph7"), ("dih", "ph7")]
tt = lambda a, t: a.set_title(t, loc="left", fontsize=8, color=INK, fontweight="bold")
where = lambda plane, ph: ("PCA" if plane == "pca" else "Dihedral") + f", pH {ph[2]}" + (" (target)" if ph == "ph4" else "")
NOTE = "White: fewer than 10 frames. Black contours: MSM free energy 1, 2, 3 kcal/mol. Dashed circles: historical basins."
fn = BoundaryNorm([0, .02, .1, .25, .5, .75, 1.0], 6)


def ramp(hex_):
    """Single-hue sequential ramp, pale neutral to the cluster's own colour and a darker step of it."""
    lo, hi = np.array(to_rgb("#eeede8")), np.array(to_rgb(hex_))
    return ListedColormap([tuple(lo + (hi - lo) * t) for t in (0, .2, .4, .65, .85, 1)][:5] + [tuple(hi * .72)])


def frac(a, plane, ph, idn, cm):
    d = D[ph]; k = IDS.index(idn); i, j, xe, ye = PLANES[plane]; x, y = d["x"][:, i], d["x"][:, j]
    n = np.histogram2d(x, y, bins=[xe, ye])[0]; h = np.histogram2d(x[d["lab"] == k], y[d["lab"] == k], bins=[xe, ye])[0]
    im = a.pcolormesh(xe, ye, np.where(n >= 10, h / np.maximum(n, 1), np.nan).T, cmap=cm, norm=fn, rasterized=True); deco(a, plane, d)
    return im


def share_sheet(rows, title, out):
    fig, ax = plt.subplots(len(rows), 4, figsize=(11.6, 2.75 * len(rows) + .7), constrained_layout=True, squeeze=False)
    for r, (idn, short, hex_) in enumerate(rows):
        cm = ramp(hex_)
        for c, (plane, ph) in enumerate(COLS):
            im = frac(ax[r, c], plane, ph, idn, cm); tt(ax[r, c], f"{short}, {where(plane, ph)}")
        cb = fig.colorbar(im, ax=ax[r, :], shrink=.86, pad=.012, aspect=16); cb.set_label("fraction of frames in bin", fontsize=7.5, color=INK); cb.ax.tick_params(labelsize=7)
    fig.suptitle(title, x=.01, ha="left", fontsize=8.5, color=INK)
    fig.savefig(out, dpi=150, facecolor=SURF); plt.close(fig)


# 1. overview: dominant cluster per bin
fig, ax = plt.subplots(2, 4, figsize=(11.6, 6.4), constrained_layout=True)
for c, (plane, ph) in enumerate(COLS):
    dominant(ax[0, c], plane, ph, "frames"); dominant(ax[1, c], plane, ph, "weight")
    tt(ax[0, c], where(plane, ph) + ", by frames"); tt(ax[1, c], where(plane, ph) + ", by MSM weight")
hand = [Patch(fc=CL[0][2], ec=INK2, lw=.3, label=CL[0][1]), Patch(fc=CL[1][2], label=CL[1][1]), Patch(fc=CL[2][2], label=CL[2][1]), Patch(fc=CL[3][2], label=CL[3][1]),
        Patch(fc=CL[4][2], label=CL[4][1]), Patch(fc=CL[5][2], label="β1 kept: core, α3 C or unit")]
fig.legend(handles=hand, loc="outside upper left", ncol=3, frameon=False, fontsize=8, alignment="left", title_fontsize=8,
           title="Overall cluster identity. One identity per frame; each bin shows its dominant cluster, pale where that cluster is below 50 % of the bin.\n" + NOTE)
fig.savefig(prefix + "_clusters_overview.png", dpi=150, facecolor=SURF); plt.close(fig)
# 2. PUF candidates, both pH
share_sheet([("P1", "PUF1 candidate", CL[2][2]), ("P2", "PUF2 candidate", CL[3][2])],
            "PUF candidates, share of each bin. PUF1 candidate: β1 + loop + α1 N displaced, core intact. PUF2 candidate: β1 + α1 + β2 displaced, core intact.\n" + NOTE, prefix + "_clusters_candidates.png")
# 3. remaining rule clusters, both pH
share_sheet([("B1", "β1 alone", CL[1][2]), ("B1X", "β1 + partial", CL[4][2]), ("CORE", "Core distorted", CL[5][2]), ("A3", "α3 C off", CL[5][2]), ("UNIT", "Unit off", CL[5][2])],
            "Remaining rule clusters, share of each bin. β1 + partial: β1 displaced with the loop or α1 N, or with the core distorted.\nRows 3–5 have β1 kept. Core distorted: the disulfide-proximal core itself moves. α3 C off: displaced or disordered. Unit off: α1C–β2, 144–167.\n" + NOTE, prefix + "_clusters_rules.png")
print("wrote", prefix)
