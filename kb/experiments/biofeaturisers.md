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
  - id: bf-rorg
    status: in progress, not promising
    question: null
    locations:
      - machine: pegasus
        root: /opig-shared/projects/hussian-simulation_hdx/_runtime/BioFeaturisers
        runs: [rorg_apo, rorg_sr19355, rorg_analysis, rorg-tools]
    authoritative_location: pegasus
    status_command: null
    artifacts: []
    figures: []
  - id: bf-cam-cdz
    status: in progress
    question: null
    locations:
      - machine: pegasus
        root: /opig-shared/projects/hussian-simulation_hdx/_runtime/BioFeaturisers
        runs: [cam-cdz-confined-20261025, cam-cdz-q15-20261027]
    authoritative_location: pegasus
    status_command: null
    artifacts: []
    figures: []
---

# BioFeaturisers / MaxENT-FK experiments

The BPTI metainference and metadynamics experiments are on Pegasus-Gate. MaxENT-FK is not yet working, so isambard holds development runs only; Coulson-Chemistry holds the earlier GPU-stack campaigns. Access requirements are recorded in [machines.yaml](machines.yaml).

Observed 2026-10-29. The machines hold different experiments, not replicas. Run output is under `_runtime/BioFeaturisers/` on both; the repositories sit beside it.

- **Coulson:** `BioFeaturisers/` (branch `moprp-basin-figures`, clean) and `JAX-ENT/` (branch `pymol-rmsd-to-reference`, clean) in the root. The MoPrP runs (the primary BioFeaturisers result), the GROMACS/PLUMED-JAX GPU stack and the TRPV4 and PLUMED-stride campaigns are under `_runtime/BioFeaturisers/cuda-86/campaigns/`. `BioFeaturisers/benchmarking/{SAXS,SASA,foldbench,precision}` holds the benchmark code and handoffs. The MoPrP seed and analysis jobs (`moprp-seed-*`, `moprp-msm*`, `moprp-torpca`) ran in the last ten days.
- **Pegasus:** the BPTI MI/PB-rate campaigns, RoRg (`rorg_apo`, `rorg_sr19355`), and the CaM-CDZ runs are under `_runtime/BioFeaturisers/`; their sbatch scripts are in `_submission_scripts/BioFeaturisers/{BPTI,RoRg}`. `projects/BioFeaturisers/` is empty. `/opig-shared` was 100% full (159G free). No jobs in the queue.

- **Isambard:** `BioFeaturisers/` (branch `dev-PLUMED`, 15 uncommitted files), `MaxENT-FK/` (branch `teaa-iso-frame-uptake`, 7 uncommitted files) and a `bioemu2/` clone are in the root. Run output is under `_runtime/runs/` (TeaA, HOIP and BPTI runs), with the sbatch sets in `_submission/` (about 20 `maxent-bioemu2-*` sets and `bpti-metadiffusion-torsion-v2`). `~/MaxENT-FK` is an older non-git copy in the home directory. The queue was empty. MaxENT-FK is not yet working, so none of the Isambard runs are recorded as experiments.

Question, status command, artifacts and figure IDs are not yet recorded. Follow the [experiment entry format](README.md#experiment-entries) when recording individual experiments.
