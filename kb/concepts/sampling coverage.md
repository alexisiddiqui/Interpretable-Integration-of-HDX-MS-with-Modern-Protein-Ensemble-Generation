---
type: concept
aliases:
  - coverage
  - conformational coverage
  - coverage, populations and kinetics
  - missing states
  - decoy
  - decoys
notation: []
sources:
  - "[[@heninEnhancedSamplingMethods2022#^c4]]"
  - "[[@heninEnhancedSamplingMethods2022#^c8]]"
  - "[[@heninEnhancedSamplingMethods2022#^c9]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c7]]"
  - "[[@bmsb2012ch2#^c18]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c4]]"
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c7]]"
---

## Definition

An ensemble can be right or wrong in three separate ways:
- **Coverage:** which conformational states are present at all.
- **Populations:** how much weight each state has at equilibrium (thermodynamics).
- **Kinetics:** how fast states interconvert (the barriers between basins of the [[conformational free-energy landscape]]).

A sampler can get one right and the others wrong. Many enhanced sampling schemes do not preserve kinetics and are useful mainly for equilibrium probabilities ([[@heninEnhancedSamplingMethods2022#^c4]]). Seeding from rarely visited states broadens exploration without necessarily estimating populations accurately ([[@heninEnhancedSamplingMethods2022#^c9]]); populations and rates need a further model, such as a Markov state model ([[@heninEnhancedSamplingMethods2022#^c8]]). Repeated AF3 seeds give diverse structures that do not approximate the solution ensemble ([[@abramsonAccurateStructurePrediction2024#^c7]]).

## Assumptions and limits

- Broader coverage is necessary for correct populations, but not sufficient (ours, from the passages above).
- Coverage bounds what reweighting can do. States never sampled get no weight, and reweighting works only where the sampled range covers the target ([[@bmsb2012ch2#^c18]]; [[importance sampling]]).
- HDX-MS uptake is an average over the ensemble. It can constrain the populations of candidate states, but cannot show which states are missing from the candidates (ours; [[HDX-MS]]).
- "Coverage" here is conformational; HDX-MS sequence coverage (peptides covering the sequence) is a different term ([[deuterium uptake]]).
- Coverage can fail in two directions. **Missing states:** reweighting changes only the weights of existing frames ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c7]]), so it cannot create a state the candidates lack (ours). **Spurious states:** plausible but unpopulated candidates, or implausible decoys, can absorb weight. In TeaA, intermediate conformations absent from the target prevented population recovery even when uptake matched ([[@siddiquiFrameworkTestingStructural2026#^c4]]). jaxENT reports the same with decoys (`projects/2-jaxENT/manuscript/report/results.tex` L63, L130; not yet citable).
- Coverage is assessed by comparing ensembles as distributions, not by counting distinct structures ([[ensemble comparison]]). The comparison needs a reference, which is itself a model.

## Why it matters here

This is the distinction §1.3 rests on: MD, enhanced sampling and learned generators differ mainly in which of the three they deliver. Generators and seeding mostly add coverage, and the thesis then estimates populations against HDX-MS ([[ensemble reweighting]]). §1.5 returns to missing states: a reweighted ensemble cannot recover a state the candidates lack.

Claims that use this term: [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]], [[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]], [[A complete picture of dynamics requires sampling in between these states.]], [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]], [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]], [[Diffusion steps are not physical simulation time.]], [[Reweighting cannot create conformational states absent from the candidate ensemble.]], [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]], [[Comparing ensembles requires comparing probability distributions over conformations, not single-structure RMSD.]].
