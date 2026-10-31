---
type: paper
citekey: alamdariEfficientSamplingHighDimensional2021
year: 2021
read: false
pdf: kb/_pdf/@alamdariEfficientSamplingHighDimensional2021.pdf
extraction: auto
needs_review: false
review_reason:
---

# Efficient Sampling of High-Dimensional Free Energy Landscapes: A Review of Parallel Bias Metadynamics (2021)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Enhanced sampling methods can be grouped as tempering methods, which use temperature, and external biasing methods. ^c1
  - page: 2
  - quote: "categorize them as either tempering or external biasing methods"
  - quote_check: pass
  - reviewed: false
- Parallel-bias metadynamics lets a single replica apply one-dimensional biases to many collective variables at once. ^c2
  - page: 4
  - quote: "PBMetaD allows a single replica of the system to simultaneously apply 1-dimensional biases to many CVs"
  - quote_check: pass
  - reviewed: false
- The one-dimensional bias potentials evolve independently and interact only through a conditional weight term, which avoids contamination between them. ^c3
  - page: 5
  - quote: "this functional form ensures that there is no contamination between the individual bias potentials"
  - quote_check: pass
  - reviewed: false
- Metadynamic metainference is a variation of parallel-bias metadynamics that adds the metainference energy for experimental data. ^c4
  - page: 4
  - quote: "variations of PBMetaD have been proposed including metadynamic metainference"
  - quote_check: pass
  - reviewed: false
- In metadynamic metainference with parallel bias, each replica is simulated with the metainference energy function plus the parallel-bias potential. ^c5
  - page: 5
  - quote: "each replica (N) is simulated using the metainference energy function (E MI ) and the PBMetaD bias factor"
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
