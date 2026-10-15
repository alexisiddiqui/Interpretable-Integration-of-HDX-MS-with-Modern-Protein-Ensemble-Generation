---
type: concept
aliases:
  - MD
  - MD simulation
  - MD simulations
  - molecular dynamics simulation
  - molecular dynamics simulations
notation:
  - {symbol: 'm_a', meaning: 'mass of atom a', units: 'g mol^-1'}
  - {symbol: 'x_a(t)', meaning: 'position of atom a at simulation time t', units: 'nm'}
sources:
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c4]]"
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c5]]"
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c2]]"
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c3]]"
  - "[[@hollingsworthMolecularDynamicsSimulation2018#^c1]]"
---

## Definition

Molecular dynamics (MD) simulations integrate Newton's equations of motion numerically to give atomistic trajectories over time. A simulation steps through time, repeatedly computing the force on each atom from an approximate [[force field]] and using it to update positions and velocities. MD is flexible: temperature, pressure, pH and the presence of ligands or other biomolecules can be varied. Given long enough sampling at constant temperature, the trajectory samples the [[Boltzmann distribution]] of the force field, not of the real protein.

## Equations

$$ m_a \frac{d^2 x_a}{dt^2} = -\nabla_{x_a} U(x) $$
^eq-newton

Source: [[@hollingsworthMolecularDynamicsSimulation2018#^c4]] and [[@hollingsworthMolecularDynamicsSimulation2018#^c5]], p. 2 (in prose; the paper displays no equation).
Manuscript form: none. **Gap:** for a displayed equation, a textbook or methods source (e.g. Karplus and McCammon) needs a quote block. Here $t$ is simulation time, not HDX labelling time; the two are not confused in context.

## Assumptions and limits

- Force fields are approximate ([[@hollingsworthMolecularDynamicsSimulation2018#^c2]]).
- A simulation needs millions to billions of time steps ([[@hollingsworthMolecularDynamicsSimulation2018#^c1]]), and processes such as conformational change often take longer than classical all-atom MD can reach ([[@hollingsworthMolecularDynamicsSimulation2018#^c3]]). This is the sampling gap that enhanced sampling and learned generators address.
- Statistics hold only after equilibration and convergence, and until then depend on the starting structures. The basic check is reproducibility across independent starts ([[equilibration and convergence]]).
- MD time $t$ is physical simulation time. It is not HDX labelling time, and not the diffusion time $\tau$ of a [[diffusion model]].
- [[enhanced sampling]] reaches rare states faster, but usually at the cost of kinetics, and recovers populations only by reweighting ([[sampling coverage]]).
- Thermostats and barostats (which give Langevin-type dynamics) are needed to sample the canonical ensemble. They are not covered here.
- Protonation states are assigned once, before the run, for one pH, and stay fixed ([[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]). A simulation "at pH 4" is therefore a simulation with the states someone chose for pH 4 ([[pKa]]).
- Experimental data can enter during the simulation rather than afterwards, through a [[restrained simulation]] or [[metainference]].

## Why it matters here

MD is the physics-based ensemble generator and the source of the Boltzmann prior in [[maximum entropy principle|MaxEnt reweighting]]. The [[diffusion model]] note links back to it through the score of the Boltzmann distribution.

Claims that use this term: [[MD is computationally expensive and may only approximate true dynamics due to force-field inaccuracies and limited sampling.]], [[Sufficiently sampled equilibrium MD targets the Boltzmann distribution of its approximate force field, not the protein's true distribution.]], [[Until MD has converged, its statistics depend on the starting structures; reproducibility across independent starts is the basic check.]], [[Learned generators are used to seed MD simulations, combining broad coverage with physics-based sampling.]], [[MD simulations allow controlled changes to the protein and its environment.]], [[MD simulations can model varied conditions such as temperature, pressure, pH and the presence of ligands or other biomolecules.]], [[MD simulations numerically integrate Newton's equations of motion, giving atomistic insight into protein dynamics over time.]].
