---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: high
status: draft
origin: thesis/chapters/01-introduction.tex#L12
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@yimDiffusionModelsProtein2024#^c6]]"
  - "[[@yimDiffusionModelsProtein2024#^c3]]"
code: []
---

## Argument

The diffusion time runs from data to noise along an artificial corrupting process (Yim et al.), and generation reverses it. Successive denoising steps are therefore not a trajectory of the protein in physical time, unlike MD time steps, and say nothing about kinetics (step ours).

## Caveats

Keep three times apart: MD time $t$, HDX labelling time and diffusion time $\tau$ ([[2026-10-13 canonical HDX and ensemble notation]]).
