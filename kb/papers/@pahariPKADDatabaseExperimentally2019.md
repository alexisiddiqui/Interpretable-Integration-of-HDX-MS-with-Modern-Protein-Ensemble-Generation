---
type: paper
citekey: pahariPKADDatabaseExperimentally2019
year: 2019
read: false
pdf: kb/_pdf/@pahariPKADDatabaseExperimentally2019.pdf
extraction: auto
needs_review: false
review_reason:
---

# PKAD: A Database of Experimentally Measured pKa Values of Ionizable Groups in Proteins (2019)

## Main point

PKAD compiles experimentally measured residue pKa values from the literature and earlier collections, 1350 residues in 157 wild-type proteins and 232 residues in 45 mutant proteins, each linked to a PDB structure and measurement conditions. It is offered as a benchmark for pKa prediction methods.

## Claims

- PKAD is a database of experimentally measured pKa values of protein residues, gathered from the literature or from existing databases. ^c1
  - page: 1
  - quote: "We present PKAD, a database of experimentally measured pKas of protein residues reported in the literature or taken from existing databases."
  - quote_check: pass
  - reviewed: false
- It holds pKa values for 1350 residues in 157 wild-type proteins and 232 residues in 45 mutant proteins, mostly Asp, Glu, His and Lys. ^c2
  - page: 1
  - quote: "The database contains pKa data for 1350 residues in 157 wild-type proteins and for 232 residues in 45 mutant proteins."
  - quote_check: pass
  - reviewed: false
- For each pKa the web server gives the PDB ID, the measurement uncertainty, salt concentration, pH range and temperature, and a computed relative solvent accessibility. ^c3
  - page: 2
  - quote: "the error (uncertainty) in pKa measurements, salt concentration, pH range and temperature used for pKa measurement"
  - quote_check: pass
  - reviewed: false
- The data come from the literature and two earlier collections, the pKa cooperative and the Grimsley et al. data set. ^c4
  - page: 2
  - quote: "They are collected from literatures and two other previously published databases"
  - quote_check: pass
  - reviewed: false
- Mean wild-type pKa values (e.g. Asp 3.43, Glu 4.14, His 6.45, Lys 10.68) lie close to the intrinsic values, but individual residues range widely with their environment. ^c5
  - page: 2
  - quote: "which are very close to their intrinsic pKas. However, the measured pKa for each ionizable residue vary in a wide range of values"
  - quote_check: pass
  - reviewed: false
- NMR is described as the most precise method for residue pKa measurement, with an accuracy of about 0.1 pK unit; indirect techniques usually have larger errors. ^c6
  - page: 1
  - quote: "NMR estimates the pKa values with the accuracy of 0.1 pK unit, making it the most precise method"
  - quote_check: pass
  - reviewed: false

## What I use from it

PKAD as the first curated collection of experimental protein pKa values, the source of the experimental test sets for pKAI and of the PKAD-2, PKAD-3 and PKAD-R successors.

## Disagreements / limitations

80% of the entries are Glu, Asp, Lys and His, with few Tyr, Cys and terminal values. Later curation found errors in the PKAD lineage ([[@chenPKADRCuratedRedesigned2025]], [[@shenKaMLsPredictingProtein2025]]).
