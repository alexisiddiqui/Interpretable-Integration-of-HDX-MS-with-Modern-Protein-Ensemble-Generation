---
type: claim
chapter: 06-jax-ka
project: 4-jax-Ka
basis: stated
confidence: high
status: supported
origin: thesis/chapters/06-jax-ka.tex
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@schlichtkrullModelingRelationalData2018#^c1]]"
code: []
---

## Argument

In an R-GCN, a node's update sums messages from its neighbours, each transformed by a weight matrix specific to the relation that connects them, plus a self-connection ([[@schlichtkrullModelingRelationalData2018#^c1]]). jax-Ka's relational edges apply the same idea inside attention: one key and value projection per relation type (i−2, i−1, i+1, i+2, same chain, other chain), so the model can treat a sequence neighbour differently from a spatial one (`projects/4-jax-Ka/code` `src/pkatrain/production_position.py`, `relation_index`).

## Caveats

R-GCN uses graph convolution, not attention; the correspondence is in the relation-specific projection, not the aggregation.
