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

Molecular dynamics (MD) simulations integrate Newton's equations of motion numerically to give atomistic trajectories over time. A simulation steps through time, repeatedly computing the force on each atom from an approximate force field and using it to update positions and velocities. MD is flexible: temperature, pressure, pH and the presence of ligands or other biomolecules can be varied. Given long enough sampling at constant temperature, the trajectory samples the [[Boltzmann distribution]] of the force field.

## Equations

$$ m_a \frac{d^2 x_a}{dt^2} = -\nabla_{x_a} U(x) $$
^eq-newton

Source: [[@hollingsworthMolecularDynamicsSimulation2018#^c4]] and [[@hollingsworthMolecularDynamicsSimulation2018#^c5]], p. 2 (in prose; the paper displays no equation).
Manuscript form: none. **Gap:** for a displayed equation, a textbook or methods source (e.g. Karplus and McCammon) needs a quote block. Here $t$ is simulation time, not HDX labelling time; the two are not confused in context.

## Assumptions and limits

- Force fields are approximate ([[@hollingsworthMolecularDynamicsSimulation2018#^c2]]).
- A simulation needs millions to billions of time steps ([[@hollingsworthMolecularDynamicsSimulation2018#^c1]]), and processes such as conformational change often take longer than classical all-atom MD can reach ([[@hollingsworthMolecularDynamicsSimulation2018#^c3]]). This is the sampling gap that enhanced sampling and learned generators address.
- Thermostats and barostats (which give Langevin-type dynamics) are needed to sample the canonical ensemble. They are not covered here.

## Why it matters here

MD is the physics-based ensemble generator and the source of the Boltzmann prior in [[maximum entropy principle|MaxEnt reweighting]]. The [[diffusion model]] note links back to it through the score of the Boltzmann distribution.

Claims that use this term: [[MD simulations are particularly useful beyond resolution because of their flexibility.]], [[MD simulations can model varied conditions such as temperature, pressure, pH and the presence of ligands or other biomolecules.]], [[MD simulations numerically integrate Newton's equations of motion, giving atomistic insight into protein dynamics over time.]].
