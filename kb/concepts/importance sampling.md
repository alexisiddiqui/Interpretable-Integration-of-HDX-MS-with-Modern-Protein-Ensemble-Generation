---
type: concept
aliases:
  - importance weights
  - effective sample size
  - ESS
  - reweighting estimator
notation:
  - {symbol: 'P(x)', meaning: 'target distribution over conformations', units: null}
sources:
  - "[[@bmsb2012ch2#^c5]]"
  - "[[@bmsb2012ch2#^c6]]"
  - "[[@bmsb2012ch2#^c7]]"
  - "[[@bmsb2012ch2#^c8]]"
  - "[[@bmsb2012ch2#^c9]]"
  - "[[@bmsb2012ch2#^c1]]"
  - "[[@heninEnhancedSamplingMethods2022#^c7]]"
  - "[[@noeBoltzmannGeneratorsSampling2019#^c3]]"
---

## Definition

Importance sampling estimates averages under a target distribution from samples drawn from a different one. Each sample is weighted by the ratio of target to sampling density, the importance weight. The estimate is only as good as the overlap between the two distributions. When the sampling distribution is much broader than the target, or misses regions the target cares about, a few weights dominate, the effective sample size collapses and the estimate can be badly wrong with nothing to show it. Ensemble reweighting is importance sampling: the frames of a simulation or generator are samples of the prior, and the fitted weights are importance weights towards the posterior.

## Equations

$$ \langle s \rangle_P = \int s(x)\, \frac{P(x)}{P_0(x)}\, P_0(x)\, dx \;\approx\; \sum_{j=1}^{M} w_j\, s(x_j), \qquad w_j = \frac{P(x_j)/P_0(x_j)}{\sum_{j'} P(x_{j'})/P_0(x_{j'})}, \quad x_j \sim P_0 $$
^eq-importance-sampling

Source: [[@bmsb2012ch2#^c5]] and [[@bmsb2012ch2#^c6]], Eqs. (2.14)–(2.16) and the self-normalised form that follows them, p. 8. Ferkinghoff-Borg writes the proposal $q(x) = \omega_q(x)/Z_q$, the target $p(x) = \omega(x)/Z$ and the importance weights $r_i = \omega(x_i)/\omega_q(x_i)$; only unnormalised densities are needed, because $Z$ and $Z_q$ cancel in the self-normalised weights (notation: [[@bmsb2012ch2#Notation]]).

## Derivation

1. Write the target average as an integral over $P$ (Eq. 2.14), then multiply and divide by the sampling distribution, here the prior $P_0$ (Eq. 2.15).
2. Replace the integral by a sum over samples from $P_0$, weighting each by $P/P_0$ (Eq. 2.16; [[@bmsb2012ch2#^c6]]). Normalising the weights removes the unknown partition functions (p. 8).
3. When $P = P_0$, all weights are equal and the estimate is the plain average (Eq. 2.17).
4. For MaxEnt, $P_\text{ME}/P_0 \propto e^{-\sum_i \lambda_i s_i(x)}$ ([[maximum entropy principle#^eq-maxent-posterior]]). The importance weights of frames drawn from the prior are then $w_j \propto w_j^0 e^{-\sum_i \lambda_i q_i(j)}$, the MaxEnt weights of [[maximum entropy principle#^eq-maxent-weights]] (step ours).

## Assumptions and limits

- Efficiency depends on how well the sampling distribution approximates the target ([[@bmsb2012ch2#^c7]], p. 9). The effective sample size can be much smaller than the number of frames ([[@bmsb2012ch2#^c8]]), and a poor match can "produce results that are arbitrarily in error with no diagnostic indication" ([[@bmsb2012ch2#^c9]]). The enhanced sampling literature states the same condition: recovering unbiased statistics "depends crucially on good overlap" ([[@heninEnhancedSamplingMethods2022#^c7]]).
- States that the prior never sampled get no weight. Reweighting redistributes populations; it cannot create conformations.
- The prior weights $w_j^0$ must be the frames' actual sampling probabilities. For an unbiased equilibrium simulation they are equal. For biased [[enhanced sampling]] they come from the bias; pooled frames from adaptive seeding have no simple sampling probability ([[sampling coverage]]). A [[Boltzmann generator]] is the case where the generator's exact density is known, so its samples can be reweighted to the Boltzmann distribution ([[@noeBoltzmannGeneratorsSampling2019#^c3]]). For a learned generator, equal $w_j^0$ means taking the generator's own distribution as the prior, which is not a Boltzmann distribution ([[knowledge-based potential]], [[reference ratio method]]) (ours).
- **Gap:** BMSB gives no formula for the effective sample size. The common estimate $N_\text{eff} = 1/\sum_j w_j^2$ (Kish) needs a source before the thesis uses it.
- Guided and force-guided generators change the sampling distribution but do not supply importance weights; ConfDiff calls its force guidance "reweighting" without computing any ([[guided diffusion]]). Their samples need weights before they can stand for populations.

## Why it matters here

Reading reweighting as importance sampling explains both its power and its limits. It is why the candidate ensemble matters so much in introduction §1.4, why a few dominant weights signal a poor prior rather than a precise answer, and why ValDX and jaxENT track how far the weights move from the prior (KL divergence, apparent work).

Claims that use this term: [[Reweighting ensembles to fit experiment while minimising deviation from the original identifies the minimal changes needed.]], [[Successful reweighting shows which conformations fit experiment, giving pseudo-structural models of solution behaviour.]], [[Offline biasing methods can be used to enhance sampling under equilibrium conditions.]], [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]], [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]], [[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]], [[Machine-learned force fields learn energies and forces for simulation, whereas Boltzmann generators generate configurations and reweight them to the Boltzmann distribution.]], [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]].
