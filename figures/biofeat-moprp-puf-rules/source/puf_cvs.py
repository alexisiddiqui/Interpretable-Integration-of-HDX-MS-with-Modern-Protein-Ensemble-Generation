"""Per-frame paper-derived PUF collective variables for the MoPrP seeded and unbiased runs.

Contacts as in macro_structure.py / segment_contacts.py: Ca pairs |i - j| >= 4 closer than 0.8 nm in the 2L39 NMR mean
(the PCA101 centre), formed within 1.2 x the native distance. Segments follow Moulick et al. 2015 (JBC 290, 25229).
Rigid-body measures are added because a helix can move while its contacts stay inside the 1.2 x tolerance: each frame
is superposed on the disulfide-proximal alpha2-alpha3 core (175-187, 201-216), and a segment's RMSD in that frame (core-fit) is compared with its
RMSD after superposing the segment on itself (self-fit). Displaced = large core-fit, small self-fit. Disordered = large self-fit.

Usage: puf_cvs.py <cartesian_features.npz> <pca101_scores.npz> <msm_weights.npz> <out.npz>
"""
import sys
import numpy as np

feat, scores, weights, out = sys.argv[1:5]
F = np.load(feat); S = np.load(scores, allow_pickle=True); W = np.load(weights)
RES = np.arange(123, 224)
centre, scale = S["ph4_center"], S["ph4_scale"]
nat = (centre * scale).reshape(101, 3)
D0 = np.linalg.norm(nat[:, None] - nat[None], axis=-1)
I, J = np.triu_indices(101, 4)
keep = D0[I, J] < 0.8
I, J, d0 = I[keep], J[keep], D0[I, J][keep]
ri, rj = RES[I], RES[J]
inn = lambda r, a, b: (r >= a) & (r <= b)
touch = lambda a, b: inn(ri, a, b) | inn(rj, a, b)
btw = lambda g1, g2: (inn(ri, *g1) & inn(rj, *g2)) | (inn(rj, *g1) & inn(ri, *g2))
within = lambda a, b: inn(ri, a, b) & inn(rj, a, b)
CORE = (172, 223)
SETS = {
    "b1_rest": btw((127, 132), (133, 223)) | btw((127, 132), (123, 126)),   # segment_contacts.py
    "a1b2_core": btw((144, 167), CORE),                                     # segment_contacts.py
    "b2_seg": touch(154, 167),                                              # segment_contacts.py
    "loop_a3": btw((133, 143), (200, 223)),                                 # segment_contacts.py
    "loop": touch(133, 143),
    "loop_nob1": touch(133, 143) & ~btw((133, 143), (127, 132)),
    "a3C212": touch(212, 223),
    "a3C217": touch(217, 223),
    "a3C_int": within(212, 223),
    "a1": touch(144, 153),
    "a1_int": within(144, 153),
    "a1_core": btw((144, 153), CORE),
    "a1N": touch(144, 148),
    "a1N_core": btw((144, 148), CORE),
    "a1C": touch(149, 153),
    "a1C_core": btw((149, 153), CORE),
    "a1_b1loop": btw((144, 153), (127, 143)),
    "b2_core": btw((154, 167), CORE),
    "b2_b1": btw((154, 167), (127, 132)),
    "b2_nob1": touch(154, 167) & ~btw((154, 167), (127, 132)),
    "core_int": within(172, 216),
}
RIG = {"b1": (127, 132), "loop": (133, 143), "a1": (144, 153), "a1N": (144, 148), "a1C": (149, 153), "b2": (154, 167),
       "a3C": (217, 223), "unit": (144, 167)}
coreidx = np.flatnonzero(inn(RES, 175, 187) | inn(RES, 201, 216))


def kabsch(P, Q):
    """Rotation and translations superposing frames P (n, m, 3) on reference Q (m, 3)."""
    pc, qc = P.mean(1, keepdims=True), Q.mean(0)
    H = np.einsum("nmi,mj->nij", P - pc, Q - qc)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(U @ Vt))
    D = np.zeros_like(H); D[:, 0, 0] = 1; D[:, 1, 1] = 1; D[:, 2, 2] = d
    return U @ D @ Vt, pc, qc


rows = {ph: [] for ph in ("ph4", "ph7")}; rig = {ph: [] for ph in rows}; pcs = {ph: [] for ph in rows}
src = {ph: [] for ph in rows}; run = {ph: [] for ph in rows}
keys = {ph: [] for ph in rows}
for k in F.files:
    if k == "feature_names":
        continue
    ph, s, *rest = k.split("__")
    z = F[k].astype(np.float64)
    X = ((z + centre) * scale).reshape(len(z), 101, 3)
    formed = np.linalg.norm(X[:, I] - X[:, J], axis=-1) < 1.2 * d0
    rows[ph].append(np.column_stack([formed[:, m].mean(1) for m in SETS.values()]))
    R, pc, qc = kabsch(X[:, coreidx], nat[coreidx])
    Y = (X - pc) @ R + qc
    cols = [np.sqrt(((Y[:, coreidx] - nat[coreidx]) ** 2).sum(-1).mean(1))]
    for a, b in RIG.values():
        ix = np.flatnonzero(inn(RES, a, b))
        cols.append(np.sqrt(((Y[:, ix] - nat[ix]) ** 2).sum(-1).mean(1)))
        R2, p2, q2 = kabsch(X[:, ix], nat[ix])
        cols.append(np.sqrt((((X[:, ix] - p2) @ R2 + q2 - nat[ix]) ** 2).sum(-1).mean(1)))
    rig[ph].append(np.column_stack(cols))
    pcs[ph].append((z @ S[f"{ph}_loadings"])[:, :2])
    src[ph] += [s] * len(z); run[ph] += [len(keys[ph])] * len(z); keys[ph].append(k)

rig_names = ["core"] + [f"{n}_{t}" for n in RIG for t in ("corefit", "selffit")]
save = dict(set_names=np.array(list(SETS)), n_contacts=np.array([int(m.sum()) for m in SETS.values()]), rig_names=np.array(rig_names))
for ph in rows:
    q, r, p = np.vstack(rows[ph]), np.vstack(rig[ph]), np.vstack(pcs[ph])
    x = W[f"{ph}_x"]
    err = np.abs(p - x[:, :2]).max()
    print(f"{ph}: frames {len(q)} vs weights {len(x)}; max |PC difference| in file order {err:.3g}; "
          f"sum w_prior {W[f'{ph}_w_prior'].sum():.4f}, sum w_maxcal {W[f'{ph}_w_maxcal'].sum():.4f}")
    save.update({f"{ph}_q": q.astype(np.float32), f"{ph}_rig": r.astype(np.float32), f"{ph}_x": x, f"{ph}_pc": p.astype(np.float32),
                 f"{ph}_wp": W[f"{ph}_w_prior"], f"{ph}_wm": W[f"{ph}_w_maxcal"], f"{ph}_src": np.array(src[ph]), f"{ph}_run": np.array(run[ph])})
np.savez_compressed(out, **save)
print(dict(zip(SETS, [int(m.sum()) for m in SETS.values()])))
