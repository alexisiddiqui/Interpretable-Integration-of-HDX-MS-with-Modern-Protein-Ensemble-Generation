---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L76
source_state: current
needs_review: true
review_reason: Support is partial or indirect
figures: []
cites:
  - "[[@fiorinUsingCollectiveVariables2013#^c1]]"
code: []
---

## Argument

Fiorin et al. describe the colvars module, which combines collective variables with biasing methods including adaptive free-energy biases such as metadynamics and adaptive biasing force.

## Caveats

Fiorin et al. p7 has a section 2.1 on runtime analysis, which covers computing colvars and their properties while a simulation runs. Nothing there guides sampling towards underexplored regions. The passage does not describe online analysis of collective variables or steering towards underexplored regions.
