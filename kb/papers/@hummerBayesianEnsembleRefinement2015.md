---
type: paper
citekey: hummerBayesianEnsembleRefinement2015
year: 2015
read: false
pdf: kb/_pdf/@hummerBayesianEnsembleRefinement2015.pdf
extraction: auto
needs_review: false
review_reason:
---

# Bayesian Ensemble Refinement by Replica Simulations and Reweighting (2015)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Ensemble refinement is becoming more important as structural biology turns to dynamic and partially disordered biomolecular structures. ^c1
  - page: 1
  - quote: "structural biology enters a new era in which dynamic and partially disordered biomolecular structures come into focus"
  - quote_check: pass
  - reviewed: false
- Dynamic and partially disordered biomolecular systems play central roles in biology, including in disease. ^c2
  - page: 1
  - quote: "play central roles in biology, both in functional cellular processes ranging from signal transduction to the formation of large cellular structures, and in disease"
  - quote_check: pass
  - reviewed: false
- The optimal Bayesian ensemble distribution for discrete configurations is identical to that of the maximum-entropy ensemble-refinement-of-SAXS (EROS) formulation. ^c3
  - page: 1
  - quote: "maximum entropy “ensemble refinement of SAXS” (EROS) formulation"
  - quote_check: pass
  - reviewed: false
- Most experimental observables report on averages over the entire ensemble of structures, so only the appropriate average over a model ensemble should match the experiment. ^c4
  - page: 1
  - quote: "most observables accessible to experiment report on averages over the entire ensemble of structures"
  - quote_check: pass
  - reviewed: false
- Bayesian replica ensemble refinement enhances sampling of relevant configurations by restraining averages of observables in coupled replica molecular dynamics simulations. ^c5
  - page: 1
  - quote: "Bayesian replica ensemble refinement enhances the sampling of relevant configurations by imposing restraints on averages of observables in coupled replica molecular dynamics simulations"
  - quote_check: pass
  - reviewed: false
- Inverse problems are typically ill-conditioned and underdetermined. ^c6
  - page: 2
  - quote: "Inverse problems are typically ill-conditioned, i.e., sensitive to input parameter variations, and underdetermined"
  - quote_check: pass
  - reviewed: false
- Bayes' theorem for model refinement is written as a proportionality without the normalising factor (Eq. 1). ^c7
  - page: 2
  - quote: "written as a proportionality without the normalizing factor"
  - quote_check: pass
  - reviewed: false
- The optimal Bayesian ensemble density is derived by variational maximisation of the posterior functional over ensemble densities. ^c8
  - page: 2
  - quote: "By variational maximization of the Bayesian posterior functional over the ensemble probability densities"
  - quote_check: pass
  - reviewed: false
- For replica refinement to converge to the optimal Bayesian ensemble as the number of replicas goes to infinity, the restraint should scale linearly with the number of replicas. ^c9
  - page: 1
  - quote: "should scale linearly with the number of replicas to ensure convergence to the optimal Bayesian result in the limit of infinitely many replicas"
  - quote_check: pass
  - reviewed: false
- The authors cite Roux and Weare, who found for a Gaussian model with strict constraints that the replica spring constant had to grow faster than linearly in N. ^c10
  - page: 7
  - quote: "the effective spring constant in the biasing potential had to grow faster than linearly in N"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $x$ | a configuration | $x$ |  |
| $y_i(x)$ | error-free value of observable $i$ for configuration $x$ | $s_i(x)$ |  |
| $y_i^\text{(obs)}$ | measured value of observable $i$ | $s_i^\text{exp}$ |  |
| $p_0(x)$ | reference distribution, the prior | $P_0(x)$ |  |
| $p(x)$ | ensemble distribution being refined | $P(x)$ |  |
| $\theta$ | confidence in the reference ensemble | — | weights the prior, like $1/\gamma$; $\theta$ is forward-model parameters |
| $\sigma$ | experimental error | $\sigma_i$ |  |

## What I use from it

## Disagreements / limitations
