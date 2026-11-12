"""Drift ("flow") maps of the seeded runs in two planes, per target pH.

For every frame x(t) of every run and a lag tau, the displacement x(t + tau) - x(t) is assigned to the bin of
x(t); the mean displacement per bin divided by tau is the drift of the projected dynamics. Seeding density does
not bias it (each arrow is conditional on position), but it inherits the projection: motion along coordinates
not shown is averaged over. Bins with fewer than MIN_PAIRS displacement pairs (or, to avoid one run dominating,
fewer than MIN_RUNS distinct runs) are left blank.

Planes: the 101-HDX-residue Cartesian PCA, and the JAX-ENT MoPrP dihedral plane (dihedral_features.py): log10
dRMSD (phi/psi vs the 2L39 NMR circular mean, PrP 124-222, rad) vs log10 beta1 dihedral deviation (mean |dphi/psi|,
PrP 127-132, deg). Drift is computed in the plotted (log10) coordinates on uniform bins; background =
unbiased MD density at the target pH.

Colours are quantised in 7 bins on the shared reference: plasma for speed, coolwarm for the signed change.
Arrow styles (same colour/length reference per plane in all three rows: 0 to the 95th percentile of speed):
  default                unit-length arrows coloured by speed (direction only)
  --magnitude-contours   speed as contour lines (7 levels, one per colour bin, lightly smoothed field), black arrows with
                         length proportional to speed and a key arrow at the reference speed
  --signed-delta         pH 7 - pH 4 row coloured by the signed speed change |drift pH 7| - |drift pH 4| on a
                         diverging blue (faster at pH 4) - grey - red (faster at pH 7) scale, +/- the reference
                         speed; arrows keep the direction (and, with --magnitude-contours, length) of the difference
  --contour-planes <pca|dih|pca,dih>
                         use the --magnitude-contours style on these planes only and unit arrows on the others (e.g.
                         speed contours on the PCA plane, direction arrows on the dihedral plane); default: all planes
                         with --magnitude-contours, none without

  --extend <ext_qc.npz[,ext_qc2.npz]> <ext_dihedrals.npz[,ext_dih2.npz]>
                         replace the runs present in the extension archives (same entries, longer production) by their
                         full trajectories; no frame is counted twice
  --compare-early-late [split_ns=20]
                         also write <out_prefix>_early_late.png: the drift from pairs starting before split_ns vs at or
                         after it, overlaid in the bins valid in both, with the cosine of the angle between them (a
                         check that the projected dynamics do not depend on time since seeding, i.e. that runs of
                         different length can be pooled)

Usage: python flow_map.py <qc.npz> <pca101_scores.npz> <basins_seed.json> <out_prefix> [tau_ns=1.0] [dihedrals.npz]
                          [--magnitude-contours] [--contour-planes <planes>] [--signed-delta] [--extend <ext_qc.npz> <ext_dih.npz>]
                          [--compare-early-late [split_ns]]
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patheffects as pe
from matplotlib.cm import ScalarMappable
from matplotlib.colors import BoundaryNorm, ListedColormap, Normalize
from matplotlib.ticker import FixedLocator, FuncFormatter

# quantised colour scales, N_BINS bins per plane on the shared reference: plasma for speed (stopped at 0.85, as its
# pale-yellow end vanishes on the light background) and coolwarm for the signed pH 7 - pH 4 change
# (blue = faster at pH 4, light grey = no change, red = faster at pH 7)
N_BINS = 7
SEQUENTIAL = ListedColormap(plt.get_cmap("plasma")(np.linspace(0.0, 0.85, N_BINS)), name="plasma_q")
DIVERGING = ListedColormap(plt.get_cmap("coolwarm")(np.linspace(0.0, 1.0, N_BINS)), name="coolwarm_q")
for _cm in (SEQUENTIAL, DIVERGING):
    _cm.set_over(_cm(N_BINS - 1)); _cm.set_under(_cm(0))

def pop_option(name, n, default=None):
    """Remove `name` and up to n following non-flag values from sys.argv; return the values (or None if absent)."""
    if name not in sys.argv:
        return None
    i = sys.argv.index(name)
    vals = []
    while len(vals) < n and i + 1 + len(vals) < len(sys.argv) and not sys.argv[i + 1 + len(vals)].startswith("--"):
        vals.append(sys.argv[i + 1 + len(vals)])
    del sys.argv[i:i + 1 + len(vals)]
    return vals or default


EXTEND = pop_option("--extend", 2)
SPLIT = pop_option("--compare-early-late", 1, ["20"])
SPLIT_NS = float(SPLIT[0]) if SPLIT else None
MAGNITUDE_CONTOURS = "--magnitude-contours" in sys.argv
SIGNED_DELTA = "--signed-delta" in sys.argv
_cp = pop_option("--contour-planes", 1)
CONTOUR_PLANES = set(_cp[0].split(",")) if _cp else ({"pca", "dih"} if MAGNITUDE_CONTOURS else set())
sys.argv = [a for a in sys.argv if a not in ("--magnitude-contours", "--signed-delta")]
qc_path, scores_path, basins_path, prefix = sys.argv[1:5]
TAU_NS = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
D = np.load(sys.argv[6]) if len(sys.argv) > 6 else None
MIN_PAIRS, MIN_RUNS = 200, 3
Q = np.load(qc_path)
S = np.load(scores_path, allow_pickle=True)
runs = json.loads(str(Q["runs"]))
basins = json.load(open(basins_path))
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e6e5e1", "#fcfcfb"
# basin markers: dark green = basins from the pH 4 MI+PB runs, mid green = from the pH 7 runs (no green in
# plasma or coolwarm, so markers do not read as data colours)
SOURCE_GREEN = {"pH 4": "#005a32", "pH 7": "#3a9d4f"}
# label angle (deg) per basin and plane, chosen so labels sit outside their circle/marker and clear of neighbours
LABEL_ANGLE = {"pca": {"ph4_1": 225, "ph7_1": 90, "ph4_2": 60, "ph4_3": 0, "ph7_2": 0, "ph7_3": -35},
               "dih": {"ph4_1": 200, "ph7_1": 0, "ph4_2": 160, "ph4_3": 80, "ph7_2": 15, "ph7_3": 55}}
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": INK2, "axes.labelcolor": INK2,
                     "xtick.color": INK2, "ytick.color": INK2, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})


# per-run coordinates (dihedral archive in the same run order as the QC archive: same task list)
PC = {i: Q[f"r{i:03d}_pc"].astype(float) for i in range(len(runs))}
TIME = {i: Q[f"r{i:03d}_time_ps"].astype(float) / 1000.0 for i in range(len(runs))}
DIH = ({i: np.column_stack([D[f"r{i:03d}_drmsd_rad"], D[f"r{i:03d}_b1_dih_dev_deg"]]).astype(float)
        for i in range(len(runs))} if D is not None else {})
# --extend takes comma-separated lists (QC archives, dihedral archives in matching order) for several extension sets
for eq_path, ed_path in (zip(EXTEND[0].split(","), EXTEND[1].split(","), strict=True) if EXTEND else ()):
    EQ, ED = np.load(eq_path), np.load(ed_path)
    ext_runs = json.loads(str(EQ["runs"]))
    assert json.loads(str(ED["entries"])) == [r["entry"] for r in ext_runs], "extension QC/dihedral run order differs"
    where = {r["entry"]: i for i, r in enumerate(runs)}
    for j, r in enumerate(ext_runs):
        i = where[r["entry"]]                          # an extension continues a run already in the base archive
        t_ext = EQ[f"r{j:03d}_time_ps"].astype(float) / 1000.0
        assert np.allclose(t_ext[:len(TIME[i])], TIME[i]), r["entry"]
        PC[i], TIME[i] = EQ[f"r{j:03d}_pc"].astype(float), t_ext
        DIH[i] = np.column_stack([ED[f"r{j:03d}_drmsd_rad"], ED[f"r{j:03d}_b1_dih_dev_deg"]]).astype(float)
        runs[i]["extended"] = True


def coords(i, plane):
    if plane == "pca":
        return PC[i]
    return np.log10(DIH[i])


def density_contours(ax, H, xe, ye, levels=5):
    """Background log10 density as grey, translucent filled contours (no edges): `levels` bands from the
    lowest occupied to the highest density, on a lightly smoothed histogram."""
    from scipy.ndimage import gaussian_filter
    xc, yc = (xe[:-1] + xe[1:]) / 2, (ye[:-1] + ye[1:]) / 2
    occupied = gaussian_filter((H > 0).astype(float), 0.8) > 0.25
    logd = np.log10(gaussian_filter(H.astype(float), 0.8) + 1e-12)
    logd = np.ma.masked_where(~occupied, logd)
    bounds = np.linspace(float(logd.min()), float(logd.max()), levels + 1)
    cs = ax.contourf(xc, yc, logd.T, levels=bounds, cmap="Greys", alpha=0.45, antialiased=True, zorder=0)
    cs.set_edgecolor("none")  # no outlines: edges drawn in the face colour double the translucency
    cs.set_linewidth(0)
    return cs


def drift(ids, plane, xe, ye, window=None):
    """Drift per bin from all pairs (x(t), x(t + tau)) of the runs `ids`; `window` = (t0, t1) ns keeps only pairs
    whose start t lies in [t0, t1)."""
    dt_ns = float(np.median(np.diff(TIME[ids[0]])))
    lag = max(1, int(round(TAU_NS / dt_ns)))
    nx, ny = len(xe) - 1, len(ye) - 1
    sum_d = np.zeros((nx, ny, 2)); count = np.zeros((nx, ny)); runs_in = [[set() for _ in range(ny)] for _ in range(nx)]
    occupancy = np.zeros((nx, ny))
    for i in ids:
        x = coords(i, plane)
        occupancy += np.histogram2d(x[:, 0], x[:, 1], bins=(xe, ye))[0]
        a, d = x[:-lag], x[lag:] - x[:-lag]
        if window is not None:
            keep = (TIME[i][:-lag] >= window[0] - 1e-9) & (TIME[i][:-lag] < window[1] - 1e-9)
            a, d = a[keep], d[keep]
        bx, by = np.digitize(a[:, 0], xe) - 1, np.digitize(a[:, 1], ye) - 1
        ok = (bx >= 0) & (bx < nx) & (by >= 0) & (by < ny)
        np.add.at(sum_d, (bx[ok], by[ok]), d[ok])
        np.add.at(count, (bx[ok], by[ok]), 1)
        for p, q in set(zip(bx[ok], by[ok])):
            runs_in[p][q].add(i)
    nruns = np.array([[len(c) for c in row] for row in runs_in])
    valid = (count >= MIN_PAIRS) & (nruns >= MIN_RUNS)
    v = np.where(valid[..., None], sum_d / np.maximum(count, 1)[..., None] / (lag * dt_ns), np.nan)
    return v, valid, occupancy, lag * dt_ns


def draw_field(ax, fig, plane, P, v, valid, label, signed=None):
    """Draw a drift (or drift-difference) field on the shared per-plane scale NORM[plane]. With `signed` (a per-bin
    signed scalar, e.g. the speed change between pH), hue follows it on a diverging +/- reference scale."""
    xe, ye = P["xe"], P["ye"]
    xc, yc = (xe[:-1] + xe[1:]) / 2, (ye[:-1] + ye[1:]) / 2
    X, Y = np.meshgrid(xc, yc, indexing="ij")
    speed = np.hypot(v[..., 0], v[..., 1])
    sx, sy = (xe[-1] - xe[0]), (ye[-1] - ye[0])
    ux, uy = v[..., 0] / sx, v[..., 1] / sy          # direction in axis-fraction space
    unit = np.hypot(ux, uy)
    cell = min((xe[1] - xe[0]) / sx, (ye[1] - ye[0]) / sy)
    vmax = NORM[plane].vmax
    # quantised scale; a fresh norm per panel (a shared instance re-signals and resets earlier colour bars' ticks)
    if signed is None:
        hue, cmap, extend = speed, SEQUENTIAL, "max"
        bounds = np.linspace(0.0, vmax, N_BINS + 1)
    else:
        hue, cmap, extend = signed, DIVERGING, "both"
        bounds = np.linspace(-vmax, vmax, N_BINS + 1)
    norm_panel = BoundaryNorm(bounds, N_BINS)

    def colourbar():
        cb = fig.colorbar(ScalarMappable(norm=norm_panel, cmap=cmap), ax=ax, shrink=0.8, pad=0.01, extend=extend)
        cb.ax.yaxis.set_major_locator(FixedLocator(bounds))
        cb.ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{x:.2g}"))
        cb.set_label(f"{label} ({P['unit']})", fontsize=8)

    if plane not in CONTOUR_PLANES:
        # lengths scale ~1/tau (displacement saturates within the lag): unit arrows coloured by speed (or signed change)
        ax.quiver(X[valid], Y[valid], (ux / unit * sx)[valid], (uy / unit * sy)[valid], hue[valid],
                  cmap=cmap, norm=norm_panel, angles="xy", scale_units="xy", scale=1.0 / (0.8 * cell),
                  width=0.0030, headwidth=4, headlength=4.5)
        colourbar()
        return
    from scipy.ndimage import gaussian_filter
    # speed contours on a lightly smoothed field (normalised convolution over the valid bins only)
    w = gaussian_filter(valid.astype(float), 1.2)
    smooth = gaussian_filter(np.where(valid, hue, 0.0), 1.2) / np.maximum(w, 1e-9)
    smooth = np.ma.masked_where(w < 0.4, smooth)
    # one contour per bin boundary: 7 speed levels (vmax/7 ... vmax) or the signed boundaries (+/- vmax/7 ... vmax)
    levels = bounds[1:] if signed is None else bounds[np.abs(bounds) > 1e-12 * vmax]
    ax.contour(xc, yc, smooth.T, levels=levels, cmap=cmap, norm=norm_panel, linewidths=1.4, linestyles="solid",
               zorder=2)
    # black arrows, length proportional to speed: the reference speed vmax spans 0.9 of a bin
    length = np.clip(speed / vmax, 0, 1.6)
    qv = ax.quiver(X[valid], Y[valid], (ux / unit * sx * length)[valid], (uy / unit * sy * length)[valid],
                   color=INK, angles="xy", scale_units="xy", scale=1.0 / (0.9 * cell), width=0.0028,
                   headwidth=4, headlength=4.5, headaxislength=4, minlength=0.2, zorder=3)
    # key: a horizontal arrow of data length sx at length factor 1, i.e. the reference speed vmax
    ax.quiverkey(qv, 0.93, 0.04, sx, f"{vmax:.2g} {P['unit']}", labelpos="W", coordinates="axes",
                 fontproperties={"size": 7.5}, color=INK, labelsep=0.05)
    colourbar()


def draw_basins(ax, plane, ph):
    """Basin circles (PCA) or seed-median markers (dihedral plane, seeds run at `ph`), in the source-pH green,
    each labelled outside its circle/marker along LABEL_ANGLE, on a light halo so arrows do not obscure it."""
    for b in basins:
        tag = f"{b['ph'].replace(' ', '').lower()}_{b['id']}"
        colour, ang = SOURCE_GREEN[b["ph"]], np.radians(LABEL_ANGLE[plane][tag])
        if plane == "pca":
            cx, cy = b["centre"]
            ax.add_patch(plt.Circle((cx, cy), b["radius"], fill=False, ec=colour, lw=1.6, ls="--", zorder=4))
            # anchor just beyond the circle edge (PCA axes are close to equal aspect)
            anchor, offset = (cx + (b["radius"] + 2) * np.cos(ang), cy + (b["radius"] + 2) * np.sin(ang)), (0, 0)
        else:
            seeds = [i for i, r in enumerate(runs) if r["basin"] == tag and r["target_ph"] == ph]
            cx = np.median([coords(i, plane)[0, 0] for i in seeds]); cy = np.median([coords(i, plane)[0, 1] for i in seeds])
            ax.scatter(cx, cy, s=60, marker="o", facecolor="none", edgecolor=colour, lw=1.8, zorder=5)
            anchor, offset = (cx, cy), (9 * np.cos(ang), 9 * np.sin(ang))
        ha = "left" if np.cos(ang) > 0.3 else ("right" if np.cos(ang) < -0.3 else "center")
        va = "bottom" if np.sin(ang) > 0.3 else ("top" if np.sin(ang) < -0.3 else "center")
        ax.annotate(f"{b['ph']} #{b['id']} {b['label']}", anchor, xytext=offset, textcoords="offset points",
                    ha=ha, va=va, fontsize=7.5, color=colour, fontweight="bold", zorder=6,
                    path_effects=[pe.withStroke(linewidth=2.5, foreground=SURF)])


PLANES = {
    "pca": dict(xe=np.linspace(-50, 140, 39), ye=np.linspace(-100, 70, 35), xlabel=f"PC1 ({S['ph4_explained'][0]:.0%})",
                ylabel=f"PC2 ({S['ph4_explained'][1]:.0%})", unit="PC units ns⁻¹",
                title="101-HDX-residue Cartesian PCA"),
    "dih": dict(xe=np.linspace(np.log10(0.42), np.log10(1.6), 31), ye=np.linspace(np.log10(7), np.log10(120), 31),
                xlabel="dRMSD vs 2L39 NMR circular mean, PrP 124–222 (rad, log scale)",
                ylabel="β1 dihedral deviation, mean |Δφ/ψ| PrP 127–132 (°, log scale)", unit="log₁₀ units ns⁻¹",
                title="JAX-ENT dihedral plane", log=True),
}
if D is not None:
    assert json.loads(str(D["entries"])) == [r["entry"] for r in runs], "dihedral archive and QC archive differ in run order"
ACTIVE = [(k, v) for k, v in PLANES.items() if k != "dih" or D is not None]
RESULTS, NORM = {}, {}
for plane, P in ACTIVE:
    for ph in ("ph4", "ph7"):
        RESULTS[(plane, ph)] = drift([i for i, r in enumerate(runs) if r["target_ph"] == ph], plane, P["xe"], P["ye"])
    speeds = np.concatenate([np.hypot(*RESULTS[(plane, ph)][0][RESULTS[(plane, ph)][1]].T) for ph in ("ph4", "ph7")])
    NORM[plane] = Normalize(vmin=0.0, vmax=float(np.percentile(speeds, 95)))   # same hue scale in all three rows
fig, axes = plt.subplots(3, 2, figsize=(17, 18))
for col, (plane, P) in enumerate(ACTIVE):
    xe, ye = P["xe"], P["ye"]
    xc, yc = (xe[:-1] + xe[1:]) / 2, (ye[:-1] + ye[1:]) / 2
    for row, ph in enumerate(("ph4", "ph7")):
        ax = axes[row, col]
        ids = [i for i, r in enumerate(runs) if r["target_ph"] == ph]
        v, valid, occupancy, tau = RESULTS[(plane, ph)]
        if plane == "pca":
            u = S[f"{ph}_u"]
        else:
            u = np.log10(np.column_stack([D[f"u_{ph}_drmsd_rad"], D[f"u_{ph}_b1_dih_dev_deg"]]).astype(float))
        H = np.histogram2d(u[:, 0], u[:, 1], bins=(xe, ye))[0]
        bg_label = "grey contours: unbiased MD log density, 5 levels"
        density_contours(ax, H, xe, ye)
        draw_field(ax, fig, plane, P, v, valid, "drift speed")
        draw_basins(ax, plane, ph)
        ax.set_xlim(xe[0], xe[-1]); ax.set_ylim(ye[0], ye[-1])
        if P.get("log"):  # coordinates are log10; label ticks with the physical values
            xt, yt = [0.5, 0.6, 0.8, 1.0, 1.5], [10, 15, 20, 30, 40, 60, 100]
            ax.set_xticks(np.log10(xt)); ax.set_xticklabels([f"{v:g}" for v in xt])
            ax.set_yticks(np.log10(yt)); ax.set_yticklabels([f"{v:g}" for v in yt])
        ax.set_xlabel(P["xlabel"]); ax.set_ylabel(P["ylabel"])
        ax.set_title(f"run at pH {ph[2]}: {P['title']}, τ = {tau:g} ns ({bg_label})", loc="left", fontsize=9.5, color=INK)
# ---------- row 3: pH 7 minus pH 4 (same seeds, only the protonation differs) ----------
for col, (plane, P) in enumerate(ACTIVE):
    ax = axes[2, col]
    xe, ye = P["xe"], P["ye"]
    xc, yc = (xe[:-1] + xe[1:]) / 2, (ye[:-1] + ye[1:]) / 2
    (v4, ok4, _, _), (v7, ok7, _, _) = RESULTS[(plane, "ph4")], RESULTS[(plane, "ph7")]
    # background: unbiased MD from both pH pooled, drawn exactly as in rows 1-2
    if plane == "pca":
        pooled = np.concatenate([S["ph4_u"], S["ph7_u"]])
    else:
        pooled = np.log10(np.concatenate([np.column_stack([D[f"u_{ph}_drmsd_rad"], D[f"u_{ph}_b1_dih_dev_deg"]])
                                          for ph in ("ph4", "ph7")]).astype(float))
    density_contours(ax, np.histogram2d(pooled[:, 0], pooled[:, 1], bins=(xe, ye))[0], xe, ye)
    if SIGNED_DELTA:
        draw_field(ax, fig, plane, P, v7 - v4, ok4 & ok7, "|drift pH 7| − |drift pH 4| (red: faster at pH 7)",
                   signed=np.hypot(v7[..., 0], v7[..., 1]) - np.hypot(v4[..., 0], v4[..., 1]))
    else:
        draw_field(ax, fig, plane, P, v7 - v4, ok4 & ok7, "|drift pH 7 − pH 4|")
    draw_basins(ax, plane, "ph4")
    ax.set_xlim(xe[0], xe[-1]); ax.set_ylim(ye[0], ye[-1])
    if P.get("log"):
        xt, yt = [0.5, 0.6, 0.8, 1.0, 1.5], [10, 15, 20, 30, 40, 60, 100]
        ax.set_xticks(np.log10(xt)); ax.set_xticklabels([f"{v:g}" for v in xt])
        ax.set_yticks(np.log10(yt)); ax.set_yticklabels([f"{v:g}" for v in yt])
    ax.set_xlabel(P["xlabel"]); ax.set_ylabel(P["ylabel"])
    ax.set_title(f"pH 7 − pH 4 drift, same {len(runs) // 2} seeds (grey contours: unbiased MD, both pH pooled)",
                 loc="left", fontsize=9.5, color=INK)

_contour = f"speed as {N_BINS} contour lines; black arrows, length ∝ speed (key = reference speed; capped at 1.6×)"
_arrows = "arrows show direction only, coloured by speed"
if CONTOUR_PLANES == {p for p, _ in ACTIVE}:
    style = _contour
elif not CONTOUR_PLANES:
    style = _arrows
else:
    style = "; ".join(f"{PLANES[p]['title']}: {_contour if p in CONTOUR_PLANES else _arrows}" for p, _ in ACTIVE)
style += f"; colours quantised in {N_BINS} bins; basin markers: dark green from pH 4 runs, mid green from pH 7 runs"
if SIGNED_DELTA:
    style += "; bottom row hue = signed speed change (blue faster at pH 4, red faster at pH 7)"
import textwrap
caption = (f"One speed scale per plane in all three rows; {style}.")
n_ext = sum(1 for r in runs if r.get("extended"))
total_ns = sum(TIME[i][-1] for i in range(len(runs)))
sampling = (f"{len(runs)} seeded runs, {len(runs) - n_ext} × {np.median([TIME[i][-1] for i in range(len(runs)) if not runs[i].get('extended')]):.0f} ns"
            + (f" + {n_ext} × {np.median([TIME[i][-1] for i in range(len(runs)) if runs[i].get('extended')]):.0f} ns (extended)" if n_ext else "")
            + f", {total_ns / 1000:.2f} µs")
fig.suptitle(f"Drift field of the {sampling}: mean displacement over τ per bin / τ; "
             f"bins with ≥{MIN_PAIRS} pairs from ≥{MIN_RUNS} runs.\n" + "\n".join(textwrap.wrap(caption, 190)),
             x=0.01, ha="left", fontsize=11, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.955))
fig.savefig(f"{prefix}.png", dpi=130)
print("wrote", f"{prefix}.png")

# ---------- early vs late drift (time since seeding) ----------
if SPLIT_NS is not None:
    EARLY, LATE = "#1b1b1b", "#e66101"
    fig, axes = plt.subplots(2, len(ACTIVE), figsize=(8.5 * len(ACTIVE), 12.5), squeeze=False)
    summary = []
    for col, (plane, P) in enumerate(ACTIVE):
        xe, ye = P["xe"], P["ye"]
        xc, yc = (xe[:-1] + xe[1:]) / 2, (ye[:-1] + ye[1:]) / 2
        X, Y = np.meshgrid(xc, yc, indexing="ij")
        sx, sy = xe[-1] - xe[0], ye[-1] - ye[0]
        cell = min((xe[1] - xe[0]) / sx, (ye[1] - ye[0]) / sy)
        for row, ph in enumerate(("ph4", "ph7")):
            ax = axes[row, col]
            ids = [i for i, r in enumerate(runs) if r["target_ph"] == ph]
            late_ids = [i for i in ids if TIME[i][-1] > SPLIT_NS + 1e-6]
            ve, oke, _, tau = drift(ids, plane, xe, ye, window=(0.0, SPLIT_NS))
            vl, okl, _, _ = drift(late_ids, plane, xe, ye, window=(SPLIT_NS, np.inf))
            both = oke & okl
            if plane == "pca":
                u = S[f"{ph}_u"]
            else:
                u = np.log10(np.column_stack([D[f"u_{ph}_drmsd_rad"], D[f"u_{ph}_b1_dih_dev_deg"]]).astype(float))
            density_contours(ax, np.histogram2d(u[:, 0], u[:, 1], bins=(xe, ye))[0], xe, ye)
            # cosine between the two drifts, in axis-fraction space (the plotted geometry)
            ue, ul = ve / [sx, sy], vl / [sx, sy]
            cos = np.sum(ue * ul, axis=-1) / (np.linalg.norm(ue, axis=-1) * np.linalg.norm(ul, axis=-1))
            ratio = np.linalg.norm(vl, axis=-1) / np.linalg.norm(ve, axis=-1)
            for v, ok, colour, name in ((ve, oke, EARLY, f"pairs starting < {SPLIT_NS:g} ns ({len(ids)} runs)"),
                                        (vl, okl, LATE, f"pairs starting ≥ {SPLIT_NS:g} ns ({len(late_ids)} runs)")):
                w = np.hypot(v[..., 0] / sx, v[..., 1] / sy)
                ax.quiver(X[ok], Y[ok], (v[..., 0] / sx / w * sx)[ok], (v[..., 1] / sy / w * sy)[ok], color=colour,
                          angles="xy", scale_units="xy", scale=1.0 / (0.8 * cell), width=0.0032 if colour == LATE else 0.0026,
                          headwidth=4, headlength=4.5, alpha=1.0 if both.any() else 0.5, zorder=3 if colour == LATE else 2,
                          label=name)
            ax.scatter(X[both], Y[both], s=10, facecolor="none", edgecolor=INK2, lw=0.5, zorder=1)
            draw_basins(ax, plane, ph)
            ax.set_xlim(xe[0], xe[-1]); ax.set_ylim(ye[0], ye[-1])
            if P.get("log"):
                xt, yt = [0.5, 0.6, 0.8, 1.0, 1.5], [10, 15, 20, 30, 40, 60, 100]
                ax.set_xticks(np.log10(xt)); ax.set_xticklabels([f"{v:g}" for v in xt])
                ax.set_yticks(np.log10(yt)); ax.set_yticklabels([f"{v:g}" for v in yt])
            ax.set_xlabel(P["xlabel"]); ax.set_ylabel(P["ylabel"])
            c = cos[both]
            stats = (f"{both.sum()} shared bins: median cos {np.median(c):.2f}, cos > 0.5 in {np.mean(c > 0.5):.0%}, "
                     f"speed late/early median {np.median(ratio[both]):.2f}") if both.any() else "no shared bins"
            summary.append((plane, ph, stats))
            ax.set_title(f"run at pH {ph[2]}: {P['title']}, τ = {tau:g} ns\n{stats}", loc="left", fontsize=9.5, color=INK)
            ax.legend(loc="upper left", fontsize=8, frameon=True, facecolor=SURF, edgecolor="none", framealpha=0.85)
    fig.suptitle(f"Does the drift depend on time since seeding? Unit arrows: drift from pairs starting before (black) and "
                 f"after (orange) {SPLIT_NS:g} ns; circles = bins valid in both (≥{MIN_PAIRS} pairs from ≥{MIN_RUNS} runs "
                 f"each); grey = unbiased MD", x=0.01, ha="left", fontsize=11, color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.965))
    fig.savefig(f"{prefix}_early_late.png", dpi=130)
    for plane, ph, stats in summary:
        print(f"early/late {plane} {ph}: {stats}")
    print("wrote", f"{prefix}_early_late.png")
