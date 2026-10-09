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
review_reason: Support is partial or indirect
figures: []
cites:
  - "[[@unkeBiomolecularDynamicsMachinelearned2024#^c1]]"
code: []
---

## Argument

Unke et al. build machine-learned force fields by training on ab initio reference data to predict energies and forces, which is a learned physical energy surface.

## Caveats

The training data are quantum-chemical reference data on molecular fragments, not existing simulations, and the paper is about force fields for MD rather than ensemble generation.
