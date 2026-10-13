---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L42
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@abramsonAccurateStructurePrediction2024#^c1]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c5]]"
code: []
---

## Argument

Abramson et al. present a diffusion-based AlphaFold 3 that predicts complexes of proteins, nucleic acids, small molecules and other types, trained with a generative procedure that produces a distribution of answers.

## Caveats

Nearest support: @abramsonAccurateStructurePrediction2024 p3 (^c5) describes a generative training procedure that produces a distribution of answers, and p1 (^c1) describes predicting complexes of nearly all molecular types, with the diffusion module directly predicting raw atom coordinates. Neither passage states that training is end-to-end, so that key term remains unsupported. The phrase end-to-end training is not used in the checked passages.
