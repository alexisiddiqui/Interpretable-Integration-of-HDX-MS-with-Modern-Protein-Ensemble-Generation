---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80
source_state: current
needs_review: true
review_reason: The phrase without distorting the landscape is too strong. Seeding leaves the dynamics unbiased, but pooled frames are not populations (Hénin ^c9).
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

Henin et al. describe adaptive seeding but do not state that it samples more efficiently or leaves the energy landscape undistorted, and they do not use the term offline biasing. The wording of the sentence (offline methods) is the author's term for what Henin et al. call adaptive seeding.
