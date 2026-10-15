---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: low
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L15
source_state: current
needs_review: false
review_reason:
figures: []
cites: []
code: []
---

## Argument

The sentence says that physics-based time integration and deep-learning generation each have limitations that combining them overcomes. Henin et al. is a review of enhanced sampling methods for molecular dynamics and contains no passage about combining physics-based sampling with deep-learning generators.

## Caveats

Likely intended source: @zhengMachineLearningGeneration2023 p1 (^c4), which says machine learning can learn low-dimensional representations of conformational space to drive additional MD sampling or directly generate conformations. That passage supports combining machine learning with MD sampling but does not state that each scheme's limitations are overcome by the combination. The cited Henin review has no such passage and is a likely mis-citation.

## Unverified citations

- [[@heninEnhancedSamplingMethods2022]]: no passage supporting this claim found
