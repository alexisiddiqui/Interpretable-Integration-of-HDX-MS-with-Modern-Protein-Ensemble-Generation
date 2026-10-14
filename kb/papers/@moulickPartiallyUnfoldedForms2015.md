---
type: paper
citekey: moulickPartiallyUnfoldedForms2015
year: 2015
read: false
pdf: kb/_pdf/@moulickPartiallyUnfoldedForms2015.pdf
extraction: auto
needs_review: false
review_reason:
---

# Partially Unfolded Forms of the Prion Protein Populated under Misfolding-Promoting Conditions (2015)

## Main point

HDX-NMR of the mouse prion protein at pH 4, where it is primed to misfold. The exchange kinetics of 34 backbone amides were measured as a function of denaturant. Residues in the two β-strands, the three α-helices and the loop between α1 and β2 exchange through denaturant-dependent subglobal unfolding, and the data are modelled as the native state in equilibrium with at least two partially unfolded forms of larger exposed surface area. This is the source of jaxENT's HDX-NMR-derived MoPrP reference.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- At pH 4, different segments of mouse PrP exchange through subglobal unfolding events of different extent. ^c1
  - page: 1
  - quote: "various segments of moPrP were found to undergo different extents of subglobal unfolding events at pH 4"
  - quote_check: pass
  - reviewed: false
- The exchange data are explained by the native state in equilibrium with at least two partially unfolded forms. ^c2
  - page: 2
  - quote: "The data suggest that the N state is in equilibrium with at least two PUFs"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The physical case for [[cooperative unfolding unit]]: whole segments open together (^c1), so exchange at residues that share no peptide is coupled. This is the second route of dependence that structured [[data splitting]] cannot remove.
- The MoPrP reference used by jaxENT is derived from these PUF populations ([[prion protein]], [[identifiability]]). Its state assignments and thermodynamic modelling (^c2) are part of the reference, not ground truth.

## Disagreements / limitations

- Measured at pH 4 with denaturant titration. The PUF populations are extrapolated through a thermodynamic model, not observed directly at zero denaturant.
- Thirty-four amides are resolved. Coverage of the remaining residues comes from the model, not from measurement.
