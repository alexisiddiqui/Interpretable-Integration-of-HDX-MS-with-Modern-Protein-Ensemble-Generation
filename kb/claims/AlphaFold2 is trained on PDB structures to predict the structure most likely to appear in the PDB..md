---
type: claim
aliases:
  - "Structure predictors are trained to return the single structure most likely to appear in the PDB."
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

AlphaFold2 is trained on PDB structures to predict the structure most likely to appear in the PDB ([[@jumperHighlyAccurateProtein2021#^c5]], [[@jumperHighlyAccurateProtein2021#^c7]]; [[protein structure predictor]]). This training target does not assign relative solution populations to alternative predictions.

## Caveats

The training-target statement concerns AlphaFold2. Deliberately perturbing its input can produce diverse candidates ([[MSA subsampling]]); their frequencies require a separate assessment before they are interpreted as conformational populations.

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L149`. The historical wording comes from this note before revision, with its original source in `origin` and its evidence links retained in `cites`.

The primary wording names AlphaFold2, the model described by the evidence, and removes the implication that every structure predictor has the same single-output formulation.

### Historical title

> Structure predictors are trained to return the single structure most likely to appear in the PDB.

### Historical argument

> AlphaFold2 is trained on PDB structures to produce the structure most likely to appear in the PDB ([[protein structure predictor]]).

### Historical caveats

> "Single" is ours: the training target is one structure per input; diversity comes from perturbing inputs ([[MSA subsampling]]).
