---
type: concept
aliases:
  - regularization
  - regulariser
  - regularizer
  - regularisation functional
  - information content
  - number of good parameters
  - chi-square
notation:
  - {symbol: '\chi^2', meaning: 'sum of squared residuals, each divided by its error variance', units: null}
  - {symbol: '\mathcal{R}', meaning: 'regularisation functional', units: null}
  - {symbol: 'N_g', meaning: 'number of good parameters: parameter directions determined by the data', units: null}
  - {symbol: '\mu_k', meaning: 'k-th eigenvalue of the curvature (Hessian) of chi^2/2', units: null}
sources:
  - "[[@bmsb2012ch13#^c4]]"
  - "[[@bmsb2012ch13#^c5]]"
  - "[[@bmsb2012ch13#^c6]]"
  - "[[@bmsb2012ch13#^c2]]"
  - "[[@bmsb2012ch13#^c9]]"
  - "[[@bmsb2012ch13#^c10]]"
---

## Definition

Regularisation selects one solution of an ill-posed [[inverse problem]] by adding a penalty, the regularisation functional, to the misfit. The penalty encodes prior expectations such as smoothness or closeness to a prior estimate. Its weight sets how far the data may pull the solution away from the prior. In Bayesian terms, the regulariser is a negative log prior and its weight is a hyperparameter that can be inferred ([[nuisance parameter]]). The maximum-entropy regulariser is a relative entropy, which links SAXS regularisation to MaxEnt ensemble reweighting. Regularisation also defines how much information the data carry: the number of good parameters counts the directions in parameter space the data determine better than the prior.

## Equations

$$ \chi^2 = \sum_i \frac{\left(s_i^\text{exp} - \langle s_i \rangle\right)^2}{\sigma_i^2} $$
^eq-chi2

Source: [[@bmsb2012ch13#^c4]]; Eq. (13.14), p. 10, where Hansen writes $I_m(q_i)$ and $I(q_i)$ for measured and predicted intensities (notation: [[@bmsb2012ch13#Notation]]).

$$ \min\; \mathcal{R} + \frac{\gamma}{2}\chi^2 $$
^eq-regularised-objective

Source: [[@bmsb2012ch13#^c4]], Eq. (13.12), p. 9 (Hansen minimises $\alpha K + \chi^2$); Bayesian form $Q = -\alpha K - \chi^2/2$ in Eqs. (13.25)–(13.29), p. 13 ([[@bmsb2012ch13#^c6]]). Dividing by $\alpha$ gives this form with $\gamma = 1/\alpha$.

$$ \mathcal{R}(w) = \sum_j \left[ w_j \ln \frac{w_j}{w_j^0} - w_j + w_j^0 \right] $$
^eq-maxent-regulariser

Source: [[@bmsb2012ch13#^c5]], Eqs. (13.16)–(13.17), p. 11, written there for a distance distribution $p_j$ with prior estimate $m_j$.

$$ N_g = \sum_k \frac{\mu_k}{\gamma^{-1} + \mu_k} $$
^eq-good-parameters

Source: [[@bmsb2012ch13#^c10]]; Eq. (13.38), p. 27, for entropy regularisation. Hansen writes the eigenvalues as $\lambda_j$ and the weight as $\alpha = \gamma^{-1}$.

## Derivation

1. Pick one solution of an ill-posed problem by minimising a weighted sum of a regulariser and $\chi^2$ ([[@bmsb2012ch13#^c4]], Eq. 13.12).
2. Read $e^{-\chi^2/2}$ as a Gaussian likelihood and $e^{-\alpha K}$ as a prior. The minimum is then the posterior maximum, and $\alpha$ is a hyperparameter ([[@bmsb2012ch13#^c6]], Eqs. 13.25–13.27).
3. Keeping only the first term of the regulariser and replacing the norm by an entropy gives the maximum-entropy method ([[@bmsb2012ch13#^c5]], Eq. 13.16).
4. If $\sum_j w_j = \sum_j w_j^0 = 1$, the $-w_j + w_j^0$ terms cancel and $\mathcal{R}(w) = D_\text{KL}(w \Vert w^0)$ ([[Kullback–Leibler divergence#^eq-kl-weights]]) (step ours). The SAXS MaxEnt regulariser is therefore the reweighting prior of [[maximum entropy principle|MaxEnt reweighting]].
5. Each eigenvalue $\mu_k$ of the $\chi^2$ curvature that is large compared with $1/\gamma$ counts as one parameter determined by the data. Overfitting lowers the prior weight and pushes $N_g$ above the number of independent data channels (Eq. 13.38 and text, pp. 27–28; [[@bmsb2012ch13#^c10]]).

## Assumptions and limits

- The numbers in BMSB ch13 (Shannon channels, $N_g$ for scattering curves) are specific to SAXS and SANS. The general point carried over is that low-information data ([[@bmsb2012ch13#^c2]]) need regularisation, and that the weight decides how much of the fit is data and how much is prior.
- $N_g$ uses a Gaussian approximation around the optimum.
- Choosing the weight by evidence (BMSB) and choosing it by held-out validation (ValDX) are different criteria. Both aim to stop the fit absorbing noise.
- Regularisation picks one solution; it does not validate it. The regularisation weight still has to be chosen by held-out data or by evidence ([[data splitting]], [[Bayes' theorem#^eq-bayes-factor]]), and a regularised fit can still overfit or reflect a poor prior ([[overfitting]]).

## Why it matters here

The regularisation weight is the one choice every reweighting method must make: MaxEnt's $\gamma$, HDXer's confidence parameter and jaxENT's loss weights. ValDX's validation splits are a way to choose it without overfitting. $N_g$ is a reminder of how few parameters HDX-MS data may determine relative to the number of conformer weights.

Claims that use this term: [[MaxEnt reweighting avoids overfitting and ensures the resulting ensemble remains physically plausible.]], [[SAXS with MD simulations and ensemble refinement gives minimal ensembles consistent with restraints, without overfitting.]], [[Uncertainty in nuisance parameters and regularisation choices can affect structural conclusions from Bayesian analyses of NMR and small-angle scattering.]], [[Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is a good choice only when the prior is reasonable.]].
