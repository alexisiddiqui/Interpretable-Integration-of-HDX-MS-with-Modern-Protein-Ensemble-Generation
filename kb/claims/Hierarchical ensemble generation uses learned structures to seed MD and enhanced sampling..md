---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: low
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L15
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@zhengMachineLearningGeneration2023#^c4]]"
code: []
---

## Argument

ValDX generates candidate ensembles in successive stages. AlphaFold2 predictions are filtered and clustered to select starting structures, which are then used for MD simulations. T-FES selects further seeds from the resulting MD ensembles to extend conformational sampling (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L182, L223, L254). Zheng et al. describe the broader use of learned representations to generate conformations or drive further MD sampling ([[@zhengMachineLearningGeneration2023#^c4]]).

## Caveats

Combining stages broadens the candidate set, but population accuracy still depends on sampling and the force field ([[sampling coverage]], [[force field]]).

