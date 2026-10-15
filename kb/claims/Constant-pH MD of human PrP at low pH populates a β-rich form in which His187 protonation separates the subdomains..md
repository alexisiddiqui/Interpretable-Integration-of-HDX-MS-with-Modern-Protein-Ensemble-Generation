---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: medium
status: draft
origin: kb/chapters/02-background.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@camposConstantpHMolecularDynamics2010#^c1]]"
  - "[[@camposConstantpHMolecularDynamics2010#^c2]]"
code: []
---

## Argument

Campos, Machuqueiro and Baptista ran constant-pH MD of human PrP across pH values and found a stable β-rich structure in one simulation at pH 2 ([[@camposConstantpHMolecularDynamics2010#^c1]]), with His187 protonation separating the subdomains ([[@camposConstantpHMolecularDynamics2010#^c2]]). It is the closest published simulation to the Chapter 5 MoPrP comparison, and it uses the method that fixed-protonation MD approximates ([[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]).

## Caveats

Human PrP, not mouse; His187 corresponds to mouse H186. The β-rich form appeared in one pH 2 run, well below the pH 4 of the MoPrP data. Their computed His187 pKa of 4.72 ([[@camposConstantpHMolecularDynamics2010#^c3]]) is close to the 4.9 to 5.1 measured for the buried His in hamster and rabbit PrP ([[@malevanetsInterplayBuriedHistidine2017#^c1]]), so at pH 4 that His is mostly protonated.
