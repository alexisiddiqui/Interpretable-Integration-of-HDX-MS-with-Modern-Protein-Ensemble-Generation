---
type: concept
aliases:
  - misspecification
  - misspecified model
  - forward-model error
  - forward-model mismatch
  - kinetic misspecification
  - compensation
  - calibration mismatch
  - miscalibration
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

## Three failures that are easily conflated

Three different things are called forward-model error, and they call for different responses (labels ours).

- **Parameter uncertainty.** The coefficients are right in form but imprecisely known. It shows as the posterior width of $\beta_C$ and $\beta_H$, or as their spread across replicate fits ([[nuisance parameter]], [[replicate uncertainty]]). More or better data narrow it.
- **Miscalibration.** The fixed coefficients are wrong for these conditions. Refitting them restores uptake agreement ([[@siddiquiFrameworkTestingStructural2026#^c7]]), and should be tried before the ensemble is rejected ([[@siddiquiFrameworkTestingStructural2026#^c15]]).
- **Inadequate functional form.** No coefficients reproduce the data, because the model's structure is wrong. Kinetic mismatch, EX1 behaviour and non-native contacts are the HDX examples. Refitting restores uptake agreement without recovering the populations, so agreement after recalibration does not validate the form (revised ValDX, `projects/1-ValDX/manuscript/report/7_results_omc.tex` L248).

The row that is operating decides the advice. Recalibration answers the second and hides the third.

## Assumptions and limits

- The error model's $\sigma$ describes random error. Systematic forward-model error is not covered unless it is modelled through the parameters ([[forward model]], [[nuisance parameter]]). Including experimental error reduces overfitting ([[@cesariUsingMaximumEntropy2018#^c2]]) but does not correct a wrong forward model. The other sources of uncertainty are tabulated in [[experimental uncertainty]].
- Compensation works in both directions. Weights can absorb forward-model error, and forward-model parameters can absorb a poor ensemble. Fitting both together raises an identifiability question ([[inverse problem]]).
- The revised ValDX manuscript benchmarks kinetic misspecification. Errors in assumed exchange kinetics drive compensatory population changes, and calibration restores uptake agreement without recovering the target populations (`7_results_omc.tex` L189–211, L248). This is not in posted v1, so it is not yet evidence.
- Fitting order matters because weights and BV coefficients can absorb the same disagreement. Under the imposed kinetic mismatch, fitting BV parameters first restored uptake agreement and limited additional population distortion (revised ValDX, L189–211, draft). The advice is conditional on the suspected mismatch, not a general fitting order, and restored agreement still validates neither kinetics nor populations. Comparing orders is a [[controlled perturbation]]; jaxENT's joint fit raises the same identifiability question.
- What is averaged over frames, log protection factor, rate or uptake, is itself a forward-model choice, and jaxENT's held-out error and population recovery can favour different choices ([[Evaluation design (jaxENT)]]).
- The confirmation's "systematic errors accumulate at the peptide level" has no supporting citation. Use the narrower BV-coefficient claim instead.

## Why it matters here

Introduction §1.5, paragraph 3: matching uptake after fitting weights and parameters is consistent with a wrong ensemble *and* a wrong model. ValDX's staged fitting and jaxENT's joint fitting both have to face this. Chapter 3 holds the kinetic benchmark. Chapter 2 §2.5 uses the three-way split to say which failure a diagnostic can detect.

Claims that use this term: [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]], [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[Recalibrating forward-model coefficients can correct a miscalibration but not an inadequate functional form.]].
