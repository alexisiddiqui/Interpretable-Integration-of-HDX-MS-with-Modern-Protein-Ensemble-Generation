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

Read together with validation error, low validation error with high Work Done shows agreement reached by substantial modification of the prior (revised `projects/1-ValDX/manuscript/report/7_results_omc.tex` L25; v1 wording [[@siddiquiFrameworkTestingStructural2026#^c11]]; [[overfitting]]). That pattern is consistent with overfitting, but high Work Done can also follow from calibration mismatch or a missing state. It shows that fitting changed the profile substantially, not why.

## Assumptions and limits

- Work Done measures the distance from the prior ensemble to the fitted one, not the distance to the true ensemble. Small values can mean a good prior or too little fitting (revised ValDX, `projects/1-ValDX/manuscript/report/7_results_omc.tex` L12, L83). Posted v1 reads small adjustments as a sign the ensemble was already representative ([[@siddiquiFrameworkTestingStructural2026#^c10]]); use the revised reading.
- It is computed through the [[Best–Vendruscolo model]], so it inherits that model's errors ([[model misspecification]]).
- It is not MaxEnt apparent work (the bias energy needed to fit, [[maximum entropy principle]]), nor a [[Kullback–Leibler divergence]] over frame weights. Those measure change in weights; Work Done measures change in the predicted protection profile.
- The patterns suggest causes; the revised manuscript says no single pattern identifies a unique cause (`7_results_omc.tex` L18, L25).
- **Units are not physics.** Work Done is reported in kJ/mol through a thermodynamic analogy, but it is not physical work. Prior and fitted profiles each use their own frame weights and BV coefficients, so the components can reflect a change in either (revised `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L508–531). Equations are in [[Work Done (ValDX)]]; the full derivation belongs in Chapter 3.
- **Not a distance between profiles (ours).** Work_shape and Work_density depend only on each residue's absolute deviation from the mean log protection factor, and Work_scale only on the mean. Reflecting a profile about its mean leaves all three at zero although protection has been inverted, so distinct profiles can score zero ([[Work Done (ValDX)]], step 3). Validation error still detects such a change.
- **Not an evidence.** [[BICePs]] ranks candidate priors by a Bayesian evidence ratio. Work Done is a diagnostic distance from the prior computed after fitting, and the two are not interchangeable.

## Why it matters here

Introduction §1.5, paragraph 4: Work Done is the "how much did fitting change the hypothesis" half of ValDX's assessment, next to held-out error.

Claims that use this term: [[Work Done quantifies how much an ensemble must be modified to match experiment.]], [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]], [[Low validation error with high Work Done shows agreement reached by substantial modification of the prior.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]], [[Distinct protection profiles can give zero Work Done, so Work Done is not a distance between profiles.]].
