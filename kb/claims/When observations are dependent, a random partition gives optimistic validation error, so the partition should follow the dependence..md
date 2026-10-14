---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: high
status: draft
origin: kb/concepts/data splitting.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites: []
code: []
---

## Argument

A validation set that is predictable from the training set measures interpolation, not the prediction the model is meant to make. Partitions that block the dependence, by region, group or structure, withhold the right kind of information ([[data splitting]]). The general source on validation with dependent observations is not yet in the vault.

## Caveats

Which partition is right depends on the intended prediction. ValDX uses two complementary partitions for that reason ([[Withholding a time point, a peptide, a sequence region or a structural region asks different predictive questions.]]).
