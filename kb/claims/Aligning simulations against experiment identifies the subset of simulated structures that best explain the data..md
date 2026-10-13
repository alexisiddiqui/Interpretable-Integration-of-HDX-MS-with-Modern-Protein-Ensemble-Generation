---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L89
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@bradshawInterpretationHDXData2020#^c1]]"
  - "[[@bradshawInterpretationHDXData2020#^c7]]"
  - "[[@cesariUsingMaximumEntropy2018#^c4]]"
code: []
---

## Argument

Bradshaw et al. generate an ensemble by MD and reweight it so that the configurations most consistent with the HDX-MS data are up-weighted and the others down-weighted. Cesari et al. describe maximum entropy methods that reweight existing simulations to agree with experiment.

## Caveats

The papers describe adjusting the weights of simulated structures, not selecting a subset, and neither says 'best explain'. 'Subset' is the author's gloss on up-weighting consistent configurations. Cesari et al. is a general review of maximum entropy reweighting and does not mention HDX-MS here.

See also [[Successful reweighting shows which conformations fit experiment, giving pseudo-structural models of solution behaviour.]], which makes a related claim.
