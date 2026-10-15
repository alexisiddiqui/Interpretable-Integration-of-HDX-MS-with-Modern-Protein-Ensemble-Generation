---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L76
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@bussiUsingMetadynamicsExplore2020#^c1]]"
  - "[[@bussiUsingMetadynamicsExplore2020#^c2]]"
  - "[[@heninEnhancedSamplingMethods2022#^c4]]"
code: []
---

## Argument

Bussi and Laio say the effectiveness of metadynamics is strongly influenced by the choice of collective variables, and that its dynamics are biased by an external potential made of a sum of Gaussians. Hénin et al. say many enhanced sampling schemes do not preserve the kinetics of the system and are primarily useful for recovering equilibrium probability distributions.

## Caveats

[[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]] states the kinetics limitation for enhanced sampling in general. Its application to metadynamics follows from the biased dynamics (step ours). The CV-dependence is stated by Bussi and Laio.

Partial support for the computational requirements. Bussi and Laio p4 say that with large Gaussians the system is strongly out of equilibrium, and p6 says filling a multidimensional space becomes more expensive as the number of CVs grows. Neither passage states complex computational requirements in general terms. Bussi and Laio also say well-tempered metadynamics reaches a quasi-equilibrium state in which the bias gives an exact estimator for the free energy, which is why the claim names kinetics and not equilibrium properties.
