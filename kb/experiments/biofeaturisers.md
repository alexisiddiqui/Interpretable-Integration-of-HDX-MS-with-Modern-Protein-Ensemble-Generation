---
project: biofeaturisers
local_repositories:
  - projects/3-BioFeaturisers/code
  - projects/3-BioFeaturisers/meta-diffusion
locations:
  - machine: coulson
    root: /u/oc/lina4225
  - machine: pegasus
    root: /opig-shared/projects/hussian-simulation_hdx
  - machine: isambard
    root: /scratch/u6xq/hussain.u6xq
experiments:
  - id: bf-moprp
    status: primary
    question: null
    locations:
      - machine: coulson
        root: /u/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns
        runs: [moprp-reference-20260925-v1, moprp-reference-ph7-20260925-v1, moprp-paired-50ns-20260925-v1]
    authoritative_location: coulson
    status_command: null
    # Metadynamics (MI+PB, pH 4 and 7), paths relative to moprp-paired-50ns-20260925-v1/figures/
    # Local mirror: ~/Coulson-Chemistry/moprp_results/ (copied 2026-10-22; the mirror is the only home of the pca_mi_cartesian_101 and msm_ext6_* files)
    artifacts:
      - figures/pca_mi_cartesian_mi-v2.png          # unbiased / MI / MI+PB / weighted, both pH, 109 residues
      - moprp_results/pca_mi_cartesian_101_mi-v2.png  # same on the 101 HDX residues, basins circled (local mirror only)
      - figures/pca_mmpb_final_bias_mi-v2.png       # MI+PB run-time weights vs final PB bias, 100-250 ns
      - figures/pca_mi_cartesian_halves_mi-v2.png   # first vs second half convergence
      - figures/basin_frames/repo_run/basins.png    # basin structures
      # MSM (6 x 100 ns + 6 x 20 ns seeded APO runs per basin and pH), under seeded_apo/msm/ or the local mirror
      - moprp_results/msm_ext6_main_fes.png         # main model stationary free energy, pH 4 and 7 (local mirror only)
      - moprp_results/msm_ext6_dG_compare.png       # PUF dG vs Folded, 7 models, both pH, HDX dG_op dashed (local mirror only)
      - moprp_results/msm_ext6_ck.png               # Chapman-Kolmogorov test, main model (local mirror only)
      - moprp_results/msm_ext6_mfpt.png             # opening / closing MFPTs, main model (local mirror only)
      - seeded_apo/msm/ext6_cartpca10_all-kmall_k100_lag5/{msm_fes,msm_its,msm_summary}.png  # main model on Coulson
    figures: []
  - id: bf-gpu-stack-campaigns
    question: null
    locations:
      - machine: coulson
        root: /u/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns
        runs: [trpv4-fastpath-20260917-v1..v10, plumed-stride-multigpu-20260915..16, plumed-callback-optimisation-20260916, bpti-mi-scaling-20260915]
    authoritative_location: coulson
    status_command: null
    artifacts: []
    figures: []
  - id: bf-bpti-pb-mi
    question: null
    locations:
      - machine: pegasus
        root: /opig-shared/projects/hussian-simulation_hdx/_runtime/BioFeaturisers
        runs: [bpti_production, bpti_matched_controls, bpti_rate_tuning, single-cv-pb, sigma-stride-pilot, basin-diagnostics, bpti_multigpu, bpti_reverse_vjp_benchmark, ada_mps_benchmark]
    authoritative_location: pegasus
    status_command: null
    artifacts: []
    figures: []
  - id: bf-teaa
    status: primary
    question: Can a target-free hinge bias plus HDX guidance and MaxEnt reweighting recover the 40:60 open:closed populations of a synthetic TeaA HDX target from Boltz-2, with no MD reference in any run?
    # Protocol: bf-teaa.md. Results log and figures live in the MaxENT-FK repo (branch teaa-iso-frame-uptake, results commit 89f183c).
    locations:
      - machine: isambard
        root: /scratch/u6xq/hussain.u6xq/_runtime/runs/TeaA_sdedit
        runs: [cvf_ung_noise_s42_n50, metad_r1..r4_s42_n50, cont_c1..c8_s101..108_n50, refa025_k1..5_s201..205_n49, ctl_k1..5, ung_noise_s43..45, metad43_r1..r4_s43_n50, cont43_c1..c8_s301..308_n50, refa025s43_k1..5_s401..405, ctls43_k1..5]
      - machine: isambard
        root: /home/u6xq/hussain.u6xq/_runtime/analysis/TeaA_cv
        runs: []
    authoritative_location: isambard
    status_command: null
    # Paths relative to MaxENT-FK/examples/TeaA/ unless under the analysis root above
    artifacts:
      - RESULTS.md
      - results/figures/pca_logdensity.png      # CA PCA log-density, MD states against generated ensembles
      - results/figures/rmsd_lobeII.png         # lobe-II RMSD landscape
      - results/figures/rmsd_allCA.png          # all-CA RMSD landscape
      - results/figures/summary_1d.png          # PC1 densities
      - sweep_a0.25_blind.csv                   # per-structure MaxEnt weights, seed 42 (analysis root)
      - sweep_s43_a0.25_blind.csv               # seed 43 (analysis root)
      - metad_history.csv                       # bias deposits, seed 42 (analysis root); metad_history_s43.csv for seed 43
    figures: []
