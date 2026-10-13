---
type: paper
citekey: bmsb2012ch4
year: 2012
read: false
pdf: kb/_pdf/@bmsb2012ch4.pdf
extraction: auto
needs_review: false
review_reason:
---

# Towards a General Probabilistic Model of Protein Structure: The Reference Ratio Method

Chapter 4 of Hamelryck, Mardia and Ferkinghoff-Borg (eds), *Bayesian Methods in Structural Bioinformatics*, Springer 2012 (DOI 10.1007/978-3-642-27225-7). Author(s): Frellsen, Jes; Mardia, Kanti V.; Borg, Mikael; Ferkinghoff-Borg, Jesper; Hamelryck, Thomas. Printed pages 125–134.

PDF note: the PDF holds this chapter only, so PDF page = printed page − 124. The book prints one shared reference list at the end, which is not in this PDF. Use this chapter for mathematical definitions and derivations; quote the sentence that introduces an equation and give the equation number in the citing note's body.


## Main point

The reference ratio method imposes a target distribution on a coarse-grained variable while keeping the fine-grained detail of an approximate generator. The result is the minimal Kullback-Leibler modification of the generator, and it explains potentials of mean force as statistical constructs.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The reference ratio method combines a fine-grained variable X with a coarse-grained variable Y = m(X). ^c1
  - page: 2
  - quote: "X is denoted the fine-grained variable and Y"
  - quote_check: pass
  - reviewed: false
- Theorem 4.1: the reference ratio pdf (Eq. 4.2) has the desired coarse-grained marginal and keeps the fine-grained conditional. ^c2
  - page: 3
  - quote: "Theorem 4.1. The conditions (v) and (vi) are satisfied for the pdf given by"
  - quote_check: pass
  - reviewed: false
- Theorem 4.2: the reference ratio distribution is the minimal Kullback-Leibler modification of the original pdf. ^c3
  - page: 3
  - quote: "In this view, the reference ratio distribution represents the minimal"
  - quote_check: pass
  - reviewed: false
- Typical samples from the local generator TORUSDBN are not compact native-like structures. ^c4
  - page: 6
  - quote: "It is important to stress that typical samples generated from TORUSDBN,"
  - quote_check: pass
  - reviewed: false
- The reference ratio method explains potentials of mean force without external physical considerations. ^c5
  - page: 9
  - quote: "does not require any external physical considerations."
  - quote_check: pass
  - reviewed: false
- Potentials of mean force should be understood not as physical potentials but as statistical constructs. ^c6
  - page: 9
  - quote: "physical potentials, but rather as statistical constructs."
  - quote_check: pass
  - reviewed: false
- The generator pdf is approximately correct on a local scale but incorrect on a global scale. ^c7
  - page: 10
  - quote: "as approximately correct on a local scale, but incorrect on a global scale."
  - quote_check: pass
  - reviewed: false

## What I use from it

Eq. 4.2 and Theorems 4.1 and 4.2. Used in [[reference ratio method]] as a conceptual precedent for correcting a generator's populations with data. Its KL is taken in the opposite direction to MaxEnt's (see [[Kullback–Leibler divergence]]).

## Disagreements / limitations
