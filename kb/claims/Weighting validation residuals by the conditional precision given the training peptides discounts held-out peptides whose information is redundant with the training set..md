---
type: claim
chapter: 02-background
project: 2-jaxENT
basis: inferred
confidence: medium
status: draft
origin: projects/2-jaxENT/code/jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L47
source_state: current
needs_review: false
review_reason: 
figures: []
cites: []
code: 
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L47-L62
---

## Argument

Inverting the full peptide covariance and then taking the validation block gives the conditional precision of the validation peptides given the training peptides. A held-out peptide that the training peptides already predict, through shared or co-moving residues, carries little conditional information and receives little weight ([[error covariance]]). This addresses the dependence that structured splits leave behind by weighting instead of partitioning ([[data splitting]]).

## Caveats

Holds for the inverse-then-split selector only. Splitting first and then inverting gives the marginal precision, which does not condition on the training block. Which block the reported results used is recorded in [[Observation weighting and selection (jaxENT)]].
