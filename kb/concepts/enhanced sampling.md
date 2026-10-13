---
type: concept
aliases:
  - enhanced sampling methods
  - biased sampling
  - metadynamics
  - adaptive sampling
  - adaptive seeding
  - frontier expansion sampling
  - FEXS
  - FES
  - T-FES
  - collective variable
  - CV
notation: []
sources:
  - "[[@heninEnhancedSamplingMethods2022#^c4]]"
  - "[[@heninEnhancedSamplingMethods2022#^c5]]"
  - "[[@heninEnhancedSamplingMethods2022#^c7]]"
  - "[[@heninEnhancedSamplingMethods2022#^c1]]"
  - "[[@heninEnhancedSamplingMethods2022#^c3]]"
  - "[[@heninEnhancedSamplingMethods2022#^c8]]"
  - "[[@heninEnhancedSamplingMethods2022#^c9]]"
  - "[[@heninEnhancedSamplingMethods2022#^c6]]"
  - "[[@zhangFrontierExpansionSampling2020#^c1]]"
  - "[[@zhangFrontierExpansionSampling2020#^c2]]"
  - "[[@bmsb2012ch2#^c16]]"
  - "[[@bmsb2012ch2#^c17]]"
---

## Definition

Enhanced sampling methods reach states that plain [[molecular dynamics|MD]] visits too rarely. They come in two families, which differ in what they cost.

**Biasing the energy.** Methods such as metadynamics add a bias along chosen collective variables (CVs), so the simulation samples a modified distribution. Unbiased statistics are recovered by reweighting, which works only with good overlap between the biased and unbiased distributions ([[@heninEnhancedSamplingMethods2022#^c7]]). Many such schemes do not preserve kinetics and are useful mainly for equilibrium probabilities; the most efficient alter the dynamics as much as possible while preserving thermodynamics ([[@heninEnhancedSamplingMethods2022#^c4]], [[@heninEnhancedSamplingMethods2022#^c5]]).

**Adaptive seeding.** Unbiased simulations are restarted from chosen points, not restrained ([[@heninEnhancedSamplingMethods2022#^c3]]), usually from regions likely to lead to barrier crossing ([[@heninEnhancedSamplingMethods2022#^c1]]). Seeding from rarely visited states broadens exploration but does not necessarily estimate populations accurately ([[@heninEnhancedSamplingMethods2022#^c9]]). Populations and rates come from stitching the trajectories together, for example in a Markov state model ([[@heninEnhancedSamplingMethods2022#^c8]]). Frontier expansion sampling (FEXS, called FES in ValDX) seeds from low-density regions of the current ensemble in Cartesian coordinates ([[@zhangFrontierExpansionSampling2020#^c1]], [[@zhangFrontierExpansionSampling2020#^c2]]); T-FES is the ValDX multiple-topology variant.

## Assumptions and limits

- Neither family gives populations for free. Biased runs need reweighting, and seeded runs need a model of the pooled frames ([[sampling coverage]]). Avoid both "preserves the equilibrium" and "destroys the equilibrium" as blanket statements.
- Results depend on the CVs or seeding criterion chosen ([[@heninEnhancedSamplingMethods2022#^c6]] for seeding).
- Extended ensembles (replica exchange, multicanonical) are a third route through an artificial distribution ([[@bmsb2012ch2#^c16]]; [[Markov chain Monte Carlo]]). None of these removes the need to assess convergence ([[@bmsb2012ch2#^c17]]; [[equilibration and convergence]]).
- Bias potentials, estimators and MSM construction are Chapter 2 material.

## Why it matters here

ValDX's MD-TFES ensembles are adaptive seeding, so their frame frequencies are candidates to be weighted, not populations. That is why ValDX and jaxENT reweight against HDX-MS rather than reading populations off the sampled frames ([[importance sampling]], [[ensemble reweighting]]).

Claims that use this term: [[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]], [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]], [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]], [[The metadynamics bias encourages exploring new states by discouraging revisits to previously sampled configurations.]], [[Metadynamics is limited by the need for appropriate CVs, complex computational requirements and loss of equilibrium properties.]], [[Online analysis of collective variables can adaptively guide sampling towards underexplored regions of conformational space.]], [[Offline biasing methods can be used to preserve equilibria while enhancing sampling.]], [[Offline methods adaptively seed new simulations from underexplored regions, sampling efficiently without distorting the landscape.]], [[These methods can be sampled over specific CVs but are also compatible with generic dimensionality reduction techniques.]], [[Frontier-Expansion Sampling is a promising avenue for enhanced sampling of conformational space.]], [[As FES only requires Cartesian coordinates to select new simulation seeds, it is flexible to the underlying topology.]].
