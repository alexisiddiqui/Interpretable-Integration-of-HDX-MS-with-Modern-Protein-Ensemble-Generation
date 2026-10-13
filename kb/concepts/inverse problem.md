---
type: concept
aliases:
  - inverse problems
  - ill-posed problem
  - ill-posed
  - identifiability
  - inferential structure determination
  - ISD
notation: []
sources:
  - "[[@bmsb2012ch12#^c8]]"
  - "[[@bmsb2012ch12#^c9]]"
  - "[[@bmsb2012ch12#^c11]]"
  - "[[@bmsb2012ch12#^c12]]"
  - "[[@bmsb2012ch12#^c13]]"
  - "[[@bmsb2012ch12#^c14]]"
  - "[[@bmsb2012ch13#^c2]]"
  - "[[@bmsb2012ch13#^c4]]"
---

## Definition

An inverse problem infers causes (a structure, an ensemble, model parameters) from their measured effects. Structural data are related to structure only through a [[forward model]], and they rarely determine it uniquely. Low-information data are ill-posed: many solutions fit equally well. The Bayesian approach does not invert the data directly. It assigns a posterior probability to every candidate structure and parameter set by combining a prior with the likelihood from the forward and error models. The posterior is then the whole answer, including its uncertainty.

## Equations

$$ p(x,\theta,\sigma \mid s^\text{exp}) \;\propto\; \prod_i \rho_\text{err}\!\left(s_i^\text{exp} \,\middle|\, s_i(x;\theta),\, \sigma_i\right)\, P_0(x)\, p(\theta)\, p(\sigma) $$
^eq-isd-posterior

Source: [[@bmsb2012ch12#^c11]], Eq. (12.2), p. 6; Eq. (12.9), p. 9 ([[@bmsb2012ch12#^c14]]). Habeck writes the prior over structures as $\pi(x) = e^{-\beta E(x)}/Z(\beta)$ and the nuisance parameters as $\alpha$ and $\sigma$ (notation: [[@bmsb2012ch12#Notation]]).

## Derivation

1. Apply [[Bayes' theorem#^eq-bayes]] to the joint unknowns: the structure $x$ and the nuisance parameters $\theta, \sigma$ ([[@bmsb2012ch12#^c11]], Eq. 12.2).
2. Take the parameters as a priori independent of the structure and of each other, so the prior factorises (Eq. 12.3, p. 7; Eq. 12.9).
3. Use the force field's Boltzmann distribution as the structure prior, $P_0(x) \propto e^{-U(x)/k_BT}$ ([[@bmsb2012ch12#^c13]], Eq. 12.7, p. 8; [[Boltzmann distribution#^eq-boltzmann]]).
4. Build the likelihood from the forward and error models ([[forward model#^eq-likelihood]]).
5. Drop the evidence $p(s^\text{exp})$: it does not depend on $x$, so it is not needed to infer the structure ([[@bmsb2012ch12#^c12]], p. 7). It is needed to compare models ([[Bayes' theorem#^eq-bayes-factor]]).
6. For ensemble-averaged data the unknown is a set of weights over candidate conformers, not one structure. The same construction then gives a posterior over $w$, with a prior that keeps $w$ near $w^0$. MaxEnt reweighting is the case where that prior is $e^{-D_\text{KL}(w\Vert w^0)}$ (step ours; [[maximum entropy principle]], step 8).

## Assumptions and limits

- Ill-posedness: when data are low in information, regularisation or a prior is needed to select one solution among the many that fit ([[@bmsb2012ch13#^c4]], p. 9; [[@bmsb2012ch13#^c2]]). See [[regularisation]].
- Habeck's ISD infers a single structure and its uncertainty. The thesis infers populations, so its posterior spread and its ensemble are different things ([[posterior uncertainty]]).
- The posterior is only as good as the forward model and the prior. Both enter the result.

## Why it matters here

The introduction (§1.4) frames HDX-MS integration as an inverse problem: uptake constrains an ensemble only through a forward model, and the weights and forward-model parameters are inferred together. Identifiability is the reason ValDX validates fits on held-out data and jaxENT reports uncertainty from replicates.

Claims that use this term: [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]], [[Interpreting dynamics measurements in structural terms is a grand challenge, as they can be indirect or ensemble-averaged.]], [[In a Bayesian description, a prior and a likelihood combine into a posterior over unknown structures and parameters.]], [[A change in HDX-MS uptake shows a change in protection but does not on its own identify the structural mechanism.]], [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]].
