---
type: claim
chapter: 02-background
project: 
basis: inferred
confidence: high
status: draft
origin: kb/concepts/experimental uncertainty.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites: 
  - "[[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c1]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c2]]"
code: []
---

## Argument

Repeatability is one component of precision ([[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c1]]), and an error estimate from repeats is a lower bound because it misses systematic error ([[@bonomiPrinciplesProteinStructural2017#^c2]]). ValDX's 5 % RSD time-point filter therefore removes imprecise time points and says nothing about back-exchange or forward-model bias ([[experimental uncertainty]]).

## Caveats

The inference joins two sources. The ValDX filter is described at `6_methods_omc.tex` L61.
