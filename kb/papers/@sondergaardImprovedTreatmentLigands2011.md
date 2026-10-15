---
type: paper
citekey: sondergaardImprovedTreatmentLigands2011
year: 2011
read: false
pdf: kb/_pdf/@sondergaardImprovedTreatmentLigands2011.pdf
extraction: auto
needs_review: false
review_reason:
---

# Improved Treatment of Ligands and Coupling Effects in Empirical Calculation and Rationalization of pKa Values (2011)

## Main point

PROPKA 3.1 extends the empirical PROPKA 3.0 rules to ionisable ligand groups and active-site residues in protein–ligand complexes, and adds algorithms for covalently and noncovalently coupled titrating groups. On the test complexes it performs similarly to or better than PROPKA 2.0.

## Claims

- PROPKA 3.1 extends the PROPKA 3.0 empirical rules to predict pKa shifts of active-site residues and ionisable ligand groups in protein–ligand complexes, and the number of automatically recognised ligand chemical groups rises to 18. ^c1
  - page: 1
  - quote: "have been extended to the prediction of pKa shifts of active site residues and ionizable ligand groups"
  - quote_check: pass
  - reviewed: false
- Two kinds of coupling are modelled; for a pair of noncovalently coupled titratable groups, PROPKA 3.1 predicts the pKa values for both possible titration orders. ^c2
  - page: 1
  - quote: "PROPKA3.1 models noncovalently coupled titrational events by predicting the resulting pKa values in both of the two possible titration orders."
  - quote_check: pass
  - reviewed: false
- Except for a few cases, PROPKA 3.1 gives results similar to or better than PROPKA 2.0 on the protein–ligand test systems. ^c3
  - page: 1
  - quote: "Except for a few cases, the new algorithms in PROPKA3.1 are found to yield results similar to or better than those obtained with PROPKA2.0"
  - quote_check: pass
  - reviewed: false
- For protonation-state changes on complexation in the trypsin and thrombin test set, the overall rms deviation from experiment was 0.18 for PROPKA 3.1 against 0.29 for PROPKA 2.0. ^c4
  - page: 8
  - quote: "The overall rms deviations between experimental protonation state changes on complexation and calculated values were 0.18 for PROPKA3.1 and 0.29 for PROPKA2.0."
  - quote_check: pass
  - reviewed: false
- Covalently coupled groups (for example two titratable groups on one aromatic ring) are handled by identifying the group that does not titrate because of the coupling and restricting it to the neutral state. ^c5
  - page: 1
  - quote: "identifying groups that are not titrating due to coupling with another titrational event and restricting these groups to the neutral state"
  - quote_check: pass
  - reviewed: false
- As in PROPKA 3.0, a group's pKa is modelled as its model pKa in water plus an environment shift summed from desolvation, hydrogen-bond, reorganisation and Coulomb terms (Eqs. 1 and 2). ^c6
  - page: 2
  - quote: "In PROPKA3.1, pKa values are modeled as:"
  - quote_check: pass
  - reviewed: false

## What I use from it

The citation for PROPKA 3.1 as the empirical, structure-based pKa predictor, with its model-pKa-plus-shift decomposition and its flagging of coupled titrating groups.

## Disagreements / limitations

Validation here is on protonation-state changes in a small set of protein–ligand complexes, not a broad benchmark of protein residue pKa values; the residue rules themselves are those of PROPKA 3.0.
