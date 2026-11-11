---
project: jax-ka
experiment_id: opig-adaptyv-028
local_root: /Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer
source_repository: /Users/alexi/Documents/opig-adaptyv-2026
source_commit: cc143a5c51e954b0f2931f8fafa089784e694afc
modal_volume: opig-eval-runs
modal_prefix: 028-poisk-free-monomer
figures: [jaxka-poisk-recipe-comparison]
---

# POISK gains distinguish binder-like sequences more strongly than binding partners

The run-4, hmask and dRSA comparison improves antibody binder/decoy discrimination, but most of the gain survives replacing the antigen. The wrong-antigen and sequence-only ablations therefore change the interpretation of the benchmark score. They distinguish an antibody-intrinsic sequence signal from recognition of the supplied partner. This is the external diagnostic comparison for [[jaxka-edge-binder]].

## Population and inputs

POISK supplies 11,247 patent-antibody binder/decoy pairs against 750 antigens. The full release has 22,494 records and 20,395 unique Fvs, with no VHHs. Decoys are sequence-similar to their paired binders. Free Fvs were folded with ABodyBuilder2 and antigens with ESMFold v1. GQT embeds each Fv and antigen separately, then scores residue pairs. Complex-mode comparisons use the released Protenix-v2 poses. The [experiment report](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:17) records construction and support.

The consolidated CSV contains 11,111 complete apo pairs and 11,115 complete bound-conformer/complex pairs. These supports are kept separate. Pairwise accuracy compares the binder with its paired decoy; chance is 0.5. CDR scores use IMGT CDR assignments. Run 4 is `ogqt-allres15-siamese-50`, hmask is `ogqt-allres15-within-hmask-50`, and dRSA is `ogqt-allres15-within-drsa-50` (seed 17 unless a replica is named).

## Improvements depend on the readout

| Apo free-monomer readout | Run 4 | Hmask | dRSA |
|---|---:|---:|---:|
| CDR edge-probability sum | 0.4480 | 0.5848 | 0.5710 |
| Maximum CDR edge probability | 0.4807 | 0.6435 | 0.6613 |
| Top-50 CDR edge mean | 0.4366 | 0.7115 | 0.7131 |
| Predicted dRSA, antigen sum | 0.4925 | 0.6377 | 0.6460 |
| Predicted-dRSA-weighted CDR edges | 0.4895 | 0.6671 | 0.6755 |

Source [summary_gqt_outputs_run4_hmask_drsa.csv](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/results/summary_gqt_outputs_run4_hmask_drsa.csv). These are different reductions of the same outputs. Top-50 CDR edges give the largest accuracy in this table; dRSA-weighted edges ask a different question and are not the numerically best readout overall. Figure [jaxka-poisk-recipe-comparison](../../figures/jaxka-poisk-recipe-comparison/fig.pdf) compares the three recipes for the general contact/burial readouts across apo monomers, bound conformers and complex poses, retaining the original experiment plot's mode colours and connected-point layout.

The blind predicted burial contribution of residue i is its predicted free exposure multiplied by its best contact probability to the partner. The dRSA-weighted edge sum multiplies each contact probability by the predicted contributions at both ends. This predicted quantity is distinct from the native RSA difference used to train the dRSA model. In complex mode, predicted burial change is calculated directly from bound minus free burial outputs. Definitions are in the [dRSA readout section](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:473).

## Wrong-antigen and sequence controls identify the shortcut

For predicted-dRSA-weighted CDR edges, hmask gives accuracy 0.667 against the correct antigen and 0.665 against a wrong antigen. dRSA gives 0.675 and 0.666, respectively. Maximum CDR contact probability gives dRSA accuracy 0.661 against the correct antigen and 0.649 against a wrong antigen. Most of the improvement therefore remains when the antigen identity is incorrect. Sources [wrong-antigen summary](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/results/summary_blind_drsa_wrong_antigen.csv) and [interpretation](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:487).

The matched Pegasus rerun extends the learned controls to dRSA. All three models use the same 22,274 pooled records and five antigen-cluster splits. Antibody-only embeddings retain approximately 0.89 binder/decoy accuracy, with little change after adding the correct or a wrong antigen. For dRSA, antibody-only, correct-antigen and wrong-antigen accuracies are 0.897, 0.893 and 0.896, respectively. These are trained logistic readouts, distinct from the untrained contact aggregations above.

