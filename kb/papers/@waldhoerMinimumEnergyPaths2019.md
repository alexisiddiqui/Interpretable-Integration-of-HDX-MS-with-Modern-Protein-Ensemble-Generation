---
type: paper
citekey: waldhoerMinimumEnergyPaths2019
year: 2019
read: false
pdf: kb/_pdf/@waldhoerMinimumEnergyPaths2019.pdf
extraction: auto
needs_review: false
review_reason:
---

# Minimum Energy Paths for Non-Adiabatic Charge Transitions in Oxide Defects (2019)

## Main point

Device physics, from the reliability of transistor gate oxides. Charge transfer between an oxide defect and the substrate is modelled as a non-radiative multiphonon transition between two parabolic potential-energy curves. The barrier is set by where the curves cross, and an applied gate bias shifts the curves relative to each other. The paper goes beyond the harmonic approximation by locating the minimum energy path on multidimensional surfaces from density functional theory. Only the two-curve picture is used here.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- In the classical limit the charge transition dynamics are set by the crossing point of the diabatic potential-energy curves of the defect. ^c1
  - page: 1
  - quote: "the charge transition dynamics are determined by the crossing point of the corresponding diabatic potential energy curves of the defects"
  - quote_check: pass
  - reviewed: false
- An applied gate bias shifts the two energy curves relative to each other, so the transition barriers depend on the bias. ^c2
  - page: 1
  - quote: "an applied gate bias shifts the energy curves relative to each other"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The two-curve construction behind panel B of `fig:intro-frustrated-memory`. A potential applied to the system moves the curves until the crossing point is reachable (^c1, ^c2). The comparison with a conformational landscape, where urea concentration or pH plays the part of the gate bias, is my own analogy ([[prion protein]]). The paper makes no claim about proteins.

## Disagreements / limitations

- Oxide defects in amorphous silica are a physical system unrelated to proteins. The source supports the energy-curve construction and nothing about prion behaviour.
