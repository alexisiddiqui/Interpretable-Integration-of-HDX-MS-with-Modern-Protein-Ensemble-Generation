---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L28
source_state: current
needs_review: true
review_reason: The sources say error modelling reduces over-fitting, not that refinement is free of it; minimal ensembles are not stated.
figures: []
cites:
  - "[[@hummerBayesianEnsembleRefinement2015#^c3]]"
  - "[[@cesariUsingMaximumEntropy2018#^c2]]"
  - "[[@cesariUsingMaximumEntropy2018#^c3]]"
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c3]]"
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c4]]"
code: []
---

## Argument

Ahmed et al. integrate new SAXS data with MD simulations by Bayesian and [[maximum entropy principle]] reweighting that minimally modifies the prior ensemble. Cesari et al. describe an ensemble-reweighting-of-SAXS method and say modelling experimental errors reduces over-fitting. Hummer and Köfinger show their optimal Bayesian ensemble matches the maximum-entropy EROS formulation.

## Caveats

None of the checked papers describes 'minimal ensembles' in the sense of a small set of structures (Hummer and Köfinger explicitly exclude minimal-set refinement), and the claim about capturing essential biological dynamics is not directly stated. The support is for the combination of SAXS, MD and maximum-entropy reweighting with error treatment.

Drop "without overfitting" when reusing this ([[overfitting]]).
