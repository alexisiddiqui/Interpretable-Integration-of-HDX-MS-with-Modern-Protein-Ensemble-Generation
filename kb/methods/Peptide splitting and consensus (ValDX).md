---
type: method
project: 1-ValDX
status: draft
needs_review: true
review_reason: The pinned ValDX package implements only the random split; the Non-Redundant (R3) and Spatial (Sp) modes that the benchmark scripts request are not in the pinned code, and no code for the staged consensus mean was located. Pin both before Chapter 3 cites this note.
code:
  - projects/1-ValDX/code@4641fbe:ValDX/Experiment_ABC.py#L70-L104
  - projects/1-ValDX/analyses@1d78b96:scripts/Figure-2_Single_Split_BV/GSD_AFS_RW_ValDXer_testing_BPTI_0.5split.py#L22
  - projects/1-ValDX/analyses@1d78b96:data/jaxENT_CrossValidation/man_pD4_R3_Sp/MoPrP_ensembles_RW_bench.py#L222-L230
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c12]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c16]]"
---

<!-- Note name: Peptide splitting and consensus (ValDX). Concepts: [[data splitting]], [[replicate uncertainty]], [[model averaging]]. -->

## What it does

ValDX partitions the HDX-MS observations before every fit so that validation error measures prediction of information the fit has not seen, then repeats the partition to measure how much the fit depends on it, and in staged protocols combines the replicate fits into one consensus prior for the next stage. The purpose of each partition comes before its algorithm. Because peptides share residues, a validation peptide can be partly known from training peptides covering the same region, which inflates apparent performance ([[@siddiquiFrameworkTestingStructural2026#^c8]]). The structured splits withhold whole regions of sequence or of structure instead of peptides at random, and on experimental data the random baselines added no discrimination beyond training error ([[@siddiquiFrameworkTestingStructural2026#^c16]]). Replicates across splits quantify the dependence of the outcome on the peptides and time points used ([[@siddiquiFrameworkTestingStructural2026#^c12]]).

## Equations

No closed form. The quantities reported per split replicate are the validation MSE, the Work Done components ([[Work Done (ValDX)]]) and, in staged protocols, the consensus weights and coefficients.

## Implementation notes

- **Algorithms** (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L70–81). Non-Redundant: k-means on each peptide's start and end positions, with a tenth of the peptide count as the number of clusters; clusters are assigned at random to reach the training fraction; any peptide sharing a residue with the other set is dropped from training. Spatial: a residue is chosen at random, the remaining residues are ordered by Cα distance from it, the training set is filled in order of proximity, and overlapping peptides are dropped. Random and Sequential are the baselines. All splits target a training fraction of 50 %, each set keeps at least 10 % of the peptides, and peptides with high overlap density are dropped stochastically at 10 % before splitting (L81).
- **Unit withheld.** Non-Redundant withholds sequence regions and Spatial withholds structural regions. For BPTI the observations are residues, so there is no peptide overlap to remove and the splits partition correlated residue-wise observations by sequence and by proximity (L52; [[cooperative unfolding unit]]).
- **Replicate counts** (L619–L667). TeaA, three replicates of four split types; BPTI and BRD4 experiments, three or ten replicates of the two structured types; staged protocols, three per stage; the kinetic benchmark, three peptide-split replicates per condition with one matched noise realisation.
- **Selection within a replicate** (L473). The fitting strength is swept on the training data and chosen by the curve-of-the-knee criterion, or by the normalised selection score in the kinetic benchmark (L674–L680). Validation MSE and recovery are not used for selection, so validation error stays an evaluation ([[model selection]]).
- **Single-stage protocols** pool the per-replicate metrics; they do not average the fits (L473).
- **Staged consensus** (L659, L672). Replicates are mean-averaged over frame weights and Best–Vendruscolo coefficients, and the mean is the prior for the next stage. This is [[model averaging]] of parameters. Averaging weights averages the predicted log protection factors only while the coefficients are fixed; with both averaged, the consensus is not the mean prediction ([[Averaging frame weights across fits averages their predicted log protection factors only while forward-model coefficients are held fixed.]]).
- **What the spread means** (L693, L606). Replicates of a later stage share the consensus of the earlier stage, so their spread is sensitivity to partitioning and not independent measurement replication. The 9 % interlaboratory reproducibility of uptake is kept as a separate reference scale ([[experimental uncertainty]]).
- **Failure modes** (L482). Overlap removal can empty a set; the remedy is to adjust the redundancy dropout or remove very long peptides. Larger fitting strengths fail more often, and extra replicates compensate.
- **Code.** The pinned package's `split_segments` (first code link) implements the random mode and lists sequential, spatial and redundancy-aware modes as not implemented. The benchmark scripts pass `R3` and `Sp` through `settings.split_mode` (second and third links), so the implementation they exercised lives in a later or separate version. The consensus mean was not located in the pinned code either.

Claims that use this method: [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]], [[Averaging reweighting fits across split replicates stabilises the consensus and reduces overfitting to particular peptide subsets.]], [[A consensus over split replicates does not by itself make the candidate ensemble representative.]], [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]].
