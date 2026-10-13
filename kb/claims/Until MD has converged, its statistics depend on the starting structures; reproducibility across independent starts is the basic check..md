---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L25
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@heninEnhancedSamplingMethods2022#^c6]]"
  - "[[@bmsb2012ch2#^c14]]"
  - "[[@bmsb2012ch2#^c15]]"
code: []
---

## Argument

Hénin et al. state that the configuration space covered by a set of short simulations is governed by their starting conditions. Ferkinghoff-Borg (BMSB ch2) warns that slow mixing reduces the effective number of samples and can mislead, and that the first test should always be the reproducibility of the sampling.

## Caveats

BMSB writes about Markov chain Monte Carlo; MD with a thermostat is the same kind of sampler ([[Markov chain Monte Carlo]]). ValDX compares MD-1Start with MD-10Start, which is this check.
