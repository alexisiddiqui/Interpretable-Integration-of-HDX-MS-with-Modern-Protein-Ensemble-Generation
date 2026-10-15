---
type: claim
chapter: 02-background
project: 
basis: inferred
confidence: medium
status: draft
origin: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L194
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@deoliveiraConstantPHMolecular2022#^c1]]"
code: []
---

## Argument

ValDX protonated its MD systems at pH 7 with pdb2gmx (`6_methods_omc.tex` L194), and jaxENT protonated at pH 7.4 with propka (`protocols.tex` L98). The MoPrP candidates for the pD 4 fit were AlphaFold2 structures with no pH-specific protonation (`protocols.tex` L183). Because fixed-protonation MD keeps the assigned states ([[@deoliveiraConstantPHMolecular2022#^c1]]), none of these ensembles represents pH 4 protonation. The Chapter 5 MoPrP simulations at pH 4 and pH 7 need states assigned for each pH, which is the question jax-Ka addresses ([[06-jax-ka]]).

## Caveats

For the jaxENT MoPrP fit the forward model counts heavy-atom contacts and hydrogen bonds, so protonation enters only through the structures sampled, not the forward model itself. The inference is about the candidates, not the fit.
