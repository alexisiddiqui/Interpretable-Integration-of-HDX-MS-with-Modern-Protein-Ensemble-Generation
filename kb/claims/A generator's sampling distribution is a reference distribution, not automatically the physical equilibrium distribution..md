---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/01-introduction.tex#L12
source_state: current
needs_review: true
review_reason: BMSB shows one generator (TORUSDBN) is right locally and wrong globally; the general statement is our inference
figures: []
cites:
  - "[[@bmsb2012ch4#^c7]]"
  - "[[@bmsb2012ch4#^c4]]"
  - "[[@bmsb2012ch3#^c13]]"
code: []
---

## Argument

Frellsen et al. describe the generator in the [[reference ratio method]] as approximately correct on a local scale but incorrect on a global scale, and its samples alone are not compact native-like structures. Borg et al. identify the reference free energy with the free energy of the prior, the sampler's own distribution. Together these support treating generated populations as a prior ([[importance sampling]]), not as equilibrium populations.

## Caveats

The BMSB example is a local fragment model, not a modern diffusion generator. For learned generators the statement is an inference; a direct source on, for example, AlphaFold or diffusion-model populations versus equilibrium would make it stated.
