---
type: paper
citekey: raddiAutomaticForwardModel2025
year: 2025
read: false
pdf: kb/_pdf/@raddiAutomaticForwardModel2025.pdf
extraction: auto
needs_review: false
review_reason:
---

# Automatic Forward Model Parameterization with Bayesian Inference of Conformational Populations (2025)

## Main point

BICePs is extended to refine forward-model parameters together with the ensemble, either by sampling them as nuisance parameters or by variationally minimising the BICePs score. Demonstrated on Karplus J-coupling parameters (toy model and ubiquitin), and stated to generalise to any differentiable forward model.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Forward-model parameters can be treated as nuisance parameters and integrated over in the full posterior. ^c1
  - page: 1
  - quote: "The first method treats FM parameters as nuisance parameters, integrating over them in the full posterior distribution"
  - quote_check: pass
  - reviewed: false
- Alternatively, forward-model parameters can be optimised by variational minimisation of the BICePs score. ^c2
  - page: 1
  - quote: "The second method employs variational minimization of a quantity called the BICePs score"
  - quote_check: pass
  - reviewed: false
- The BICePs score reports the free energy of turning on the experimental restraints. ^c3
  - page: 1
  - quote: "reports the free energy of “turning on” the experimental restraints"
  - quote_check: pass
  - reviewed: false
- Refining forward models requires accounting for random and systematic errors in the experimental data. ^c4
  - page: 1
  - quote: "In refining these FMs, it is important to consider random and systematic errors inherent to the experimental data"
  - quote_check: pass
  - reviewed: false
- BICePs infers all sources of error by sampling their posterior from the data with MCMC. ^c5
  - page: 1
  - quote: "BICePs infers all possible sources of error by sampling the posterior distribution of these parameters directly from the data"
  - quote_check: pass
  - reviewed: false
- With replica averaging, BICePs is a MaxEnt reweighting method that needs no adjustable regularisation parameter. ^c6
  - page: 1
  - quote: "making it a maximum-entropy (MaxEnt) reweighting method, and unique in that no adjustable regularization parameters are required"
  - quote_check: pass
  - reviewed: false
- The BICePs score reflects the total evidence for a model and can be used to optimise forward-model parameters. ^c7
  - page: 1
  - quote: "the BICePs score, which reflects the total evidence for a model, can be used for variational optimization"
  - quote_check: pass
  - reviewed: false
- The demonstration refines Karplus-relation parameters. ^c8
  - page: 1
  - quote: "we refine parameters that modulate the Karplus relation"
  - quote_check: pass
  - reviewed: false
- The framework is stated to generalise to any differentiable forward model. ^c9
  - page: 1
  - quote: "our framework naturally generalizes optimization to any differentiable forward model"
  - quote_check: pass
  - reviewed: false

## Notation

<!-- Only for sources whose equations a concept uses. One row per symbol the concepts rely on or that clashes with the thesis notation.
| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $E(x)$ | force-field energy | $U(x)$ | |
| $\beta$ | inverse temperature | — | write 1/k_BT |
Canonical is one $symbol$ declared by a concept, or —. Delete this section if unused. -->

## What I use from it

The BICePs score as an evidence that can be optimised, the inferred error model, and the closest published analogue to jaxENT's joint weight and BV-parameter fitting ([[BICePs]], [[nuisance parameter]]).

## Disagreements / limitations

Only Karplus J-coupling forward models are tested. No HDX protection-factor or uptake model is fitted, so the analogy to BV-parameter fitting is methodological, not a benchmark. The local PDF is arXiv v2 (June 2025).