---

# BioFeaturisers / MaxENT-FK experiments

The BPTI metainference and metadynamics experiments are on Pegasus-Gate, the MoPrP runs and the GPU-stack campaigns are on Coulson-Chemistry, and the TeaA metadiffusion experiment is on Isambard (protocol in [bf-teaa.md](bf-teaa.md)). Access requirements are recorded in [machines.yaml](machines.yaml).

Observed 2026-10-29; Isambard re-observed 2026-11-01. The machines hold different experiments, not replicas. Run output is under `_runtime/BioFeaturisers/` on Coulson and Pegasus; the repositories sit beside it.

- **Coulson:** `BioFeaturisers/` (branch `moprp-basin-figures`, clean) and `JAX-ENT/` (branch `pymol-rmsd-to-reference`, clean) in the root. The MoPrP runs (the primary BioFeaturisers result), the GROMACS/PLUMED-JAX GPU stack and the TRPV4 and PLUMED-stride campaigns are under `_runtime/BioFeaturisers/cuda-86/campaigns/`. `BioFeaturisers/benchmarking/{SAXS,SASA,foldbench,precision}` holds the benchmark code and handoffs. The MoPrP seed and analysis jobs (`moprp-seed-*`, `moprp-msm*`, `moprp-torpca`) ran in the last ten days.
- **Pegasus:** the BPTI MI/PB-rate campaigns are under `_runtime/BioFeaturisers/`, with their sbatch scripts in `_submission_scripts/BioFeaturisers/{BPTI,RoRg}`. The RoRg (`rorg_apo`, `rorg_sr19355`) and CaM-CDZ runs sit beside them and are not recorded as experiments. `projects/BioFeaturisers/` is empty. `/opig-shared` was 100% full (159G free). No jobs in the queue.

- **Isambard:** `BioFeaturisers/` (branch `dev-PLUMED`, 15 uncommitted files), `MaxENT-FK/` (branch `teaa-iso-frame-uptake`, observed 2026-11-01 with `predict.py` and `run_config.py` modified, two commits ahead of origin, and an untracked 4.3 GB `core` file) and a `bioemu2/` clone are in the root. Run output is under `_runtime/runs/` (TeaA, HOIP and BPTI runs), with the sbatch sets in `_submission/` (about 20 `maxent-bioemu2-*` sets and `bpti-metadiffusion-torsion-v2`). The TeaA analysis scripts and score dumps are in `~/_runtime/analysis/`, and `~/_submit/teaa_sdedit.sbatch` launches the runs. `~/MaxENT-FK` is an older non-git copy in the home directory. The queue was empty. Only TeaA is recorded as an experiment; the HOIP, BPTI and `maxent-bioemu2-*` runs are not.

Question, status command, artifacts and figure IDs are not yet recorded. Follow the [experiment entry format](README.md#experiment-entries) when recording individual experiments.
