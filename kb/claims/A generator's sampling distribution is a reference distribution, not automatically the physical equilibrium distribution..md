---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/01-introduction.tex#L12
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@bmsb2012ch4#^c7]]"
  - "[[@bmsb2012ch4#^c4]]"
  - "[[@bmsb2012ch3#^c13]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c7]]"
code: []
---

## Argument

Frellsen et al. describe the generator in the [[reference ratio method]] as approximately correct on a local scale but incorrect on a global scale, and its samples alone are not compact native-like structures. Borg et al. identify the reference free energy with the free energy of the prior, the sampler's own distribution. Together these support treating generated populations as a prior ([[importance sampling]]), not as equilibrium populations.

## Caveats

Abramson et al. state that AF3's repeated random seeds do not approximate the solution ensemble, a direct modern case.

The BMSB example is a local fragment model, not a modern diffusion generator. For learned generators the statement is an inference; a direct source on, for example, AlphaFold or diffusion-model populations versus equilibrium would make it stated.
