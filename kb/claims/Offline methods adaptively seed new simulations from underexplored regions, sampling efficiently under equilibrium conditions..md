---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@heninEnhancedSamplingMethods2022#^c1]]"
  - "[[@heninEnhancedSamplingMethods2022#^c2]]"
  - "[[@heninEnhancedSamplingMethods2022#^c3]]"
  - "[[@heninEnhancedSamplingMethods2022#^c9]]"
code: []
---

## Argument

Henin et al. describe adaptive seeding as starting simulations from regions likely to lead to barrier crossing, because crossing into regions not previously sampled adds information, and note that simulations are not restrained but merely instantiated.

## Caveats

Hénin et al. state that seeding from low-population states enhances exploration but not necessarily the estimate of the probability distribution. See [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]].

Each seeded simulation runs without bias, since the simulations are instantiated and not restrained (^c3), so equilibrium conditions describe the dynamics. They do not describe the pooled frames, whose frequencies are not populations (^c9). Henin et al. do not state that seeding samples more efficiently, and they do not use the term offline biasing. That term is the author's for what they call adaptive seeding.
