---
type: paper
citekey: reisPypKaFlexiblePython2020
year: 2020
read: false
pdf: kb/_pdf/@reisPypKaFlexiblePython2020.pdf
extraction: auto
needs_review: false
review_reason:
---

# PypKa: A Flexible Python Module for Poisson–Boltzmann-Based pKa Calculations (2020)

## Main point

PypKa is an open-source Python wrapper that couples Poisson–Boltzmann calculations (DelPhi) to Monte Carlo sampling of protonation states, including proton tautomers, to predict pKa values from a single structure. With a protein dielectric of 15 it reaches an RMSE of 0.82 on a large experimental benchmark, and less solvated residues remain the hardest to predict.

## Claims

- PypKa follows the established approach that couples Poisson–Boltzmann calculations to Monte Carlo sampling of protonation states. ^c1
  - page: 3
  - quote: "PypKa uses an established framework for estimating pKa values which couples PB calculations to MC sampling of protonation states"
  - quote_check: pass
  - reviewed: false
- PypKa was built as a scalable, flexible Poisson–Boltzmann pKa predictor with proton tautomers, meant to slot into pipelines. ^c2
  - page: 2
  - quote: "PypKa was developed to be a highly scalable and flexible PB-based pKa predictor with proton tautomers that is easy to integrate into a pipeline"
  - quote_check: pass
  - reviewed: false
- The method solves a thermodynamic cycle with model compounds (fragments of amino acid residues), whose solution pKa values (pKmod) can be calibrated. ^c3
  - page: 3
  - quote: "requires solving a thermodynamic cycle containing model compounds (typically fragments of amino acid residues) whose pKa values in solution (pKmod) can be calibrated"
  - quote_check: pass
  - reviewed: false
- The protein dielectric of 15 minimised the RMSE, at 0.82 pK units on the full benchmark set and 1.24 on a subset. ^c4
  - page: 3
  - quote: "is the one that minimizes the RMSE (0.82 in full set and 1.24 in the subset)"
  - quote_check: pass
  - reviewed: false
- The Null model assumes that pKa values in the protein stay at their values in water, and it has an RMSE of 0.95 on the benchmark. ^c5
  - page: 3
  - quote: "the Null model (0.95), which assumes that the pKa values in the protein remain the same as in water"
  - quote_check: pass
  - reviewed: false
- The Null model's solution pKa values are those measured on Ala-based pentapeptides in Pace's laboratory, which already include some main-chain effects. ^c6
  - page: 3
  - quote: "the solution pKa values used were the ones measured with Ala-based pentapeptides in Pace’s Lab"
  - quote_check: pass
  - reviewed: false
- The authors identify less solvated residues as the main challenge for PypKa, and probably for other fixed-structure methods. ^c7
  - page: 4
  - quote: "the less solvated residues in the large data set are a real challenge for our method"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c2 describe the PB/MC method that labels pKPDB, the main jax-Ka training set (see [[@reisPKPDBProteinData2022]]).
- ^c4, ^c5 bound the label quality: PypKa beats the Null model by about 0.1 pK units in RMSE, and ^c7 says the gain is smallest where shifts are largest.

## Disagreements / limitations
