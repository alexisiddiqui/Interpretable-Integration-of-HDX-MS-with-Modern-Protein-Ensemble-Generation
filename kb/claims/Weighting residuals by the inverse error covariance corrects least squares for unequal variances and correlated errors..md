---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: high
status: supported
origin: kb/concepts/error covariance.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites: 
  - "[[@bmsb2012ch8#^c1]]"
  - "[[@bmsb2012ch8#^c8]]"
code: []
---

## Argument

Ordinary least squares is inaccurate when variances are uneven or observations correlated ([[@bmsb2012ch8#^c1]]), and the correction is to weight by the inverse of the covariance matrix ([[@bmsb2012ch8#^c8]]). This is the Gaussian likelihood with correlated errors ([[error covariance#^eq-gls]]).

## Caveats

Theobald states it for the superposition of structures. The statement is general, but the quoted context is Procrustes analysis, not regression on HDX data.
