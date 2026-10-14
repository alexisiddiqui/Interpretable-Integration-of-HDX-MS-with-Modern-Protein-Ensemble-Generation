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
  - "[[@bradshawInterpretationHDXData2020#^c20]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
code: []
---

## Argument

Withholding time points tests extrapolation in time for peptides the fit has seen ([[@bradshawInterpretationHDXData2020#^c20]]). Withholding a random peptide tests little beyond training error because of overlap ([[@siddiquiFrameworkTestingStructural2026#^c8]]). Withholding a sequence region or a structural region tests prediction of unseen parts of the chain or the fold. The unit withheld therefore has to be stated with every validation result ([[data splitting]], [[model selection]]).

## Caveats

The table of units is ours. Which question matters depends on the hypothesis being tested.
