---
type: claim
chapter: 06-jax-ka
project: 4-jax-Ka
basis: stated
confidence: high
status: supported
origin: thesis/chapters/06-jax-ka.tex
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@reisPypKaFlexiblePython2020#^c1]]"
code: []
---

## Argument

PypKa solves the Poisson–Boltzmann equation for the electrostatic energies of protonation states and samples the states by Monte Carlo to obtain titration curves and pKa values ([[@reisPypKaFlexiblePython2020#^c1]]). It is the method behind the pKPDB labels that jax-Ka is trained on ([[pKPDB holds PypKa pKa estimates for structures across the PDB, so a model trained on it learns PypKa's pKas, not experimental ones.]]).

## Caveats

Like any continuum method, PypKa depends on its dielectric model and on the single input structure. Its own accuracy against experiment bounds what a model trained on it can reach.
