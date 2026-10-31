---
type: paper
citekey: prinzMarkovModelsMolecular2011
year: 2011
read: false
pdf: kb/_pdf/@prinzMarkovModelsMolecular2011.pdf
extraction: auto
needs_review: false
review_reason:
---

# Markov Models of Molecular Kinetics: Generation and Validation (2011)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- A Markov state model approximates the long-time statistical dynamics of a molecule as a Markov chain on a discrete partition of configuration space. ^c1
  - page: 1
  - quote: "the long-time statistical dynamics of a molecule is approximated by a Markov chain on a discrete partition of configuration space"
  - quote_check: pass
  - reviewed: false
- MSMs can extract long-time kinetic information from many short trajectories. ^c2
  - page: 1
  - quote: "extracting long-time kinetic information from short trajectories"
  - quote_check: pass
  - reviewed: false
- Projecting dynamics onto one or two order parameters such as RMSD or principal components can hide barriers and give a distorted picture of kinetics. ^c3
  - page: 1
  - quote: "these projection techniques have been shown to disguise the true and often complex nature of the kinetics"
  - quote_check: pass
  - reviewed: false
- The implied timescale of each eigenvalue of the transition matrix is the physical timescale on which the corresponding process relaxes. ^c4
  - page: 6
  - quote: "which is often called the ith implied timescale"
  - quote_check: pass
  - reviewed: false
- The lag-time dependence of the implied timescales is used to choose the lag time, and the resulting model must then be validated. ^c5
  - page: 13
  - quote: "observing the lag timedependence of the implied timescales is a useful approach to choose a lag time"
  - quote_check: pass
  - reviewed: false
- The best MSM does not come from the most metastable discretisation. ^c6
  - page: 1
  - quote: "the best MSM is not obtained by the most metastable discretization"
  - quote_check: pass
  - reviewed: false
- Clusters that straddle the transition region fail to resolve the slow eigenfunctions, so a plain k-means discretisation can be worse than a metastable one. ^c7
  - page: 13
  - quote: "some clusters cross over the transition region and fail to resolve the slow eigenfunctions"
  - quote_check: pass
  - reviewed: false
- The paper gives an efficient estimator for reversible transition matrices and a test that a MSM reproduces the kinetics of the MD data. ^c8
  - page: 1
  - quote: "an efficient estimator for reversible transition matrices and a robust test to validate that a MSM reproduces the kinetics"
  - quote_check: pass
  - reviewed: false
- The MSM theory requires dynamics with a unique stationary distribution; Nose-Hoover and Berendsen thermostats are either not ergodic or do not give the correct stationary distribution. ^c9
  - page: 5
  - quote: "Nosé-Hoover and Berendsen are either not ergodic or do not generate the correct stationary distribution for the desired ensemble"
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
