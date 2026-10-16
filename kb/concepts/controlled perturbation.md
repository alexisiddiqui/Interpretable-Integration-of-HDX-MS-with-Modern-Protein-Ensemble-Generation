---
type: concept
aliases:
  - controlled perturbations
  - diagnostic perturbation
  - perturbation benchmark
  - controlled comparison
  - data removal
notation: []
sources:
  - "[[@bonomiPrinciplesProteinStructural2017#^c10]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c4]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c5]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c15]]"
---

## Definition

A controlled perturbation changes one suspected deficiency of a fit on purpose, holds the rest fixed, and asks how the result responds. The change can be to the data, the candidates, the forward model or the protocol. Removing part of the input data is the simplest case. A large change in the resulting ensemble is a typical sign of poor accuracy ([[@bonomiPrinciplesProteinStructural2017#^c10]]). Adding structures with known status is another. Plausible intermediates absent from the true ensemble prevented population recovery even when uptake matched ([[@siddiquiFrameworkTestingStructural2026#^c4]]), and entirely incorrect structures reached low training error by exploiting the flexibility of the fit ([[@siddiquiFrameworkTestingStructural2026#^c5]]).

Replicate variation locates instability. Controlled comparisons test whether changing a suspected source of mismatch changes the result. Holding other factors fixed makes the comparison informative, while interactions between deficiencies can limit causal attribution.

## Assumptions and limits

- **One factor at a time.** Holding the starting ensemble fixed controls the comparison but does not exclude interactions between the perturbed factor and other deficiencies.
- **The perturbation must match the suspected cause.** A pattern that points to calibration mismatch is tested by recalibrating before the ensemble is rejected ([[@siddiquiFrameworkTestingStructural2026#^c15]]), not by changing the candidates.
- **Revised ValDX only (draft).** Imposed kinetic mismatch and fitting order (`projects/1-ValDX/manuscript/report/7_results_omc.tex` L189–211), and behaviour under clustering as a diagnostic (L234–235). Not in posted v1.
- **jaxENT only (draft).** Fits of the α-synuclein data against MD of different lengths and a control ensemble, used to separate sampling limits from simulation setup (`projects/2-jaxENT/manuscript/report/results.tex` L207–211). The figure caption's stronger reading conflicts with ValDX ([[replicate uncertainty]]).
- A stable result under perturbation is necessary, not sufficient. Every run can share the same missing state ([[sampling coverage]]).

## Why it matters here

Q1 asks how variation across fits can guide controlled comparisons of possible causes of instability. [[Replicate uncertainty]] locates instability; controlled perturbations test suspected causes such as [[model misspecification]] or limited [[sampling coverage]]. Chapter 2 §2.4 develops these comparisons through cross-validation and competing structural hypotheses. Related validation by held-out data is [[data splitting]].

Claims that use this term: [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]], [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]], [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]], [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]].

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L224`; the historical wording comes from this note before revision, and its evidence remains in the linked source notes and manuscript references.

The primary wording describes a test of a suspected cause. It keeps the interaction limit in the interpretation instead of promising attribution from a single changed factor.

### Historical wording

> Replicate spread shows where a fit is unstable. A controlled perturbation is how the instability is attributed to a cause, because only the perturbed factor differs between the runs being compared.

> Q1 asks how uncertainty can identify sources of instability. Uncertainty localises; controlled perturbations attribute. This is the step between [[replicate uncertainty]] and a statement about [[model misspecification]] or [[sampling coverage]]. Chapter 2 §2.4, "Cross-Validation with Overlapping Measurements" and "Identifiability and Competing Structural Hypotheses". Related validation by held-out data is [[data splitting]].
