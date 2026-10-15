---
type: paper
citekey: paceProteinIonizableGroups2009
year: 2009
read: false
pdf: kb/_pdf/@paceProteinIonizableGroups2009.pdf
extraction: auto
needs_review: false
review_reason:
---

# Protein Ionizable Groups: pK Values and Their Contribution to Protein Stability and Solubility (2009)

## Main point

A review of what measured pK values show about ionizable groups in proteins. The values are shifted from the intrinsic (pentapeptide) values by dehydration, charge–charge interactions and hydrogen bonding, and buried or ion-paired groups can contribute substantially to stability and to its pH dependence.

## Claims

- Asp, Glu, Tyr and Cys side chains are uncharged below their pK and negatively charged above it, whereas His, Lys and Arg are positively charged below their pK and uncharged above it. ^c1
  - page: 1
  - quote: "For Asp, Glu, Tyr, and Cys, the ionizable groups are uncharged below their pK and negatively charged above their pK"
  - quote_check: pass
  - reviewed: false
- In T4 lysozyme the buried Asp-70–His-31 salt bridge shifts both pK values between the folded and unfolded protein (Asp-70 0.5 against 3.5–4; His-31 9.1 against 6.8) and contributes about 4 kcal/mol to stability. ^c2
  - page: 4
  - quote: "Asp-70 has a pK of 0.5 in the folded protein and 3.5– 4 in the unfolded protein"
  - quote_check: pass
  - reviewed: false
- The intrinsic pK (pKint) is the pK a group would have in a protein if it were fully exposed to solvent, not hydrogen-bonded and unaffected by formal charges; the tabulated pKint values come from blocked Ala-Ala-X-Ala-Ala pentapeptides. ^c3
  - page: 1
  - quote: "These are generally referred to as the intrinsic pK (pKint) values"
  - quote_check: pass
  - reviewed: false
- For groups on the protein surface, where most ionizable groups sit, charge–charge interactions are the main cause of pK shifts, as concluded from comparing an acidic RNase Sa with a basic variant of similar structure. ^c4
  - page: 3
  - quote: "charge-charge interactions are the chief perturbant of the pK values of ionizable groups on the protein surface"
  - quote_check: pass
  - reviewed: false
- A hydrogen bond raises a group's pK when it is more favourable with the protonated state and lowers it when it is more favourable with the deprotonated state; such bonds can shift pK values by several units. ^c5
  - page: 3
  - quote: "The effect of hydrogen bonding on a pK will depend on whether the interactions are more favorable with the protonated state of the group"
  - quote_check: pass
  - reviewed: false
- Buried Asp-76 in RNase T1, whose pK is lowered to 0.6 by hydrogen bonding and the positive charge on the protein, contributes substantially both to stability and to its pH dependence (D76A is 3.8 kcal/mol less stable). ^c6
  - page: 4
  - quote: "This buried carboxyl group makes a large contribution to the stability and to the pH dependence of the stability"
  - quote_check: pass
  - reviewed: false

## What I use from it

The sign convention for charge relative to pK (acids neutral below, bases charged below) for the net-charge part of the `pKa` concept, and the three pKa-shift determinants with worked examples for `pKa shift`.

## Disagreements / limitations

The review gives no Henderson–Hasselbalch equation; the protonated fraction is sourced from [[@thurlkillPKValuesIonizable2006]] ^c3.
