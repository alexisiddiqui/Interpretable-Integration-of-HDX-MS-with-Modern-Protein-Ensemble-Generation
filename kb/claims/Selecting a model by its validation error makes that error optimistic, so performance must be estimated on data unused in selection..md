---
type: claim
chapter: 02-background
project: 
basis: stated
confidence: high
status: draft
origin: kb/concepts/model selection.md
source_state: current
needs_review: false
review_reason: 
figures: []
cites: []
code: []
---

## Argument

The model that scores best on a held-out set has been chosen for that score, so the same score overstates its performance on new data. Evaluation needs a test set that played no part in selection, or a nested procedure ([[model selection]]). The general source is not yet in the vault.

## Caveats

ValDX selects on the training sweep by a knee criterion and keeps validation error as evaluation. jaxENT selects on validation and evaluates against an external reference ([[Evaluation design (jaxENT)]]).
