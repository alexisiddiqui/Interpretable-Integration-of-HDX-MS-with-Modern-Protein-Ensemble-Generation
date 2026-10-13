---
type: paper
citekey: heninEnhancedSamplingMethods2022
year: 2022
read: false
pdf: kb/_pdf/@heninEnhancedSamplingMethods2022.pdf
extraction: auto
needs_review: false
review_reason:
---

# Enhanced Sampling Methods for Molecular Dynamics Simulations (2022)

## Main point

A LiveCoMS review of enhanced sampling for MD: collective-variable biasing (metadynamics, ABF, umbrella), extended ensembles, and adaptive seeding. Most schemes alter the dynamics to recover equilibrium probabilities, and reweighting needs overlap between biased and unbiased distributions.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Adaptive seeding seeds simulations from regions likely to lead to free-energy barrier crossing. ^c1
  - page: 37
  - quote: "Adaptive seeding thus seeks to seed simulations from regions of space that are likely to lead to free energy barrier crossing"
  - quote_check: pass
  - reviewed: false
- Crossing into regions of space not previously sampled adds valuable information for reconstructing probability distributions. ^c2
  - page: 37
  - quote: "crossing into regions of space not previously sampled adds valuable information to reconstruct probability distributions"
  - quote_check: pass
  - reviewed: false
- In adaptive seeding, simulations are not restrained to a region but are instantiated strategically. ^c3
  - page: 36
  - quote: "the simulations are not restricted to a region with restraints or constraints, but instead are merely instantiated"
  - quote_check: pass
  - reviewed: false
- Many enhanced sampling schemes do not preserve kinetics and are mainly useful for recovering equilibrium probability distributions. ^c4
  - page: 4
  - quote: "many enhanced sampling schemes do not preserve the kinetics of the system, and are therefore primarily useful to recover equilibrium probability distributions"
  - quote_check: pass
  - reviewed: false
- The most efficient sampling methods arguably alter the dynamics as much as possible while preserving thermodynamics. ^c5
  - page: 4
  - quote: "the most efficient sampling methods arguably alter the dynamics as much as possible while preserving thermodynamics"
  - quote_check: pass
  - reviewed: false
- In seeding, the configuration space covered by a set of short simulations is governed by their starting conditions. ^c6
  - page: 15
  - quote: "the configuration space covered by a set of (relatively short) simulations is governed by the choice of their starting conditions"
  - quote_check: pass
  - reviewed: false
- Unbiased statistics can be recovered from biased simulations by reweighting, but only with good overlap between biased and unbiased distributions. ^c7
  - page: 20
  - quote: "unbiased statistics can be recovered by reweighting. Success of this, however, depends crucially on good overlap between the biased and unbiased distributions"
  - quote_check: pass
  - reviewed: false
- Adaptive seeding uses Markov state models to stitch trajectories into a model of both equilibrium populations and conversion rates. ^c8
  - page: 37
  - quote: "not only the equilibrium population of metastable states, but also the rates of conversion between these states"
  - quote_check: pass
  - reviewed: false
- Seeding from low-population microstates enhances exploration but does not necessarily estimate the probability distribution of low free-energy states accurately. ^c9
  - page: 37
  - quote: "well-suited to enhance the exploration of space, but not necessarily to accurately estimate the probability distribution of low free energy states"
  - quote_check: pass
  - reviewed: false

## What I use from it

Introduction §1.3 and [[enhanced sampling]]: biased sampling recovers equilibrium only by reweighting (^c4, ^c7); kinetics are usually lost (^c4, ^c5); adaptive seeding broadens exploration, but populations need an MSM or similar (^c8, ^c9); seeded coverage depends on starting conditions (^c6). See [[sampling coverage]].

## Disagreements / limitations
