---
type: claim
chapter: 01-introduction
project:
basis: inferred
confidence: high
status: draft
origin: projects/1-ValDX/manuscript/report/7_results_omc.tex#L246
source_state: current
needs_review: true
review_reason: Follows from reweighting changing only the weights of existing frames (Lee, Bradshaw); the revised ValDX manuscript states it without a citation and posted v1 does not.
figures: []
cites:
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c7]]"
  - "[[@bradshawInterpretationHDXData2020#^c7]]"
code: []
---

## Argument

HDXer biases the relative populations of frames in a previously generated candidate ensemble (Lee et al.); reweighting up-weights and down-weights existing configurations (Bradshaw et al.). A state that is not among the frames therefore receives no weight (step ours; [[importance sampling]], [[sampling coverage]]).

## Caveats

Missing states need more sampling, not more fitting. Bayesian replica refinement with on-the-fly simulation is a different method and can move structures.
