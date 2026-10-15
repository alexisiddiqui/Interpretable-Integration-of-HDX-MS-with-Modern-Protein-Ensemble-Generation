---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: low
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L72
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@zhengMachineLearningGeneration2023#^c5]]"
code: []
---

## Argument

Deep-learning generators can provide multiple starting conformations for subsequent MD sampling (`milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex` L72). Zheng et al. identify seeding additional MD simulations as a use of autoencoder-generated conformations ([[@zhengMachineLearningGeneration2023#^c5]]). ValDX applies this approach by selecting structurally diverse AlphaFold2 predictions before simulation (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L182, L223).

## Caveats

The generator supplies starting conformations. Their subsequent sampling remains subject to the force field and the simulation time available ([[sampling coverage]]).

