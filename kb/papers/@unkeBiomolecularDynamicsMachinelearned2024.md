---
type: paper
citekey: unkeBiomolecularDynamicsMachinelearned2024
year: 2024
read: false
pdf: kb/_pdf/@unkeBiomolecularDynamicsMachinelearned2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# Biomolecular Dynamics with Machine-Learned Quantum-Mechanical Force Fields Trained on Diverse Chemical Fragments (2024)

## Main point

GEMS trains machine-learned force fields on "bottom-up" and "top-down" chemical fragments, allowing nanosecond MD of more than 25,000 atoms (for example solvated crambin) at essentially ab initio quality. Empirical force fields are efficient but less reliable; earlier MLFFs struggled with long-range interactions.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- A machine-learned force field is built by training a model on ab initio reference data to predict energies and forces. ^c1
  - page: 1
  - quote: "To construct an MLFF, a machine learning (ML) model is trained on ab initio reference data to predict energies and forces"
  - quote_check: pass
  - reviewed: false
- For larger systems, empirical force fields are used because they are efficient, though less reliable than quantum-mechanical calculations. ^c2
  - page: 1
  - quote: "For larger systems, efficient but less reliable empirical force fields are used"
  - quote_check: pass
  - reviewed: false

## What I use from it

Introduction §1.3 and [[force field]]: an MLFF learns energies and forces and is used inside MD (^c1). It improves the force field, not the sampling; it is not a Boltzmann generator.

## Disagreements / limitations
