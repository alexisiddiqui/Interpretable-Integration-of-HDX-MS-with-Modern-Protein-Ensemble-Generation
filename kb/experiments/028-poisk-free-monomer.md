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

A trained logistic readout on pooled GQT embeddings reaches about 0.89 pairwise accuracy under antigen-cluster holdout, with essentially the same score using antibody-only features or a wrong antigen. VH/VL amino-acid and dipeptide composition alone reaches 0.95. No decoy antibody is a binder in another pair, so binder/decoy pool membership can be learned from the antibody. Antigen-cluster separation does not remove that shortcut. The report additionally records that 90% of test binders share an 80%-identity VH cluster with training. These are distinct issues; the wrong-antigen result directly establishes the absence of a required pairing contribution to the high classifier score. Source [trained-readout ablations](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:84).

The dRSA replica results confirm that the blind discrimination gain is reproducible across seeds. Predicted-dRSA-weighted CDR accuracy is 0.675, 0.677 and 0.654 for seeds 17, 29 and 43. Length alone does not explain the result. After regressing out length and Fv composition, residual accuracy remains 0.619, but the wrong-antigen result still prevents interpreting that residual as partner specificity. Source [replicas and confound analysis](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:503).

## Removing the decoy pool exposes a smaller pairing signal

The binders-only comparison holds the antibody fixed and ranks its own antigen against wrong antigens from different antigen clusters on the same side of the split. Five antigen-cluster splits are used, with three training negatives and nine test negatives per binder. Antibody-only features cancel within each comparison.

| Learned blind readout, binders only | Right-versus-wrong accuracy | Top-1 among 10 antigens |
|---|---:|---:|
| Run-4 embedding products | 0.538 ± 0.008 | 0.124 |
| Hmask embedding products | 0.566 ± 0.011 | 0.147 |
| Sequence-composition products | 0.532 ± 0.016 | 0.124 |
| Hmask antigen embedding only | 0.498 | 0.104 |

The hmask representation retains a small pairing signal under this comparison. It does not retain the 0.89 binder/decoy classifier performance. These are learned readouts on the benchmark, distinct from the untrained edge sums. Source [binders-only comparison](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:119).

## Pose-dependent signal and screening consequence

With the Protenix-v2 pose supplied, predicted antigen burial change gives pairwise accuracy about 0.575. Four run-4 GQT pose features increase antigen-held-out ipSAE pairwise accuracy from 0.718 to 0.735, while 1-in-50 top-1 falls from about 0.30 to 0.27. Thus the pairwise improvement does not establish better retrieval from a diverse pool. Hmask and dRSA do not materially improve the pose-based burial/contact readouts over run 4. Source [summary and combination analysis](/Users/alexi/Documents/opig-adaptyv-2026/experiments/028-poisk-free-monomer/README.md:58).

The [[046-atlas-kras-screen|ATLAS application]] therefore treats blind scores as candidate priorities, with explicit target-context contrasts and subsequent complex prediction. POISK supplies a reason to test those candidates structurally, rather than interpreting the blind score as calibrated affinity or specificity.

## Source record

The experiment directory and the top-100 report files had no uncommitted changes when inspected at the source commit above. The [source receipt](../../.experiments/jaxka-binder-isambard-2026-11-04/opig-source-receipt.json) records hashes of the report and comparison tables. Original structures, cached features and detailed outputs remain on `opig-eval-runs:/028-poisk-free-monomer/`. Existing comparison plots remain in the source experiment's `results/` directory. The thesis figure `jaxka-poisk-recipe-comparison` retains its source CSV, plotted data, build script, caption and provenance in `figures/jaxka-poisk-recipe-comparison/`.
