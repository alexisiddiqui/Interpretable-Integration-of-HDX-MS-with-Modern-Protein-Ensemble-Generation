---
type: paper
citekey: kasaharaNovelApproachDynamic2014
year: 2014
read: false
pdf: kb/_pdf/@kasaharaNovelApproachDynamic2014.pdf
extraction: auto
needs_review: false
review_reason:
---

# A Novel Approach of Dynamic Cross Correlation Analysis on Molecular Dynamics Simulations and Its Application to Ets1 Dimer--DNA Complex (2014)

## Main point

Dynamic cross-correlation (DCC) quantifies correlated atomic motion in MD trajectories but assumes one mean position per atom. The multi-modal extension (mDCC) fits a Gaussian mixture to each atom's positions to capture transient, multi-modal correlations, applied to the Ets1 dimer–DNA complex.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- DCC analysis is widely used to quantify correlation coefficients of motion between atoms in MD trajectories. ^c1
  - page: 2
  - quote: "the dynamic cross correlation (DCC) analysis has been extensively applied to quantify the correlation coefficients of motions between atoms"
  - quote_check: pass
  - reviewed: false
- DCC between two atoms is defined as the normalised time average of the dot product of their displacements from mean positions (Eq. 1). ^c2
  - page: 2
  - quote: "The DCC between the ith and jth atoms is defined by the following equation"
  - quote_check: pass
  - reviewed: false
- DCC can miss correlated motions because it relies on displacements from a single average coordinate. ^c3
  - page: 2
  - quote: "it could overlook some kinds of correlative motions, due to its reliance on displacements from the uniquely determined average coordinate"
  - quote_check: pass
  - reviewed: false
- DCC has a definite meaning only when an atom's coordinate follows a unimodal distribution. ^c4
  - page: 2
  - quote: "the DCC has a definitive meaning if an atomic coordinate behaves under a uni-modal distribution"
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

The standard DCC definition (Eq. 1, PDF p. 2) for [[positional covariance]], and its stated limit for multi-modal motion.

## Disagreements / limitations

The mDCC extension itself is not used in the thesis.
