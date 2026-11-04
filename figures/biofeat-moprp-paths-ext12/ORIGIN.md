# biofeat-moprp-paths-ext12

Reference figure set for the trajectories of the MoPrP basin-seeded unbiased runs, per starting basin and pooled. It is not yet planned as a thesis figure. Protocol in `kb/experiments/bf-moprp.md`.

- `seeded_paths_ext12_pca`: paths of the 120 extended seeds on the 101-HDX-residue Cartesian PCA plane, one panel per source basin (pH 4 Folded, PUF2, PUF3; pH 7 Folded, PUF1, PUF3-like) and target pH (rows). Greens are the extended seeds (running mean 1 ns; circle start, diamond 20 ns, square last frame), yellow the 20 ns short runs of the same basin and pH, light grey the unbiased MD at the target pH.
- `seeded_paths_ext12_dih`: the same on the JAX-ENT dihedral plane (dRMSD against 2L39, β1 dihedral deviation).
- `cart_pca_unbiasedfit_ext12`: Cartesian PCA (2L39 centring and scaling) fitted on the unbiased MD, with all ext12 seeded runs projected.
- Source: local mirror `~/Coulson-Chemistry/moprp_results/` (copied 2026-11-03, byte-identical). SHA-256 prefixes: `4ea29e7b` seeded_paths_ext12_pca, `5bd31d0a` seeded_paths_ext12_dih, `bb543904` cart_pca_unbiasedfit_ext12.
- Code: the plotting script for these three files is not in the local mirror; it is on Coulson under `moprp-paired-50ns-20260925-v1/seeded_apo/`.
