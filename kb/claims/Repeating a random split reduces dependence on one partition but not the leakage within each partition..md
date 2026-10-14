---
type: claim
chapter: 02-background
project: 
basis: inferred
confidence: high
status: draft
origin: kb/concepts/data splitting.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites: 
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
code: []
---

## Argument

Every random partition leaves validation peptides predictable from training peptides that share their residues ([[@siddiquiFrameworkTestingStructural2026#^c8]]). Averaging over many such partitions gives a precise estimate of an optimistic quantity ([[data splitting]]).

## Caveats

Random splitting is appropriate when the sampled units are independent for the intended prediction. For overlapping peptides that condition fails.
