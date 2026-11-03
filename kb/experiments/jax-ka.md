---
project: jax-ka
local_repositories:
  - projects/4-jax-Ka/code
  - /Users/alexi/Documents/opig-adaptyv-2026
locations:
  - machine: isambard
    root: /scratch/u6xq/hussain.u6xq
  - machine: coulson
    root: /u/oc/lina4225
experiments:
  - id: opig-adaptyv-027
    question: How do extremophile fine-tuning and pKa steering differ in surface chemistry, complex confidence and predicted pH-selective binding?
    locations:
      - machine: local
        root: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface
        runs: [results]
      - machine: modal
        root: opig-design-runs:027-extremophile-vs-pka-surface
        runs: [anchors-all-2026-10-28, anchors-target-2026-10-28, search-target-2026-10-28, complexcheck-target-2026-10-28, select-2026-10-29, selectcheck-2026-10-29, select-yield-2026-10-29, selectcheck-yield-2026-10-30]
    authoritative_location: modal
    status_command: /Users/alexi/Documents/opig-adaptyv-2026/.venv/bin/modal volume ls opig-design-runs 027-extremophile-vs-pka-surface --json
    artifacts:
      - results/analysis.json
      - results/fold-check-foldcheck-2026-10-28.json
      - results/fold-check-complexcheck-target-2026-10-28.json
      - results/selectivity-sweep-select-2026-10-29.json
      - results/selectivity-sweep-select-yield-2026-10-29.json
      - results/fold-check-selectcheck-2026-10-29.json
      - results/fold-check-selectcheck-yield-2026-10-30.json
      - results/binding-ph-bindingph-select-2026-10-29.json
      - results/binding-ph-bindingph-yield-2026-10-30.json
    figures: [jaxka-extremophile-overlap, jaxka-extremophile-chemistry, jaxka-extremophile-complex-confidence, jaxka-complex-linkage-selectivity, jaxka-extremophile-monomer-refolding]
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
      - machine: coulson
        root: /u/oc/lina4225/_runtime/jax-Ka/pkabench/audits
        runs: [relation-figures-v1, relation-memory-v1]
    authoritative_location: isambard
    status_command: null
    # Paths are relative to the pkabench runtime root on the machine named before the colon.
    artifacts:
      - isambard:audits/relation-figures-v1/runs.csv                         # selection.json export of the 21 relation-map runs; pkabench.relation_plots; copied to figures/jaxka-relational-edges
      - coulson:audits/relation-memory-v1/memory.csv                         # full-backprop memory and step time, 9 configs x 9 buckets, A40 job 779030; figures/jaxka-relational-memory
      - coulson:audits/relation-memory-v1/edges.csv                          # attended pairs per sampled training graph
      - coulson:audits/relation-memory-v1/coord.csv                          # coordinate-only gradient memory and time, job 779031; figures/jaxka-coordinate-gradients
      - coulson:audits/relation-memory-v1/slurm.csv                          # host MaxRSS of the Isambard training jobs (GPU memory not recorded)
    # jaxka-pkai-siamese holds tables transcribed from the jax-Ka note experiments/3_paired_complex/48_pkai_joint_scale.md.
    figures: [jaxka-relational-edges, jaxka-relational-memory, jaxka-coordinate-gradients, jaxka-pkai-siamese]
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
      - audits/propka-components-v2-ligands/out/report.json                  # ligands rerun with corrected atom names, 17 complete
      - audits/propka-components-v4-ligands/out/report.json                  # all 39 ligand tasks, unique residue names, water-only ignore list
      - audits/glycan-protein-sasa-v1/out/report.json                        # protein SASA shielded by glycans, 29 complexes; tables only (site_sasa.csv)
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
      - audits/short-gap-absolute-rescore-v1                                 # PINDER loss under absolute-pKa short-tail radii, by label size; tables only
      - campaigns/coordinate-pool-inclusive-v1/rejections.parquet            # rejection codes, not yet plotted
      - universe/structural-freeze-v1
      - pretraining/pinder-pkai-v1
      - pretraining/pkpdb-full-v1
      - training/pool-v4
      - audits/cutoff-figures-v3/components/plots/component_cutoffs.png      # pkabench.cutoff_plots; copied to figures/jaxka-component-cutoffs
      - audits/cutoff-figures-v3/gaps/plots/gap_cutoffs.png                  # gap radii, PypKa short and pKAI long gaps; copied to figures/jaxka-gap-cutoffs
    figures: [jaxka-component-cutoffs, jaxka-gap-cutoffs]
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

[Experiment 027](027-extremophile-vs-pka-surface.md) compares extremophile fine-tuning with pKa surface steering at matched charge changes, then tests complex confidence and predicted pH-selective binding with target context. The note records the three result arguments, the online mutation-ranking consequence and the data for the proposed figures. Its source runs are in the local `opig-adaptyv-2026` repository.

Observed 2026-10-29.

- **Coulson:** three checkouts of `alexisiddiqui/jax-Ka` in the root: `jax-Ka/` (branch `benchmark`, 107 uncommitted files, last commit 2026-10-13), `jax-Ka-ph/` (`ph-aux`, clean) and `jax-Ka-augmentation-main/` (`main`, clean). Their `experiments/` layout matches `projects/4-jax-Ka/code/experiments/`. Run output sits in `_runtime/jax-Ka/` (`anm-pilot-v1`, `pkabench`, `logs`). The `anm-*` jobs (feature-cache pools, ten-mode runs) and the `pkai-scan` array were queued or running in the last ten days.
- **Isambard:** `jax-Ka/` (branch `main`, clean, last commit 2026-10-21) and `jax-Ka-crop/` (a production-crop worktree), with the same `experiments/` layout. Run output is in `_runtime/jax-Ka/` (`ogqt-*`, `6sc6-*`, `pkabench`, `anm-pilot-v1`). The `_submission/` sets from 2026-10-27 to 2026-10-29 (`gqt-*`, `teacher-*`, `nonlinear-*`, `pkpdb-*`) are the most recent GQT work. `_wt/` holds worktrees (`ph-aux`, `pkai-*`). The queue was empty.

Training and the benchmark experiments run on Isambard, which holds most of the experiments. Data cleaning (curation, the experimental admission and inventory scripts, the pKa benchmark caches and manifests) was done on Coulson. The two machines hold checkouts of the same repository, so a result's code state has to be read from the machine that produced it.

The `jax-Ka` checkout on Coulson has uncommitted changes, so any result produced from it needs the code state recorded before it is used. The data-cleaning entry records its question and artifacts; the other entries do not yet. Decisions on the masking noise targets and the data pipeline record are in `kb/decisions/` (2026-10-29). Follow the [experiment entry format](README.md#experiment-entries) when recording individual experiments.
