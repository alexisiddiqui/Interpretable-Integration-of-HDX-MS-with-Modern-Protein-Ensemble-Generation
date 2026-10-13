---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L67
source_state: current
needs_review: true
review_reason: Conflates machine-learned force fields (Unke) with Boltzmann generators (Noé); see the MLFF vs Boltzmann generator claim.
figures: []
cites:
  - "[[@unkeBiomolecularDynamicsMachinelearned2024#^c1]]"
code: []
---

## Argument

Unke et al. build machine-learned force fields by training on ab initio reference data to predict energies and forces, which is a learned physical energy surface.

## Caveats

Use [[Machine-learned force fields learn energies and forces for simulation, whereas Boltzmann generators generate configurations and reweight them to the Boltzmann distribution.]] to keep the two apart.

The training data are quantum-chemical reference data on molecular fragments, not existing simulations, and the paper is about force fields for MD rather than ensemble generation.
