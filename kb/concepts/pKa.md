---
type: concept
aliases:
  - pK
  - pKa value
  - acid dissociation constant
  - Henderson–Hasselbalch
  - protonation state
  - protein charge
notation:
  - {symbol: '\text{p}K_{a,i}', meaning: 'pKa of titratable site i: the pH at which the site is half protonated', units: null}
  - {symbol: '\text{p}K_{a,\text{model}}', meaning: 'model-compound pKa of a titratable group, measured in an unstructured peptide', units: null}
  - {symbol: '\alpha_i', meaning: 'protonated fraction of titratable site i at a given pH', units: null}
  - {symbol: 'Q', meaning: 'net charge of a protein at a given pH, in units of the elementary charge', units: null}
sources:
  - "[[@paceProteinIonizableGroups2009#^c1]]"
  - "[[@thurlkillPKValuesIonizable2006#^c1]]"
  - "[[@thurlkillPKValuesIonizable2006#^c2]]"
  - "[[@thurlkillPKValuesIonizable2006#^c3]]"
  - "[[@grimsleySummaryMeasuredPK2009#^c6]]"
---

## Definition

A titratable group gains or loses a proton depending on the pH of the solution. Its pKa is the pH at which it is half protonated: below the pKa the protonated form dominates, above it the deprotonated form. In a protein, the titratable groups are the side chains of Asp, Glu, His, Cys, Tyr, Lys and Arg and the two termini. Acids (Asp, Glu, Cys, Tyr, C-terminus) are neutral when protonated and negative when deprotonated; bases (His, Lys, Arg, N-terminus) are positive when protonated and neutral when deprotonated ([[@paceProteinIonizableGroups2009#^c1]]).

The reference point is the model-compound pKa, the value a group has in an unstructured peptide where nothing in its environment perturbs it. Thurlkill et al. measured these values in alanine pentapeptides ([[@thurlkillPKValuesIonizable2006#^c1]], [[@thurlkillPKValuesIonizable2006#^c2]]). A group's pKa in a folded protein differs from its model value by the [[pKa shift]].

## Equations

$$ \alpha_i = \frac{1}{1 + 10^{\,\text{pH} - \text{p}K_{a,i}}} $$
^eq-hh

Source: [[@thurlkillPKValuesIonizable2006#^c3]], Eq. 1, p. 4, which fits titration data to $y = 10^{\text{p}K_a - \text{pH}}/(1 + 10^{\text{p}K_a - \text{pH}})$; dividing through gives the form above. Their Eq. 2 adds a Hill coefficient, which came out as 1 for the pentapeptides. The form treats each site as independent.

$$ Q(\text{pH}) = \sum_{i \in \text{bases}} \alpha_i \; - \sum_{i \in \text{acids}} \left(1 - \alpha_i\right) $$
^eq-net-charge

Source: step ours, from the charges of the two forms ([[@paceProteinIonizableGroups2009#^c1]]: acids are uncharged and bases charged below their pK) and Eq. ^eq-hh applied to every site.

## Assumptions and limits

- Eq. ^eq-hh holds for one site that titrates independently. Coupled sites give titration curves that do not follow it, and a single apparent pKa then summarises a curve rather than a property of one site (Onufriev, Case & Ullmann 2001; Ullmann 2003; not seeded).
- Model-compound values depend on the reference peptide, temperature and ionic strength. Thurlkill et al. report them for alanine pentapeptides at 25 °C in 0.1 M salt (KCl in the abstract, NaCl in a table footnote), and Grimsley et al. later revised the Asp value from 3.67 to 3.94 ([[@grimsleySummaryMeasuredPK2009#^c6]]). Quote the revised value.
- A pKa measured in D₂O is not the same number as in H₂O, and a pD reading needs the glass-electrode correction ([[intrinsic exchange rate#^eq-pd]]).

## Why it matters here

The pKa sets which groups change state between two pH values. For MoPrP the relevant change is pH 7 to pH 4: it crosses the model pKa of His and approaches those of Asp and Glu, so the protein gains positive charge ([[Between pH 7 and pH 4, His side chains become protonated and Asp and Glu partly protonated, so a protein's net charge becomes more positive.]]). The same quantity is what jax-Ka predicts per site (Chapter 6).

Claims that use this term: [[Between pH 7 and pH 4, His side chains become protonated and Asp and Glu partly protonated, so a protein's net charge becomes more positive.]], [[A group whose pKa differs between two states makes the equilibrium between those states pH-dependent.]].
