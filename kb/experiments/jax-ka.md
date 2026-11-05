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
  - id: jaxka-edge-binder
    question: Which contact targets, negative constructions and geometry augmentations improve free-partner interface recognition while retaining backbone pKa prediction?
    locations:
      - machine: isambard
        root: /scratch/u6xq/hussain.u6xq/_runtime/jax-Ka/pkabench/audits
        runs: [residue-siamese-v1-50, residue-siamese-v1-50-v4, negatives-v1, hotspot-mask-v2, drsa-within-v1, anm-aug-v1, anm-edge-v1, drsa-anm-v1, drsa-cap-v1, drsa-rel-v1, datascale-v1]
      - machine: isambard
        root: /scratch/u6xq/hussain.u6xq/_submission
        runs: [residue-siamese-v1, hotspot-mask-v2, drsa-within-v1, anm-aug-v1, anm-edge-v1, drsa-anm-v1, drsa-cap-v1, drsa-rel-v1, datascale-v1]
    authoritative_location: isambard
    status_command: null
    artifacts:
      - negatives-v1/decoy-ranking/report.json
      - negatives-v1/sweep/decoy-ranking/report.md
      - anm-aug-v1/seeds/gates/gates.md
      - anm-edge-v1/gates/gates.md
      - drsa-within-v1/gates.md
      - drsa-anm-v1/gates.md
      - drsa-cap-v1/w128/s17/gates.md
      - drsa-cap-v1/w128/s29/gates.md
      - drsa-cap-v1/w128/s43/gates.md
      - drsa-rel-v1/rel61/s17/gates.md
      - drsa-rel-v1/rel61/s29/gates.md
      - drsa-rel-v1/rel61/s43/gates.md
      - drsa-rel-v1/rel66/s17/gates.md
      - drsa-rel-v1/rel66/s29/gates.md
      - drsa-rel-v1/rel66/s43/gates.md
      - datascale-v1/w064/masked2/report.json
      - datascale-v1/w128/masked2/report.json
      - datascale-v1/e40-w064/masked2/report.json
      - datascale-v1/e40-w128/masked2/report.json
    figures: [jaxka-pinder-recipe-comparison, jaxka-pinder-ablations]
  - id: opig-adaptyv-028
    question: Do run-4, hmask and dRSA scores distinguish antibody binders from decoys through recognition of the supplied antigen?
    locations:
      - machine: local
        root: /Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer
        runs: [results]
      - machine: modal
        root: opig-eval-runs:028-poisk-free-monomer
        runs: [featcache, gqt]
    authoritative_location: modal
    status_command: null
    artifacts:
      - README.md
      - results/summary_gqt_outputs_run4_hmask_drsa.csv
      - results/summary_blind_drsa_wrong_antigen.csv
      - results/logreg_summary.csv
      - results/logreg_nodecoy_summary.csv
    figures: [jaxka-poisk-recipe-comparison]
  - id: opig-adaptyv-046
    question: Can blind hmask-GQT screening of ATLAS interfaces prioritise a KRAS G12D pMHC candidate with predicted mutant preference?
    locations:
      - machine: local
        root: /Users/alexi/Documents/opig-adaptyv-2026/experiments/046-atlas-fragment-hit
        runs: [results/atlas-c5-hmask-fragments-20261031-a]
      - machine: local
        root: /Users/alexi/Documents/opig-adaptyv-2026/data/designs/055-kras-top100-pilot/esmfold2-results
      - machine: modal
        root: opig-atlas-surface-clusters:atlas-c5-hmask-fragments-20261031-a
        runs: [full, esmfold2-target-msa/20261101-a/cases, top100-method-pilot/20261101-a]
    authoritative_location: modal
    status_command: null
    artifacts:
      - experiments/045-atlas-voronoi-clustering/interface_only/README.md
      - experiments/046-atlas-fragment-hit/README.md
      - experiments/055-kras-top100-pilot/README.md
      - data/designs/055-kras-top100-pilot/esmfold2-results/RESULTS.md
      - data/designs/055-kras-top100-pilot/esmfold2-results/candidate-results.csv
      - data/designs/055-kras-top100-pilot/esmfold2-results/results.json
    figures: []
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
    question: How accurately can backbone and sequence predict pKa and binding-induced pKa shifts, and which representations and training objectives improve the comparison?
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

[[06-jax-ka]] develops backbone pKa and binding-shift prediction, then extends the shared representation to a free-partner edge binder. Training is on Isambard and data cleaning is on Coulson-Chemistry. The external binder benchmark and ATLAS screen are in `/Users/alexi/Documents/opig-adaptyv-2026`, with bulk outputs on Modal. Access requirements are recorded in [machines.yaml](machines.yaml).

[[jaxka-edge-binder]] records the run-4, hmask and dRSA recipes, negative-training comparisons, ANM consistency and final 50% width/relation-map ablations. Its source map identifies the Isambard audit reports and frozen `_submission` code snapshots. Nineteen reports and eight definition/launch files were downloaded with remote checksum verification to `.experiments/jaxka-binder-isambard-2026-11-04/`; `receipt.json` and `source-receipt.json` preserve exact source paths and hashes.

[[028-poisk-free-monomer]] records the improvement across run 4, hmask and dRSA, the wrong-antigen and sequence-only controls, and the smaller pairing signal after removing the decoy pool. The source CSV `experiments/028-poisk-free-monomer/results/summary_gqt_outputs_run4_hmask_drsa.csv` is the consolidated comparison; the experiment report supplies the controls needed to interpret it.

[[046-atlas-kras-screen]] connects interface-library construction (045), the 69,060-representative blind hmask screen (046) and the 100-source, 300-prediction ESMFold2 comparison (055). It records the checkpoint, target-context gates, high-confidence lead and WT comparison. The screen used hmask, not the later dRSA export.

[Experiment 027](027-extremophile-vs-pka-surface.md) compares extremophile fine-tuning with pKa surface steering at matched charge changes, then tests complex confidence and predicted pH-selective binding with target context. The note records the three result arguments, the online mutation-ranking consequence and the data for the proposed figures. Its source runs are in the local `opig-adaptyv-2026` repository.

The backbone controls and early GQT comparisons remain in `projects/4-jax-Ka/code/experiments/4_backbone/` and `3_paired_complex/48_pkai_joint_scale.md`. The two machines hold checkouts of the same repository, but the frozen training snapshots identify the code used for later Isambard experiments. A current checkout commit is not a substitute for a run's recorded protocol and code hashes. Data-cleaning decisions remain in [[2026-10-29 jax-Ka masking noise targets]] and [[2026-10-29 jax-Ka data pipeline record and teacher]].

[[jaxka-edge-binder#Data scaling]] incorporates the completed seed-17 width-64 and width-128 runs at 100% data under 20- and 40-epoch schedules. Width 128 improves contact AP and antibody/antigen discrimination at full data under the 20-epoch schedule; the longer schedule gives mixed gains. Executed protocols use the complete PeSTo store and the histories record zero fallback visits. `jaxka-pinder-recipe-comparison` and `jaxka-pinder-ablations` provide the main recipe comparison and supporting diagnostics, with frozen reports, regeneration scripts and captions. The full-data retrieval receipt is `.experiments/jaxka-pinder-2026-11-05/receipt.json`.
