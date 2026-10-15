---
type: paper
citekey: stantonBenchmarkingPKaPrediction2008
year: 2008
read: false
pdf: kb/_pdf/@stantonBenchmarkingPKaPrediction2008.pdf
extraction: auto
needs_review: false
review_reason:
---

# Benchmarking pKa Prediction Methods for Residues in Proteins (2008)

## Main point

Stanton and Houk benchmark MD/GB/TI, PROPKA and literature pKa methods on 80 residues (20 each of Asp, Glu, Lys and His), half of them shifted by at least 1 pKa unit; both methods run here give an RMSD of 1.4. They argue that benchmarks dominated by surface residues flatter methods, and find solvent accessibility a better predictor of error than the size of the shift.

## Claims

- When a benchmark is mostly low-variant residues, even a null model that gives every Asp the model pKa of 4 appears to be a good model, whether or not it captures the interactions. ^c1
  - page: 3
  - quote: "if a benchmark set includes a majority of low variants, even a model that predicts every Asp residue to have a pKa of 4"
  - quote_check: pass
  - reviewed: false
- Solvent accessibility was a somewhat better predictor of error than the shift, with error falling as accessibility rises, so buried residues are the hardest. ^c2
  - page: 14
  - quote: "The SASA proved to be a somewhat better predictor and did show the expected trend of decreasing error with increasing solvent accessibility"
  - quote_check: pass
  - reviewed: false
- Reported RMSDs of about 1 pKa unit are misleading because most benchmark data are surface residues with small shifts. ^c3
  - page: 2
  - quote: "However, this is somewhat misleading considering that most of the data are dominated by residues that are on the surface of the protein"
  - quote_check: pass
  - reviewed: false
- Against the authors' expectation, the size of the shift (variance) did not predict the error. ^c4
  - page: 14
  - quote: "However, the variance was not shown to be a good predictor of the error in pKa calculations."
  - quote_check: pass
  - reviewed: false
- The benchmark has 80 residues, 20 each of Asp, Glu, Lys and His. ^c5
  - page: 1
  - quote: "The benchmark set includes 80 different residues (20 each for Asp, Glu, Lys, and His)"
  - quote_check: pass
  - reviewed: false
- The authors recommend that a benchmark include a substantial number of high-variant residues. ^c6
  - page: 3
  - quote: "it is important for a benchmark to include a significant number of high variants"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c3 justify reporting the null model beside every jax-Ka error and splitting results by shift size. ^c1 is an argument; the paper never scores a null model, so cite PypKa ([[@reisPypKaFlexiblePython2020#^c5]]) for a measured null-model RMSE.
- ^c2, ^c4 motivate stratifying by burial (SASA) as well as by |ΔpKa|.

## Disagreements / limitations
