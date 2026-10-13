---
type: concept
aliases:
  - Bayes theorem
  - Bayes' rule
  - Bayesian inference
  - Bayesian ensemble refinement
  - posterior
  - likelihood
  - prior
notation: []
sources:
  - "[[@bmsb2012ch1#^c1]]"
  - "[[@bmsb2012ch1#^c2]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c7]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c8]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c3]]"
---

## Definition

Bayes' theorem updates a prior belief about a hypothesis or model in the light of data. The posterior is proportional to the likelihood, which carries the information in the data, times the prior, which carries what was known before. In ensemble refinement, the "model" is a probability density over conformations. Maximising the posterior functional over such densities gives an optimal reweighted ensemble. For discrete configurations, this is identical to the maximum-entropy solution.

## Equations

$$ p(h \mid d) = \frac{p(d \mid h)\, p(h)}{p(d)} \;\propto\; p(d \mid h)\, p(h) $$
^eq-bayes

Source: [[@bmsb2012ch1#^c1]], Eq. (1.1), p. 5; [[@hummerBayesianEnsembleRefinement2015#^c7]], Eq. (1), p. 2.
Manuscript form: none displayed. The HDXer loss of milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L142 is a negative log-posterior: apparent work as a log-prior plus a Gaussian error likelihood $\rho_\text{err}$.

## Derivation

1. Hummer and Köfinger maximise the Bayesian posterior functional over ensemble densities $p(x)$, with a reference distribution $p_0(x)$ as prior ([[@hummerBayesianEnsembleRefinement2015#^c8]], Eqs. (21) and (24)).
2. For discrete configurations, the optimal ensemble equals that of the maximum-entropy EROS formulation ([[@hummerBayesianEnsembleRefinement2015#^c3]]). The same weights follow from the [[maximum entropy principle]] when the error model is included.

## Assumptions and limits

- Results depend on the prior (the force field, or the generator) and on the error model in the likelihood (typically Gaussian, uncorrelated). Hummer and Köfinger assume uncorrelated errors in their Eq. (4).
- The confidence parameter that trades prior against likelihood ($\gamma$ in the HDXer loss above) is not set by the theorem. It has to be chosen, and ValDX uses validation to choose it.

## Why it matters here

The Bayesian reading turns reweighting into inference: the fitted weights become a posterior, so uncertainty in them is meaningful. That is the frame for the jaxENT chapter's replicate-based uncertainty and for comparing MaxEnt with Bayesian refinement in Chapter 2.

Claims that use this term: [[SAXS ensembles have been refined against scattering profiles using Bayesian inference and maximum entropy reweighting.]].
