---
type: method
project: 2-jaxENT
status: draft
needs_review: true
review_reason: Trace the reported figures to their fitting and selection procedures before updating the manuscript, including whether coordinate-covariance rescoring was used and, where applicable, which validation block (conditional or marginal) selected the reported models.
code:
  - projects/2-jaxENT/code@37043b5:docs/averaging_mode_soft_regression.md#L8-L16
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/moprp_weighted_loss.py#L51-L78
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L40-L62
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L84-L121
  - projects/2-jaxENT/code@37043b5:jaxent/examples/common/analysis/rescore_crossval_coordinate_sigma.py#L146-L156
  - projects/2-jaxENT/code@37043b5:jaxent/examples/1_IsoValidation_OMass/fitting/jaxENT/run_sigma_source_sidecar.py#L132-L249
  - projects/2-jaxENT/code@37043b5:jaxent/examples/1_IsoValidation_OMass/fitting/jaxENT/sidecar_selection.py#L40-L73
  - projects/2-jaxENT/code@37043b5:jaxent/src/data/loader.py#L202-L217
  - projects/2-jaxENT/code@37043b5:jaxent/src/opt/losses.py#L1541-L1600
  - projects/2-jaxENT/code@37043b5:plans/hdx_noise_model_implementation_handoff.md#L621
  - projects/2-jaxENT/code@37043b5:plans/hdx_noise_model_implementation_handoff.md#L673-L676
  - projects/2-jaxENT/code@37043b5:plans/hdx_moprp_pivot_calibration.md#L903-L913
sources:
  - "[[@bmsb2012ch8#^c8]]"
---

<!-- Note name: Observation weighting and selection (jaxENT). Concepts: [[error covariance]], [[model selection]], [[positional covariance]]. -->

## What it does

jaxENT fits the experimental uptake with an ordinary mean squared error and then selects, within each split replicate, the saved model that scores best on that replicate's validation data under a weighted error (first code link, policy adopted 2026-10-04). Two weightings are in use. For MoPrP, `moprp.weights` supplies the observed normalised variance/SD denominators for the peptide-by-time-point matrix, with the supplied values applied directly as cellwise weights (author clarification, 2026-10-28). For the synthetic ISO benchmark the weight matrix is the inverse of a covariance built from the candidate ensemble's coordinates and pushed through the peptide map. The purpose of the second is to score held-out peptides by how much information they carry that the training peptides do not already supply, given shared residues and co-moving residues, which addresses the dependence that structured splits leave behind by weighting instead of partitioning ([[error covariance]], [[data splitting]]). Recovery and effective sample size are evaluation-only. The reference information used by the ISO covariance variants is recorded below.

## Equations

Coordinate covariance (fourth and fifth code links). With $C$ the residue Cα covariance of the aligned candidate ensemble under uniform frame weights, $M$ the residue-averaging peptide map whose row for peptide $p$ holds $1/|p|$ on its residues, and $\lambda$ a ridge chosen for a condition number of $10^8$,

$$ \Sigma = M C M^\top + \lambda I $$
^eq-coordinate-sigma

The same matrix is applied at every time point. Two validation blocks are available (third code link). Inverting then taking the validation block gives the conditional precision of the validation peptides given the training peptides; taking the block then inverting gives the marginal precision.

$$ P_V^{\text{cond}} = \left(\Sigma^{-1}\right)_{VV}, \qquad P_V^{\text{marg}} = \left(\Sigma_{VV}\right)^{-1} $$
^eq-validation-blocks

Each is trace-normalised so that $\operatorname{tr}(P_V) = |V|$, and the selection score is

$$ s = \frac{1}{2\,|V|\,T}\sum_{t} r_t^\top P_V\, r_t $$
^eq-sigma-score

For MoPrP the score is $s = \tfrac{1}{2}\,\text{mean}(w \odot r^2)$ over peptide and time point, with $w$ the file weights used without squaring, inversion or normalisation (second code link). The general principle, weighting by the inverse covariance, is [[error covariance#^eq-gls]] ([[@bmsb2012ch8#^c8]]).

## Implementation notes

- **Selection only, for MoPrP.** The coordinate-Σ rescoring reads saved convergence checkpoints of fits made with ordinary MSE and reselects them; it does not refit (third to fifth code links). The ISO sidecar fits with the closed-coordinate Σ as well as selecting with it (sixth and seventh code links).
- **The ISO "closed" Σ is partly circular.** Its frame weights are uniform over the closed cluster and zero elsewhere, and those cluster labels are the ones recovery is scored against (sixth link, `population_weights`). The "gt" variant uses the 40:60 target populations and is fully circular; it is kept only for comparison.
- **MoPrP weights.** The observed normalised variance/SD denominators are supplied per peptide and time point and applied directly to scale the matrix (author clarification, 2026-10-28). The raw-weighted helper implements $\tfrac{1}{2}\,\text{mean}(w \odot r^2)$ without further squaring, inversion or normalisation (second code link).
- **Noise-model comparison.** A Phase-3 test rejected the fixed diagonal, and a protection-factor-propagated covariance, as components of a Gaussian observation covariance (twelfth link). That test asked whether they describe the measurement noise; the selection policy uses them as weights, which is a different question.
- **Which block is reported.** The rescoring script computes both the conditional and marginal selectors. The note does not yet record which the reported results used. State it before the thesis quotes a number ([[Weighting validation residuals by the conditional precision given the training peptides discounts held-out peptides whose information is redundant with the training set.]]).
- **Normalisation.** The manuscript divides the precision by its Frobenius norm (`projects/2-jaxENT/manuscript/report/methods/analysis.tex` L24–37); the loader trace-normalises so that the mean diagonal weight is one (eighth link). The thesis follows the code.
- **Legacy path.** The manuscript's fitted covariance-weighted MSE (ninth link; `results.tex` L31–72) used, for MoPrP, the covariance of the experimental uptake curves across time points plus a ridge, and for TeaA a covariance over frames of predicted quantities weighted by the target populations. Neither describes measurement error or overlap, so the manuscript sentence "accounting for experimental uncertainty and correlations between fragments" is not reused. The manuscript needs updating to the policy above.
- **What the weighting assumes.** Weighting by the coordinate Σ treats residual errors as co-varying the way the structure does ([[A covariance built from candidate-ensemble coordinates describes how peptides are expected to co-vary structurally, so weighting residuals by it assumes their errors co-vary in the same way.]]). That is stated as an assumption, not tested.

Claims that use this method: [[A covariance built from candidate-ensemble coordinates describes how peptides are expected to co-vary structurally, so weighting residuals by it assumes their errors co-vary in the same way.]], [[Weighting validation residuals by the conditional precision given the training peptides discounts held-out peptides whose information is redundant with the training set.]].
