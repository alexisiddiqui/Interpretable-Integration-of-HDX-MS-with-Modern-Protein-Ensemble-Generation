---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L21
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c2]]"
  - "[[@bmsb2012ch12#^c13]]"
  - "[[@unkeBiomolecularDynamicsMachinelearned2024#^c2]]"
code: []
---

## Argument

Hollingsworth and Dror state that MD force fields are inherently approximate, and Unke et al. call empirical force fields efficient but less reliable. In BMSB the Boltzmann distribution of the force field is the prior over structures. A converged equilibrium simulation therefore samples the [[Boltzmann distribution]] defined by its [[force field]], and its populations inherit force-field error (step ours).

## Caveats

Needs a canonical thermostatted simulation and converged sampling ([[equilibration and convergence]]). A methods or textbook source stating it directly would make this stated.
