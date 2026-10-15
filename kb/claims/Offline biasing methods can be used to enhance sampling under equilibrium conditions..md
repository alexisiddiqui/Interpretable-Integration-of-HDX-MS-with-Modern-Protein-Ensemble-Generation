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
  - "[[@heninEnhancedSamplingMethods2022#^c3]]"
code: []
---

## Argument

Henin et al. describe adaptive seeding methods, which restart simulations from regions likely to lead to barrier crossing and are the closest match to offline methods in the review. The simulations are not restrained but merely instantiated, so each runs without bias.

## Caveats

Equilibrium conditions describe each seeded simulation, not the pooled frames. [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]]

Henin et al. do not use the term offline biasing, which is the author's term for adaptive seeding. Li and Ma (2025) is a likely mis-citation here, since it is about biasing true reaction coordinates, which is an online biasing method.

## Unverified citations

- [[@liEnhancedSamplingProtein2025]]: no passage supporting this claim found
