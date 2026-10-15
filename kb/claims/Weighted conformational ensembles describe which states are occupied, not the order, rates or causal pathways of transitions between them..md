---
type: claim
chapter: 02-background
project:
basis: inferred
confidence: medium
status: draft
origin: thesis/chapters/02-background.tex#L79
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@tibertiENCORESoftwareQuantitative2015#^c6]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c3]]"
code: []
---

## Argument

Frame weights are populations, so a reweighted ensemble is an equilibrium distribution over states. Similarity scores built on such distributions do not capture changes in dynamics or in transition rates (Tiberti et al.). Under EX2, the measured exchange rate depends on the fraction of time an amide is open, an equilibrium quantity, and not on how fast it opens (Skinner et al.). Neither the data nor the weights therefore carry the order of transitions or the rates between states ([[conformational kinetics]], [[population shift]]).

## Caveats

EX1 exchange does report opening rates, so the boundary is for the EX2 regime that ensemble integration assumes. Trajectories, such as unrestrained simulations started from fitted states, can suggest pathways, but that evidence comes from the dynamics and not from the weights.
