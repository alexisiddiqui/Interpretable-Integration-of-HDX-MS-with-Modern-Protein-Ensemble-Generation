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
  - evidence
  - marginal likelihood
  - Bayes factor
  - model comparison
notation:
  - {symbol: 's^\text{exp}', meaning: 'all measured values (the data)', units: null}
  - {symbol: '\mathcal{M}', meaning: 'a model or hypothesis under comparison', units: null}
  - {symbol: 'p(s^\text{exp} \mid \mathcal{M})', meaning: 'evidence (marginal likelihood) of model M', units: null}
  - {symbol: 'B_{12}', meaning: 'Bayes factor of model 1 against model 2', units: null}
sources:
  - "[[@bmsb2012ch1#^c1]]"
  - "[[@bmsb2012ch1#^c2]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c7]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c8]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c3]]"
  - "[[@bmsb2012ch1#^c6]]"
  - "[[@bmsb2012ch1#^c5]]"
  - "[[@bmsb2012ch12#^c12]]"
  - "[[@bmsb2012ch12#^c16]]"
  - "[[@bmsb2012ch13#^c8]]"
  - "[[@bmsb2012ch2#^c3]]"
---

## Definition

Bayes' theorem updates a prior belief about a hypothesis or model in the light of data. The posterior is proportional to the likelihood, which carries the information in the data, times the prior, which carries what was known before. In ensemble refinement, the "model" is a probability density over conformations. Maximising the posterior functional over such densities gives an optimal reweighted ensemble. For discrete configurations, this is identical to the maximum-entropy solution.

## Equations

$$ p(x \mid s^\text{exp}) = \frac{p(s^\text{exp} \mid x)\, P_0(x)}{p(s^\text{exp})} \;\propto\; p(s^\text{exp} \mid x)\, P_0(x) $$
^eq-bayes

Source: [[@bmsb2012ch1#^c1]], Eq. (1.1), p. 5, written for a hypothesis $h$ and data $d$ (notation: [[@bmsb2012ch1#Notation]]); [[@hummerBayesianEnsembleRefinement2015#^c7]], Eq. (1), p. 2 (notation: [[@hummerBayesianEnsembleRefinement2015#Notation]]). With nuisance parameters, see [[inverse problem#^eq-isd-posterior]].
Manuscript form: none displayed. The HDXer loss of milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L142 is a negative log-posterior: apparent work as a log-prior plus a Gaussian error likelihood $\rho_\text{err}$.

$$ B_{12} = \frac{p(s^\text{exp} \mid \mathcal{M}_1)}{p(s^\text{exp} \mid \mathcal{M}_2)} = \frac{\int p(s^\text{exp} \mid \theta_1, \mathcal{M}_1)\, p(\theta_1 \mid \mathcal{M}_1)\, d\theta_1}{\int p(s^\text{exp} \mid \theta_2, \mathcal{M}_2)\, p(\theta_2 \mid \mathcal{M}_2)\, d\theta_2} $$
^eq-bayes-factor

Source: [[@bmsb2012ch1#^c6]], Eq. (1.6), p. 25, written there with data $\mathbf{d}$ and models $M_1, M_2$. The evidence integral is also Eqs. (13.23)–(13.24) of BMSB ch13, and a ratio of partition functions $Z/Z_\pi$ in BMSB ch2 (Eq. 2.5, p. 5; [[@bmsb2012ch2#^c3]]).

## Derivation

1. Hummer and Köfinger maximise the Bayesian posterior functional over ensemble densities $p(x)$, with a reference distribution $p_0(x)$ as prior ([[@hummerBayesianEnsembleRefinement2015#^c8]], Eqs. (21) and (24)).
2. For discrete configurations, the optimal ensemble equals that of the maximum-entropy EROS formulation ([[@hummerBayesianEnsembleRefinement2015#^c3]]). The same weights follow from the [[maximum entropy principle]] when the error model is included.
3. To compare models instead of inferring parameters, keep the evidence $p(s^\text{exp})$, which parameter inference can drop. Integrating the parameters out gives the Bayes factor, which works like a likelihood ratio without fixing the parameters at their best values ([[@bmsb2012ch1#^c6]], Eq. 1.6). The model to prefer is the one for which measuring the data shrinks the accessible parameter volume least, an automatic Occam factor ([[@bmsb2012ch13#^c8]], p. 18).

## Assumptions and limits

- Structure determination can ignore the evidence ([[@bmsb2012ch12#^c12]], p. 7); model comparison cannot.
- A single best structure (MAP) only locates one maximum of the posterior ([[@bmsb2012ch12#^c16]], p. 13). It is a fair summary only when the posterior is sharply peaked and unimodal ([[@bmsb2012ch1#^c5]], p. 11). See [[posterior uncertainty]].

- Results depend on the prior (the force field, or the generator) and on the error model in the likelihood (typically Gaussian, uncorrelated). Hummer and Köfinger assume uncorrelated errors in their Eq. (4).
- The confidence parameter that trades prior against likelihood ($\gamma$ in the HDXer loss above) is not set by the theorem. It has to be chosen, and ValDX uses validation to choose it.

## Why it matters here

The Bayesian reading turns reweighting into inference: the fitted weights become a posterior, so uncertainty in them is meaningful. That is the frame for the jaxENT chapter's replicate-based uncertainty and for comparing MaxEnt with Bayesian refinement in Chapter 2. The Bayes factor is the Bayesian answer to comparing candidate ensembles or forward models, which ValDX approaches through validation instead.

Claims that use this term: [[SAXS ensembles have been refined against scattering profiles using Bayesian inference and maximum entropy reweighting.]], [[In a Bayesian description, a prior and a likelihood combine into a posterior over unknown structures and parameters.]].