| Learned blind readout | Run 4 | Hmask | dRSA |
|---|---:|---:|---:|
| GQT summary scores (18 features) | 0.697 ± 0.009 | 0.741 ± 0.005 | 0.777 ± 0.011 |
| Pooled embeddings, antibody only | 0.894 ± 0.006 | 0.891 ± 0.004 | 0.897 ± 0.008 |
| Antibody embeddings plus correct-antigen products | 0.895 ± 0.004 | 0.889 ± 0.008 | 0.893 ± 0.009 |
| Same features, wrong antigen | 0.892 ± 0.004 | 0.890 ± 0.004 | 0.896 ± 0.006 |
| VH/VL amino-acid composition, no GQT | 0.864 ± 0.008 | 0.864 ± 0.008 | 0.864 ± 0.008 |
| VH/VL amino-acid and dipeptide composition, no GQT | 0.949 ± 0.004 | 0.949 ± 0.004 | 0.949 ± 0.004 |

Values are mean ± SD across five antigen-cluster splits. Sequence-composition controls are shared, use no GQT model, and are repeated across columns for comparison. The GQT arms average approximately 5,449 test pairs per split; sequence controls average 5,549. Source [matched binder/decoy readouts](../../.experiments/poisk-drsa-20261110/collected/results/logreg_blind_all3_summary.csv).

No decoy antibody is a binder in another pair, so binder/decoy pool membership can be learned from the antibody. Antigen-cluster separation does not remove that shortcut. The original report additionally records that 90% of test binders share an 80%-identity VH cluster with training. These are distinct issues; the wrong-antigen result directly establishes that the high classifier score does not require the correct pairing. Source [trained-readout design and sequence controls](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:84).

The dRSA replica results confirm that the blind discrimination gain is reproducible across seeds. Predicted-dRSA-weighted CDR accuracy is 0.675, 0.677 and 0.654 for seeds 17, 29 and 43. Length alone does not explain the result. After regressing out length and Fv composition, residual accuracy remains 0.619, but the wrong-antigen result still prevents interpreting that residual as partner specificity. Source [replicas and confound analysis](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:503).

## Removing the decoy pool exposes a smaller pairing signal

The binders-only comparison holds the antibody fixed and ranks its own antigen against wrong antigens from different antigen clusters on the same side of the split. Five antigen-cluster splits are used, with three training negatives and nine test negatives per binder. Antibody-only features cancel within each comparison.

The matched comparison reports right-versus-wrong pairwise accuracy as mean ± SD across five splits. Chance is 0.5.

| Learned blind readout | Run 4 | Hmask | dRSA |
|---|---:|---:|---:|
| GQT summary scores (18 features) | 0.501 ± 0.005 | 0.515 ± 0.010 | 0.528 ± 0.006 |
| Elementwise antibody–antigen embedding products | 0.539 ± 0.009 | 0.562 ± 0.013 | 0.535 ± 0.011 |
| Bilinear antibody–antigen embedding products | 0.530 ± 0.015 | 0.551 ± 0.015 | 0.547 ± 0.011 |
| Antigen embedding only | 0.501 ± 0.004 | 0.498 ± 0.004 | 0.500 ± 0.003 |
| Sequence-composition products, no GQT | 0.532 ± 0.016 | 0.532 ± 0.016 | 0.532 ± 0.016 |

Top-1 retrieval places the correct antigen first among ten candidates. The values below are split means; chance is 0.1.

| Learned blind readout | Run 4 | Hmask | dRSA |
|---|---:|---:|---:|
| Elementwise antibody–antigen embedding products | 0.124 | 0.146 | 0.128 |
| Bilinear antibody–antigen embedding products | 0.123 | 0.134 | 0.135 |
| Antigen embedding only | 0.105 | 0.104 | 0.105 |
| Sequence-composition products, no GQT | 0.125 | 0.125 | 0.125 |

The summary-score arm uses one stored wrong antigen and approximately 2,621 test binders per split, so top-1-of-10 retrieval is not available for that arm. The embedding and composition arms use nine test alternatives and approximately 5,459 test binders per split. Source [matched binders-only readouts](../../.experiments/poisk-drsa-20261110/collected/results/logreg_nodecoy_all3_summary.csv); [original comparison design](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:119).

