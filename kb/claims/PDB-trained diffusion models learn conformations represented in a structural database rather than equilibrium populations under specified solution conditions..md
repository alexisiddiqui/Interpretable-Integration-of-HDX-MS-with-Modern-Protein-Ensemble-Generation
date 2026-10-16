---
type: claim
aliases:
  - "Diffusion models trained on PDB structures learn a distribution concentrated on folded, low-energy states rather than the equilibrium distribution."
chapter: 02-background
project:
basis: stated
confidence: high
status: supported
origin: thesis/chapters/02-background.tex#L45
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@wangProteinConformationGeneration2024#^c2]]"
  - "[[@liuExEnDiffExperimentGuidedDiffusion2025#^c1]]"
  - "[[@yimDiffusionModelsProtein2024#^c8]]"
code: []
---

## Argument

PDB-trained diffusion models learn conformations represented in a structural database rather than equilibrium populations under specified solution conditions. Structure databases provide a limited sample of conformations for each sequence, so the learned distribution reflects that representation ([[diffusion model]], [[knowledge-based potential]]). Generated diversity therefore requires a separate assessment of the populations assigned to it.

## Caveats

None beyond those in the linked concept.

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L153`. The historical wording comes from this note before revision, with its original source in `origin` and its evidence links retained in `cites`.

The primary wording identifies the training distribution directly and makes the solution conditions explicit. The previous low-energy description remains as historical shorthand for database bias.

### Historical title

> Diffusion models trained on PDB structures learn a distribution concentrated on folded, low-energy states rather than the equilibrium distribution.

### Historical argument

> Structure databases hold a few points per sequence near energy minima, so the training distribution is not the equilibrium distribution; PDB-trained samplers give ensembles of limited diversity ([[diffusion model]], [[knowledge-based potential]]).
