---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@heninEnhancedSamplingMethods2022#^c9]]"
  - "[[@heninEnhancedSamplingMethods2022#^c8]]"
code: []
---

## Argument

Hénin et al. state that seeding from low-population microstates is well suited to enhance exploration but not necessarily to estimate the probability distribution of low free-energy states accurately. Populations and rates come from stitching the trajectories together, for example in a Markov state model.

## Caveats

Seeding from low-population macrostates converges free energies better but explores less (same page). Pooled frames from adaptive seeding are not equilibrium populations without such a model or reweighting ([[sampling coverage]]).
