---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L84
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@zhangFrontierExpansionSampling2020#^c2]]"
code: []
---

## Argument

Zhang and Gong select simulation seeds using only the Cartesian coordinates of backbone or C-alpha atoms ([[@zhangFrontierExpansionSampling2020#^c2]]). ValDX extends the approach to sample concurrently from starting structures with different topologies (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L254, L769).

## Caveats

The coordinate representation is described by Zhang and Gong; the multiple-topology extension is ValDX's T-FES implementation.

