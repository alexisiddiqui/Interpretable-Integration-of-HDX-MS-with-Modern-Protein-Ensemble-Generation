---
type: concept
aliases:
  - nuisance parameters
  - hyperparameter
  - hyperparameters
  - marginalisation
  - marginalization
  - data weight
  - hybrid energy
notation:
  - {symbol: '\gamma', meaning: 'weight of the data term relative to the prior', units: null}
sources:
  - "[[@bmsb2012ch12#^c1]]"
  - "[[@bmsb2012ch1#^c4]]"
  - "[[@bmsb2012ch13#^c3]]"
  - "[[@bmsb2012ch12#^c15]]"
  - "[[@bmsb2012ch12#^c17]]"
  - "[[@bmsb2012ch12#^c18]]"
  - "[[@bmsb2012ch13#^c6]]"
  - "[[@bmsb2012ch13#^c7]]"
---

## Definition

A nuisance parameter is one that is not of primary interest but has to be included to model the data: an error scale, a forward-model coefficient, or the weight given to the data against the prior. Bayesian inference treats nuisance parameters like any other unknown. They get a prior, they are inferred with the structure, and they are integrated out (marginalised) when only the structure is of interest. Fixing them by hand instead hides their uncertainty in the result.

## Equations

$$ p(x \mid s^\text{exp}) = \iint p(x,\theta,\sigma \mid s^\text{exp})\; d\theta\, d\sigma $$
^eq-marginal

Source: [[@bmsb2012ch1#^c4]], p. 8 (stated in prose); for the noise level, [[@bmsb2012ch13#^c3]], p. 4.

$$ -\ln p(x,\theta,\sigma \mid s^\text{exp}) = -\sum_i \ln \rho_\text{err}\!\left(s_i^\text{exp} \mid s_i(x;\theta),\sigma_i\right) + \frac{U(x)}{k_BT} - \ln p(\theta) - \ln p(\sigma) + \text{const} $$
^eq-hybrid-energy

Source: [[@bmsb2012ch12#^c15]], Eq. (12.15), p. 12. Habeck writes $\beta E(x)$ for $U(x)/k_BT$ (notation: [[@bmsb2012ch12#Notation]]).

$$ \gamma = \frac{1}{\sigma^2} $$
^eq-data-weight

Source: [[@bmsb2012ch12#^c17]], p. 22 ($w_\text{data} = 1/\sigma^2$), from Eqs. (12.1), (12.11) and (12.16).

## Derivation

1. Write the negative log posterior of [[inverse problem#^eq-isd-posterior]] ([[@bmsb2012ch12#^c15]], Eq. 12.15).
2. Keep only the terms that depend on $x$: $-\ln L(x,\theta) + U(x)/k_BT$. This has the form of the hybrid energy $w_\text{data} E_\text{data}(x) + E_\text{phys}(x)$ used in conventional structure calculation (Eq. 12.1, p. 2), with $w_\text{data}E_\text{data} = -\sum_i \ln \rho_\text{err}$ (Eq. 12.16).
3. With a Gaussian error model and one shared $\sigma$, $-\ln \rho_\text{err}$ summed over observables is $\frac{1}{2\sigma^2}\sum_i (s_i^\text{exp} - s_i)^2$ plus $n \ln \sigma$ (Eq. 12.11, p. 10). The data weight is therefore $\gamma = 1/\sigma^2$ ([[@bmsb2012ch12#^c17]]).
4. Because the posterior is normalised, the $n \ln \sigma$ term stops $\sigma$ growing without bound. The conditional posterior of the precision $\sigma^{-2}$ is a Gamma distribution (Eqs. 12.13–12.14, p. 10), so $\sigma$ can be sampled with the structure instead of being tuned by hand ([[@bmsb2012ch12#^c17]]).
5. The estimated $\sigma$ is itself informative: it balances the data sources and serves as a figure of merit for the fit ([[@bmsb2012ch12#^c18]], p. 23).
6. In SAXS, the regularisation weight is a hyperparameter of the same kind. It gets a scale prior $p(\alpha) = 1/\alpha$ (Eq. 13.33, p. 14) and is estimated from its posterior ([[@bmsb2012ch13#^c6]], p. 13). Averaging over hyperparameters gives error estimates for the result ([[@bmsb2012ch13#^c7]], p. 14).
7. The confidence parameter of the HDXer loss weights the data term against the apparent-work prior, so it has the role of $\gamma$ (step ours; [[Bayes' theorem]], [[maximum entropy principle]] step 8).

## Assumptions and limits

- Marginalising needs a prior on each nuisance parameter. Scale parameters take $1/\alpha$-type priors.
- Habeck's $\sigma$ is one value shared by all data of a kind. HDX data have heteroscedastic, correlated errors, so one $\sigma$ is a simplification.
- When forward-model parameters and ensemble weights both affect the prediction, they can trade off against each other. Whether the data separate them is an empirical question for each system (step ours). This is research question 2 of the thesis.
- A fitted nuisance parameter can hide model error as well as quantify it: forward-model coefficients absorb mismatch ([[model misspecification]]). Variation of fitted values across replicate splits is one check ([[replicate uncertainty]]).
- In [[metainference]] the per-datum uncertainty $\sigma_{r,i}$ is a nuisance parameter sampled with the structures. A large inferred value weakens that datum's restraint, which protects against noise but can also hide forward-model error.

## Why it matters here

The forward-model coefficients ($\beta_C$, $\beta_H$) and the data weight are nuisance parameters for the quantity of interest, the populations. ValDX chooses the data weight by validation. jaxENT infers forward-model parameters jointly with the weights. The introduction (§1.5) cites Bayesian NMR and SAXS analyses for the point that these choices change structural conclusions.

jaxENT penalises, by an L1 term, the deviation of $\beta_C$ and $\beta_H$ from their prior values (`projects/2-jaxENT/manuscript/report/results.tex` L155–161, manuscript only). Knowledge of the coefficients then enters as a prior on a nuisance parameter, not only through the frame weights.


Claims that use this term: [[MaxEnt reweighting seeks new weights that minimise the discrepancy with experimental uptake while staying close to the prior.]], [[Uncertainty in nuisance parameters and regularisation choices can affect structural conclusions from Bayesian analyses of NMR and small-angle scattering.]], [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]], [[Metainference infers an uncertainty for each datum alongside the structures, so the restraint weakens where data or forward model are unreliable.]].
