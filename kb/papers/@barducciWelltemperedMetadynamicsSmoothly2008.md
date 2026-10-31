---
type: paper
citekey: barducciWelltemperedMetadynamicsSmoothly2008
year: 2008
read: false
pdf: kb/_pdf/@barducciWelltemperedMetadynamicsSmoothly2008.pdf
extraction: auto
needs_review: false
review_reason:
---

# Well-Tempered Metadynamics: A Smoothly Converging and Tunable Free-Energy Method (2008)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Metadynamics biases the dynamics with a history-dependent potential built as a sum of Gaussians deposited along the trajectory in collective-variable space. ^c1
  - page: 1
  - quote: "the system evolution is biased by a historydependent potential"
  - quote_check: pass
  - reviewed: false
- In ordinary metadynamics the free-energy estimate does not converge to a definite value in a single run but fluctuates around the correct result. ^c2
  - page: 1
  - quote: "in a single run, the free energy does not converge to a definite value but fluctuates around the correct result"
  - quote_check: pass
  - reviewed: false
- The average error of ordinary metadynamics is proportional to the square root of the bias deposition rate, so slower deposition costs more time to fill the surface. ^c3
  - page: 1
  - quote: "leading to an average error which is proportional to the square root of the bias potential deposition rate"
  - quote_check: pass
  - reviewed: false
- Well-tempered metadynamics gives a free-energy estimate that converges to the exact result in the long-time limit. ^c4
  - page: 1
  - quote: "we obtain an estimate of the FES that converges to the exact result in the long time limit"
  - quote_check: pass
  - reviewed: false
- Well-tempered metadynamics can be implemented in a metadynamics code by rescaling the Gaussian heights, which decrease as the bias builds up. ^c5
  - page: 2
  - quote: "our scheme can easily be implemented in any metadynamics code by rescaling the height of the Gaussians"
  - quote_check: pass
  - reviewed: false
- Well-tempered metadynamics lets the user control which regions of the free-energy surface are explored. ^c6
  - page: 1
  - quote: "our approach offers the possibility of controlling the regions of FES that are physically meaningful to explore"
  - quote_check: pass
  - reviewed: false
- Standard metadynamics and unbiased sampling are the two limiting cases of well-tempered metadynamics. ^c7
  - page: 1
  - quote: "this new method provides a unified framework whose limiting cases are standard metadynamics and nonbiased standard sampling"
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
