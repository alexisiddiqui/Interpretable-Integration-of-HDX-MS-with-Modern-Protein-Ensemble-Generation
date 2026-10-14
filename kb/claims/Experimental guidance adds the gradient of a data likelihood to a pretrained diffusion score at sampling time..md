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
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c3]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c6]]"
code: []
---

## Argument

ExEnDiff splits the conditional score by Bayes' rule into the pretrained score and a likelihood gradient, which with a Gaussian likelihood becomes a harmonic restraint added at inference ([[guided diffusion#^eq-guided-score]]).

## Caveats

The likelihood on noisy coordinates is approximated at the posterior mean (ExEnDiff ^c4). ConfDiff adds an energy gradient instead of a data likelihood.
