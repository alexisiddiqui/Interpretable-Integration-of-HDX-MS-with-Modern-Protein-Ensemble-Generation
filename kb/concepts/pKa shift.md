---
type: concept
aliases:
  - pKa shifts
  - ΔpKa
  - shifted pKa
  - pKa determinants
notation:
  - {symbol: '\Delta\text{p}K_{a,i}', meaning: 'pKa shift of site i: its pKa in the protein minus the model-compound pKa of its group', units: null}
  - {symbol: '\Delta\text{p}K_{\text{desolv},i}', meaning: 'desolvation contribution to the pKa shift of site i (PROPKA term)', units: null}
  - {symbol: '\Delta\text{p}K_{\text{HB},i}', meaning: 'hydrogen-bond contribution to the pKa shift of site i (PROPKA term)', units: null}
  - {symbol: '\Delta\text{p}K_{\text{Coul},i}', meaning: 'charge–charge (Coulomb) contribution to the pKa shift of site i (PROPKA term)', units: null}
sources:
  - "[[@olssonPROPKA3ConsistentTreatment2011#^c1]]"
  - "[[@liVeryFastEmpirical2005#^c1]]"
  - "[[@grimsleySummaryMeasuredPK2009#^c1]]"
  - "[[@grimsleySummaryMeasuredPK2009#^c2]]"
  - "[[@grimsleySummaryMeasuredPK2009#^c3]]"
  - "[[@grimsleySummaryMeasuredPK2009#^c4]]"
  - "[[@liVeryFastEmpirical2005#^c5]]"
  - "[[@isomLargeShiftsPKa2011#^c1]]"
  - "[[@isomLargeShiftsPKa2011#^c2]]"
---

## Definition

A titratable group in a folded protein does not keep its [[pKa|model-compound pKa]]. Its environment makes one protonation state more or less favourable, and the difference is the pKa shift. Three effects account for most of it: charge–charge interactions, hydrogen bonds (charge–dipole) and dehydration ([[@grimsleySummaryMeasuredPK2009#^c3]]). Burial removes the group from water, which penalises the charged form: buried carboxyl, hydroxyl and thiol groups shift up and buried amino groups shift down ([[@grimsleySummaryMeasuredPK2009#^c4]]), and desolvation is the main reason buried groups shift in PROPKA ([[@liVeryFastEmpirical2005#^c5]]). Hydrogen bonds to the group stabilise one form. Nearby charges stabilise the opposite charge and destabilise the same charge. PROPKA estimates the shift as a sum of these contributions ([[@liVeryFastEmpirical2005#^c1]], [[@olssonPROPKA3ConsistentTreatment2011#^c1]]).

Most measured pKa values in folded proteins lie close to the model values, and large shifts are the exception ([[@grimsleySummaryMeasuredPK2009#^c1]], [[@grimsleySummaryMeasuredPK2009#^c2]]). The extreme cases are charges buried in the protein interior: engineered Lys residues inside staphylococcal nuclease titrate as low as 5.3 against 10.4 in water, because they are buried in an at least partly dehydrated state ([[@isomLargeShiftsPKa2011#^c1]], [[@isomLargeShiftsPKa2011#^c2]]).

## Equations

$$ \Delta\text{p}K_{a,i} = \text{p}K_{a,i} - \text{p}K_{a,\text{model}} \approx \Delta\text{p}K_{\text{desolv},i} + \Delta\text{p}K_{\text{HB},i} + \Delta\text{p}K_{\text{Coul},i} $$
^eq-propka

Source: [[@liVeryFastEmpirical2005#^c1]], Eq. 1, p. 2 (model pKa plus hydrogen-bond, desolvation and charge–charge terms); [[@olssonPROPKA3ConsistentTreatment2011#^c1]], Eqs. 5–8, p. 3, which splits the perturbation into self (desolvation and intrinsic electrostatics, including hydrogen bonds) and Coulomb terms (notation: [[@olssonPROPKA3ConsistentTreatment2011#Notation]]). The three terms are PROPKA's empirical categories, not separately measurable quantities; the grouping above follows Li et al.

## Assumptions and limits

- The decomposition is PROPKA's empirical model, fitted to experimental pKa values. Other methods (Poisson–Boltzmann with Monte Carlo sampling, constant-pH MD) divide the shift differently. The methods themselves are introduced in the Chapter 6 preface ([[06-jax-ka]]).
- A shift is defined for one structure. Conformational change moves the environment, and therefore the shift, which is why fixed protonation in MD is an approximation ([[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]).
- Shifts are hardest to predict for buried groups, which are also the groups whose shifts matter most for stability.

## Why it matters here

The pKa shift is the quantity that structure contributes. jax-Ka predicts it per site as a bounded correction to a group reference pKa (Chapter 6). For MoPrP, a buried His with a lowered pKa changes state at a different pH from a surface His ([[prion protein]]).

Claims that use this term: [[Most measured pKa values in folded proteins lie close to model-compound values, and large shifts occur for buried or interacting groups.]].
