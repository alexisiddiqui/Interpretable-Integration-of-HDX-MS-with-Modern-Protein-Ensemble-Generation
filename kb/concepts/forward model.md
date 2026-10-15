---
type: concept
aliases:
  - forward models
  - error model
  - structure-to-observable model
  - likelihood function
notation:
  - {symbol: 's_i(x;\theta)', meaning: 'forward-model prediction of observable i for conformation x and forward-model parameters theta', units: null}
  - {symbol: '\theta', meaning: 'forward-model parameters', units: null}
  - {symbol: '\sigma_i', meaning: 'error scale (standard deviation) of observable i', units: null}
  - {symbol: '\rho_\text{err}', meaning: 'error model: probability of a measured value given its prediction', units: null}
sources:
  - "[[@bmsb2012ch12#^c10]]"
  - "[[@bmsb2012ch12#^c14]]"
  - "[[@bmsb2012ch12#^c4]]"
  - "[[@bmsb2012ch13#^c1]]"
  - "[[@cesariUsingMaximumEntropy2018#^c11]]"
---

## Definition

A forward model predicts what an experiment would measure for a given structure. It is a deterministic function of the conformation and of its own parameters, such as the Best–Vendruscolo coefficients. Because predictions and measurements never agree exactly, a second, probabilistic ingredient is needed: an error model, which scores the discrepancy. Together they give the likelihood, the probability of the data given a structure and the parameters. For ensemble-averaged data such as HDX-MS and SAXS, the prediction compared with experiment is the ensemble average of the per-conformer predictions.

## Equations

$$ p(s^\text{exp} \mid x,\theta,\sigma) = \prod_i \rho_\text{err}\!\left(s_i^\text{exp} \,\middle|\, s_i(x;\theta),\, \sigma_i\right) $$
^eq-likelihood

Source: [[@bmsb2012ch12#^c14]], Fig. 12.1 (p. 8) and Eq. (12.8) (p. 9); the forward model as "mock" data: [[@bmsb2012ch12#^c10]], p. 6. Habeck writes the forward model $f_i(x;\alpha)$, the data $y_i$ and the error model $g$, with one $\sigma$ (notation: [[@bmsb2012ch12#Notation]]).

$$ \rho_\text{err}\!\left(s_i^\text{exp} \mid s_i, \sigma_i\right) = \frac{1}{\sqrt{2\pi}\,\sigma_i} \exp\!\left[-\frac{\left(s_i^\text{exp} - s_i\right)^2}{2\sigma_i^2}\right] $$
^eq-gaussian-error

Source: [[@bmsb2012ch12#^c14]]; Eq. (12.11), p. 10, written there with a single $\sigma$ for all measurements.

$$ \langle s_i \rangle_w(\theta) = \sum_j w_j\, s_i(x_j;\theta) $$
^eq-ensemble-prediction

Source: the continuous form is the MaxEnt constraint of [[@cesariUsingMaximumEntropy2018#^c11]], Eq. (2), p. 2; the sum over conformers is ours. SAXS gives a linear example, $I(q_i) = \sum_j T_{ij} p_j + e_i$ ([[@bmsb2012ch13#^c1]]; Eq. 13.10, p. 9).

## Derivation

1. Predict idealised "mock" data from the structure with the forward model, then score their discrepancy from the measurements with an error model ([[@bmsb2012ch12#^c10]], p. 6).
2. Treat the measurements as independent, so the likelihood is a product over observables ([[@bmsb2012ch12#^c14]], Eq. 12.8).
3. A Gaussian error model gives Eq. (12.11), and its negative logarithm is half a $\chi^2$ ([[regularisation#^eq-chi2]]).
4. For an ensemble, replace $s_i(x;\theta)$ by the weighted average [[#^eq-ensemble-prediction]] (step ours). For HDX the quantity averaged matters: [[Best–Vendruscolo model#^eq-bv-ensemble]] averages $\ln P_f$, whereas uptake is non-linear in $\ln P_f$.

## Assumptions and limits

- Independence of measurements is an assumption ([[@bmsb2012ch12#^c14]]). HDX peptides overlap, so their predictions share residues and their errors are correlated. The correction is to weight residuals by the inverse error covariance ([[error covariance#^eq-gls]]); which covariance is meant has to be stated.
- $\sigma_i$ models random error. Systematic forward-model error is not covered unless it is modelled, for example through $\theta$ ([[nuisance parameter]]). Habeck lists neglected dynamics and averaging among the sources of discrepancy (p. 6).
- Structure-based NMR calculations rarely model data as ensemble averages ([[@bmsb2012ch12#^c4]]). HDX-MS and SAXS data are averages, so the comparison object is the ensemble, not a structure.
- When the forward model is wrong, the inferred weights and parameters absorb the mismatch and the fit can still look good ([[model misspecification]]).
- Sampling-time methods need its gradient as well as its value. A [[restrained simulation]] applies forces through it, [[metainference]] does the same with inferred errors, and [[guided diffusion]] differentiates it at each denoising step. Reweighting needs only values ([[HDX protection-factor model]] covers the HDX case).

## Why it matters here

The forward model is where structure meets HDX-MS. Its form and parameters are part of the inference, not a neutral translation, which is the point of introduction §1.4 and of the joint ensemble–parameter inference in jaxENT. The [[Best–Vendruscolo model]] is the HDX instance, and [[inverse problem]] places it inside Bayesian inference.

jaxENT's covariance weighting is a selection-time weighting of validation residuals by a geometric peptide covariance, recorded in [[Observation weighting and selection (jaxENT)]]; the manuscript's fitted covariance-weighted MSE (`projects/2-jaxENT/manuscript/report/results.tex` L37–72) is the legacy path. jaxENT also computes uptake in an additive interval-hazard form that avoids repeated frame-wise uptake calculation (`projects/2-jaxENT/code/docs/bv_uptake_models.md`). Both are project methods for method notes, not evidence.


Claims that use this term: [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]], [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]], [[In a Bayesian description, a prior and a likelihood combine into a posterior over unknown structures and parameters.]], [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]], [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]].
