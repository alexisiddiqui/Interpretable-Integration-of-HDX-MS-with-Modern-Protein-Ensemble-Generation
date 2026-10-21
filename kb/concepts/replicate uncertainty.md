---
type: concept
aliases:
  - replicate analysis
  - replicate fits
  - fitting instability
  - robustness
  - sensitivity to data selection
  - partition sensitivity
  - between-split agreement
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c12]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c13]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c14]]"
  - "[[@bradshawInterpretationHDXData2020#^c2]]"
---

## Definition

Replicate uncertainty is the spread of results across repeated fits that use different selections of the data, such as different training splits. Fitting outcomes depend strongly on which peptides and time points are used, and replicates quantify this ([[@siddiquiFrameworkTestingStructural2026#^c12]]). A conclusion that changes between replicates depends on the data selection, not only on the protein.

The replicates serve two roles, and the order matters. First they are compared, and their spread is reported as sensitivity to partitioning. Then, in a staged protocol, they are combined into a consensus by [[model averaging]], which becomes the prior for the next stage. The spread is the diagnostic; the consensus is the estimate.

Between-split agreement is a third reading. Non-Redundant and Spatial splits withhold different structural information, so close agreement between their averages supports a result that does not depend on the partition, and disagreement locates the dependence in the regions withheld (`projects/1-ValDX/manuscript/report/7_results_omc.tex` L55).

The same test applies to the representation ([[clustering]]). Clustering an ensemble into representative structures gives compact, interpretable ensembles with little loss of accuracy ([[@siddiquiFrameworkTestingStructural2026#^c13]]), and a conclusion read off representatives should not depend on how many there are. Stable conclusions let a fitted ensemble be treated as a structural hypothesis that can be ranked against data or rejected ([[@bradshawInterpretationHDXData2020#^c2]], [[@siddiquiFrameworkTestingStructural2026#^c14]]).

## Assumptions and limits

- Replicate spread is not [[posterior uncertainty]] (what the data leave undetermined under one model) and not physical heterogeneity (the populations). It measures sensitivity to the data chosen. The full set of quantities called uncertainty is tabulated in [[experimental uncertainty]].
- Split replicates are not measurement replicates. ValDX keeps the 9 % interlaboratory reproducibility of uptake apart from the spread across split replicates, which measures sensitivity to peptide-level partitioning (`6_methods_omc.tex` L606). In staged protocols the replicates share the consensus weights or parameters of the preceding stage, so their variation does not represent independent measurement-noise replication (L693).
- The ValDX supplement's "global confidence" and "local confidence" are shorthand for reproducibility under the Non-Redundant and Spatial splits. They are not calibrated probabilities or confidence intervals (`9_Supplementary_information.tex` L89).
- It locates where a model is unstable but does not by itself say whether sampling, structure or the forward model is at fault (revised ValDX, `7_results_omc.tex` L18, L242). Attributing the instability needs a [[controlled perturbation]] that changes one suspected cause. The jaxENT Fig. 5 caption claims uncertainty separates sampling from force-field limitations (`projects/2-jaxENT/manuscript/report/results.tex` L203); that conflicts with ValDX and should not be reused.
- Small spread shows stability, not uniqueness. Replicates can agree on one of several ensembles that fit equally well ([[identifiability]]).
- Agreement between replicates is necessary, not sufficient: all replicates can share the same missing state or forward-model error ([[sampling coverage]], [[model misspecification]]). The same logic applies to MD replicates ([[equilibration and convergence]]).
- Stability across cluster sizes is in the revised manuscript only (`7_results_omc.tex` L235).
- jaxENT maps replicate uncertainty onto weights, protection factors and structure (`results.tex` L173, L195, L197). It is useful for interpretation, but not yet citable. It belongs in a jaxENT method note, not yet written.

## Why it matters here

Introduction §1.5, paragraph 5: uncertainty and interpretation. Replicate spread, residual maps and representative structures are how ValDX and jaxENT make a fitted ensemble inspectable rather than a single optimum. Chapter 2 §2.5 uses the two roles to separate what a split replicate assesses from what the consensus estimates ([[Peptide splitting and consensus (ValDX)]]).

Claims that use this term: [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]], [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]], [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]], [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]], [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]], [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]], [[Averaging reweighting fits across split replicates stabilises the consensus and reduces overfitting to particular peptide subsets.]].
