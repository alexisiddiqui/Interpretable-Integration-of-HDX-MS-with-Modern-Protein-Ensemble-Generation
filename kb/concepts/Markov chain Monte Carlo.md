---
type: concept
aliases:
  - MCMC
  - Monte Carlo
  - Metropolis-Hastings
  - Metropolis–Hastings
  - detailed balance
  - ergodicity
  - extended ensemble
notation:
  - {symbol: '\mathcal{T}(x'' \mid x)', meaning: 'Markov-chain transition probability from x to x''', units: null}
  - {symbol: '\mathcal{Q}(x'' \mid x)', meaning: 'proposal distribution of a Monte Carlo move from x to x''', units: null}
  - {symbol: 'a(x'' \mid x)', meaning: 'Metropolis–Hastings acceptance probability of a move from x to x''', units: null}
sources:
  - "[[@bmsb2012ch2#^c10]]"
  - "[[@bmsb2012ch2#^c11]]"
  - "[[@bmsb2012ch2#^c12]]"
  - "[[@bmsb2012ch2#^c13]]"
  - "[[@bmsb2012ch2#^c14]]"
  - "[[@bmsb2012ch2#^c15]]"
  - "[[@bmsb2012ch2#^c16]]"
  - "[[@bmsb2012ch2#^c17]]"
  - "[[@bmsb2012ch2#^c18]]"
---

## Definition

Markov chain Monte Carlo (MCMC) samples a distribution known only up to its normalisation by running a random walk whose long-run distribution is the target. If every state can be reached (ergodicity) and the transition rule satisfies detailed balance with respect to the target, the chain converges to the target. The Metropolis–Hastings algorithm builds such a rule from any proposal by accepting or rejecting moves. Convergence ([[equilibration and convergence]]) is never guaranteed in finite time: slow mixing makes consecutive samples redundant and leaves results dependent on where the chain started. Extended ensembles (parallel tempering, multicanonical sampling), one family of [[enhanced sampling]], sample an easier artificial distribution and recover target averages by reweighting.

## Equations

$$ P(x)\, \mathcal{T}(x' \mid x) = P(x')\, \mathcal{T}(x \mid x') $$
^eq-detailed-balance

Source: [[@bmsb2012ch2#^c10]] and [[@bmsb2012ch2#^c11]], Eq. (2.22), p. 11. Ferkinghoff-Borg writes the transition matrix $W(x' \mid x)$ (notation: [[@bmsb2012ch2#Notation]]).

$$ \mathcal{T}(x' \mid x) = \mathcal{Q}(x' \mid x)\, a(x' \mid x), \qquad a(x' \mid x) = \min\left\{1,\ \frac{P(x')\, \mathcal{Q}(x \mid x')}{P(x)\, \mathcal{Q}(x' \mid x)}\right\} $$
^eq-metropolis-hastings

Source: [[@bmsb2012ch2#^c12]], Eqs. (2.23) and (2.25), p. 11. The proposal is written $q(x' \mid x)$ there.

## Derivation

1. A Markov chain is fixed by its transition probabilities. If it is irreducible (ergodic) and aperiodic, it has a unique limit distribution (Eqs. 2.18–2.21, pp. 10–11).
2. Detailed balance with respect to $P$ is a sufficient condition for that limit to be $P$ ([[@bmsb2012ch2#^c11]], Eq. 2.22).
3. Split each transition into a proposal and an acceptance (Eq. 2.23). Detailed balance then fixes only the ratio of acceptances (Eq. 2.24), and the Metropolis–Hastings choice satisfies it ([[@bmsb2012ch2#^c12]], Eq. 2.25).
4. The normalisation of $P$ cancels in the acceptance ratio, so only an unnormalised density, such as $e^{-U(x)/k_BT}$, is needed (p. 11). For the same reason, sampling yields only ratios of partition functions ([[@bmsb2012ch2#^c13]], p. 17).

## Assumptions and limits

- Results are valid only after the chain has converged. Slow mixing reduces the effective number of samples and can give misleading results ([[@bmsb2012ch2#^c14]], p. 18).
- "The first and foremost test should always be the reproducibility of the sampling" ([[@bmsb2012ch2#^c15]], p. 19), for example from independent starting points.
- Extended ensembles replace the target with an artificial distribution ([[@bmsb2012ch2#^c16]], p. 21). Their samples must be reweighted back to the target, which works only where the sampled range covers it ([[@bmsb2012ch2#^c18]], p. 42). They "do not alleviate the need for making critical assessment of the convergence" ([[@bmsb2012ch2#^c17]], p. 30).
- MD with a thermostat is also a sampler of the [[Boltzmann distribution]], and the same convergence caveats apply (ours).

## Why it matters here

Every candidate ensemble in the thesis comes from a sampler: MD, enhanced sampling or a learned generator. Sampling quality is therefore part of the inference. Generated diversity is not, by itself, evidence of equilibrium populations (introduction §1.5). Biased or adaptive samples need reweighting before their weights mean populations (§1.3), and reproducibility across replicates is the basic convergence check, as in jaxENT.

Claims that use this term: [[MD is computationally expensive and may only approximate true dynamics due to force-field inaccuracies and limited sampling.]], [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]], [[Offline biasing methods can be used to enhance sampling under equilibrium conditions.]], [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]].
