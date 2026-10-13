---
type: concept
aliases:
  - equilibration
  - convergence
  - sampling convergence
  - starting-structure dependence
  - reproducibility of sampling
notation: []
sources:
  - "[[@bmsb2012ch2#^c14]]"
  - "[[@bmsb2012ch2#^c15]]"
  - "[[@bmsb2012ch2#^c17]]"
  - "[[@heninEnhancedSamplingMethods2022#^c6]]"
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c1]]"
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c3]]"
---

## Definition

A simulation's statistics describe the equilibrium ensemble only once it has forgotten where it started (equilibration) and has visited the relevant states often enough for averages to stop changing (convergence). Until then, what a set of simulations covers is governed by their starting conditions ([[@heninEnhancedSamplingMethods2022#^c6]]). Slow mixing reduces the effective number of samples and can give misleading results with no obvious sign ([[@bmsb2012ch2#^c14]]). The basic test is reproducibility: independent runs from different starts should give the same answer ([[@bmsb2012ch2#^c15]]).

## Assumptions and limits

- Convergence cannot be proven from a finite run, only tested. Agreement between replicates is necessary, not sufficient: all of them can miss the same state.
- Equilibration has to be repeated for each new system or starting state, and conformational changes often take longer than all-atom MD can reach ([[@hollingsworthMolecularDynamicsSimulation2018#^c1]], [[@hollingsworthMolecularDynamicsSimulation2018#^c3]]). This is the cost that [[enhanced sampling]] and learned generators try to avoid.
- Enhanced sampling does not remove the need to assess convergence ([[@bmsb2012ch2#^c17]]).
- The same idea for Monte Carlo is in [[Markov chain Monte Carlo]]; MD with a thermostat is a sampler of the same kind (ours).
- **Gap:** the confirmation cites Lazim et al. (2020) for the cost of equilibration, but the one Lazim quote in the KB is about the cost of all-atom MD in general ([[@lazimAdvancesMolecularDynamics2020#^c1]]). A passage on equilibration itself is still needed.

## Why it matters here

ValDX compares single-start MD (MD-1Start) with multiple-start MD (MD-10Start), which is the reproducibility test applied to ensemble generation. jaxENT's replicate analysis plays the same role. In introduction §1.3 this explains why more sampling or more starting structures does not by itself settle the populations ([[sampling coverage]]).

Claims that use this term: [[Until MD has converged, its statistics depend on the starting structures; reproducibility across independent starts is the basic check.]], [[Physics-based methods are useful for detailed analysis but limited by the computational cost of equilibration.]], [[Sampling is limited because equilibration must be repeated for each new system or starting conformational state.]], [[Sufficiently sampled equilibrium MD targets the Boltzmann distribution of its approximate force field, not the protein's true distribution.]], [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]].
