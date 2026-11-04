"""Structural fingerprint of each MSM macrostate, to check the PCA basin labels against the HDX PUF definitions
(Moulick et al. 2015, pD 4: PUF1 = beta1, the beta1-alpha1 loop and the alpha3 C-terminus disordered;
PUF2 = in addition alpha1 and beta2 detached from the alpha2-alpha3 core).

Frames: every trajectory in cartesian_features.npz (seeded runs incl. extensions, unbiased MD), Ca of PrP 123-223
aligned to AF3 model 0; nm coordinates recovered as (z + centre) * scale with the stored PCA101 centre / scale.
Macrostate of a frame: PCA101 position (z @ loadings) within R of a basin centre (as msm_build.py).
Native contacts: Ca pairs |i - j| >= 4 closer than 0.8 nm in the 2L39 NMR mean (the PCA101 centre); a contact is
formed in a frame when the pair is within 1.2 x its native distance. Reported per frame and averaged per macrostate:
  Q per segment      fraction of the native contacts of the segment's residues that are formed
  Q between groups   fraction of native contacts formed between {alpha1, beta2 region} and the alpha2-alpha3 core,
                     and between beta1 and the rest
Plain frame averages (no MSM weights): structure conditional on the macrostate.

With an msm_report.json from a segment-MaxCal run (msm_build.py MSM_OPEN_OBS), each row also gives the macrostate's
free energy vs Folded from the MSM alone and after MaxCal (Bayesian medians; pH 7 = pH 4 correction carried over).

Usage: python macro_structure.py <cartesian_features.npz> <pca101_scores.npz> <basins_seed.json> <out_prefix> [R]
                                 [msm_report.json]
"""
import json
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

feat_path, scores_path, basins_path, prefix = sys.argv[1:5]
R = float(sys.argv[5]) if len(sys.argv) > 5 else 15.0
REPORT = json.load(open(sys.argv[6])) if len(sys.argv) > 6 else None
F = np.load(feat_path)
S = np.load(scores_path, allow_pickle=True)
RES = np.arange(123, 224)
SEGMENTS = [("β1 127–132", 127, 132), ("β1–α1 loop 133–143", 133, 143), ("α1 144–153", 144, 153),
            ("β2 region 154–167", 154, 167), ("α2 172–193", 172, 193), ("α2–α3 loop 194–199", 194, 199),
            ("α3 N 200–211", 200, 211), ("α3 C 212–223", 212, 223)]
GROUPS = [("α1+β2 ↔ α2–α3 core", (144, 167), (172, 223)), ("β1 ↔ rest", (127, 132), (133, 223)),
          ("β1–α1 loop ↔ α3", (133, 143), (200, 223))]
HDX_ROLE = {"β1 127–132": "PUF1", "β1–α1 loop 133–143": "PUF1", "α3 C 212–223": "PUF1", "α1 144–153": "PUF2",
            "β2 region 154–167": "PUF2"}

basins = json.load(open(basins_path))
CENTRES = {"F": [np.array(b["centre"]) for b in basins if b["label"] == "Folded"]}
for b in basins:
    if b["label"] != "Folded":
        CENTRES[b["label"].replace("-like", "L")] = [np.array(b["centre"])]
MACROS = ["F", "PUF1", "PUF2", "PUF3", "PUF3L", "I"]
LABEL = {"F": "Folded", "PUF1": "PUF1", "PUF2": "PUF2", "PUF3": "PUF3", "PUF3L": "PUF3-like", "I": "intermediate"}
# what each PCA basin is structurally (this analysis), with its original basin label
STRUCT = {"F": "Folded", "I": "intermediate (mixed; β1 partly off)", "PUF1": "α2–α3 loop disordered  [basin 'PUF1']",
          "PUF2": "β1 detached  [basin 'PUF2']", "PUF3": "β1 detached, far  [basin 'PUF3']",
          "PUF3L": "β1 detached + loop–α3 lost  [basin 'PUF3-like']"}
ROW_ORDER = ["F", "I", "PUF1", "PUF2", "PUF3", "PUF3L"]


def macro(pc):
    lab = np.full(len(pc), "I", dtype=object)
    for n, cs in CENTRES.items():
        for c in cs:
            lab[np.linalg.norm(pc - c, axis=1) < R] = n
    return lab


# native contacts from the 2L39 mean (identical centre / scale for both pH)
centre, scale = S["ph4_center"], S["ph4_scale"]
nat = (centre * scale).reshape(101, 3)
D0 = np.linalg.norm(nat[:, None] - nat[None], axis=-1)
I, J = np.triu_indices(101, 4)
keep = D0[I, J] < 0.8
I, J, d0 = I[keep], J[keep], D0[I, J][keep]
ri, rj = RES[I], RES[J]


def in_(r, a, b):
    return (r >= a) & (r <= b)


seg_masks = [in_(ri, a, b) | in_(rj, a, b) for _, a, b in SEGMENTS]
grp_masks = [(in_(ri, *g1) & in_(rj, *g2)) | (in_(rj, *g1) & in_(ri, *g2)) for _, g1, g2 in GROUPS]
cols = [s[0] for s in SEGMENTS] + [g[0] for g in GROUPS]
masks = seg_masks + grp_masks

