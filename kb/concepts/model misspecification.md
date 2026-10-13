---
type: concept
aliases:
  - misspecification
  - misspecified model
  - forward-model error
  - forward-model mismatch
  - kinetic misspecification
  - compensation
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c7]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c15]]"
  - "[[@bradshawInterpretationHDXData2020#^c13]]"
  - "[[@cesariUsingMaximumEntropy2018#^c2]]"
---

## Definition

A model is misspecified when no setting of its adjustable parts reproduces the process that generated the data. In ensemble integration the adjustable parts are the frame weights and the forward-model parameters. If the [[forward model]] or the assumed exchange kinetics are wrong, the fit still moves the weights and parameters until the predictions match as well as they can. The mismatch is then absorbed into the quantities being inferred, and a good fit no longer shows that they are right (ours).

In HDX-MS the main case is the [[Best–Vendruscolo model]]. Its optimal coefficients depend on the protein and conditions ([[@bradshawInterpretationHDXData2020#^c13]]), and they mainly compensate for differences between the experimental conditions and those the model was calibrated under ([[@siddiquiFrameworkTestingStructural2026#^c7]]). A pattern that points to calibration mismatch calls for recalibrating before the ensemble is rejected ([[@siddiquiFrameworkTestingStructural2026#^c15]]).

## Assumptions and limits

- The error model's $\sigma$ describes random error. Systematic forward-model error is not covered unless it is modelled through the parameters ([[forward model]], [[nuisance parameter]]). Including experimental error reduces overfitting ([[@cesariUsingMaximumEntropy2018#^c2]]) but does not correct a wrong forward model.
- Compensation works in both directions. Weights can absorb forward-model error, and forward-model parameters can absorb a poor ensemble. Fitting both together raises an identifiability question ([[inverse problem]]).
- The revised ValDX manuscript benchmarks kinetic misspecification. Errors in assumed exchange kinetics drive compensatory population changes, and calibration restores uptake agreement without recovering the target populations (`projects/1-ValDX/manuscript/report/7_results_omc.tex` L189–211, L248). This is not in posted v1, so it is not yet evidence.
- The confirmation's "systematic errors accumulate at the peptide level" has no supporting citation. Use the narrower BV-coefficient claim instead.

## Why it matters here

Introduction §1.5, paragraph 3: matching uptake after fitting weights and parameters is consistent with a wrong ensemble *and* a wrong model. ValDX's staged fitting and jaxENT's joint fitting both have to face this. Chapter 3 holds the kinetic benchmark.

Claims that use this term: [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]], [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[Structure-to-uptake models rely on hydrogen bonding and solvent exposure but add systematic errors that accumulate at peptide level.]].
