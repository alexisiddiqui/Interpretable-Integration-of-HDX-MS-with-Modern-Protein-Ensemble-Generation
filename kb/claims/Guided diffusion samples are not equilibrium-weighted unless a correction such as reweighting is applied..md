---
type: claim
chapter: 02-background
project:
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/02-background.tex#L66
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c10]]"
  - "[[@wangProteinConformationGeneration2024#^c4]]"
code: []
---

## Argument

Guidance changes the sampling distribution but computes no importance weights. ExEnDiff concedes it does not give accurate free-energy differences, and ConfDiff's target is the generator's distribution tilted by a Boltzmann factor, not the Boltzmann distribution itself ([[guided diffusion]], [[importance sampling]]).

## Caveats

ExEnDiff's abstract claims the samples capture the underlying Boltzmann distribution (^c2); ConfDiff calls force guidance reweighting (^c7).
