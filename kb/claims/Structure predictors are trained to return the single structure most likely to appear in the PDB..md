---
type: claim
chapter: 02-background
project:
basis: stated
confidence: high
status: supported
origin: thesis/chapters/02-background.tex#L40
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@jumperHighlyAccurateProtein2021#^c7]]"
  - "[[@jumperHighlyAccurateProtein2021#^c5]]"
code: []
---

## Argument

AlphaFold2 is trained on PDB structures to produce the structure most likely to appear in the PDB ([[protein structure predictor]]).

## Caveats

"Single" is ours: the training target is one structure per input; diversity comes from perturbing inputs ([[MSA subsampling]]).
