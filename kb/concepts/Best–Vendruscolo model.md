---
type: concept
aliases:
  - Best-Vendruscolo model
  - BV model
  - BV
  - Best–Vendruscolo
notation:
  - {symbol: '\beta_C', meaning: 'BV coefficient for heavy-atom contacts', units: null}
  - {symbol: '\beta_H', meaning: 'BV coefficient for amide hydrogen bonds', units: null}
  - {symbol: 'N_C(i,j)', meaning: 'heavy atoms within 6.5 Å of the amide N of residue i in conformer j, excluding residues i-2 to i+2', units: null}
  - {symbol: 'N_H(i,j)', meaning: 'hydrogen bonds to the amide H of residue i in conformer j', units: null}
  - {symbol: 'q_i(j)', meaning: 'BV feature (predicted ln protection) of residue i in conformer j', units: null}
sources:
  - "[[@bestStructuralInterpretationHydrogen2006#^c2]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c4]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c5]]"
  - "[[@bradshawInterpretationHDXData2020#^c12]]"
  - "[[@bradshawInterpretationHDXData2020#^c13]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c7]]"
---

## Definition

The Best–Vendruscolo (BV) model is a phenomenological forward model that predicts a residue's [[protection factor]] from coordinates. The log protection factor is a weighted sum of two counts for the amide: heavy-atom contacts, as a proxy for burial, and hydrogen bonds. It is averaged over the conformers of a [[structural ensemble]]. The weights $\beta_C$ and $\beta_H$ are empirical. Best and Vendruscolo set them to 0.35 and 2.0, but their optimal values depend on the protein and conditions.

## Equations

$$ q_i(j) = \beta_C N_C(i,j) + \beta_H N_H(i,j) $$
^eq-bv-feature

Source: [[@bestStructuralInterpretationHydrogen2006#^c2]] and [[@bestStructuralInterpretationHydrogen2006#^c4]], first display, pp. 1–2; [[@bradshawInterpretationHDXData2020#^c12]], Eq. (1), p. 7.
Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L403 (writes $q_i(x)$); projects/2-jaxENT/manuscript/report/methods/HDX.tex#L19 (writes $\log \text{PF}_i = \beta_h N_i^H + \beta_c N_i^C$).

$$ \ln P_{f,i} = \sum_j w_j\, q_i(j) = \langle q_i \rangle_w $$
^eq-bv-ensemble

Source: [[@bestStructuralInterpretationHydrogen2006#^c5]], p. 2; [[@bradshawInterpretationHDXData2020#^c12]], Eq. (1), p. 7 (uniform weights).
Manuscript form: 6_methods_omc.tex#L385; projects/2-jaxENT/manuscript/report/methods/HDX.tex#L29 ("time averaging" over snapshots).

## Assumptions and limits

- The ensemble average is taken over $\ln P_f$, not over $P_f$, and so is a geometric mean of protection. This is a modelling choice, not a physical identity.
- $\beta_C$ and $\beta_H$ are calibration parameters, not mechanistic quantities ([[@bradshawInterpretationHDXData2020#^c13]]). jaxENT fits them jointly with the weights, which is a jaxENT method, not part of this concept.
- Hard cutoffs (6.5 Å, 2.4 Å) make the counts discontinuous in the coordinates. Differentiable variants are a Chapter 5 topic.
- The model's systematic error adds to peptide averaging in [[deuterium uptake]].
- The β coefficients mainly compensate for differences between the experimental conditions and those the model was calibrated under ([[@siddiquiFrameworkTestingStructural2026#^c7]]), so fitted values can absorb forward-model mismatch ([[model misspecification]]).
- **Variants.** The original counts contacts with a hard cutoff. A switch-function variant smooths the cutoff (Radou et al. 2014; not yet in the KB), which makes the count differentiable. ValDX generated synthetic targets with the switch form and fitted with the hard cutoff, a deliberate mismatch (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L624). Other model families are in [[HDX protection-factor model]].

## Why it matters here

BV is the structure-to-observable map shared by HDXer, ValDX and jaxENT. Under [[maximum entropy principle|MaxEnt reweighting]], its linearity in the features is what makes the bias a linear function of $q_i(j)$.

Claims that use this term: [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]], [[To bridge structural ensembles and experimental HDX data, HDXer employs the Best-Vendruscolo (BV) model.]], [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]].
