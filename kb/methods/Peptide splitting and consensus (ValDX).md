---
type: method
project: 1-ValDX
status: draft
needs_review: true
review_reason: The inspected code (0b79aad) combines the BV constants by the median where the manuscript states the mean, and no inspected script sets the 10 % peptide dropout; which code and settings produced the reported runs is not established. Settle both before Chapter 3 cites this note.
code:
  - projects/1-ValDX/code@0b79aad:ValDX/Experiment_ABC.py#L350-L354
  - projects/1-ValDX/code@0b79aad:ValDX/Experiment_ABC.py#L747-L753
  - projects/1-ValDX/code@0b79aad:ValDX/VDX_dataclasses.py#L577-L627
  - projects/1-ValDX/code@0b79aad:ValDX/VDX_dataclasses.py#L693-L755
  - projects/1-ValDX/code@0b79aad:ValDX/VDX_dataclasses.py#L856-L892
  - projects/1-ValDX/code@0b79aad:ValDX/VDX_dataclasses.py#L447-L457
  - projects/1-ValDX/code@0b79aad:ValDX/VDX_Settings.py#L35-L36
  - projects/1-ValDX/code@0b79aad:ValDX/ValidationDX.py#L3054-L3091
  - projects/1-ValDX/code@0b79aad:figure_scripts/kinetic_simulation/04_TeaA_kinetic_sweep.py#L75-L86
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
- **Staged consensus, manuscript** (L659, L672). Replicates are mean-averaged over weights and parameters to give the prior for the next stage. This is [[model averaging]] of parameters. Averaging weights averages the predicted log protection factors only while the coefficients are fixed, and with the constants also replaced by a consensus the result is not the mean prediction ([[Averaging frame weights across fits averages their predicted log protection factors only while forward-model coefficients are held fixed.]]).
- **Staged consensus, inspected code** (ValidationDX.py L3054–3091). In `run_sweep_methods` the consensus is taken per split type over the training weights of the replicates. The frame weights are mean-averaged and renormalised to a mean of one, and the Bc and Bh constants are combined by the median. The next stage starts from these weights and constants. The pinned kinetic script reaches this function through `04_TeaA_kinetic_sweep.py` L83–86.
- **What the spread means** (L693, L606). Replicates of a later stage share the consensus of the earlier stage, so their spread is sensitivity to partitioning and not independent measurement replication. The 9 % interlaboratory reproducibility of uptake is kept as a separate reference scale ([[experimental uncertainty]]).
- **Failure modes** (L482). Overlap removal can empty a set; the remedy is to adjust the redundancy dropout or remove very long peptides. Larger fitting strengths fail more often, and extra replicates compensate.
- **Code.** The ValDX submodule is pinned to `origin/GSD-stats-HPC` at 0b79aad (2026-09-14). Until 2026-10-15 it was pinned to `main` (4641fbe, 2023-12-13), which implements only the random mode in `split_segments` and lists the others as not implemented. `main` is an ancestor of the branch, which is 72 commits ahead of it. `split_segments` sends R3 to `redundant_sequence_split` and Sp to `neighbours_split` (Experiment_ABC.py L350–354, L747–753). `redundant_sequence_split` clusters the start and end residues with k-means, using the larger of a tenth of the peptide count and four clusters, and assigns `int(k × training fraction)` clusters to training at random. It then removes overlap, and retries with a new seed if either set falls below 10 % of the peptides or the sets intersect (VDX_dataclasses.py L577–627). `neighbours_split` picks a random protein residue, orders the HDX-covered residues by Cα distance from it, fills training in that order and removes overlap (L693–755). Both match the manuscript's description (L70–81), apart from the four-cluster floor.
- **Overlap handling and dropout, inspected code.** `drop_intersection` removes overlapping peptides from both sets when `hard_intersection` is False, which is the settings default, and moves them to the validation set when it is True (VDX_dataclasses.py L856–892). The manuscript removes them from the training set for the Non-Redundant split and drops them for the Spatial split. The pinned BRD4 sweep scripts set it True and the pinned kinetic script leaves the default. The 10 % stochastic dropout of high-overlap peptides (L81) is `drop_centrality`, which defaults to False (VDX_Settings.py L35–36), and no script on the branch or in the pinned analyses sets it True.
- **Not established for the reported runs.** Whether the published benchmarks ran this code, and so whether their consensus took the mean or the median of the BV constants, whether the 10 % dropout was applied, and which overlap setting each benchmark used.

Claims that use this method: [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]], [[Averaging reweighting fits across split replicates stabilises the consensus and reduces overfitting to particular peptide subsets.]], [[A consensus over split replicates does not by itself make the candidate ensemble representative.]], [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]].
