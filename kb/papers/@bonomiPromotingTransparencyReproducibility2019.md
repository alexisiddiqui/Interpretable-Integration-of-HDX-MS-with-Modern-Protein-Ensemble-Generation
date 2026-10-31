---
type: paper
citekey: bonomiPromotingTransparencyReproducibility2019
year: 2019
read: false
pdf: kb/_pdf/@bonomiPromotingTransparencyReproducibility2019.pdf
extraction: auto
needs_review: false
review_reason:
---

# Promoting Transparency and Reproducibility in Enhanced Molecular Simulations (2019)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- PLUMED is an open-source library interfaced with MD codes, so enhanced sampling and collective variables are computed outside the engine. ^c1
  - page: 1
  - quote: "PLUMED is an open-source C++ library that can be interfaced with many state-ofthe-art MD codes"
  - quote_check: pass
  - reviewed: false
- PLUMED retrieves atom positions from the host MD code, calculates collective variables and bias potentials, and returns external forces to the MD code. ^c2
  - page: 1
  - quote: "to communicate external forces back to the MD code and hence modify the dynamics"
  - quote_check: pass
  - reviewed: false
- PLUMED can compute collective variables, including user-defined ones built on neural networks, and can process stored trajectories after the run. ^c3
  - page: 1
  - quote: "PLUMED can also calculate these descriptors a posteriori on precalculated trajectories"
  - quote_check: pass
  - reviewed: false
- The PLUMED consortium disseminates enhanced-sampling protocols to promote transparency and reproducibility. ^c4
  - page: 1
  - quote: "we outline our efforts to promote transparency and reproducibility by disseminating protocols for enhanced-sampling molecular simulations"
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
