---
type: claim
chapter: 02-background
project:
basis: inferred
confidence: high
status: draft
origin: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L508
source_state: current
needs_review: true
review_reason: Derived from the Work equations (step ours); not stated in the manuscript.
figures: []
cites: []
code: []
---

## Argument

Work_shape and Work_density depend on each residue's absolute deviation from the mean log protection factor, $a_i = |\log P_{f,i} - \overline{\log P_f}|$, and Work_scale on the mean alone ([[Work Done (ValDX)]]). Reflecting a centred profile about its mean, so that protected residues become exposed and exposed ones protected, leaves every $a_i$ and the mean unchanged. All three components are then zero although the profile has been inverted. Work Done therefore measures change in protection contrast and its distribution, not distance between profiles.

## Caveats

Reflection is an extreme case chosen to show the boundary. The same holds for any change that moves residues from above the mean to below it by the same amount, because only the absolute deviations enter. Validation error, which compares predictions with data, still detects such a change ([[Work Done]]).
