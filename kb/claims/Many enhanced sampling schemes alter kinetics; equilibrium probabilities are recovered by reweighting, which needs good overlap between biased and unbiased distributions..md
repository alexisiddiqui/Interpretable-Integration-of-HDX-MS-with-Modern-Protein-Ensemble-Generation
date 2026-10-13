---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L76
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@heninEnhancedSamplingMethods2022#^c4]]"
  - "[[@heninEnhancedSamplingMethods2022#^c5]]"
  - "[[@heninEnhancedSamplingMethods2022#^c7]]"
code: []
---

## Argument

Hénin et al. state that many enhanced sampling schemes do not preserve the kinetics of the system and are primarily useful to recover equilibrium probability distributions; the most efficient ones alter the dynamics as much as possible while preserving thermodynamics. Unbiased statistics are recovered by reweighting, whose success depends on good overlap between the biased and unbiased distributions.

## Caveats

Some methods do preserve or allow recovery of kinetics (Hénin et al. flag these). This replaces the blanket "loss of equilibrium properties" for metadynamics: what is usually lost is kinetics, and equilibrium is recovered by reweighting.
