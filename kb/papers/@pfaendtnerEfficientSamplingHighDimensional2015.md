---
type: paper
citekey: pfaendtnerEfficientSamplingHighDimensional2015
year: 2015
read: false
pdf: kb/_pdf/@pfaendtnerEfficientSamplingHighDimensional2015.pdf
extraction: auto
needs_review: false
review_reason:
---

# Efficient Sampling of High-Dimensional Free-Energy Landscapes with Parallel Bias Metadynamics (2015)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Choosing collective variables is a main difficulty of metadynamics: they must cover all slow modes, yet exploration becomes exponentially less efficient as their number grows. ^c1
  - page: 1
  - quote: "the efficiency of the exploration decreases exponentially with the number of CVs"
  - quote_check: pass
  - reviewed: false
- Parallel-bias metadynamics applies several low-dimensional bias potentials at once, so many collective variables can be biased without a high-dimensional bias. ^c2
  - page: 1
  - quote: "applying multiple parallel bias potentials in low dimensionality"
  - quote_check: pass
  - reviewed: false
- Each low-dimensional free energy is read from its own bias potential, and the full high-dimensional free energy is recovered by standard reweighting. ^c3
  - page: 1
  - quote: "the full high-dimensional free energy can be easily recovered by standard reweighting techniques"
  - quote_check: pass
  - reviewed: false
- In well-tempered metadynamics the Gaussian deposition rate decreases with simulation time, in contrast to standard metadynamics. ^c4
  - page: 2
  - quote: "at variance with standard MetaD, the deposition rate decreases with simulation time"
  - quote_check: pass
  - reviewed: false
- Applying several one-dimensional well-tempered biases together would contaminate them when the variables are correlated, so each bias is built from a conditional histogram. ^c5
  - page: 2
  - quote: "in terms of the histogram of the subset of the conformations visited when the corresponding bias potential was active"
  - quote_check: pass
  - reviewed: false
- In parallel-bias metadynamics the number of replicas is chosen independently of the number of biased collective variables. ^c6
  - page: 1
  - quote: "the number of replicas of the systems can be chosen independently from the number of CVs that need to be biased"
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
