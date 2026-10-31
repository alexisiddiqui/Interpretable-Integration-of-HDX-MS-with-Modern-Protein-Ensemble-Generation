---
type: paper
citekey: larsenCombiningMolecularDynamics2020
year: 2020
read: false
pdf: kb/_pdf/@larsenCombiningMolecularDynamics2020.pdf
extraction: auto
needs_review: false
review_reason:
---

# Combining Molecular Dynamics Simulations with Small-Angle X-Ray and Neutron Scattering Data to Study Multi-Domain Proteins in Solution (2020)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Scattering intensities from simulation frames were computed with Pepsi-SAXS, fitting the forward scattering, excluded water volume, hydration-shell density and a constant background. ^c1
  - page: 6
  - quote: "the forward scattering, I(0), was fitted along with the excluded water volume"
  - quote_check: pass
  - reviewed: false
- Fitting all four scattering parameters freely for each conformation can overfit the data, so a single global set is estimated per ensemble. ^c2
  - page: 6
  - quote: "Fitting all four parameters freely and for each conformation could lead to a drastic overfit of the data"
  - quote_check: pass
  - reviewed: false
- The reweighting regularisation parameter theta balances trust in the data against trust in the simulation. ^c3
  - page: 8
  - quote: "with θ being a regularization parameter that balances the trust in data versus simulation"
  - quote_check: pass
  - reviewed: false
- Reduced chi-squared divides by the number of data points minus the number of fitted scattering parameters. ^c4
  - page: 8
  - quote: "conventionally estimated as the number of data points, M, minus the number of fitting parameters, K"
  - quote_check: pass
  - reviewed: false
- Simulations are compared with experiment through the calculated I(q), because the experimental radius of gyration includes the hydration shell while the simulation value is computed in vacuo. ^c5
  - page: 10
  - quote: "we do not expect perfect agreement between the Rg from SAXS and the Rg calculated from the atomic coordinates"
  - quote_check: pass
  - reviewed: false
- Held-out SANS data can cross-validate reweighting against SAXS and help choose theta. ^c6
  - page: 17
  - quote: "can also be used to cross-validate the reweighting of SAXS data to prevent overfitting"
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
