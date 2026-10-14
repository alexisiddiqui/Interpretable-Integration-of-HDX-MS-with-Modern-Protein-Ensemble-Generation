---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: draft
origin: projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L37
source_state: current
needs_review: false
review_reason: 
figures: []
cites: []
code: []
---

## Argument

The revised ValDX manuscript says structured splits "reduce dependence and minimise overlap without guaranteeing statistical independence" (`1_introduction_omc.tex` L37). The methods give the two reasons. Residue-wise BPTI observations have no peptide overlap yet can remain correlated through shared structural environments, and "neither strategy guarantees the absence of correlations between sets" (`6_methods_omc.tex` L52). Peptides that still overlap across the boundary are dropped after partitioning, which changes the realised training fraction (L73, L81). The physical route is cooperative opening ([[cooperative unfolding unit]]).

## Caveats

Posted v1 says the splits "ensure that validation error reflects true predictive performance" and give "genuinely withheld" regions. Do not reuse that wording. Upgrade this claim when a revised preprint is posted.
