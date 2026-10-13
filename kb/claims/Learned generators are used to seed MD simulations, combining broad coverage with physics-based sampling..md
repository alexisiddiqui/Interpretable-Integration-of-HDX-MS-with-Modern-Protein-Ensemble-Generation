---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: supported
origin: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L85
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@zhengMachineLearningGeneration2023#^c5]]"
  - "[[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c2]]"
  - "[[@zhengMachineLearningGeneration2023#^c4]]"
code: []
---

## Argument

Zheng et al. say generated conformations may be most suitable as initial structures to seed additional MD, and that learned representations can drive additional MD sampling. Vani et al. use reduced-MSA AlphaFold2 conformations as the initialisation for RAVE molecular dynamics. ValDX's AF2-seeded and T-FES ensembles follow this pattern.

## Caveats

Seeding broadens coverage but does not make the pooled frequencies populations ([[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]]); representativeness still has to be assessed against data.
