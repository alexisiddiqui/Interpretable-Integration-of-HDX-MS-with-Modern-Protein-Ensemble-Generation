---
type: paper
citekey: bmsb2012ch1
year: 2012
read: false
pdf: kb/_pdf/@bmsb2012ch1.pdf
extraction: auto
needs_review: false
review_reason:
---

# An Overview of Bayesian Inference and Graphical Models

Chapter 1 of Hamelryck, Mardia and Ferkinghoff-Borg (eds), *Bayesian Methods in Structural Bioinformatics*, Springer 2012 (DOI 10.1007/978-3-642-27225-7). Author(s): Hamelryck, Thomas. Printed pages 3–48.

PDF note: the PDF holds this chapter only, so PDF page = printed page − 2. The book prints one shared reference list at the end, which is not in this PDF. Use this chapter for mathematical definitions and derivations; quote the sentence that introduces an equation and give the equation number in the citing note's body.


## Main point

Bayesian inference updates a prior with a likelihood to give a posterior over hypotheses. Nuisance parameters are integrated out, point estimates are a last resort, and models are compared by their evidence. The chapter also derives the Boltzmann distribution from maximum entropy.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Bayesian probability calculus uses Bayes' theorem (Eq. 1.1). ^c1
  - page: 5
  - quote: "The Bayesian probability calculus makes use of Bayes’ theorem"
  - quote_check: pass
  - reviewed: false
- The posterior is proportional to the likelihood, which brings in the data, times the prior. ^c2
  - page: 5
  - quote: "The posterior distribution is proportional to the product of the likelihood, which brings in the information in the data"
  - quote_check: pass
  - reviewed: false
- Bayesian structure determination aims at a posterior over structures, obtained in practice by sampling an ensemble of structures. ^c3
  - page: 4
  - quote: "a posterior distribution over the space of relevant protein structures; this can be accomplished by sampling an ensemble of protein structures."
  - quote_check: pass
  - reviewed: false
- In the Bayesian approach, latent nuisance parameters are integrated out (marginalised). ^c4
  - page: 8
  - quote: "such latent nuisance parameters are dealt with by simply integrating"
  - quote_check: pass
  - reviewed: false
- Point estimates such as MAP make most sense only when the posterior is sharply peaked and unimodal. ^c5
  - page: 11
  - quote: "point estimates will make most sense when the posterior is sharply peaked and unimodal."
  - quote_check: pass
  - reviewed: false
- The Bayes factor (Eq. 1.6) resembles a likelihood ratio but integrates over the parameters. ^c6
  - page: 25
  - quote: "Bayes factor is similar to the classic likelihood ratio, but involves integrating"
  - quote_check: pass
  - reviewed: false
- The maximum entropy solution is the distribution that reproduces the average energy while maximising entropy, giving the Boltzmann distribution. ^c7
  - page: 28
  - quote: "The solution is a probability distribution over the states which results in the correct average value for the energy and which maximizes the entropy."
  - quote_check: pass
  - reviewed: false
- Any probability distribution can be written in Boltzmann form. ^c8
  - page: 29
  - quote: "Any probability distribution can be cast in the form of a Boltzmann distribution"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $h$ | hypothesis | — | write $x$ for a structure, $\mathcal{M}$ for a model |
| $d$ | data | $s^\text{exp}$ |  |
| $\theta$ | parameters of a model | — | the thesis $\theta$ is forward-model parameters only |
| $M_1, M_2$ | models compared by a Bayes factor | $\mathcal{M}$ | $M$ is also a number of observations (p. 12) |
| $B$ | Bayes factor | $B_{12}$ |  |
| $E_k$ | energy of state $k$ | $U(x)$ |  |
| $U$ | internal (average) energy | — | write $\mathbb{E}_p[U]$; the thesis $U$ is the potential energy |
| $\beta$ | inverse temperature, $1/T$ or $1/kT$; also a Lagrange multiplier | — | write $1/k_BT$; $\beta_C, \beta_H$ are BV coefficients |
| $\alpha$ | Lagrange multiplier for normalisation; Dirichlet and Beta parameters | — | MaxEnt multipliers are $\lambda_i$ |
| $Z$ | partition function | $Z$ |  |
| $F$ | Helmholtz free energy | $F$ |  |
| $S$ | entropy | $S$ |  |
| $L$ | loss function; also the Lagrangian | — |  |

## What I use from it

Bayes' theorem (Eq. 1.1), marginalisation of nuisance parameters, MAP versus the full posterior, the Bayes factor (Eq. 1.6), and the maximum-entropy route to the Boltzmann distribution. Used in [[Bayes' theorem]], [[nuisance parameter]], [[posterior uncertainty]] and [[Boltzmann distribution]].

## Disagreements / limitations
