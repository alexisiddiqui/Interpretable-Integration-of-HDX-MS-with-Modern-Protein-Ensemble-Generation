---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L67
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@noeBoltzmannGeneratorsSampling2019#^c1]]"
  - "[[@noeBoltzmannGeneratorsSampling2019#^c2]]"
code: []
---

## Argument

Noé et al. say Boltzmann generators generate unbiased equilibrium samples in one shot, where simulating these systems otherwise takes vast computational effort in small MD steps.

## Caveats

This is a statement about [[Boltzmann generator|Boltzmann generators]], not machine-learned force fields; do not cite Unke for it. The accuracy is retained only after reweighting ([[@noeBoltzmannGeneratorsSampling2019#^c3]]).

Boltzmann generators are trained on the energy function of the system, not on existing simulations.
