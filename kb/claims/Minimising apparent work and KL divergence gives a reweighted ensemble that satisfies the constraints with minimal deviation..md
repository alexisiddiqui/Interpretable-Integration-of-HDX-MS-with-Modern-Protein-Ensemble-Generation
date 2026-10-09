---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: medium
status: draft
origin: milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex#L214
source_state: current
needs_review: true
review_reason: Support is partial or indirect
figures: []
cites:
  - "[[@cesariUsingMaximumEntropy2018#^c6]]"
  - "[[@cesariUsingMaximumEntropy2018#^c9]]"
code: []
---

## Argument

Cesari et al. describe the [[maximum entropy principle]] as giving the distribution satisfying the experimental constraints that is closest to the prior, with closeness measured by the Kullback-Leibler divergence.

## Caveats

Cesari et al. do not use apparent work (W_app), and the equivalence of W_app with the KL divergence is not stated in the cited papers. Lee et al. p9 (block ^c10) and Bradshaw et al. p9 describe apparent work as the bias cost in HDXer, but neither is cited here. The statement that W_app is related to the Kullback-Leibler divergence (D_KL = W_app / k_e T) is in Bradshaw et al. p9 (@bradshawInterpretationHDXData2020 ^c11), the likely intended source; it is not cited here. Jaynes (1957) has no PDF.

## Unverified citations

- [[@jaynesInformationTheoryStatistical1957]]: no PDF
