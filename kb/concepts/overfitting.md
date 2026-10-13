---
type: concept
aliases:
  - over-fitting
  - overfit
  - generalisation
  - generalization
  - training error
  - validation error
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c5]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c6]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c2]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c3]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c11]]"
  - "[[@cesariUsingMaximumEntropy2018#^c2]]"
  - "[[@cesariUsingMaximumEntropy2018#^c7]]"
---

## Definition

A model overfits when it reproduces the data it was fitted to by exploiting its flexibility, rather than by capturing what generated the data. Its error on the training data is then low but says little about the truth. Generalisation is the opposite test: does the fitted model predict data it was not fitted to?

For ensemble reweighting, an ensemble of incorrect structures can reach low training error simply through the flexibility of the fit ([[@siddiquiFrameworkTestingStructural2026#^c5]]). Experimental agreement alone cannot separate a representative ensemble from one forced into agreement ([[@siddiquiFrameworkTestingStructural2026#^c6]]). In the TeaA benchmark, ensembles with similar training error recovered different populations ([[@siddiquiFrameworkTestingStructural2026#^c2]], [[@siddiquiFrameworkTestingStructural2026#^c3]]).

## Assumptions and limits

- Regularisation and error models *reduce* overfitting. Cesari et al. call modelling experimental error fundamental to reduce it ([[@cesariUsingMaximumEntropy2018#^c2]]), and minimal correction is a good choice only if the prior is reasonable ([[@cesariUsingMaximumEntropy2018#^c7]]). Neither guarantees a correct ensemble ([[regularisation]], [[maximum entropy principle]]).
- Held-out error is only as independent as the split. Overlapping peptides leak information ([[data splitting]]).
- Low validation error together with high [[Work Done]] signals agreement reached by excessive modification ([[@siddiquiFrameworkTestingStructural2026#^c11]]). This is a diagnostic pattern, not a threshold.
- Overfitting is one way a fit misleads. [[model misspecification]] and missing candidates ([[sampling coverage]]) can also give a good fit to the wrong ensemble, and held-out error does not tell these apart.

## Why it matters here

Introduction §1.5, paragraph 4. This is why ValDX reports validation error and Work Done rather than training error, and why the thesis does not say that MaxEnt "avoids overfitting".

Claims that use this term: [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], [[Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is a good choice only when the prior is reasonable.]], [[Low validation error with high Work Done signals agreement reached by excessive modification of the ensemble.]], [[MaxEnt reweighting avoids overfitting and ensures the resulting ensemble remains physically plausible.]].
