---
type: claim
chapter: 02-background
project:
basis: stated
confidence: high
status: supported
origin: thesis/chapters/02-background.tex#L66
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c7]]"
code: []
---

## Argument

In ExEnDiff, too small a restraint weight leaves samples inconsistent with the data, and too large a weight makes the sampling path noisy and the structures unphysical ([[guided diffusion]]).

## Caveats

The weight is a tuning choice without a principled setting, like the restraint constant in [[restrained simulation]].
