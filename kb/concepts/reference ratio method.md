---
type: concept
aliases:
  - reference ratio
  - reference distribution
  - reference distributions
notation:
  - {symbol: '\xi(x)', meaning: 'coarse-grained variable of conformation x', units: null}
  - {symbol: 'P_0(\xi)', meaning: 'marginal of the prior on the coarse-grained variable xi', units: null}
  - {symbol: 'P^*(\xi)', meaning: 'target distribution of the coarse-grained variable xi', units: null}
  - {symbol: '\hat P(x)', meaning: 'reference-ratio distribution over conformations', units: null}
sources:
  - "[[@bmsb2012ch4#^c1]]"
  - "[[@bmsb2012ch4#^c2]]"
  - "[[@bmsb2012ch4#^c3]]"
  - "[[@bmsb2012ch4#^c4]]"
  - "[[@bmsb2012ch4#^c7]]"
  - "[[@bmsb2012ch3#^c11]]"
  - "[[@bmsb2012ch3#^c12]]"
  - "[[@bmsb2012ch3#^c13]]"
  - "[[@bmsb2012ch2#^c3]]"
---

## Definition

The reference ratio method corrects a generator so that a coarse-grained variable follows a desired distribution, while keeping the generator's fine-grained detail. The generator's own marginal on the coarse variable is the reference distribution: divide it out, multiply in the target, and the conditional distribution of fine-grained structure given the coarse variable is unchanged. The result is the smallest change to the generator, in Kullback–Leibler terms, that has the target marginal. It explains knowledge-based potentials as ratios against the reference that a sampler implies. For the thesis it is a conceptual precedent for correcting a generator's populations with data, not the derivation of MaxEnt reweighting.

## Equations

$$ \hat P(x) = \frac{P^*\big(\xi(x)\big)}{P_0\big(\xi(x)\big)}\, P_0(x) $$
^eq-reference-ratio

Source: [[@bmsb2012ch4#^c2]], Theorem 4.1, Eq. (4.2), p. 3; [[@bmsb2012ch3#^c12]], Eqs. (3.66)–(3.72), pp. 25–26. Frellsen et al. write the generator $g(x)$, its marginal $g_1(y)$, the target $f_1(y)$ and the coarse variable $Y = m(X)$ (notation: [[@bmsb2012ch4#Notation]]). Borg et al. write $q(r \mid a)$, $\tilde q(\lambda \mid a)$ and $p(\lambda \mid a)$ (notation: [[@bmsb2012ch3#Notation]]).

$$ \hat P = \arg\min_{P\,:\; P(\xi) = P^*(\xi)} D_\text{KL}(P_0 \Vert P) $$
^eq-reference-ratio-kl

Source: [[@bmsb2012ch4#^c3]], Theorem 4.2, p. 3 (proof p. 4), written $\arg\min_{h \in D} \text{KL}[g \Vert h]$.

## Derivation

1. Take a fine-grained variable $x$ and a coarse-grained variable $\xi = \xi(x)$ that is a many-to-one function of it ([[@bmsb2012ch4#^c1]], p. 2).
2. Ask for a density whose $\xi$-marginal is $P^*$ and whose conditional $P(x \mid \xi)$ is the generator's $P_0(x \mid \xi)$ (Eq. 4.1, p. 2).
3. Any density factorises as $P(x) = P(\xi(x))\, P(x \mid \xi(x))$ (Eq. 4.3). Insert the two requirements and use $P_0(x \mid \xi) = P_0(x)/P_0(\xi)$ to obtain [[#^eq-reference-ratio]] ([[@bmsb2012ch4#^c2]], Eq. 4.2).
4. Among all densities with marginal $P^*$, this one minimises $D_\text{KL}(P_0 \Vert P)$ ([[@bmsb2012ch4#^c3]], Theorem 4.2).
5. The same density minimises the other direction, $D_\text{KL}(P \Vert P_0)$, under the same constraint. By the chain rule, $D_\text{KL}(P \Vert P_0) = D_\text{KL}(P^* \Vert P_0(\xi)) + \mathbb{E}_{P^*}\!\left[D_\text{KL}\big(P(x\mid\xi) \Vert P_0(x\mid\xi)\big)\right]$. The first term is fixed, and the second is zero only when the conditionals agree (step ours).
6. MaxEnt reweighting fixes only a few ensemble averages $\langle s_i \rangle$, not a whole marginal. Its solution $P_0\, e^{-\sum_i \lambda_i s_i}$ ([[maximum entropy principle#^eq-maxent-posterior]]) becomes the reference ratio only if the constraints pin down the entire distribution of $\xi$, for example indicator functions on every $\xi$ bin (step ours). The two methods share the minimum-information idea and differ in what the data constrain.

## Assumptions and limits

- The reference must be the generator's own marginal. With a sampler, the proper reference for a knowledge-based potential is the marginal implied by the sampler alone ([[@bmsb2012ch3#^c11]], [[@bmsb2012ch3#^c13]], p. 27). This needs the sampler to satisfy detailed balance (footnote, p. 27).
- $P_0(\xi)$ is rarely known in closed form. It is estimated from samples, iteratively when $\xi$ is high-dimensional (Eq. 3.76, p. 27).
- The construction assumes the generator is right locally and wrong globally ([[@bmsb2012ch4#^c7]], p. 10). Samples from the local generator TORUSDBN alone are not compact native-like structures ([[@bmsb2012ch4#^c4]], p. 6).
- In BMSB ch2 the same word "reference distribution" means any distribution against which a target is measured, as in a ratio of partition functions $Z/Z_\pi$ ([[@bmsb2012ch2#^c3]], Eq. 2.4, p. 5).
- Guided diffusion faces the same problem from the other side: it biases a learned prior towards data or energy without a principled correction of the remaining statistics ([[guided diffusion]]).

## Why it matters here

The reference ratio method shows a principled way to impose coarse-grained statistics on a generator without destroying its fine-grained structure. That is the move the thesis makes when reweighting or guiding generated ensembles with HDX-MS. It also makes the introduction's point (§1.4) exact: what a statistical correction means depends on the reference distribution implied by the generator.

Claims that use this term: [[The meaning of a statistical correction depends on the reference distribution implied by the model or sampling procedure.]], [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]].
