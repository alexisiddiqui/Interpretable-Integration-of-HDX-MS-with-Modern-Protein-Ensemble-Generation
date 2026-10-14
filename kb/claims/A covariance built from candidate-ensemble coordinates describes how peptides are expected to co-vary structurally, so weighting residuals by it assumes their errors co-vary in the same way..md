---
type: claim
chapter: 02-background
project: 2-jaxENT
basis: inferred
confidence: medium
status: draft
origin: projects/2-jaxENT/code/jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L84
source_state: current
needs_review: false
review_reason: 
figures: []
cites: []
code: 
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L84-L121
---

## Argument

jaxENT's coordinate covariance is the residue Cα covariance of the candidate ensemble pushed through the peptide map, $\Sigma = MCM^\top + \lambda I$ (pinned lines). It encodes shared residues and co-moving residues, which is [[positional covariance]] at the peptide level. Using its inverse as a weight treats the residual errors as having that covariance ([[error covariance]], [[Observation weighting and selection (jaxENT)]]).

## Caveats

The assumption is stated here, not tested. The Phase-3 noise-model test rejected a protection-factor-propagated covariance as a Gaussian observation covariance; the selection-time use asks a different question.
