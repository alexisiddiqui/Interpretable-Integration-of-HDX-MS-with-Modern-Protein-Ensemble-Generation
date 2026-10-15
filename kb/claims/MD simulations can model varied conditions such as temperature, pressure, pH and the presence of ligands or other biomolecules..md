---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: low
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L23
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@karplusMolecularDynamicsSimulations2002#^c3]]"
code: []
---

## Argument

Karplus and McCammon say molecular dynamics simulations have been used to study the effect of solvent and temperature on protein structure and dynamics.

## Caveats

Temperature and solvent are covered. Karplus and McCammon also mention simulations with an explicit solvent and/or membrane environment (p2) and the binding of antiviral drugs to a viral capsid (p2). Pressure and pH are not stated as conditions simulated: pH appears only for a normal-mode (not MD) calculation on virus swelling (p6).

For pH specifically, standard MD holds the protonation states assigned before the run ([[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]), so "modelling pH" means choosing states for one pH, not letting them respond.
