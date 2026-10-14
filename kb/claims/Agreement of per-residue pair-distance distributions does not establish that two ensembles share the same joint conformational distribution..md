---
type: claim
chapter: 02-background
project:
basis: inferred
confidence: high
status: draft
origin: thesis/chapters/02-background.tex#L79
source_state: current
needs_review: true
review_reason: Follows from marginals versus joint distributions; no source states it for pair-distance W1.
figures: []
cites: []
code: []
---

## Argument

ValDX compares ensembles by the [[Wasserstein distance]] between each residue's distribution of pairwise Cα distances, averaged over residues (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L310–326). Each per-residue distribution is a marginal of the full conformational distribution. Different couplings between residues can give identical marginals, so small values show that the per-residue marginals agree, not that the two ensembles are the same.

## Caveats

Large values do show a real difference in those marginals. The point bounds what agreement means, not what disagreement means.
