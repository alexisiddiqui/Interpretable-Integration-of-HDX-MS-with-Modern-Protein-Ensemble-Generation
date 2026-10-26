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
  - "[[@cesariUsingMaximumEntropy2018#^c6]]"
  - "[[@cesariUsingMaximumEntropy2018#^c7]]"
  - "[[@cesariUsingMaximumEntropy2018#^c15]]"
code: []
---

## Argument

Cesari et al. say that the [[maximum entropy principle]] gives, among the distributions satisfying the experimental constraints, the one closest to the prior, and that accounting for experimental errors is fundamental to reducing over-fitting. If the prior is reasonable, a minimal correction is expected to be a good choice. With an MD force field as the prior, the prior at thermal equilibrium is the Boltzmann distribution, and a set of frames sampled from it starts with uniform weights (step ours).

## Caveats

The paper does not say that MaxEnt avoids overfitting without modelling experimental error, or that the result is physically plausible whatever the prior. It warns that the principle should be used with care when force fields perform poorly (p19) and that enforcing data inconsistent with the prior can severely distort the posterior (p11). 'Physically plausible' is not used, so the claim says close to the prior.

[[Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is expected to be a good choice when the prior is reasonable.]] states the error-modelling condition on its own. ValDX shows fitted ensembles can match uptake with the wrong populations ([[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]]).
