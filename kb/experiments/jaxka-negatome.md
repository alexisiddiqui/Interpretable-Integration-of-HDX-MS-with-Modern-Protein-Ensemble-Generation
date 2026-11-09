---
project: jax-ka
experiment_ids: [negatome-gate-v1, apo-negatome-v1, negatome-matched-v1]
authoritative_location: isambard
runtime_root: /scratch/u6xq/hussain.u6xq/_runtime/jax-Ka/pkabench
submission_root: /scratch/u6xq/hussain.u6xq/_submission
staged_inputs: .experiments/jaxka-negatome-recovery
---

# Negatome separates partner discrimination from structure-preparation effects

Negatome was used for both training and evaluation of the free-partner edge binder. Matching the preparation of positive and negative partners exposed a preference for cropped structures in the original Negatome-trained model. Training with matched preparation partly reduced that preference, but improvements in Negatome ranking did not extend to antibody–antigen swap accuracy. This comparison belongs after the generated-negative experiments in [[jaxka-edge-binder]] and before the sequence-shortcut analysis in [[028-poisk-free-monomer]].

## Negative evidence and training construction

The experiment used the [Negatome 2.0](https://doi.org/10.1093/nar/gkt1079) combined-stringent set, which combines literature and structural evidence for non-interaction. It is not a uniform collection of experimental nonbinding measurements. For a PINDER complex, a chain with a Negatome-listed non-partner became the anchor for comparison with its observed partner. Training excluded complexes whose observed interaction was itself listed in Negatome, retained at most two non-partners per complex and capped reuse of each non-partner at twenty complexes. The [training-triple builder](../../.experiments/jaxka-negatome-recovery/source/data/build_train_triples.py) and [evaluation-triple builder](../../.experiments/jaxka-negatome-recovery/negatome-gate-v1/source/build_triples.py) define the mappings and exclusions.

The original `aponeg` recipe added a listwise Negatome loss of weight 0.3 to the early within-ranking recipe, which retained a retyped-decoy term of weight 0.1. For each anchor, candidates included residues from the observed partner and up to 32 exposed residues from a Negatome non-partner. The latter received zero target weight. AlphaFold inputs for the observed partners were cropped to the crystal-observed residues, while Negatome inputs were full-length monomers. The matched follow-up used full-length AlphaFold models for both candidate partners, with positive contact labels transferred by alignment. The `negm` and `aponegm` variants differed in whether AlphaFold augmentation also acted on the ordinary separated-state branch. These are separate ablations from hmask and dRSA. The [original protocol](../../.experiments/jaxka-negatome-recovery/runs/apo-v1-50-within03-aponeg-w064-s17/protocol.json) and [matched protocol](../../.experiments/jaxka-negatome-recovery/runs/negm-v1-50-within03-aponegm-w064-s17/protocol.json) retain the objective coefficients and input definitions.

## Matching preparation changes the apparent discrimination

The matched evaluation held the anchor fixed and compared its observed partner with the same Negatome non-partner. Both candidate partners were represented as full-length AlphaFold monomers. Scoring averaged residue-pair contact probabilities over the eligible surfaces, using RSA at least 0.1 and pLDDT at least 70. Accuracy was averaged over comparisons within each complex and then across complexes, with ties contributing one half. The [evaluation implementation](../../.experiments/jaxka-negatome-recovery/source/score_matched.py) distinguishes this score from the contact-anchored readout.

For the original `aponeg` model, accuracy fell from 0.881 with cropped true partners to 0.550 with full-length true partners on the same 74 complexes. On a separate control containing 418 complexes and no Negatome negatives, it preferred the cropped version of the same partner in 95.0% of cases. This identifies sensitivity to preparation as an explanation for part of the apparent recognition gain. The [paired evaluation](../../.experiments/jaxka-negatome-recovery/reports/matched/report.md) gives both comparisons and their supports.

## Matched training gives limited and mixed gains

The full matched evaluation contained 95 complexes. These differ from the 74-complex subset with both cropped and full-length scores, so the two supports remain separate.

| Training recipe | Matched Negatome accuracy, 95 complexes | All-AlphaFold antibody–antigen swap accuracy | Clean crystal pKa selection MAE |
|---|---:|---:|---:|
| Within-ranking control | 0.475 | 0.6382 | 0.6121 |
| Original apo plus Negatome (`aponeg`) | 0.501 | 0.6090 | 0.6215 |
| Matched Negatome (`negm`) | 0.477 | 0.5798 | 0.6182 |
| Apo plus matched Negatome (`aponegm`) | 0.587 | 0.5933 | 0.6223 |

The [follow-up report](../../.experiments/jaxka-negatome-recovery/negatome-matched-v1/reports/gates/gates.md) reports a standard error of approximately 0.051 for each matched Negatome accuracy. All recipes use seed 17. The rise to 0.587 is accompanied by lower antibody–antigen swap accuracy and greater pKa error. In the paired 74-complex subset, `aponegm` reaches only 0.529, compared with 0.550 for `aponeg`; the full-cohort improvement is therefore not a uniform gain across these supports. The [full matched report](../../.experiments/jaxka-negatome-recovery/negatome-matched-v1/reports/matched/report.md) retains the subsets and preparation controls.

## Place in the results argument

The Negatome comparison tests whether curated negative evidence removes the ambiguity exposed by generated decoys. The cropped/full-length control shows why negative labels alone cannot make a ranking result interpretable when structure preparation differs between classes. The matched-training follow-up then tests the corrective comparison and establishes its limited transfer. POISK asks the next question, whether discrimination remains when the target is replaced and sequence composition is controlled. Preparation dependence and sequence leakage are distinct explanations, each requiring its own comparison.

The [recovery receipt](../../.experiments/jaxka-negatome-recovery/receipt.json) records remote source paths and checksums for 80 files. The recovered training driver, loader and apo implementation match all twelve corresponding source hashes recorded across the four recovered run protocols. [[Loss functions and training recipes (jax-Ka)]] links this additional objective for the appendix.
