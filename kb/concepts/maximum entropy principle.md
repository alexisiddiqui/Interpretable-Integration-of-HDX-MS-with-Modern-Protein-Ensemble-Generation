---
type: concept
aliases:
  - MaxEnt
  - maximum entropy
  - MaxEnt principle
notation: []
---

## Definition

The maximum entropy principle is a recipe for choosing the least biased probability distribution that is compatible with constraints derived from data. Applied to simulated ensembles, it gives the reweighted distribution that agrees with the experimental observations while staying as close as possible to the prior ensemble.

## Why it matters here

MaxEnt reweighting is the prior-preserving fitting step that lets an HDX-MS dataset adjust a simulated ensemble without overfitting, which is the central operation in integrating HDX-MS with ensemble generation in ValDX and JaxENT.

Claims that use this term: [[HDXer implements a MaxEnt optimisation framework to reweight the simulated ensemble.]], [[MaxEnt reweighting avoids overfitting and ensures the resulting ensemble remains physically plausible.]], [[MaxEnt reweighting seeks new weights that minimise the discrepancy with experimental uptake while staying close to the prior.]], [[Maximum Entropy (MaxEnt) optimisation is one approach to fitting simulated ensembles to experimental data.]], [[Minimising apparent work and KL divergence gives a reweighted ensemble that satisfies the constraints with minimal deviation.]], [[Reweighting ensembles to fit experiment while minimising deviation from the original identifies the minimal changes needed.]], [[SAXS ensembles have been refined against scattering profiles using Bayesian inference and maximum entropy reweighting.]], [[SAXS with MD simulations and ensemble refinement gives minimal ensembles consistent with restraints, without overfitting.]], [[The MaxEnt reweighting optimisation problem is solved with the method of Lagrange multipliers.]].
