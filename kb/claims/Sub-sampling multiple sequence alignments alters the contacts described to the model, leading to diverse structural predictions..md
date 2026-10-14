---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L63
source_state: current
needs_review: true
review_reason: Support is partial or indirect
figures: []
cites:
  - "[[@steinSPEACH_AFSamplingProtein2022#^c1]]"
  - "[[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c1]]"
code: []
---

## Argument

Vani et al. say that reducing the size of the input MSA in AlphaFold2 increases the conformational diversity explored. Stein and Mchaourab mutate the MSA in silico and obtain conformations not seen with the default MSA.

## Caveats

Stein and Mchaourab use in silico mutagenesis of the MSA, not sub-sampling.

That reduced MSA depth gives ensemble predictions is also stated by Monteiro da Silva et al. (^c4). The contact mechanism is contested ([[Whether MSA clustering recovers alternative states through evolutionary couplings is contested.]]).
