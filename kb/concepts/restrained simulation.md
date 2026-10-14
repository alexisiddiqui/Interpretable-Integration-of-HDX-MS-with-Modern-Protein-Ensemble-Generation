---
type: concept
aliases:
  - restrained simulations
  - restrained MD
  - experimentally restrained simulation
  - experimentally restrained MD
  - replica-averaged restraints
  - replica-averaged simulation
  - restrained-ensemble simulation
  - replica ensemble refinement
notation:
  - {symbol: 'N_\text{rep}', meaning: 'number of replicas simulated in parallel', units: null}
  - {symbol: '\kappa', meaning: 'force constant of a restraint on replica-averaged observables', units: null}
  - {symbol: 'U_\text{RE}', meaning: 'potential energy of a replica-restrained ensemble simulation', units: kJ mol^-1}
sources:
  - "[[@cesariUsingMaximumEntropy2018#^c4]]"
  - "[[@cesariUsingMaximumEntropy2018#^c16]]"
  - "[[@cesariUsingMaximumEntropy2018#^c18]]"
  - "[[@cesariUsingMaximumEntropy2018#^c19]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c4]]"
  - "[[@hummerBayesianEnsembleRefinement2015#^c9]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c4]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c5]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c9]]"
  - "[[@biancanielloStructureDynamicsMisfolding2025#^c6]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c1]]"
  - "[[@andersonHDXMSMDSimulations2022#^c3]]"
---

## Definition

A restrained simulation adds an experimental term to the force field during sampling, rather than reweighting frames afterwards. Maximum-entropy methods can be implemented either as reweighting of existing simulations or by on-the-fly optimisation ([[@cesariUsingMaximumEntropy2018#^c4]]). The restraint is applied to the average of an observable over replicas simulated in parallel, not to each structure, because the data are ensemble averages. Bayesian replica ensemble refinement restrains averages of observables in coupled replica MD ([[@hummerBayesianEnsembleRefinement2015#^c4]]). Replica-averaged MD restrained with NMR chemical shifts is one application ([[@biancanielloStructureDynamicsMisfolding2025#^c6]]).

## Equations

$$ U_\text{RE}(x_1, \dots, x_{N_\text{rep}}) = \sum_{r=1}^{N_\text{rep}} U(x_r) + \frac{\kappa}{2} \sum_{i} \left( \frac{1}{N_\text{rep}} \sum_{r=1}^{N_\text{rep}} s_i(x_r) - s_i^\text{exp} \right)^2 $$
^eq-replica-restraint

Source: [[@cesariUsingMaximumEntropy2018#^c18]], Eq. (18), p. 7. Cesari writes $V_\text{RE}(q_1, \dots, q_{N_\text{rep}})$, $V_0(q_i)$, $k$, replica index $i$ and observable index $j$. Canonical: $U$, $x_r$, $\kappa$ (because $k$ is a rate constant), replica index $r$, observable index $i$.

## Derivation

1. Each replica feels the force of the restraint on the average. As $N_\text{rep}$ grows, fluctuations of the average shrink and the force becomes constant in time. A constant force on $s_i$ is a linear tilt of the potential, the MaxEnt form [[maximum entropy principle#^eq-maxent-potential]] ([[@cesariUsingMaximumEntropy2018#^c16]]; Cesari p. 7, text after Eq. 18).
2. So the restrained ensemble matches the maximum-entropy ensemble in the limit of many replicas ([[@cesariUsingMaximumEntropy2018#^c18]]; reported in [[@bonomiPrinciplesProteinStructural2017#^c4]]).
3. To enforce the average exactly, $\kappa$ must grow faster than $N_\text{rep}$ ([[@cesariUsingMaximumEntropy2018#^c19]]). If the data are noisy, the Bayesian treatment instead scales the restraint linearly with $N_\text{rep}$ ([[@hummerBayesianEnsembleRefinement2015#^c9]], [[@bonomiPrinciplesProteinStructural2017#^c5]]). That is the bridge to [[metainference]].

## Assumptions and limits

- The [[forward model]] is evaluated, and differentiated, at every step. A restrained simulation therefore needs an observable that can be computed as a collective variable with forces.
- $N_\text{rep}$ and $\kappa$ are choices. Too few replicas or too weak a restraint leaves the average unenforced; the exact limit is reached only asymptotically (above).
- Sampling replaces reweighting's coverage problem: unlike reweighting, the simulation can visit states the prior ensemble lacked. Reweighting is inaccurate when the prior differs strongly from the target ([[@bonomiPrinciplesProteinStructural2017#^c9]]); restraining avoids that, at the cost of new simulations ([[sampling coverage]], [[ensemble reweighting]]).
- Forward-model error is pushed into the structures, as in reweighting ([[model misspecification]]).
- For HDX the route is less developed. Restraining observables in simulations is the stated aim of HDX refinement ([[@wanReconcilingSimulatedEnsembles2020#^c1]]), and some groups have restrained simulations with HDX-MS for simpler systems ([[@andersonHDXMSMDSimulations2022#^c3]]). ValDX's future-work chapter notes that no optimised BV collective variable exists in PLUMED (`projects/1-ValDX/manuscript/report/8_future_work.tex` L36; manuscript only).

## Why it matters here

Chapter 2, "Experimentally Restrained Simulations and Metainference". It is the sampling-time counterpart of the [[maximum entropy principle]]: the same tilt, applied during MD rather than to fixed frames. The project's own differentiable HDX restraint stays in its research chapter.

Claims that use this term: [[Restraining replica-averaged observables in MD reproduces the maximum-entropy ensemble in the limit of many replicas.]], [[Several groups have restrained simulations or pruned ensembles post hoc with HDX-MS data, mainly for simpler systems.]].
