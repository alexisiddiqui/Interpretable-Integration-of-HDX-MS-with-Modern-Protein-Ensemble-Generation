---
type: concept
aliases:
  - covariance-weighted residuals
  - covariance-weighted MSE
  - generalised least squares
  - generalized least squares
  - GLS
  - Mahalanobis distance
  - correlated errors
  - heteroscedasticity
  - precision matrix
  - inverse-covariance weighting
notation:
  - {symbol: '\Sigma', meaning: 'covariance matrix of the observation errors across peptides', units: null}
  - {symbol: 'r_t', meaning: 'vector of residuals between predicted and measured peptide uptake at labelling time t', units: null}
sources:
  - "[[@bmsb2012ch8#^c1]]"
  - "[[@bmsb2012ch8#^c8]]"
  - "[[@bmsb2012ch12#^c14]]"
  - "[[@crookEmpiricalBayesFunctional2022#^c1]]"
  - "[[@crookEmpiricalBayesFunctional2022#^c2]]"
---

## Definition

Ordinary least squares treats every observation as having the same variance and no correlation with the others. When variances differ or errors are correlated it is inaccurate, and the correction is to weight the residuals by the inverse of the error covariance matrix ([[@bmsb2012ch8#^c1]], [[@bmsb2012ch8#^c8]]). Theobald states this for the superposition of structures, where neighbouring atoms covary through bonds. The statement is the same for any least-squares fit. With a Gaussian error model the weighted sum of squares is the negative log likelihood up to a constant, so the weighting is not a heuristic but the likelihood of correlated Gaussian errors ([[forward model#^eq-likelihood]]).

## Equations

$$ \chi^2_\Sigma = r_t^\top \Sigma^{-1} r_t $$
^eq-gls

Source: [[@bmsb2012ch8#^c8]], p. 5, stated in prose for Procrustes superposition; the residual form is ours. When $\Sigma$ is diagonal this is [[regularisation#^eq-chi2]] with $\sigma_i^2$ on the diagonal (step ours).
Manuscript form: projects/2-jaxENT/manuscript/report/methods/analysis.tex#L31 writes $\mathcal{L}_\Sigma = \frac{1}{|\mathcal{T}|}\sum_t \frac{1}{2} r_t^\top (\Sigma^{-1}/\lVert\Sigma^{-1}\rVert_F)\, r_t$, with a Frobenius normalisation that the code replaces by a trace normalisation ([[Observation weighting and selection (jaxENT)]]).

## Assumptions and limits

- $\Sigma$ has to be estimated. A sample covariance from $n$ samples has rank at most $n - 1$, so with few time points or few frames it is singular and needs a ridge or shrinkage before inversion (step ours).
- The weighting corrects the fit for whatever $\Sigma$ describes. If $\Sigma$ is estimated from the candidate ensemble's structural fluctuations rather than from measurement error, the fit is weighted by expected structural co-variation, and that assumption has to be stated.
- Likelihoods in ensemble refinement multiply over observables, which assumes independent errors ([[@bmsb2012ch12#^c14]]). HDX peptides overlap, so the assumption fails at the prediction level through shared residues ([[forward model]]).

## In integrative practice

HDX-MS statistics recognise the dependence between overlapping peptides and leave it unmodelled. Crook et al. list it as the first limitation of their functional model and note that it shows up as clustered p-values for overlapping peptides ([[@crookEmpiricalBayesFunctional2022#^c1]], [[@crookEmpiricalBayesFunctional2022#^c2]]). Ensemble-reweighting likelihoods for HDX treat peptides as independent.

## Why it matters here

jaxENT builds $\Sigma$ from geometry rather than from replicate measurements. The candidate ensemble's residue [[positional covariance]] is pushed through the residue-averaging peptide map, $\Sigma = M C M^\top + \lambda I$, so two peptides covary when they share residues or when their residues move together. The matrix is used to weight validation residuals during model selection, not to fit. The purpose is to score held-out peptides by how much independent information they carry given the training peptides, which addresses the dependence that structured [[data splitting]] cannot remove by weighting instead of partitioning. The assumption to state is that residual errors covary as the structure does. The construction, the choice between conditional and marginal validation blocks, and the separate measured-precision weight for MoPrP are in [[Observation weighting and selection (jaxENT)]]. No literature predecessor is needed for the construction; the literature supplies the principle in this note.

Claims that use this term: [[Weighting residuals by the inverse error covariance corrects least squares for unequal variances and correlated errors.]], [[Correlations between overlapping peptides are recognised in HDX-MS statistics but left unmodelled.]], [[A covariance built from candidate-ensemble coordinates describes how peptides are expected to co-vary structurally, so weighting residuals by it assumes their errors co-vary in the same way.]], [[Weighting validation residuals by the conditional precision given the training peptides discounts held-out peptides whose information is redundant with the training set.]].
