---
type: paper
citekey: choderaMarkovStateModels2014
year: 2014
read: false
pdf: kb/_pdf/@choderaMarkovStateModels2014.pdf
extraction: auto
needs_review: false
review_reason:
---

# Markov State Models of Biomolecular Conformational Dynamics (2014)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- An MSM consists of a discretisation of the molecular state space into conformational sets and a matrix of transition probabilities between them estimated at a lag time. ^c1
  - page: 2
  - quote: "using two objects: (1) a discretization of the high-dimensional molecular state space"
  - quote_check: pass
  - reviewed: false
- A longer lag time gives a higher-fidelity model with coarser temporal resolution. ^c2
  - page: 2
  - quote: "with larger τ providing models of higher fidelity but coarser termporal resolution"
  - quote_check: pass
  - reviewed: false
- The stationary distribution follows from the transition matrix, and the MSM recovers equilibrium properties even when the short trajectories did not start from equilibrium. ^c3
  - page: 2
  - quote: "even if the short trajectories used to construct it were not initiated from equilibrium"
  - quote_check: pass
  - reviewed: false
- The transition matrix is estimated over the largest connected set of states by an iterative maximum-likelihood estimator that respects detailed balance. ^c4
  - page: 6
  - quote: "proceeds via an iterative maximum likelihood estimator that respects detailed balance"
  - quote_check: pass
  - reviewed: false
- Statistical uncertainty needs all transition matrices consistent with the data, not only the most likely one. ^c5
  - page: 6
  - quote: "it is important to consider not only the most likely transition matrix, but all such matrices statistically consistent with the data"
  - quote_check: pass
  - reviewed: false
- Implied-timescale estimates converge slowly with lag time because the error falls as the inverse of the lag time. ^c6
  - page: 7
  - quote: "explaining the slow convergence observed in implied timescale plots of recent papers"
  - quote_check: pass
  - reviewed: false
- Dynamical reweighting allows data from several temperatures to feed one MSM. ^c7
  - page: 6
  - quote: "a dynamical reweighting method [30] that permits use of data from all temperatures"
  - quote_check: pass
  - reviewed: false
- EMMA and MSMBuilder are software packages for constructing and validating MSMs from simulation data. ^c8
  - page: 7
  - quote: "facilitate the construction and validation of Markov state models from molecular simulation data"
  - quote_check: pass
  - reviewed: false

## Notation

<!-- Only for sources whose equations a concept uses. One row per symbol the concepts rely on or that clashes with the thesis notation.
| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $E(x)$ | force-field energy | $U(x)$ | |
| $\beta$ | inverse temperature | — | write 1/k_BT |
Canonical is one $symbol$ declared by a concept, or —. Delete this section if unused. -->

## What I use from it

## Disagreements / limitations
