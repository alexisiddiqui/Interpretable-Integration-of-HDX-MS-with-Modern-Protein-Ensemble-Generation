---
type: claim
aliases:
  - "Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is a good choice only when the prior is reasonable."
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
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

Accounting for experimental error reduces overfitting in MaxEnt reweighting. Minimal correction is expected to be a good choice when the prior is reasonable ([[@cesariUsingMaximumEntropy2018#^c2]], [[@cesariUsingMaximumEntropy2018#^c7]]).

## Caveats

Replaces the confirmation's "avoids overfitting and ensures the resulting ensemble remains physically plausible". Regularisation reduces overfitting but does not validate the fit ([[overfitting]], [[regularisation]]).

## Wording history

The earlier title, "Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is a good choice only when the prior is reasonable.", appeared in the introduction hub and thesis paragraph on held-out validation. The revised wording follows Cesari et al.'s conditional expectation without turning it into a necessary condition.
