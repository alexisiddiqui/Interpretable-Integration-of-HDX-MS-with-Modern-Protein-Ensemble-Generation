---
type: concept
aliases:
  - replicate analysis
  - replicate fits
  - fitting instability
  - robustness
  - sensitivity to data selection
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c12]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c13]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c14]]"
  - "[[@bradshawInterpretationHDXData2020#^c2]]"
---

## Definition

Replicate uncertainty is the spread of results across repeated fits that use different selections of the data, such as different training splits. Fitting outcomes depend strongly on which peptides and time points are used, and replicates quantify this ([[@siddiquiFrameworkTestingStructural2026#^c12]]). A conclusion that changes between replicates depends on the data selection, not only on the protein.

The same test applies to the representation ([[clustering]]). Clustering an ensemble into representative structures gives compact, interpretable ensembles with little loss of accuracy ([[@siddiquiFrameworkTestingStructural2026#^c13]]), and a conclusion read off representatives should not depend on how many there are. Stable conclusions let a fitted ensemble be treated as a structural hypothesis that can be ranked against data or rejected ([[@bradshawInterpretationHDXData2020#^c2]], [[@siddiquiFrameworkTestingStructural2026#^c14]]).

## Assumptions and limits

- Replicate spread is not [[posterior uncertainty]] (what the data leave undetermined under one model) and not physical heterogeneity (the populations). It measures sensitivity to the data chosen.
- It locates where a model is unstable but does not by itself say whether sampling, structure or the forward model is at fault (revised ValDX, `projects/1-ValDX/manuscript/report/7_results_omc.tex` L18, L242). Attributing the instability needs a [[controlled perturbation]] that changes one suspected cause. The jaxENT Fig. 5 caption claims uncertainty separates sampling from force-field limitations (`projects/2-jaxENT/manuscript/report/results.tex` L203); that conflicts with ValDX and should not be reused.
- Agreement between replicates is necessary, not sufficient: all replicates can share the same missing state or forward-model error ([[sampling coverage]], [[model misspecification]]). The same logic applies to MD replicates ([[equilibration and convergence]]).
- Stability across cluster sizes is in the revised manuscript only (`7_results_omc.tex` L235).
- jaxENT maps replicate uncertainty onto weights, protection factors and structure (`results.tex` L173, L195, L197). It is useful for interpretation, but not yet citable. It belongs in a jaxENT method note, not yet written.

## Why it matters here

Introduction §1.5, paragraph 5: uncertainty and interpretation. Replicate spread, residual maps and representative structures are how ValDX and jaxENT make a fitted ensemble inspectable rather than a single optimum.

Claims that use this term: [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]], [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]], [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]], [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]], [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]].
