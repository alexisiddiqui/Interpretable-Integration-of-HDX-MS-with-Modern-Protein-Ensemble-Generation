---
type: claim
chapter: 06-jax-ka
project: 4-jax-Ka
basis: stated
confidence: high
status: supported
origin: thesis/chapters/06-jax-ka.tex
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@reisPypKaFlexiblePython2020#^c5]]"
  - "[[@reisFastInterpretableDeep2022#^c4]]"
  - "[[@reisPypKaFlexiblePython2020#^c4]]"
  - "[[@stantonBenchmarkingPKaPrediction2008#^c1]]"
  - "[[@stantonBenchmarkingPKaPrediction2008#^c3]]"
code: []
---

## Argument

On PypKa's experimental benchmark, a null model that keeps every group at its model-compound pKa has an RMSE of 0.95 ([[@reisPypKaFlexiblePython2020#^c5]]), against 0.82 for PypKa at its best dielectric ([[@reisPypKaFlexiblePython2020#^c4]]). On the pKAI benchmark of 736 residues the null model scores 1.09, against 1.07 for PypKa, 1.11 for PROPKA and 0.98 for pKAI+ ([[@reisFastInterpretableDeep2022#^c4]]). Stanton and Houk explain why: benchmark sets are dominated by surface groups with small shifts, so even a constant pKa for every Asp looks good, and reported RMSDs near one unit mislead ([[@stantonBenchmarkingPKaPrediction2008#^c1]], [[@stantonBenchmarkingPKaPrediction2008#^c3]]). Because most measured pKas lie near model values ([[Most measured pKa values in folded proteins lie close to model-compound values, and large shifts occur for buried or interacting groups.]]), overall error rewards predicting no shift. A predictor has to be judged against the null model and on the shifted sites, which is why jax-Ka reports a null baseline and large-shift error.

## Caveats

Stanton and Houk argue the point but do not score a null model themselves; the numbers are from the PypKa and pKAI papers, each on its own benchmark set. The jax-Ka null adapter and large-shift MAE are in `projects/4-jax-Ka/code/experiments/`.
