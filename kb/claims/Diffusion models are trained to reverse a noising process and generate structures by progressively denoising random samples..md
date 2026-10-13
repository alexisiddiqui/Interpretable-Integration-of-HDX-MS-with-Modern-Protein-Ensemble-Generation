---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L42
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@yimDiffusionModelsProtein2024#^c6]]"
  - "[[@yimDiffusionModelsProtein2024#^c2]]"
code: []
---

## Argument

Yim et al. describe training as sequentially corrupting examples with additive noise until they are noise, and training a network to reverse the corruption steps. Generation progressively modifies noisy samples toward clean examples ([[diffusion model]]).

## Caveats

The SDE form and score matching are Chapter 2 material.