acc = {ph: {m: [np.zeros(len(cols)), 0] for m in MACROS} for ph in ("ph4", "ph7")}
for k in F.files:
    if k == "feature_names":
        continue
    ph = k.split("__")[0]
    z = F[k].astype(np.float64)
    lab = macro(z @ S[f"{ph}_loadings"])
    X = ((z + centre) * scale).reshape(len(z), 101, 3)
    formed = np.linalg.norm(X[:, I] - X[:, J], axis=-1) < 1.2 * d0          # (frames, contacts)
    q = np.column_stack([formed[:, m].mean(axis=1) for m in masks])
    for m in MACROS:
        sel = lab == m
        if sel.any():
            acc[ph][m][0] += q[sel].sum(axis=0); acc[ph][m][1] += int(sel.sum())

Q = {ph: {m: (v[0] / v[1] if v[1] else np.full(len(cols), np.nan)) for m, v in acc[ph].items()} for ph in acc}
N = {ph: {m: acc[ph][m][1] for m in MACROS} for ph in acc}
out = {"radius": R, "columns": cols, "native_contacts": int(len(d0)),
       "Q": {ph: {m: [float(x) for x in Q[ph][m]] for m in MACROS} for ph in Q},
       "Q_rel_F": {ph: {m: [float(x) for x in Q[ph][m] / Q[ph]["F"]] for m in MACROS} for ph in Q},
       "frames": N}
json.dump(out, open(f"{prefix}.json", "w"), indent=1)

INK, INK2, SURF = "#0b0b0b", "#52514e", "#fcfcfb"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "figure.facecolor": SURF, "axes.facecolor": SURF,
                     "axes.edgecolor": INK2, "xtick.color": INK2, "ytick.color": INK2})
def dg_text(ph, m):
    if REPORT is None or m == "F":
        return ""
    seg = REPORT["ph"][ph]["segment_maxcal"]
    pre = (REPORT["ph"][ph]["dG_ci95"] if ph == "ph4" else seg["prior"]["dG"]).get(m)
    post = seg["hdx" if ph == "ph4" else "transfer_hdx"]["dG"].get(m)
    if pre is None or post is None:
        return ""
    return f"{pre[1]:.1f} → {post[1]:.1f}"


fig, axes = plt.subplots(1, 2, figsize=(21, 6.6), sharey=True, gridspec_kw=dict(wspace=0.32))
for ax, ph in zip(axes, ("ph4", "ph7")):
    M = np.array([Q[ph][m] / Q[ph]["F"] for m in ROW_ORDER])
    im = ax.imshow(M, cmap="RdBu", vmin=0.4, vmax=1.6, aspect="auto")
    for (a, b), v in np.ndenumerate(M):
        ax.text(b, a, f"{v:.2f}", ha="center", va="center", fontsize=7.5,
                color="w" if abs(v - 1) > 0.4 else INK)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels([f"{c}\n[HDX {HDX_ROLE[c]}]" if c in HDX_ROLE else c for c in cols], rotation=40, ha="right",
                       fontsize=7.5)
    ax.axvline(len(SEGMENTS) - 0.5, color=INK, lw=1.2)
    ax.set_yticks(range(len(ROW_ORDER)))
    ax.set_yticklabels([STRUCT[m] for m in ROW_ORDER], fontsize=8.5)
    if REPORT is not None:
        x0 = len(cols) - 0.5 + 0.25
        ax.text(x0, -0.55, "ΔG (kcal/mol)\nMSM → MaxCal", fontsize=7.5, color=INK2, ha="left", va="bottom")
        for k, m in enumerate(ROW_ORDER):
            ax.text(x0, k, dg_text(ph, m) or "—", fontsize=9, color=INK, ha="left", va="center", clip_on=False)
    for k in range(1, len(ROW_ORDER)):
        ax.axhline(k - 0.5, color=SURF, lw=1.5)
    ax.set_title(f"run at pH {ph[2]}", loc="left", fontsize=10.5, color=INK, fontweight="bold")
fig.colorbar(im, ax=axes, shrink=0.8, pad=0.08, label="native-contact fraction relative to Folded")
fig.suptitle(f"What each macrostate is: native Cα contacts kept per segment (left of the line) and between structural "
             f"groups (right), relative to Folded (2L39 contacts, {len(d0)} pairs; PCA101 circles r = {R:g}; all frames)"
             + ("\nrows: ΔG vs Folded from the MSM alone → after MaxCal (fitted at pH 4 to HDX "
                + ", ".join(f"{ {'b1_rest': 'β1 opening', 'b2_seg': 'β2-region opening'}.get(c, c)} {t['dG']:g} ± {t['sd']:g}"
                            for c, t in REPORT["ph"]["ph4"]["segment_maxcal"]["targets"].items())
                + " kcal/mol; pH 7 = same correction); [HDX …] under a column = the HDX PUF that segment belongs to"
                if REPORT else ""),
             x=0.01, y=1.04, ha="left", fontsize=10.5, color=INK)
fig.savefig(f"{prefix}.png", dpi=130, bbox_inches="tight")
print(f"{len(d0)} native contacts; wrote {prefix}.png, {prefix}.json")
for ph in ("ph4", "ph7"):
    print(ph)
    for m in MACROS:
        print(f"  {m:6s} {N[ph][m] / 1e4:6.2f} us  " + "  ".join(f"{v:.2f}" for v in Q[ph][m] / Q[ph]["F"]))
print("columns:", cols)
