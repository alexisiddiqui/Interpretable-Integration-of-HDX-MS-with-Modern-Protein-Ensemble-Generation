---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/01-introduction.tex#L18
source_state: current
needs_review: true
review_reason: AF3 (Abramson ^c7) states it for one modern generator; the general statement, and the MCMC passages, remain our inference.
figures: []
cites:
  - "[[@bmsb2012ch2#^c9]]"
  - "[[@bmsb2012ch2#^c14]]"
  - "[[@bmsb2012ch2#^c15]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c7]]"
code: []
---

## Argument

Ferkinghoff-Borg shows that sampling can be arbitrarily wrong with no diagnostic indication, that slow mixing reduces the effective number of samples, and that reproducibility is the first convergence test ([[Markov chain Monte Carlo]], [[importance sampling]]). Samples can look diverse and still have the wrong frequencies.

## Caveats

Abramson et al. state directly that repeated AF3 seeds do not approximate the solution ensemble.

Consider adding \supercite{bmsb2012ch2} to the sentence in 01-introduction.tex.
