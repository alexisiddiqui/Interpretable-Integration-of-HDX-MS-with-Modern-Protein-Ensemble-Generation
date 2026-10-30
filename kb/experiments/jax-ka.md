---
project: jax-ka
local_repositories:
  - projects/4-jax-Ka/code
locations:
  - machine: isambard
    root: /scratch/u6xq/hussain.u6xq
  - machine: coulson
    root: /u/oc/lina4225
experiments:
  - id: jaxka-training
    question: null
    locations:
      - machine: isambard
        root: /scratch/u6xq/hussain.u6xq/jax-Ka/experiments
        runs: [1_benchmark, 1b_noise_floor, 2_finetune, 3_paired_complex, 4_backbone, 5_ligands]
      - machine: isambard
        root: /scratch/u6xq/hussain.u6xq/_runtime/jax-Ka
        runs: ["ogqt-benchmark-*", "ogqt-heterogeneous-*", "ogqt-cache-validation-*", 6sc6-gradient-7349322, 6sc6-abc-7349803]
      - machine: isambard
        root: /scratch/u6xq/hussain.u6xq/_submission
        runs: ["gqt-*", "teacher-*", "nonlinear-*", "pkpdb-*", "coupled-titration-*", "residue-weights-*", "ph-edges-*", "site-edges-*"]
    authoritative_location: isambard
    status_command: null
    artifacts: []
    figures: []
  - id: jaxka-data-cleaning
    question: Which site labels stay trustworthy after components are stripped and unmodelled regions are masked, and how many sites and complexes survive in each split?
    locations:
      - machine: coulson
        root: /u/oc/lina4225/jax-Ka/experiments
        runs: [1_benchmark/curation, experimental_pilot]
      - machine: coulson
        root: /u/oc/lina4225/_runtime/jax-Ka/pkabench
        runs: [audits, caches, manifests, exports, overlays]
    authoritative_location: coulson
    status_command: null
    # Paths are relative to the pkabench runtime root on coulson unless marked isambard. Isambard holds copies of pretraining/ and training/pool-v4 only.
    # Plots (PNG/PDF/SVG) are staged with checksums in .experiments/jaxka-data-cleaning/ (pulled 2026-10-30).
    artifacts:
      - audits/buffer-propka-v2/plots/all_buffers_error_vs_distance.png      # buffers, PROPKA, 26 complexes
      - audits/buffer-propka-v2/plots/error_vs_distance.png                  # one buffer removed at a time
      - audits/buffer-propka-v2/plots/error_vs_sasa.png
      - audits/buffer-propka-v2/plots/error_vs_exposure.png
      - audits/buffer-propka-v2/plots/retained_sites_vs_radius.png
      - audits/glycan-propka-ccd-v1/plots/error_vs_distance.png              # glycans, PROPKA with CCD typing, 29 complexes
      - audits/glycan-propka-ccd-v1/plots/error_vs_sasa.png                  # glycan's own SASA, not protein shielding
      - audits/glycan-propka-ccd-v1/plots/error_vs_exposure.png
      - audits/glycan-propka-ccd-v1/plots/retained_sites_vs_radius.png
      - audits/propka-components-v1/plots/sasa_vs_change.png                 # ligands (17) and metals (11), against exposure only; ligand typing flawed, see decision note
      - audits/radial-error-v2-nearcomplete/plots/error_vs_distance.png      # gaps, PypKa, 23 complexes
      - audits/radial-error-v2-nearcomplete/plots/sites_excluded_vs_radius.png
      - audits/radial-error-v2-nearcomplete/anchor-analysis-v2/anchor_error.png
      - audits/radial-error-v2-nearcomplete/anchor-analysis-v2/anchor_retention.png
      - audits/radial-error-v2-nearcomplete/internal-anchor-analysis-v1/internal_anchor_error.png
      - audits/radial-long-tails-v1/anchor-analysis-v2/anchor_error.png
      - audits/label-overlap-v1/hist_pkai_train_mask.png
      - audits/shift-by-environment-v1/shift_by_environment.png
      - campaigns/production-nojax-v1/report_figures/interface_mae.png       # pKAI closer to PypKa than pKAI+
      - campaigns/production-nojax-v1/report_figures/interface_coverage.png
      - isambard:audits/atlas-split-v1/atlas-phate-split.png                 # not yet confirmed as the pool split
      - isambard:audits/atlas-phate-check-v1/nearest-training-audit.png
      - audits/pinder-longgap-v1                                             # pKAI gap calibration, tables only
      - audits/pinder-exp-leak-v1
      - campaigns/coordinate-pool-inclusive-v1/rejections.parquet            # rejection codes, not yet plotted
      - universe/structural-freeze-v1
      - pretraining/pinder-pkai-v1
      - pretraining/pkpdb-full-v1
      - training/pool-v4
    figures: []
  - id: jaxka-anm-augmentation
    question: null
    locations:
      - machine: coulson
        root: /u/oc/lina4225/_runtime/jax-Ka/anm-pilot-v1
      - machine: coulson
        root: /u/oc/lina4225/jax-Ka-augmentation-main
    authoritative_location: coulson
    status_command: null
    artifacts: []
    figures: []
---

# jax-Ka experiments

Training is on isambard and data cleaning is on Coulson-Chemistry. Access requirements are recorded in [machines.yaml](machines.yaml).

Observed 2026-10-29.

- **Coulson:** three checkouts of `alexisiddiqui/jax-Ka` in the root: `jax-Ka/` (branch `benchmark`, 107 uncommitted files, last commit 2026-10-13), `jax-Ka-ph/` (`ph-aux`, clean) and `jax-Ka-augmentation-main/` (`main`, clean). Their `experiments/` layout matches `projects/4-jax-Ka/code/experiments/`. Run output sits in `_runtime/jax-Ka/` (`anm-pilot-v1`, `pkabench`, `logs`). The `anm-*` jobs (feature-cache pools, ten-mode runs) and the `pkai-scan` array were queued or running in the last ten days.
- **Isambard:** `jax-Ka/` (branch `main`, clean, last commit 2026-10-21) and `jax-Ka-crop/` (a production-crop worktree), with the same `experiments/` layout. Run output is in `_runtime/jax-Ka/` (`ogqt-*`, `6sc6-*`, `pkabench`, `anm-pilot-v1`). The `_submission/` sets from 2026-10-27 to 2026-10-29 (`gqt-*`, `teacher-*`, `nonlinear-*`, `pkpdb-*`) are the most recent GQT work. `_wt/` holds worktrees (`ph-aux`, `pkai-*`). The queue was empty.

Training and the benchmark experiments run on Isambard, which holds most of the experiments. Data cleaning (curation, the experimental admission and inventory scripts, the pKa benchmark caches and manifests) was done on Coulson. The two machines hold checkouts of the same repository, so a result's code state has to be read from the machine that produced it.

The `jax-Ka` checkout on Coulson has uncommitted changes, so any result produced from it needs the code state recorded before it is used. The data-cleaning entry records its question and artifacts; the other entries do not yet. Decisions on the masking noise targets and the data pipeline record are in `kb/decisions/` (2026-10-29). Follow the [experiment entry format](README.md#experiment-entries) when recording individual experiments.
