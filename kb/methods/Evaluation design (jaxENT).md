---
type: method
project: 2-jaxENT
status: draft
needs_review: false
review_reason:
code:
  - projects/2-jaxENT/code@37043b5:jaxent/examples/1_IsoValidation_OMass/fitting/jaxENT/analyze_within_trajectory_selection.py#L1-L7
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/analysis/compare_moprp_raw.py#L125-L135
  - projects/2-jaxENT/code@37043b5:jaxent/src/data/splitting/split.py#L795-L816
  - projects/2-jaxENT/code@37043b5:jaxent/src/data/loader.py#L178-L186
  - projects/2-jaxENT/code@37043b5:jaxent/examples/2_CrossValidation/fitting/jaxENT/splitdata_CrossVal.py#L109-L110
  - projects/2-jaxENT/code@37043b5:jaxent/examples/2_CrossValidation/fitting/jaxENT/splitdata_CrossVal.py#L146
  - projects/2-jaxENT/code@37043b5:docs/averaging_mode_soft_regression.md#L93-L148
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c12]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
---

<!-- Note name: Evaluation design (jaxENT). Concepts: [[model selection]], [[data splitting]], [[replicate uncertainty]]. -->

## What it does

jaxENT separates model selection from evaluation against reference populations. The inner layer selects, within each of three split replicates, on that replicate's HDX-MS validation set ([[Observation weighting and selection (jaxENT)]]). The outer layer evaluates the selected models against the HDX-NMR-derived MoPrP populations or the synthetic truth of the ISO benchmark. Ground-truth recovery and effective sample size are evaluation-only (first code link), and the error on the full dataset is report-only (second code link). The structure is selection separated from evaluation, nested in structure with a single outer evaluation rather than a resampled outer loop ([[model selection]]). The use of reference information in covariance construction is recorded separately in [[Observation weighting and selection (jaxENT)]]. The manuscript's "representative models are then selected by test error minimisation" (`projects/2-jaxENT/manuscript/report/experiments/protocols.tex` L325) describes the legacy path and is not reused.

## Equations

Recovery is $100\,(1 - \sqrt{D_\text{JS}^{(2)}})$ between selected and reference populations ([[Ground-truth recovery (jaxENT)#^eq-gtr]]). Validation error within a replicate is the weighted score of [[Observation weighting and selection (jaxENT)#^eq-sigma-score]].

## Implementation notes

- **Splits differ from ValDX.** The MoPrP split script runs random, sequence, sequence-cluster, stratified and spatial splits with overlap removal on (fifth code link) and seven sequence clusters (sixth link), without the redundancy dropout and the tenth-of-peptides cluster rule of ValDX ([[Peptide splitting and consensus (ValDX)]]). The two projects therefore ask slightly different questions of the same split names.
- **MoPrP splits retain overlap.** MoPrP has only 11–13 heavily overlapping peptides, and its splits retain some overlap (author clarification, 2026-10-28). Validation scores therefore remain dependent on shared residue coverage ([[data splitting]]). In the implementation, overlap removal trims the merged validation topologies against the training topologies, and the final sets are filled with every datapoint that intersects each merged topology (third link). A peptide that straddles the boundary can intersect both and appear in both sets; the train/validation fragment-disjointness assert is commented out (fourth link). The retained overlap is a documented limitation of this small dataset.
- **Replicates.** Three split replicates per split type; their spread is partition sensitivity ([[@siddiquiFrameworkTestingStructural2026#^c12]], [[replicate uncertainty]]). jaxENT selects one model per replicate and does not form a consensus ([[model averaging]]).
- **Negative controls.** The α-synuclein buffer conditions are fitted to the same Tris-MD ensemble as negative fitting controls (`results.tex` L207), which withholds a condition rather than a peptide ([[data splitting]] unit table).
- **Frame-averaging semantics are a forward-model choice.** Averaging log protection factors, rates or uptake over frames gives different predictions. In the ISO baseline, rate and uptake averaging fit held-out uptake better while log-protection-factor candidates recovered the populations better, and letting the three modes compete per replicate selects different modes in different replicates (seventh link; [[Averaging log protection factors, exchange rates or uptake over frames are different forward models, and held-out uptake error and population recovery can favour different choices.]]). Record the mode with every reported fit ([[model misspecification]]).
- **What the outer evaluation establishes.** Recovery against the MoPrP reference is recovery of an HDX-NMR-derived population set with its own state assignments ([[identifiability]], [[prion protein]]). Prefer "reference recovery" for MoPrP in thesis prose ([[Ground-truth recovery (jaxENT)]]).

Claims that use this method: [[Selecting a model by its validation error makes that error optimistic, so performance must be estimated on data unused in selection.]], [[Averaging log protection factors, exchange rates or uptake over frames are different forward models, and held-out uptake error and population recovery can favour different choices.]].
