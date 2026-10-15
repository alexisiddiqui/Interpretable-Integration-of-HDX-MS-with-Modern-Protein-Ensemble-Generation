---
type: claim
chapter: 06-jax-ka
project: 4-jax-Ka
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/06-jax-ka.tex
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@reisPKPDBProteinData2022#^c1]]"
  - "[[@reisPKPDBProteinData2022#^c3]]"
  - "[[@reisFastInterpretableDeep2022#^c2]]"
  - "[[@reisFastInterpretableDeep2022#^c3]]"
code: []
---

## Argument

pKPDB is a database of theoretical pKa values for PDB structures ([[@reisPKPDBProteinData2022#^c1]]), computed with PypKa at default parameters ([[@reisPKPDBProteinData2022#^c3]]). jax-Ka's absolute-pKa loss uses these values (`projects/4-jax-Ka/code` `models/ogqt-relational-50-frozen/model.json`, objective), and its PINDER bound/free labels come from pKAI, which is itself trained on PypKa shifts from the PDB ([[@reisFastInterpretableDeep2022#^c2]]); pKAI+ uses the same theoretical training set with a penalty on large shifts, not experimental pKas ([[@reisFastInterpretableDeep2022#^c3]]). The training target is therefore a computational method, and experiment enters only at validation (PKAD-R and PKAD-3).

## Caveats

The second half is our inference about what the training set implies. pKAI's paper gives two training-set sizes (6 million shifts in the abstract, about 3 million in the Methods). pKPDB gives two sizes, about 12.5 million pKas on p. 1 and 8.5 million on p. 2; check before quoting a number.
