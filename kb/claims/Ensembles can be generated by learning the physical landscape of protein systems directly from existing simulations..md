---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L67
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@noeBoltzmannGeneratorsSampling2019#^c1]]"
  - "[[@noeBoltzmannGeneratorsSampling2019#^c4]]"
code: []
---

## Argument

Noé et al. say Boltzmann generators are trained by combining training by energy and training by example, and generate unbiased one-shot equilibrium samples of proteins.

## Caveats

Unke et al. were cited here before. Their machine-learned force fields predict energies and forces from ab initio reference data for use in MD, which is a different object from a Boltzmann generator ([[Machine-learned force fields learn energies and forces for simulation, whereas Boltzmann generators generate configurations and reweight them to the Boltzmann distribution.]]).

In Noé et al. training by energy is the main principle, so "from existing simulations" holds only for training by example. The samples must be reweighted to the Boltzmann distribution to compute thermodynamics (^c3).
