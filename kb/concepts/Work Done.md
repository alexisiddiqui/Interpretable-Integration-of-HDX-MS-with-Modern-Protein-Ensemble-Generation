---
type: concept
aliases:
  - Work Done metrics
  - Work_opt
  - departure from the prior
  - modification required to fit
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c9]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c11]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c15]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c10]]"
---

## Definition

Work Done is ValDX's family of uptake-independent metrics that quantify how much an ensemble must be modified to match experiment ([[@siddiquiFrameworkTestingStructural2026#^c9]]). They compare the ensemble-averaged [[protection factor]] profile before and after fitting. Work_shape measures changes in the profile's shape, Work_scale its overall magnitude, and Work_density how the profile is reorganised. Different patterns point to different problems. For example, Work_scale alone suggests calibration mismatch, so recalibration comes before rejecting the ensemble ([[@siddiquiFrameworkTestingStructural2026#^c15]]).

Read together with validation error, low validation error with high Work Done signals agreement reached by excessive modification ([[@siddiquiFrameworkTestingStructural2026#^c11]]; [[overfitting]]).

## Assumptions and limits

- Work Done measures the distance from the prior ensemble to the fitted one, not the distance to the true ensemble. Small values can mean a good prior or too little fitting (revised ValDX, `projects/1-ValDX/manuscript/report/7_results_omc.tex` L12, L83). Posted v1 reads small adjustments as a sign the ensemble was already representative ([[@siddiquiFrameworkTestingStructural2026#^c10]]); use the revised reading.
- It is computed through the [[Best–Vendruscolo model]], so it inherits that model's errors ([[model misspecification]]).
- It is not MaxEnt apparent work (the bias energy needed to fit, [[maximum entropy principle]]), nor a [[Kullback–Leibler divergence]] over frame weights. Those measure change in weights; Work Done measures change in the predicted protection profile.
- The patterns suggest causes; the revised manuscript says no single pattern identifies a unique cause (`7_results_omc.tex` L18, L25).
- Equations and the thermodynamic analogy belong in Chapter 3.

## Why it matters here

Introduction §1.5, paragraph 4: Work Done is the "how much did fitting change the hypothesis" half of ValDX's assessment, next to held-out error.

Claims that use this term: [[Work Done quantifies how much an ensemble must be modified to match experiment.]], [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]], [[Low validation error with high Work Done signals agreement reached by excessive modification of the ensemble.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]].
