---
type: claim
chapter: 02-background
project:
basis: stated
confidence: high
status: supported
origin: projects/1-ValDX/manuscript/report/7_results_omc.tex#L220
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@wanReconcilingSimulatedEnsembles2020#^c4]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c6]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c7]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c11]]"
code: []
---

## Argument

BICePs samples a posterior over populations and nuisance parameters for the unknown uncertainty ([[@wanReconcilingSimulatedEnsembles2020#^c4]]), with a Jeffreys prior on $\sigma$ ([[@wanReconcilingSimulatedEnsembles2020#^c11]]). Competing models are ranked ([[@wanReconcilingSimulatedEnsembles2020#^c6]]) by a Bayes factor of each model's evidence against a uniform-population null ([[@wanReconcilingSimulatedEnsembles2020#^c7]]; [[BICePs]]).

## Caveats

The ranking is among the priors supplied and under the chosen forward model. The cited description is from Wan et al. 2020; the BICePs v2.0 software paper (Raddi et al. 2023) is not yet in the KB.
