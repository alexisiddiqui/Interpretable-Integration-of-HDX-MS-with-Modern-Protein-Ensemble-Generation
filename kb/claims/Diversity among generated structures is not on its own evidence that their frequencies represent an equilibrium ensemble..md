---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/01-introduction.tex#L118
source_state: current
needs_review: true
review_reason: The supporting passages concern MCMC convergence; applying them to learned generators is our inference, and the .tex sentence has no citation yet
figures: []
cites:
  - "[[@bmsb2012ch2#^c9]]"
  - "[[@bmsb2012ch2#^c14]]"
  - "[[@bmsb2012ch2#^c15]]"
code: []
---

## Argument

Ferkinghoff-Borg shows that sampling can be arbitrarily wrong with no diagnostic indication, that slow mixing reduces the effective number of samples, and that reproducibility is the first convergence test ([[Markov chain Monte Carlo]], [[importance sampling]]). Samples can look diverse and still have the wrong frequencies.

## Caveats

Consider adding \supercite{bmsb2012ch2} to the sentence in 01-introduction.tex.
