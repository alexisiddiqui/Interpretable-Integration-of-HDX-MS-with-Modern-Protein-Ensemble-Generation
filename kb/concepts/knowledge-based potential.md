---
type: concept
aliases:
  - knowledge-based potentials
  - KBP
  - inverse Boltzmann
  - potential of mean force
  - reference state
notation:
  - {symbol: '\xi(x)', meaning: 'coarse-grained variable of conformation x', units: null}
  - {symbol: '\Delta F(\xi)', meaning: 'free energy along xi relative to a reference state', units: 'kJ mol^-1'}
  - {symbol: '\tilde P(\xi)', meaning: 'reference-state distribution of xi', units: null}
  - {symbol: 'P(\xi)', meaning: 'marginal of the target distribution on the coarse-grained variable xi', units: null}
  - {symbol: 'n_\text{obs}(\xi)', meaning: 'observed count of xi in a structure database', units: null}
  - {symbol: 'n_\text{exp}(\xi)', meaning: 'count of xi expected in the reference state', units: null}
sources:
  - "[[@bmsb2012ch3#^c4]]"
  - "[[@bmsb2012ch3#^c5]]"
  - "[[@bmsb2012ch3#^c6]]"
  - "[[@bmsb2012ch3#^c7]]"
  - "[[@bmsb2012ch3#^c8]]"
  - "[[@bmsb2012ch3#^c9]]"
  - "[[@bmsb2012ch3#^c10]]"
  - "[[@bmsb2012ch3#^c11]]"
  - "[[@bmsb2012ch3#^c14]]"
  - "[[@bmsb2012ch4#^c5]]"
  - "[[@bmsb2012ch4#^c6]]"
  - "[[@bmsb2012ch1#^c8]]"
---

## Definition

A knowledge-based potential (KBP) is a [[statistical potential]] built from counts in a structure database. It turns statistics of known protein structures into an "energy" by inverting the Boltzmann distribution: features seen more often than expected get low energy. The expectation comes from a reference state. In statistical mechanics, a free energy along a coarse-grained variable relative to an interaction-free reference is well defined, and Eq. 3.33 gives it as a probability ratio. KBPs use the same formula with database statistics pooled across different proteins, so their reference state is ill-defined and their "energies" are not physical free energies. They are statistical constructs, and their meaning depends on the reference distribution they imply.

## Equations

$$ e^{-\Delta F(\xi)/k_BT} = \frac{P(\xi)}{\tilde P(\xi)} = \frac{n_\text{obs}(\xi)}{n_\text{exp}(\xi)} $$
^eq-inverse-boltzmann

Source: [[@bmsb2012ch3#^c5]], Eq. (3.33), p. 10. Borg et al. write the coarse-grained variable as $\lambda$, the target as $p_\beta(\lambda)$ and $\beta$ for $1/k_BT$ (notation: [[@bmsb2012ch3#Notation]]). Here $n_\text{obs}$ and $n_\text{exp}$ are the observed counts and those expected in the reference state.

## Derivation

1. A free energy along a coarse-grained variable, $F(\xi)$, contains an entropy contribution, so strictly it is no longer a potential of mean force ([[@bmsb2012ch3#^c4]], Eq. 3.30, p. 9).
2. Measured against the interaction-free state of the *same* system, the free-energy difference is a ratio of two probabilities ([[@bmsb2012ch3#^c5]], Eq. 3.33). This is well defined.
3. KBPs apply Eq. 3.33 to statistics of many *different* proteins, the "inverse Boltzmann law" ([[@bmsb2012ch3#^c6]], p. 11). The resulting "energy" differs from the physical energy of the state ([[@bmsb2012ch3#^c7]], p. 14).
4. Unless strict self-consistency conditions hold, KBPs are "typically only crude approximations" ([[@bmsb2012ch3#^c8]], p. 21). There is no a priori reason to expect a particular KBP to be a physical free energy ([[@bmsb2012ch3#^c9]], p. 23), and they can only be assessed by using them in a full canonical calculation ([[@bmsb2012ch3#^c10]], p. 23).
5. If the KBP is used with a given sampler or prior, the reference state is no longer arbitrary. It is the marginal that the sampler implies ([[@bmsb2012ch3#^c11]], p. 25). See [[reference ratio method]].

## Assumptions and limits

- Any distribution can be written in Boltzmann form, with energy $-\ln P$ ([[@bmsb2012ch1#^c8]], p. 29). Writing a density as an energy does not make it physical.
- KBPs are in general not free energies or potentials of mean force in the statistical-mechanics sense ([[@bmsb2012ch3#^c14]], p. 28). The reference ratio method explains them as statistical constructs, not physical potentials ([[@bmsb2012ch4#^c5]], [[@bmsb2012ch4#^c6]], p. 9).

## Why it matters here

Learned generators and their scores raise the same question. A generator's log-density or confidence score is a statistical quantity. It becomes a free energy only with a defined probabilistic model and reference distribution, which is the caution of introduction §1.3. The populations reported by a generator are its own distribution, a prior to be checked against experiment, not an equilibrium result ([[diffusion model]], [[importance sampling]]).

Claims that use this term: [[Deep-learning models trained on large structural datasets learn conformation distributions, and sampling them yields ensembles.]], [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]], [[A knowledge-based potential is not a thermodynamic free energy unless its probabilistic model and reference distribution are defined.]], [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]].
