---
type: paper
citekey: liVeryFastEmpirical2005
year: 2005
read: false
pdf: kb/_pdf/@liVeryFastEmpirical2005.pdf
extraction: auto
needs_review: false
review_reason:
---

# Very Fast Empirical Prediction and Rationalization of Protein pKa Values (2005)

## Main point

PROPKA, an empirical method, predicts protein pKa values from structure in seconds by adding to a model pKa the desolvation, hydrogen-bond and charge–charge perturbations estimated from the positions and chemistry of nearby groups. It reports the determinants of each prediction alongside the value.

## Claims

- A group's pKa is predicted by adding an environmental perturbation ΔpKa to its unperturbed model value pKModel (Eq. 1, p. 2), with ΔpKa built from hydrogen-bond, desolvation and charge–charge terms related empirically to nearby groups, and the program runs in a few seconds. ^c1
  - page: 1
  - quote: "The pKa value of an ionizable group in a protein is predicted by applying an environmental perturbation"
  - quote_check: pass
  - reviewed: false
- On 314 pKa values (233 carboxyl, 12 Cys, 45 His, 24 Lys) the RMSD from experiment is 0.89, falling to 0.79 for the 285 values left after removing upper and lower limits (abstract; summary). ^c2
  - page: 15
  - quote: "The method can predict pKa values with an overall RMSD of 0.79 from experimental values"
  - quote_check: pass
  - reviewed: false
- Each prediction is broken down into its determinants, shown for Asp102 of RNase H as separate desolvation, hydrogen-bond and Coulomb contributions (Fig. 3). ^c3
  - page: 8
  - quote: "The determinants of the pKa value of Asp102 in RNase H (2RN2): (a) desolvation effects, (b) hydrogen bonding, and (c) Coulomb interactions"
  - quote_check: pass
  - reviewed: false
- Across 269 Asp and Glu residues in 26 proteins, hydrogen bonding is the main predicted determinant of their pKa values, with charge–charge interactions appearing far less often (Table V). ^c4
  - page: 14
  - quote: "the hydrogen-bonding effects are the main determinants of Asp and Glu pKa values in these 26 proteins"
  - quote_check: pass
  - reviewed: false
- Buried carboxyl groups often have pKa values above their model values and buried His residues below theirs, and desolvation is the primary reason for these shifts. ^c5
  - page: 5
  - quote: "Desolvation is the primary reason for these pKa shifts"
  - quote_check: pass
  - reviewed: false

## What I use from it

The original PROPKA form pKa = pKModel + ΔpKa and its model values (Asp 3.80, Glu 4.50, His 6.50; Table I), cited with PROPKA3 for the decomposition in `pKa shift`.

## Disagreements / limitations
