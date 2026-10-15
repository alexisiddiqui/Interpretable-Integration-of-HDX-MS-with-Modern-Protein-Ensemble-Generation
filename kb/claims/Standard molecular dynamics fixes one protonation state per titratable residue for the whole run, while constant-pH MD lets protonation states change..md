---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: high
status: supported
origin: kb/chapters/02-background.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@deoliveiraConstantPHMolecular2022#^c1]]"
  - "[[@deoliveiraConstantPHMolecular2022#^c2]]"
code: []
---

## Argument

In conventional MD the protonation state of each titratable residue is set before the run and held fixed ([[@deoliveiraConstantPHMolecular2022#^c1]]). Constant-pH MD lets the states change during the simulation in response to pH and conformation ([[@deoliveiraConstantPHMolecular2022#^c2]]). A fixed-protonation run at pH 4 therefore samples the conformations consistent with the states someone assigned, not the coupled distribution of conformations and protonation ([[molecular dynamics]], [[pKa shift]]).

## Caveats

Constant-pH MD costs more and its accuracy depends on its own models; it is not a free fix. The thesis uses fixed-protonation MD throughout, so the point is a stated limit, not a method change.
