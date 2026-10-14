---
type: claim
chapter: 02-background
project:
basis: stated
confidence: high
status: supported
origin: thesis/chapters/02-background.tex#L79
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@bmsb2012ch8#^c7]]"
  - "[[@bmsb2012ch8#^c1]]"
code: []
---

## Argument

Ordinary least-squares superposition assumes equal atomic variances and independent atoms, and can be inaccurate when either fails ([[@bmsb2012ch8#^c1]]). In simulated ensembles with known covariance, the covariance estimated after least-squares superposition was biased and showed a strong artefactual pattern of correlation ([[@bmsb2012ch8#^c7]]). RMSF and dynamic cross-correlation are computed after such an alignment ([[positional covariance]]).

## Caveats

Theobald's evidence comes from simulated structures drawn from a matrix normal model. How large the artefact is in a given MD ensemble depends on how heterogeneous its fluctuations are and on which atoms are used for the fit.
