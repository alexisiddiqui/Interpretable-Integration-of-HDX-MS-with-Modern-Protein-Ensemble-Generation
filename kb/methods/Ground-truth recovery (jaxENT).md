---
type: method
project: 2-jaxENT
status: draft
needs_review: true
review_reason: The manuscript does not state the logarithm base, and the 0–100% range holds only in base 2; add the base to analysis.tex.
code:
  - projects/2-jaxENT/code@37043b5:jaxent/src/analysis/pf_variance.py#L389-L413
sources:
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c5]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c5]]"
---

<!-- Note name: Ground-truth recovery (jaxENT). Concept: [[ensemble comparison]]. -->

## What it does

Ground-truth recovery (GTR) scores how closely recovered state populations match a reference distribution. It turns the Jensen–Shannon divergence ([[ensemble comparison#^eq-jsd]]) into a percentage, 100 for identical distributions and 0 for maximal divergence (`projects/2-jaxENT/manuscript/report/methods/analysis.tex` L5–14).

## Equations

$$ \text{GTR}(P, Q) = 100\left(1 - \sqrt{D_\text{JS}^{(2)}(P, Q)}\right) $$
^eq-gtr

Manuscript form: projects/2-jaxENT/manuscript/report/methods/analysis.tex#L10 (no base stated). Here $D_\text{JS}^{(2)}$ is computed with base-2 logarithms. $\sqrt{D_\text{JS}}$ is a metric ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c5]]), so GTR is linear in a distance between the two population vectors.

## Implementation notes

- **Base 2 is required for the stated range.** In base 2, $D_\text{JS} \in [0, 1]$ and GTR spans 0–100. With natural logs, $D_\text{JS} \le \ln 2$ ([[@tibertiENCORESoftwareQuantitative2015#^c5]]), so GTR could not fall below $100(1-\sqrt{\ln 2}) \approx 16.7$. The code uses base 2 throughout. `jensen_shannon_divergence` uses `log2` and clips to [0, 1] before `jensen_shannon_recovery_percent` (pinned lines). Several ATLAS analysis scripts call `scipy.spatial.distance.jensenshannon(..., base=2)`, which already returns the square root, so they use `1 - jensenshannon(...)` without a further square root (e.g. `jaxent/examples/ATLAS_BV/analysis/bv_uptake_model_validation.py` L634). The two routes agree. State "base 2" in `analysis.tex`.
- **Recovery is relative to the reference.** For TeaA the reference populations are exact by construction. For MoPrP the target is HDX-NMR-derived and Boltzmann-weighted (`results.tex` L97), so "ground truth" there is an experimentally derived reference that depends on state assignments and thermodynamic assumptions ([[identifiability]], [[prion protein]]). Prefer "reference recovery" for MoPrP in thesis prose.
- GTR depends on the state definitions. Coarser states make recovery easier ([[clustering]]).
