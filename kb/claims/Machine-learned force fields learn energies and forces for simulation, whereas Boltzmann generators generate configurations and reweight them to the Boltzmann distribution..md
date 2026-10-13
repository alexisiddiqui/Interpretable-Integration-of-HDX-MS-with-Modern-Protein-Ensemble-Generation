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
  - "[[@unkeBiomolecularDynamicsMachinelearned2024#^c1]]"
  - "[[@noeBoltzmannGeneratorsSampling2019#^c1]]"
  - "[[@noeBoltzmannGeneratorsSampling2019#^c3]]"
code: []
---

## Argument

Unke et al. train a model on ab initio reference data to predict energies and forces, which is then used to run MD. Noé et al. generate equilibrium samples in one shot, and state that to compute thermodynamics the samples must be reweighted to the Boltzmann distribution. The first improves the [[force field]]; the second is a sampler ([[Boltzmann generator]]).

## Caveats

The confirmation cites the two papers together under "learned force fields"; they belong under different explanations.
