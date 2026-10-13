---
type: concept
aliases:
  - Boltzmann weight
  - Boltzmann factor
  - canonical ensemble
  - partition function
  - Helmholtz free energy
notation:
  - {symbol: 'x', meaning: 'a molecular conformation (atomic coordinates)', units: null}
  - {symbol: 'U(x)', meaning: 'potential energy of conformation x', units: 'kJ mol^-1'}
  - {symbol: 'k_B', meaning: 'Boltzmann constant', units: 'J K^-1'}
  - {symbol: 'R', meaning: 'molar gas constant', units: 'J mol^-1 K^-1'}
  - {symbol: 'T', meaning: 'absolute temperature', units: 'K'}
  - {symbol: 'Z', meaning: 'configurational partition function', units: null}
  - {symbol: 'F', meaning: 'Helmholtz free energy', units: 'kJ mol^-1'}
  - {symbol: 'S', meaning: 'thermodynamic entropy of the ensemble', units: 'J K^-1'}
sources:
  - "[[@bmsb2012ch3#^c1]]"
  - "[[@bmsb2012ch3#^c2]]"
  - "[[@bmsb2012ch3#^c3]]"
  - "[[@cesariUsingMaximumEntropy2018#^c15]]"
---

## Definition

At thermal equilibrium, the probability of a conformation is proportional to the exponential of minus its energy divided by $k_BT$. Low-energy conformations are therefore exponentially more likely. The partition function $Z$ normalises the distribution, and its logarithm gives the Helmholtz free energy. The free energy is the average energy minus $T$ times the entropy. An MD force field defines $U(x)$, so the Boltzmann distribution is the prior that a simulated ensemble samples.

## Equations

$$ p(x) = \frac{1}{Z} e^{-U(x)/k_BT}, \qquad Z = \int e^{-U(x)/k_BT}\, dx $$
^eq-boltzmann

Source: [[@bmsb2012ch3#^c1]], Eq. (3.1), p. 3 (with momenta), and Eq. (3.6), p. 4 (configurational $Z$); [[@cesariUsingMaximumEntropy2018#^c15]], p. 3.
Manuscript form: none displayed. Bradshaw writes the frame weights as $\propto \exp\{-U(X)/k_BT\}$ (Eq. 4 context).

$$ F = -k_BT \ln Z $$
^eq-helmholtz

Source: [[@bmsb2012ch3#^c2]], Eq. (3.7), p. 4.

$$ F = \mathbb{E}_p[U] - TS $$
^eq-free-energy-entropy

Source: [[@bmsb2012ch3#^c3]], Eq. (3.9), p. 5.

## Assumptions and limits

- The system is at equilibrium at fixed $T$ (canonical ensemble).
- In practice $U(x)$ is an approximate force field, so the "Boltzmann prior" of a simulation inherits force-field error.
- BMSB uses $\beta = 1/k_BT$. The thesis writes $1/k_BT$ explicitly, because $\beta_C$ and $\beta_H$ already use $\beta$ ([[2026-10-13 canonical HDX and ensemble notation]]).

## Why it matters here

The Boltzmann distribution links energy to population. It is the prior in [[maximum entropy principle|MaxEnt reweighting]], and it is why reweighting can be read as a correction to the potential. It also underlies the [[conformational free-energy landscape]] and the $\Delta G_\text{op}$ of a [[protection factor]].
