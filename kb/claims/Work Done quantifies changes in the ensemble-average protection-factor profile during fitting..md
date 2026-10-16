---
type: claim
aliases:
  - "Work Done quantifies how much an ensemble must be modified to match experiment."
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L510
source_state: current
needs_review: false
review_reason: 
figures: []
cites:
  - "[[@siddiquiFrameworkTestingStructural2026#^c9]]"
code: []
---

## Argument

Work Done quantifies changes in the ensemble-average [[protection factor]] profile during fitting ([[Work Done]]). ValDX separates changes in relative protection between residues, overall protection and the distribution of protection across residues (`projects/1-ValDX/manuscript/report/7_results_omc.tex#L12`).

## Caveats

Not MaxEnt apparent work, and not a KL divergence over frame weights.

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L218`. The historical wording comes from this note before revision, with its original source in `origin` and its evidence links retained in `cites`.

The primary wording names the quantity measured and the change applied during fitting. The previous title is broader shorthand and can suggest that Work Done measures a necessary population correction.

### Historical title

> Work Done quantifies how much an ensemble must be modified to match experiment.

### Historical argument

> ValDX defines uptake-independent Work Done metrics that measure how much the ensemble-averaged protection-factor profile changes during fitting ([[Work Done]]).
