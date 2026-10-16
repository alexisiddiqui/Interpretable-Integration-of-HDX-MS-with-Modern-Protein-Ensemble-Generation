---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: high
status: supported
origin: kb/concepts/model selection.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@cawleyOverfittingModelSelection2010#^c1]]"
  - "[[@cawleyOverfittingModelSelection2010#^c2]]"
code: []
---

## Argument

The model that scores best on a held-out set has been chosen for that score, so the same score overstates its performance on new data. Evaluation needs a test set that played no part in selection, or a nested procedure ([[model selection]]). Cawley and Talbot show that common evaluation practices carry this selection bias, and that selection must be repeated whenever a model is fitted to a new sample ([[@cawleyOverfittingModelSelection2010#^c1]], [[@cawleyOverfittingModelSelection2010#^c2]]).

## Caveats

ValDX selects on the training sweep by a knee criterion and keeps validation error as evaluation. jaxENT selects on validation and evaluates against an external reference ([[Evaluation design (jaxENT)]]).
