---
type: paper
citekey: essmannSmoothParticleMesh1995
year: 1995
read: false
pdf: kb/_pdf/@essmannSmoothParticleMesh1995.pdf
extraction: auto
needs_review: false
review_reason:
---

# A Smooth Particle Mesh Ewald Method (1995)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The smooth particle mesh Ewald method evaluates long-range electrostatics through B-spline interpolation of the structure factors. ^c1
  - page: 2
  - quote: "reformulated in terms of efficient B-spline interpolation of the structure factors"
  - quote_check: pass
  - reviewed: false
- B-splines give analytic gradients and improved accuracy compared with Lagrange interpolation. ^c2
  - page: 2
  - quote: "leads to analytic gradients as well as a significant improvement in the accuracy"
  - quote_check: pass
  - reviewed: false
- Arbitrary accuracy is reachable independent of system size at a cost scaling as N log N. ^c3
  - page: 2
  - quote: "arbitrary accuracy can be achieved, independent of system size N, at a cost that scales as N log(N)"
  - quote_check: pass
  - reviewed: false
- Simulations that do not truncate Coulomb interactions avoid the unrealistic behaviour seen with cutoffs. ^c4
  - page: 2
  - quote: "simulations using current force fields without truncation of Coulombic interactions do not exhibit this unrealistic behavior"
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
