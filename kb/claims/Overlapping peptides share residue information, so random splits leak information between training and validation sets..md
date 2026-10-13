---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L70
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
code: []
---

## Argument

Because peptides overlap, a random split puts peptides in the validation set whose uptake is predictable from training peptides covering similar regions, which inflates apparent validation performance ([[data splitting]]).

## Caveats

Peptide overlap also correlates errors, which most likelihoods assume away ([[forward model]]).
