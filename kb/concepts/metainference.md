---
type: concept
aliases:
  - metadynamic metainference
  - metadynamics metainference
  - metadynamics–metainference
  - M&M
notation:
  - {symbol: 'U_\text{MI}', meaning: 'metainference energy, the negative log posterior over replicas and error parameters', units: kJ mol^-1}
  - {symbol: '\sigma_{r,i}', meaning: 'effective uncertainty of datum i in replica r, combining finite-replica and data/forward-model error', units: null}
sources:
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c1]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c2]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c3]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c4]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c5]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c7]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c8]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c9]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c10]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c1]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c2]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c3]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c5]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c6]]"
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c9]]"
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c10]]"
---

## Definition

Metainference is a Bayesian form of [[restrained simulation]]. It integrates experimental data with prior knowledge and is designed to handle all sources of error in the data as well as sample heterogeneity ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c1]]). Replicas are simulated in parallel and observables are averaged over them ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c2]]). Unlike a fixed restraint, each datum has its own uncertainty, which is sampled with the structures as a [[nuisance parameter]]. Models are generated with an energy equal to the negative log posterior ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c3]]).

The error model matters because the error sources are hard to separate. Noise and structural heterogeneity are difficult to tell apart ([[@bonomiPrinciplesProteinStructural2017#^c1]]). Error estimates from experiment are usually lower bounds that miss systematic error ([[@bonomiPrinciplesProteinStructural2017#^c2]]), and the [[forward model]] is often inaccurate ([[@bonomiPrinciplesProteinStructural2017#^c3]]).

Metadynamic metainference (M&M) adds a metadynamics bias on collective variables to each replica, for sampling ([[enhanced sampling]]). Ahmed et al. used it with SAXS data on α-synuclein ([[@ahmedRefinementASynucleinEnsembles2021#^c9]], [[@ahmedRefinementASynucleinEnsembles2021#^c10]]).

## Equations

$$ U_\text{MI}(x_1, \dots, x_{N_\text{rep}}, \sigma) = k_BT \sum_{r=1}^{N_\text{rep}} \left\{ -\ln P_0(x_r) + \sum_i \left[ \frac{\left(s_i^\text{exp} - \bar s_i\right)^2}{2\sigma_{r,i}^2} + \ln \sigma_{r,i} - \ln p(\sigma_{r,i}) \right] \right\}, \qquad \bar s_i = \frac{1}{N_\text{rep}} \sum_{r=1}^{N_\text{rep}} s_i(x_r) $$
^eq-metainference-energy

Source: [[@bonomiMetadynamicMetainferenceEnhanced2016#^c4]], Eq. (19), p. 9 (Gaussian noise model). Bonomi writes $E^G_\text{MI}(\mathbf X, \boldsymbol\sigma)$, $p(X_r)$, $d_i$ and $f_i(\mathbf X)$. Canonical: $U_\text{MI}$, $P_0(x_r)$, $s_i^\text{exp}$ and $\bar s_i$ (notation: [[@bonomiMetadynamicMetainferenceEnhanced2016#Notation]]). Here $\sigma_{r,i}^2$ is the sum of a finite-replica (standard-error) term and a term for experimental, systematic and forward-model error. $p(\sigma_{r,i})$ is the prior on that uncertainty.

## Derivation

1. Fix $\sigma_{r,i}$ and drop the data and forward-model error. The data term becomes a harmonic restraint on the replica average, [[restrained simulation#^eq-replica-restraint]], and metainference reduces to replica-averaged maximum-entropy modelling ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c5]]). Its strength then grows faster than linearly with $N_\text{rep}$, as MaxEnt requires ([[@bonomiPrinciplesProteinStructural2017#^c6]]).
2. With error present, the strength grows linearly with $N_\text{rep}$ and is modulated by the inferred uncertainty ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c7]], [[@bonomiPrinciplesProteinStructural2017#^c5]]). Noisy data restrain less.

## Assumptions and limits

- Sampling still has to be solved. Without the metadynamics bias, runs on alanine dipeptide were not ergodic; in 612 of 2400 runs one minimum was never visited ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c8]]). Larger systems need more biased CVs ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c9]]), and the cost grows with system size ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c10]]).
- Bonomi 2016 tests M&M only on alanine dipeptide with synthetic data, and forward-model error only as simulated outliers (paper note).
- Inferring $\sigma$ protects against overfitting noisy data, but it does not identify which error source is present. A large inferred $\sigma$ can hide [[model misspecification]] ([[nuisance parameter]]).
- Every datum needs a forward model with forces. No HDX collective variable has been published (ValDX future work, `projects/1-ValDX/manuscript/report/8_future_work.tex` L36–40; manuscript only).

## Why it matters here

Chapter 2, "Experimentally Restrained Simulations and Metainference". jaxENT's introduction places metadynamics–metainference beside BioEn and HDXer as existing frameworks (`projects/2-jaxENT/manuscript/report/introduction.tex` L8). It is the closest published route to the restrained-generation part of the thesis.

Claims that use this term: [[Metainference infers an uncertainty for each datum alongside the structures, so the restraint weakens where data or forward model are unreliable.]], [[Without errors in data or forward model, metainference reduces to replica-averaged maximum-entropy restraints.]], [[Experimental error estimates are usually lower bounds because they miss systematic errors.]], [[Noise in the data and structural heterogeneity are difficult to tell apart.]].
