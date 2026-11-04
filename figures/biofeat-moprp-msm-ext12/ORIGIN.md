# biofeat-moprp-msm-ext12

Reference figure set for the MoPrP stationary MSMs built from the ext12 basin-seeded unbiased trajectories (24 × 20 ns + 120 × 100 ns, 12.48 μs). It is not yet planned as a thesis figure. Protocol in `kb/experiments/bf-moprp.md`.

- Main model: Cartesian Cα PCA on the 101 HDX residues (10 PCs, fitted on unbiased MD), direct k-means, K = 100, lag 5 ns. The macrostate circles (F, PUF1, PUF2, PUF3, PUF3L) are the historical PCA basin labels; `macro_structure_ext12_maxcal2` gives what each one is structurally.
- `msm_ext12_main_fes`: stationary free energy at pH 4 and pH 7, PCA plane and JAX-ENT dihedral plane.
- `msm_ext12_mfpt`: opening (F to X) and closing (X to F) mean first-passage times, both pH, log scale.
- `msm_ext12_dG_compare`: PUF ΔG against Folded across seven MSM constructions (Bayesian 95 %), HDX ΔG_op dashed.
- `msm_ext12_ck`, `msm_ext12_main_its`, `msm_ext12_main_summary`: Chapman–Kolmogorov test, implied timescales and ΔG summary of the main model.
- `macro_structure_ext12_maxcal2` (+ `.json`): native Cα contact fraction per segment and between groups for each macrostate, relative to Folded, with ΔG from the MSM alone and after two-constraint MaxCal.
- `segment_maxcal_ext12_dGop`, `segment_maxcal_ext12_states`: segment-opening MaxCal free energies and macrostate free energies with opening and closing MFPTs.
- `fes_maxcal2_k100_lag5_pca`: free energy before and after the two-constraint MaxCal (β1 opening 2.2 ± 0.2, β2-region opening 3.1 ± 0.5 kcal mol⁻¹ at pH 4, same correction at pH 7), PCA plane.
- Source: local mirror `~/Coulson-Chemistry/moprp_results/` (copied 2026-11-03, byte-identical); the Coulson originals are under `moprp-paired-50ns-20260925-v1/seeded_apo/` on Coulson-Chemistry. SHA-256 prefixes: `7b7a7e7e` msm_ext12_main_fes, `b320ccd8` msm_ext12_mfpt, `182baae6` msm_ext12_dG_compare, `482411ec` msm_ext12_ck, `75ca7c66` msm_ext12_main_its, `992f914d` msm_ext12_main_summary, `49051fba` macro_structure_ext12_maxcal2, `1d0aaf8b` segment_maxcal_ext12_dGop, `738f04af` segment_maxcal_ext12_states, `1c047aff` fes_maxcal2_k100_lag5_pca.
- Code: `source/msm_build.py` (models and MaxCal), `source/msm_plots.py`, `source/macro_structure.py`, `source/segment_maxcal_plots.py`, `source/fes_maxcal_plots.py`, copied from `~/Coulson-Chemistry/moprp_seeded/`. `source/msm_report_ext12seg2_q0.5_k100_lag5.json` is the report of the selected two-constraint model (`msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag5`), with raw transition counts, MFPTs and MaxCal summaries.
