---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L63
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c2]]"
code: []
---

## Argument

Vani et al. use reduced-MSA AlphaFold2 to generate many possible conformations as the starting point for RAVE simulations.

## Caveats

Vani et al. note that reducing the MSA gives no relative probabilities and introduces thermodynamically improbable structures, which is why they add Boltzmann ranking. They do not state that the sub-sampled ensemble captures dynamics.
