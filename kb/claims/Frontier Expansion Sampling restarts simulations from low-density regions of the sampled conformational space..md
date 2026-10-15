---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L82
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@zhangFrontierExpansionSampling2020#^c1]]"
code: []
---

## Argument

Frontier Expansion Sampling identifies low-density regions in a coordinate representation of the current ensemble and selects structures there to seed further simulations ([[enhanced sampling]]). Zhang and Gong proposed the method to improve conformational sampling ([[@zhangFrontierExpansionSampling2020#^c1]]). The confirmation manuscript describes the iterative seed-selection procedure (`milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex` L82).

## Caveats

Zhang and Gong call the method FEXS. They note that boosting sampling around frontier structures may disrupt the Boltzmann distribution of sampled structures (p2), so broader coverage does not establish accurate conformational populations.

