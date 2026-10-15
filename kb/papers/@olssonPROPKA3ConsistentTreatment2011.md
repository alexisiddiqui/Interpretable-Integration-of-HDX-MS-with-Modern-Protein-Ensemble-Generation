---
type: paper
citekey: olssonPROPKA3ConsistentTreatment2011
year: 2011
read: false
pdf: kb/_pdf/@olssonPROPKA3ConsistentTreatment2011.pdf
extraction: auto
needs_review: false
review_reason:
---

# PROPKA3: Consistent Treatment of Internal and Surface Residues in Empirical pKa Predictions (2011)

## Main point

PROPKA3 predicts a residue's pKa as its water (model) value plus an empirical environmental perturbation built from desolvation, hydrogen-bond and Coulomb terms. Its change from PROPKA2 is to interpolate smoothly between internal and surface residues instead of classifying them, which improves agreement with experiment and removes erratic sensitivity to small structural changes.

## Claims

- PROPKA3 writes a residue's protein pKa as its water (model) pKa plus an environmental perturbation (Eq. 5), expressed as a sum of effective contributions from protein groups; the perturbation splits into a self term and a Coulomb (charge–charge) term (Eq. 6), the self term into desolvation and intrinsic electrostatics (Eq. 7), and the latter into hydrogen bonding plus a residual electrostatic term (Eq. 8) (p. 3). ^c1
  - page: 3
  - quote: "Thus, we express the total environmental perturbation as a sum of effective perturbation contributions from protein groups"
  - quote_check: pass
  - reviewed: false
- PROPKA3 replaces the earlier split of residues into internal and surface classes, which gave erratic and discontinuous behaviour, with a consistent interpolation between the two descriptions. ^c2
  - page: 1
  - quote: "We have introduced a new and consistent approach to interpolate the description between the previously distinct classifications into internal and surface residues"
  - quote_check: pass
  - reviewed: false
- Against experiment, PROPKA3 gives RMSD 0.79 for Asp and Glu (PROPKA2 0.91), 0.75 for Tyr (0.97), 0.65 for Lys (0.72) and 1.00 for His (1.37), with fewer outliers. ^c3
  - page: 1
  - quote: "it is found to agree better with experiment than the previous implementation (in parentheses)"
  - quote_check: pass
  - reviewed: false
- The water pKa of each residue type, usually called the model value, is taken as known (table S1), leaving only the protein-induced difference to compute. ^c4
  - page: 3
  - quote: "which is usually referred to as the model value, is the pKa value of the corresponding residue in water"
  - quote_check: pass
  - reviewed: false
- The perturbative description is expected to fail when the perturbation becomes too large or, more importantly, when it comes with significant structural rearrangement. ^c5
  - page: 3
  - quote: "If the perturbation becomes too large or, more importantly, is associated with significant structural rearrangement, it is quite likely that this description will fail."
  - quote_check: pass
  - reviewed: false
- Each pH unit of shift caused by the protein environment corresponds to 1.36 kcal/mol of perturbed solvation free energy. ^c6
  - page: 3
  - quote: "each pH-unit shift from the protein environment corresponds to 1.36 kcal/mol of perturbed solvation free energy"
  - quote_check: pass
  - reviewed: false
- In the benchmark set, as in most, the large majority of experimental pKa values are shifted by only −1.5 to 0.5 units, so the set mostly tests the model pKa rather than the predicted perturbation. ^c7
  - page: 9
  - quote: "the vast majority of experimental pKa values is only shifted by -1.5 to 0.5 pH units and therefore reflects the model pKa value"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $\text{p}K_{a,i}^\text{Protein}$ | pKa of residue i in the protein (Eq. 5) | $\text{p}K_{a,i}$ |  |
| $\text{p}K_{a,i}^\text{Water}$ | model value, the pKa of the residue in water (Eq. 5) | $\text{p}K_{a,\text{model}}$ | values in table S1 |
| $\Delta\text{p}K_{a,i}^{\text{Water}\to\text{Protein}}$ | environmental perturbation (Eqs 5–6) | $\Delta\text{p}K_{a,i}$ | superscript dropped after Eq. 5 |
| $\Delta\text{p}K_{a,i}^\text{Desolv}$ | desolvation term (Eq. 7) | — | written as the desolvation contribution |
| $\Delta\text{p}K_{a,i}^\text{HB}$ | hydrogen-bond term (Eq. 8) | — | written as the hydrogen-bond contribution |
| $\Delta\text{p}K_{a,i}^{QQ}$ | Coulomb (charge–charge) term (Eq. 6) | — | written as the charge–charge contribution |

## What I use from it

The decomposition of a pKa shift into desolvation, hydrogen-bond and charge–charge terms (Eqs 5–8) for the `pKa shift` concept, with its accuracy and the warning that it fails under large structural rearrangement.

## Disagreements / limitations
