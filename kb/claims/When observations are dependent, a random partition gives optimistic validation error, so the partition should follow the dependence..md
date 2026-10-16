---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: high
status: supported
origin: kb/concepts/data splitting.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@robertsCrossvalidationStrategiesData2017#^c1]]"
  - "[[@robertsCrossvalidationStrategiesData2017#^c2]]"
code: []
---

## Argument

A validation set that is predictable from the training set measures interpolation, not the prediction the model is meant to make. Partitions that block the dependence, by region, group or structure, withhold the right kind of information ([[data splitting]]). Roberts et al. find that cross-validation which ignores dependence structure seriously underestimates predictive error, and recommend blocked partitions wherever such structure exists ([[@robertsCrossvalidationStrategiesData2017#^c1]], [[@robertsCrossvalidationStrategiesData2017#^c2]]).

## Caveats

Which partition is right depends on the intended prediction. ValDX uses two complementary partitions for that reason ([[Withholding a time point, a peptide, a sequence region or a structural region asks different predictive questions.]]).
