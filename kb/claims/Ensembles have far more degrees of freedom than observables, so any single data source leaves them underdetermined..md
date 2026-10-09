---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L11
source_state: current
needs_review: true
review_reason: Support is partial or indirect
figures: []
cites:
  - "[[@berlinRecoveringRepresentativeConformational2013#^c1]]"
  - "[[@berlinRecoveringRepresentativeConformational2013#^c2]]"
code: []
---

## Argument

Berlin et al. state that the number of ensemble degrees of freedom generally greatly exceeds the number of independent observables, so that deconvolving data directly into a representative ensemble is an ill-posed problem.

## Caveats

The manuscript says 'in every case' and 'any single data source'; Berlin et al. say 'generally' and work with NMR (residual dipolar coupling) data on diubiquitin. The general statement is theirs, but the universal wording is stronger.

Also stated in: milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L87
Also stated in: milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L93

The confirmation-report sentences are "there is no tractable way to directly invert experimental measurements into a structural ensemble" (L87, cited to Lee et al.) and "fitting simulations against experimental data is an ill-posed problem" (L93, cited to Cesari et al.). The Berlin blocks above are likely the intended support, but Berlin is not among the cites at either line.

Lee et al. (2021) is likely mis-cited at milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex L87: it describes HDXer reweighting but does not discuss inverting measurements or its intractability. Likely intended source for L87 and L93: Berlin ^c2 here, and Hummer and Koefinger p2 (@hummerBayesianEnsembleRefinement2015 ^c6, inverse problems are typically ill-conditioned and underdetermined).

Cesari et al. (2018) never uses "ill-posed" or "underdetermined" and is likely mis-cited at milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex L93.

## Unverified citations

- [[@leeInterpretingHydrogenDeuteriumExchange2021]]: no passage supporting this claim found
- [[@cesariUsingMaximumEntropy2018]]: no passage supporting this claim found