With the antibody fixed, the elementwise hmask readout ranks the correct antigen above a wrong antigen in 56.2% of comparisons and first among ten in 14.6%, against 50% and 10% by chance. dRSA gives 53.5% and 12.8%, close to the sequence-composition control at 53.2% and 12.5%. Under this readout, dRSA's stronger binder/decoy discrimination does not translate into better antigen pairing. Bilinear products give dRSA accuracy 0.547 and hmask accuracy 0.551, so the comparison also depends on the learned readout. These results describe trained classifiers on the benchmark; they do not establish partner specificity of the untrained screening scores. Split SDs describe variation across partitions and are not a significance test of differences between recipes.

## Pose-dependent signal and screening consequence

With the Protenix-v2 pose supplied, predicted antigen burial change gives pairwise accuracy about 0.575. Four run-4 GQT pose features increase antigen-held-out ipSAE pairwise accuracy from 0.718 to 0.735, while 1-in-50 top-1 falls from about 0.30 to 0.27. Thus the pairwise improvement does not establish better retrieval from a diverse pool. Hmask and dRSA do not materially improve the pose-based burial/contact readouts over run 4. Source [summary and combination analysis](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:58).

The [[046-atlas-kras-screen|ATLAS application]] used blind scores as candidate priorities, then investigated the proposed interactions through matched target-context contrasts and subsequent complex prediction. POISK limits the interpretation of those priorities. Binder/decoy discrimination does not by itself establish useful prospective enrichment, calibrated affinity or partner specificity.

## Source record

The experiment directory and the top-100 report files had no uncommitted changes when inspected at the source commit above. The [source receipt](../../.experiments/jaxka-binder-isambard-2026-11-04/opig-source-receipt.json) records hashes of the report and comparison tables. The original Modal location is `opig-eval-runs:/028-poisk-free-monomer/`. The [archive manifest](/Users/alexi/Documents/opig-adaptyv-2026/docs/archive_manifest_2026-11-07.md:67) records five POISK parts copied with matching SHA-256 hashes to `Pegasus-Gate:/scratch/bulk/hussain/_archive/modal-2026-11-07/opig-eval-runs/`; the files and manifests were also checked directly on Pegasus. Existing comparison plots remain in the source experiment's `results/` directory. The thesis figure `jaxka-poisk-recipe-comparison` retains its source CSV, plotted data, build script, caption and provenance in `figures/jaxka-poisk-recipe-comparison/`.


The dRSA extension and matched controls ran in `Pegasus-Gate:/scratch/bulk/hussain/poisk-drsa-20261110/`. The dRSA code revision is `305b074b0174506bfd857d9fbac3aede2d4d5348`, using `ogqt-allres15-within-drsa-50`, seed 17. Free-antibody embeddings were extracted from the archived folds with cached dRSA antigen embeddings; no new folding was performed. The A40/GTX 1080 Ti comparison on 252 records passed the numerical check (embedding relative L2 difference 0.000275). The [coverage audit](../../.experiments/poisk-drsa-20261110/collected/coverage.json) confirms 91 chunks and identical sets of 22,274 records for run4, hmask and dRSA, with finite blind embeddings and exposure summaries. CPU control job `185520` completed both readout analyses. Detailed scripts, model hashes and runtime records are in the [run provenance](../../.experiments/poisk-drsa-20261110/provenance.json); new result CSVs remain in the Pegasus working directory's `results/` and the linked local copies.

The matched rerun uses 18 scalar features. The earlier run4/hmask analysis used 11, before seven predicted-burial summaries were added (`dbur_fv`, `dbur_cdr`, `dbur_ag`, `dbur_total`, `dbur_cdr_frac`, `edge_x_dbur`, `edge_x_dbur_cdr`). All three models above use the same expanded feature set. The earlier report gives hmask elementwise pairing accuracy 0.566 ± 0.011 and top-1 retrieval 0.147; the matched rerun gives 0.562 ± 0.013 and 0.146. The [reproduction comparison](../../.experiments/poisk-drsa-20261110/collected/results/reproduction_check.json) records the numerical differences from the earlier runs. Antigen-only controls reproduce exactly, while fitted embedding readouts show small shifts; their cause has not been isolated. The three-model comparison therefore uses the matched rerun throughout.
