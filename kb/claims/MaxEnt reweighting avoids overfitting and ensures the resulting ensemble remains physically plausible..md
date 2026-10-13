---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: low
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L95
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@cesariUsingMaximumEntropy2018#^c2]]"
  - "[[@cesariUsingMaximumEntropy2018#^c7]]"
code: []
---

## Argument

Cesari et al. say that modelling experimental errors in the [[maximum entropy principle]] is fundamental to reducing over-fitting, and that if the prior is reasonable a minimal correction is expected to be a good choice.

## Caveats

The paper does not say MaxEnt itself avoids overfitting or ensures physical plausibility. Overfitting is reduced only when experimental errors are modelled, and the paper warns that the principle should be used with care when force fields perform poorly (p19) and that enforcing data inconsistent with the prior can severely distort the posterior (p11). 'Physically plausible' is not used.
