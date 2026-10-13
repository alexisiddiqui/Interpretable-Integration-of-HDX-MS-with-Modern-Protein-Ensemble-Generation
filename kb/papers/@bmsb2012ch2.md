---
type: paper
citekey: bmsb2012ch2
year: 2012
read: false
pdf: kb/_pdf/@bmsb2012ch2.pdf
extraction: auto
needs_review: false
review_reason:
---

# Monte Carlo Methods for Inference in High-Dimensional Systems

Chapter 2 of Hamelryck, Mardia and Ferkinghoff-Borg (eds), *Bayesian Methods in Structural Bioinformatics*, Springer 2012 (DOI 10.1007/978-3-642-27225-7). Author(s): Ferkinghoff-Borg, Jesper. Printed pages 49–96.

PDF note: the PDF holds this chapter only, so PDF page = printed page − 48. The book prints one shared reference list at the end, which is not in this PDF. Use this chapter for mathematical definitions and derivations; quote the sentence that introduces an equation and give the equation number in the citing note's body.


## Main point

Monte Carlo methods estimate expectations and free-energy ratios by sampling. Importance sampling and MCMC are only as good as the overlap between the sampled and target distributions and the convergence of the chain. Generalised ensembles and histogram reweighting recover target averages from biased sampling.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- A target distribution is a weight function known up to its normalisation, the partition function (Eq. 2.1). ^c1
  - page: 2
  - quote: "up to a normalization constant, Z, also known as the partition function."
  - quote_check: pass
  - reviewed: false
- Any probability distribution can be brought to canonical (Boltzmann) form by redefining an energy (Eq. 2.3). ^c2
  - page: 3
  - quote: "any probability distribution can be brought to the canonical form by a suitable"
  - quote_check: pass
  - reviewed: false
- A reference distribution is distinguished from the target distribution (Eq. 2.4). ^c3
  - page: 5
  - quote: "reference state in distinction to the target distribution p."
  - quote_check: pass
  - reviewed: false
- With the prior as reference, the energy is the negative log-likelihood (Eq. 2.9). ^c4
  - page: 6
  - quote: "is the “energy” associated with the likelihood-function."
  - quote_check: pass
  - reviewed: false
- Importance sampling draws from a biased distribution and corrects with importance weights (Eqs. 2.14-2.16). ^c5
  - page: 8
  - quote: "The basis of importance sampling is to impose a certain bias in the"
  - quote_check: pass
  - reviewed: false
- The correcting ratios are the importance weights. ^c6
  - page: 8
  - quote: "are known as the importance weights."
  - quote_check: pass
  - reviewed: false
- Importance sampling is efficient only if the sampling distribution resembles the target. ^c7
  - page: 9
  - quote: "The efficiency of the importance sampling relies crucially on how well"
  - quote_check: pass
  - reviewed: false
- The effective sample size of importance sampling can be far smaller than the apparent sample size. ^c8
  - page: 9
  - quote: "the effective sample size can be much smaller than the apparent sample size"
  - quote_check: pass
  - reviewed: false
- A poor importance-sampling distribution can give arbitrarily wrong results with no diagnostic warning. ^c9
  - page: 9
  - quote: "produce results that are arbitrarily in error with no diagnostic indication"
  - quote_check: pass
  - reviewed: false
- MCMC transition rules satisfy detailed balance (Eq. 2.22). ^c10
  - page: 11
  - quote: "satisfy the detailed balance equation,"
  - quote_check: pass
  - reviewed: false
- Detailed balance is a sufficient condition for the chain to converge to the target distribution. ^c11
  - page: 11
  - quote: "sufficient requirement to insure that the sampled distribution will converge to the"
  - quote_check: pass
  - reviewed: false
- The acceptance rates of MCMC can be chosen freely; Metropolis-Hastings is the standard choice (Eqs. 2.23-2.25). ^c12
  - page: 11
  - quote: "There is a considerable freedom in the choice of acceptance rates"
  - quote_check: pass
  - reviewed: false
- MCMC sampling only gives ratios of partition functions, not absolute values. ^c13
  - page: 17
  - quote: "This reflects the fact, that MCMC-sampling only allows ratios of"
  - quote_check: pass
  - reviewed: false
- Slow mixing reduces the effective number of samples and can give misleading results. ^c14
  - page: 18
  - quote: "mixing reduces the effective number of samples and may easily lead to results which"
  - quote_check: pass
  - reviewed: false
- The first test of convergence should be the reproducibility of the sampling. ^c15
  - page: 19
  - quote: "The first and foremost test should always be the reproducibility of the sampling"
  - quote_check: pass
  - reviewed: false
- Extended ensembles replace the target with an artificial distribution that is easier to sample. ^c16
  - page: 21
  - quote: "is replaced with an “artificial” distribution constructed either as an extension"
  - quote_check: pass
  - reviewed: false
- Advanced sampling methods do not remove the need to assess convergence critically. ^c17
  - page: 30
  - quote: "do not alleviate the need for making critical assessment of the convergence"
  - quote_check: pass
  - reviewed: false
- Histogram reweighting to another temperature requires that the sampled range covers the target (Eqs. 2.69-2.70). ^c18
  - page: 42
  - quote: "The only two prerequisites for this reweighting scheme is that the variation of the"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $x$ | state | $x$ |  |
| $p(x) = \omega(x)/Z$ | target distribution, from an unnormalised weight | $P(x)$ |  |
| $\pi(x)$ | reference distribution; the prior in a Bayes model | $P_0(x)$ |  |
| $q(x)$ | importance-sampling proposal | $P_0(x)$ | when the samples are frames of a prior |
| $r_i$, $\tilde r_i$ | importance weights, normalised | $w_j$ | sample index $i$ becomes conformer index $j$ |
| $E(x)$ | energy, or $-\ln\omega(x)$ (Eq. 2.3) | $U(x)$ | a statistical energy unless $\omega$ is a Boltzmann weight |
| $\beta$ | inverse temperature | — | write $1/k_BT$ |
| $k$ | Boltzmann constant | $k_B$ |  |
| $\mathcal{D}$ | data | $s^\text{exp}$ |  |
| $W(x' \mid x)$ | transition matrix | $\mathcal{T}(x' \mid x)$ |  |
| $q(x' \mid x)$ | proposal of a Monte Carlo move | $\mathcal{Q}(x' \mid x)$ |  |
| $a(x' \mid x)$ | acceptance probability | $a(x' \mid x)$ |  |
| $f(x)$, $y$ | collective variable and its value | $\xi(x)$ | also written $\lambda$ (p. 6) |
| $\lambda$ | collective variables (p. 6); a Lagrange parameter (Eq. 2.59) | — | write $\xi$; $\lambda_i$ are MaxEnt multipliers |
| $p_0(x)$ | initial distribution of the chain | — | not the prior; $P_0$ is the prior |
| $t$, $T$ | Monte Carlo time, chain length | — | $t$ is labelling time and $T$ temperature |
| $g(E)$ | density of states | — | $g(\tau)$ is the diffusion coefficient |
| $\Omega$ | state space | — |  |

## What I use from it

The reference distribution (Eq. 2.4), importance weights and effective sample size (Eqs. 2.14-2.16), detailed balance and convergence diagnostics, and reweighting of biased samples. Used in [[importance sampling]] and [[Markov chain Monte Carlo]]. The point carried into the thesis: diverse samples are not evidence of correct populations.

## Disagreements / limitations
