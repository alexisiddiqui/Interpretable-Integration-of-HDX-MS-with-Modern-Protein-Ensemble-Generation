# biofeat-moprp-paths-ext12

Reference figure set for the trajectories of the MoPrP basin-seeded unbiased runs, per starting basin and pooled. It is not yet planned as a thesis figure. Protocol in `kb/experiments/bf-moprp.md`.

- `seeded_paths_ext12_pca`: paths of the 120 extended seeds on the 101-HDX-residue Cartesian PCA plane, one panel per source basin (pH 4 #1 Folded, #2 β1-detached arm near, #3 β1-detached arm far; pH 7 #1 Folded, #2 core-distorted lobe, #3 detached β1–α1 set) and target pH (rows). Greens are the extended seeds (running mean 1 ns; circle start, diamond 20 ns, square last frame), yellow the 20 ns short runs of the same basin and pH, light grey the unbiased MD at the target pH.
- `seeded_paths_ext12_dih`: the same on the JAX-ENT dihedral plane (dRMSD against 2L39, β1 dihedral deviation).
- `cart_pca_unbiasedfit_ext12`: Cartesian PCA (2L39 centring and scaling) fitted on the unbiased MD, with all ext12 seeded runs projected.
- Source: local mirror `~/Coulson-Chemistry/moprp_results/` (copied 2026-11-03, byte-identical). SHA-256 prefixes: `b29a4e9b` seeded_paths_ext12_pca, `01bf77e0` seeded_paths_ext12_dih, `e98f26fd` cart_pca_unbiasedfit_ext12.
- Code: `trajectory_paths.py` and `torsion_pca.py` (`cart_pca_unbiasedfit_ext12`) on Coulson under `moprp-paired-50ns-20260925-v1/seeded_apo/`; they are not in the local mirror.
- Relabelled on 2026-11-08 on Coulson `comp1400` (job 784309) with the structural state names. The old "PUF1" circle is the core-distorted lobe, "PUF2" the β1-detached arm, near, "PUF3" the β1-detached arm, far, and "PUF3-like" the detached β1–α1 set. Each figure was redrawn by its original script with its original arguments, and `../biofeat-moprp-puf-rules/source/relabel_run.py` replaces text only, at save time, from `../biofeat-moprp-puf-rules/source/relabel_map.json`; `../biofeat-moprp-puf-rules/source/moprp-relabel.sbatch` lists every command. HDX labels and candidate names are unchanged.
