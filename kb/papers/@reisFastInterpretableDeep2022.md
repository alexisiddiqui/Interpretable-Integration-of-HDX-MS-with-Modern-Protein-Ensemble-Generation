---
type: paper
citekey: reisFastInterpretableDeep2022
year: 2022
read: false
pdf: kb/_pdf/@reisFastInterpretableDeep2022.pdf
extraction: auto
needs_review: false
review_reason:
---

# A Fast and Interpretable Deep Learning Approach for Accurate Electrostatics-Driven pKa Predictions in Proteins (2022)

## Main point

pKAI is a small fully connected network that maps the distance-weighted N, O and S atoms around a titratable residue to its pKa shift, trained only on PypKa (Poisson–Boltzmann) pKa values for PDB structures. pKAI reproduces PypKa at a fraction of the cost, and pKAI+, the same model with a penalty on the predicted shift, gives the lowest RMSE against 736 experimental pKa values.

## Claims

- pKAI has three fully connected hidden layers in a pyramidal configuration fitted to pKa shifts; its input encodes only nitrogen, oxygen and sulfur atoms within 15 Å of the titratable residue (up to 250 atoms in 16 classes, each weighted by inverse distance) plus the residue type. ^c1
  - page: 3
  - quote: "three fully connected hidden layers in a pyramidal configuration fitted to the pKa shifts of titratable amino acids"
  - quote_check: pass
  - reviewed: false
- pKAI is trained on theoretical pKa shifts computed with PypKa over PDB structures (the pKPDB database), not on experimental values; the abstract gives 6 million theoretical shifts. ^c2
  - page: 5
  - quote: "Our training set was comprised of pKa values calculated using PypKa on a large number of proteins taken from the Protein Data Bank."
  - quote_check: pass
  - reviewed: false
- pKAI+ adds a regularisation term that penalises the magnitude of the predicted pKa shift, biasing predictions towards the pKa values in water; it is trained on the same theoretical set as pKAI, not on experimental pKa values. ^c3
  - page: 5
  - quote: "It should be noted that pKAI+ was not trained on experimental pKa values but rather on the same training set as pKAI."
  - quote_check: pass
  - reviewed: false
- On 736 experimental pKa values from 97 proteins (from PKAD), pKAI+ reached an RMSE of 0.98, against 1.07 for PypKa, 1.11 for PROPKA and 1.09 for the null model of water pKa values. ^c4
  - page: 6
  - quote: "pKAI+ (RMSE of 0.98) is able to outperform both PypKa (RMSE of 1.07) and PROPKA"
  - quote_check: pass
  - reviewed: false
- Because pKAI only applies a learned function to each residue, its run time scales sublinearly with protein size and the speedup over PypKa can exceed 1000-fold. ^c5
  - page: 5
  - quote: "This results in a sublinear scaling performance and a pKAI speedup that can exceed over a 1000"
  - quote_check: pass
  - reviewed: false
- On the theoretical test set pKAI reproduces the PypKa pKa shifts with an MAE of 0.31, an RMSE of 0.52 and an R2 of 0.93, against an RMSE of 1.89 for the null model. ^c6
  - page: 5
  - quote: "with an MAE value of 0.31, an RMSE of 0.52, and an R2 of 0.93"
  - quote_check: pass
  - reviewed: false
- pKAI (not pKAI+) is the best of the tested models for assigning a fixed protonation state at biologically relevant pH values. ^c7
  - page: 7
  - quote: "pKAI is the best model for assigning a fixed protonation state to a protein at biologically relevant pH values"
  - quote_check: pass
  - reviewed: false

## What I use from it

The description of pKAI and pKAI+ as fast surrogates of a Poisson–Boltzmann predictor, trained on PypKa values, with their experimental RMSEs set against PypKa, PROPKA and the null model.

## Disagreements / limitations

The abstract says 6 million theoretical pKa shifts, whereas Methods describes pKPDB as about 3 million values. The experimental benchmark is small (736 residues) and the null model nearly matches the physics-based methods on it, which the authors acknowledge. pKAI+ improves on PypKa only for experimental shifts below 1 pK unit.
