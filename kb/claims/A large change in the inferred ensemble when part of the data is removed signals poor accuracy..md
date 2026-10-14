---
type: claim
chapter: 02-background
project:
basis: stated
confidence: high
status: supported
origin: thesis/chapters/02-background.tex#L74
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@bonomiPrinciplesProteinStructural2017#^c10]]"
code: []
---

## Argument

Bonomi et al. give data removal as a test of accuracy. If removing a fraction of the input data changes the resulting ensemble a lot, the ensemble is probably inaccurate ([[controlled perturbation]], [[data splitting]]).

## Caveats

The converse does not hold. An ensemble that is stable under data removal can still share a missing state or a forward-model error across every subset ([[replicate uncertainty]], [[sampling coverage]]).
