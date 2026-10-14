---
type: method
project: 1-ValDX
status: draft
needs_review: true
review_reason: Residue weights in Work_density are multiplied by, not divided by, their sum in both the manuscript and the code; confirm the intended definition before quoting values.
code:
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure-0_IsoValidation/TeaA_Compare_RW_ensembles.ipynb#L96997-L97035
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c9]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c15]]"
---

<!-- Note name: Work Done (ValDX). Concept: [[Work Done]]. -->

## What it does

Work Done compares the ensemble-averaged [[protection factor]] profile before and after fitting and reports how much it changed ([[@siddiquiFrameworkTestingStructural2026#^c9]]). Prior and fitted profiles are each computed with their own frame weights and [[Best–Vendruscolo model|BV]] coefficients, so every component can reflect a change in either. All components are distances from the prior, not from a true ensemble, and they differ from HDXer's apparent work, which describes only the change in frame weights (revised `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L508–531).

Each residue $i$ of the $N$ compared residues has an absolute deviation from the mean log protection factor, $a_i = |\log P_{f,i} - \overline{\log P_f}|$, and a centred protection score $H_\text{opt}(X;i) = RT\,a_i$. Hats denote the fitted ensemble $\hat X$.

## Equations

$$ \text{Work}_\text{shape} = \frac{RT}{N}\sum_{i=1}^{N}\left|\, a_i - \hat a_i \,\right| $$
^eq-work-shape

Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L532 (Eq. `work_shape`). Measures change in protection contrast, not its direction.

$$ \text{Work}_\text{scale} = RT\left|\, \overline{\log P_f} - \overline{\log \hat P_f} \,\right| $$
^eq-work-scale

Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L547 (Eq. `work_scale`). A shift in overall protection, which points to calibration ([[@siddiquiFrameworkTestingStructural2026#^c15]]).

$$ w_\text{opt}(X;i) = e^{-a_i}\sum_{j} e^{-a_j}, \qquad S_\text{opt}(X;i) = -R\,w_\text{opt}(X;i)\ln w_\text{opt}(X;i), \qquad \text{Work}_\text{density} = \frac{T}{1000N}\sum_{i=1}^{N}\left| S_\text{opt}(\hat X;i) - S_\text{opt}(X;i) \right| $$
^eq-work-density

Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L555 (Eq. `work_density`), written exactly as here. See implementation notes on the product.

$$ \text{Work}_\text{opt} = \frac{1}{1000N}\sum_{i=1}^{N}\left| \left[H_\text{opt}(\hat X;i) - T S_\text{opt}(\hat X;i)\right] - \left[H_\text{opt}(X;i) - T S_\text{opt}(X;i)\right] \right| $$
^eq-work-opt

Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L563 (Eq. `work_opt`). Shape and density changes can offset within a residue, so Work_opt is at most their sum, and it excludes Work_scale (L577). $H$ is in J/mol and $S$ in J mol⁻¹ K⁻¹ here, so dividing by 1000 gives kJ/mol (L530).

$\Delta\text{MSE}_\text{opt} = \text{MSE}_\text{final} - \text{MSE}_\text{initial}$ reports the change in fit alongside them (L581).

## Derivation

Why distinct profiles can give zero Work Done.
1. Work_shape and $S_\text{opt}$, and so Work_density and Work_opt, depend on the profile only through the set $\{a_i\}$ (Eqs. above).
2. Work_scale depends only on the mean $\overline{\log P_f}$.
3. Reflect the profile about its mean, $\log \hat P_{f,i} = 2\,\overline{\log P_f} - \log P_{f,i}$. The mean is unchanged and every $\hat a_i = a_i$, so all four components are zero although protection has been inverted (step ours). The same holds for any change that only flips which residues lie above the mean. A numerical check with a 40-residue profile gave components below $10^{-14}$ kJ/mol for an RMS profile change of 2.4 log units.

Claim: [[Distinct protection profiles can give zero Work Done, so Work Done is not a distance between profiles.]]

## Implementation notes

- **The density weights are not normalised.** The manuscript writes $w_\text{opt} = e^{-a_i}\sum_j e^{-a_j}$, and every ValDX comparison notebook computes `Pi_opt = Z_opt * exp(-H_opt/RT)` with `Z_opt` the sum of $e^{-a_j}$ (TeaA notebook at the pinned lines; the same line appears in `BPTI_Compare_RW_ensembles.ipynb` and `Compare_RW_ensembles.ipynb`). A normalised weight would divide by the sum. In the numerical check the product weights summed to about 370, 39 of 40 exceeded 1, and those residues' "entropy" contributions were negative. Work_density and Work_opt are still well-defined differences, but the entropy reading of them does not hold as written. Decide whether the product is intended, and if not, correct the code and recompute before quoting values.
- **Units are an analogy.** kJ/mol and the $H - TS$ form make Work Done look like thermodynamic work. It is not physical work and not a Bayesian evidence ([[BICePs]]).
- The code also computes `H_conf`, `H_interaction`, `G_quasi` and Boltzmann-like "likelihoods" from these quantities. The manuscript does not use them; ignore them unless they enter a figure.
- Full equations and the comparison with HDXer apparent work and the BICePs score belong in Chapter 3 (`thesis/chapters/03-valdx.tex` L9).
