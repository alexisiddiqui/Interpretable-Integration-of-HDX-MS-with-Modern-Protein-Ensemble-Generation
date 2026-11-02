---
type: method
project: 3-BioFeaturisers
status: draft
needs_review: true
review_reason: The synthetic amide-H direction was wrong until BioFeaturisers 39b8069 (2026-11-02), so every TeaA target and run used a near-inert hydrogen-bond term. Decide whether the TeaA target and runs are regenerated with the fixed placement, and whether bf-teaa.md carries the caveat, before the TeaA numbers are written up.
code:
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/core/switching.py#L19-L23
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/config.py#L28-L39
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/hdx/exclusion_jax.py#L48-L59
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/hdx/forward.py#L377-L403
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/hdx/forward.py#L453-L471
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/hdx/predict.py#L96-L101
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/hdx/hdxrate.py#L190-L200
sources:
  - "[[@bestStructuralInterpretationHydrogen2006#^c4]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c5]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c10]]"
---

<!-- Note name: Sigmoid-switch BV forward model (BioFeaturisers). Concepts: [[Best–Vendruscolo model]], [[HDX protection-factor model]], [[protection factor]], [[intrinsic exchange rate]], [[deuterium uptake]], [[forward model]]. Used by: [[Hinge-coordinate metadiffusion (BioFeaturisers)]], kb/experiments/bf-bpti.md, kb/experiments/bf-teaa.md. -->

## What it does

Restrained sampling and guided generation both move atoms along the gradient of a mismatch between predicted and measured HDX. The original [[Best–Vendruscolo model]] counts contacts and hydrogen bonds with hard distance cutoffs, so its prediction is piecewise constant in the coordinates and has no gradient to follow. BioFeaturisers keeps the BV functional form and replaces each step function with a sigmoid. The predicted [[protection factor]] then varies smoothly with every atom position, and the same function serves reweighting, metainference and metadiffusion. A steep sigmoid approaches the hard cutoff, so the smooth model is a differentiable approximation of BV and not a different physical model.

The model has two stages. Coordinates give a residue-wise $\ln P_f$ (the structure-to-protection map), and intrinsic exchange rates turn $\ln P_f$ into peptide uptake at the experimental labelling times ([[deuterium uptake]]). Restraints on protection factors, as in the BPTI experiment, use the first stage alone. Restraints on uptake, as in TeaA, use both.

## Equations

Each contact is counted with a sigmoid of its distance $d$, a cutoff $r$ and a steepness $b$,

$$ s(d; r, b) = \frac{1}{1 + \exp\left[-b\,(r - d)\right]} $$
^eq-bf-switch

which equals one well inside the cutoff, zero well outside, and one half at $d = r$. For the amide of residue $i$, heavy-atom contacts are counted from the amide N to every heavy atom $j$, and hydrogen bonds from the amide H to every backbone carbonyl O $k$,

$$ N_C(i) = \sum_{j \in \mathcal{V}_C(i)} s\!\left(\lVert x_{N_i} - x_j \rVert;\, r_C, b_C\right), \qquad N_H(i) = \sum_{k \in \mathcal{V}_H(i)} s\!\left(\lVert x_{H_i} - x_k \rVert;\, r_H, b_H\right) $$
^eq-bf-counts

where $\mathcal{V}_C(i)$ and $\mathcal{V}_H(i)$ are the atoms that pass the sequence exclusion. A pair on the same chain is dropped when the residue separation is at most $m$ (`seq_sep_min`), so $m = 2$ removes residues $i-2$ to $i+2$ and $m = 0$ removes only residue $i$. The protection factor follows the BV form with an added offset,

$$ \ln P_{f,i} = \beta_0 + \beta_C N_C(i) + \beta_H N_H(i) $$
^eq-bf-lnpf

Source: [[@bestStructuralInterpretationHydrogen2006#^c4]], first display, pp. 1–2, for the burial and hydrogen-bond terms; the sigmoid contact count and its sharpness parameters follow [[@wanReconcilingSimulatedEnsembles2020#^c10]]. Manuscript form: projects/2-jaxENT/manuscript/report/methods/HDX.tex#L19-L21 (the hard-cutoff form, without $\beta_0$).

An ensemble of structures $j$ with weights $w_j$ is averaged in $\ln P_f$, with uniform weights when none are given,

$$ \ln P_{f,i} = \sum_j w_j \left[\beta_0 + \beta_C N_C(i,j) + \beta_H N_H(i,j)\right] $$
^eq-bf-ensemble

Source: [[@bestStructuralInterpretationHydrogen2006#^c5]], p. 2. Manuscript form: projects/2-jaxENT/manuscript/report/methods/HDX.tex#L27-L31 (time averaging).

Uptake follows from first-order exchange under EX2 conditions. With the intrinsic rate $k_{\mathrm{int},i}$ of residue $i$, the observed rate is $k_{\mathrm{obs},i} = k_{\mathrm{int},i}\, e^{-\ln P_{f,i}}$, and a peptide $p$ sums the exchangeable residues it contains,

$$ D_p(t) = \sum_{i \in p} \left[1 - \exp\!\left(-k_{\mathrm{int},i}\, e^{-\ln P_{f,i}}\, t\right)\right] $$
^eq-bf-uptake

Manuscript form: projects/2-jaxENT/manuscript/report/methods/HDX.tex#L44 (single residue) and #L54 (peptide). The code takes rates and times in minutes and leaves out residues that cannot exchange. The ensemble average is taken in $\ln P_f$ before this step, so $D_p(t)$ is the uptake of the geometric-mean protection and not the average of per-frame uptakes (`predict.py`, which averages $\ln P_f$ and then calls `predict_uptake`). A frame-uptake average would differ wherever protection varies between frames.

## Implementation notes

- **Defaults.** $\beta_C = 0.35$, $\beta_H = 2.0$, $\beta_0 = 0$, $r_C = 6.5$ Å, $r_H = 2.5$ Å, $b_C = b_H = 5$ Å$^{-1}$, $m = 2$ (`HDXConfig`). The hard-cutoff BV model uses 2.4 Å for the hydrogen-bond cutoff ([[Best–Vendruscolo model]]), and the code default is 2.5 Å. A tanh switch (equivalent to the sigmoid with $b = 2k$) and a PLUMED-style rational switch can replace the sigmoid (`switch_fn`).
- **Which atoms count.** Hydrogen-bond acceptors are backbone carbonyl O atoms only (`backbone_O_idx`), so side-chain and water acceptors are not counted. Heavy-atom selection is set at featurisation (`include_hetatm`, `exchange_mask`).
- **Synthetic amide H.** When a structure has no amide H, the code places one 1.01 Å from the amide N on the far side from both neighbours, trans to the previous C=O. Up to BioFeaturisers 43cc194 the sign was reversed, so the H sat between the Cα and previous-C neighbours. Against the DSSP position (N plus 1.01 Å along the previous C–O direction) on 5PTI, the old placement was 2.02 Å away for all 57 residues tested and the corrected one is 0.10 Å away (mean; maximum 0.22 Å). On the TeaA open MD frame, which has explicit H, the old synthetic H gave a mean $N_H$ of 0.35 at $b_H = 1$ and 0.002 at $b_H = 5$, against 0.78 and 0.61 from the explicit H (294 residues, residue-separation exclusion of 2). The corrected sign reproduces the explicit values (correlation 1.00 at $b_H = 1$ and 0.99 at $b_H = 5$). The hydrogen-bond term was therefore close to inert for any structure without H atoms, and the larger steepness removed it almost entirely. The explicit H is used wherever the structure has one. The fix is commit 39b8069 on `main`, with a test against the DSSP position. The numbers come from a numpy reimplementation of the formula, not from the library call, and the copy vendored in MaxENT-FK (`externals/biofeaturisers`) still has the old placement line. The audit script `src/maxent_fk/analysis/scripts/hbond_geometry_audit.py` in MaxENT-FK was written for the same symptom (a near-inert $N_H$).
- **Where each experiment stands on the synthetic H.** The TeaA target and every generated Boltz structure were scored on the heavy-atom Boltz topology (`examples/TeaA/generate_target.py` reorders the MD frames onto it) with the old placement, so both sides of the comparison used the same misplaced H and the fit is self-consistent. What it reflects is a model in which hydrogen bonds contribute little. The TeaA runs have not been repeated with the fixed placement. The BPTI and MoPrP simulations contain explicit H, so they used the real amide H and are unaffected.
- **TeaA settings.** Defaults for $\beta_C$, $\beta_H$, $r_C$, $r_H$ and $b_C$, with $b_H = 1$, `fit_parameters: false` in the run configs (so the β coefficients are not refitted), intrinsic rates at pH 7.0 and 300 K from HDXrate, and times of 10, 60, 600, 3600 and 7200 s. The `run.yaml` in the pinned MaxENT-FK commit has 298.15 K, and the resolved configs of the seed-43 runs on Isambard have 300 K.
- **Intrinsic rates.** HDXrate gives $k_{\mathrm{int}}$ per residue from sequence, pH and temperature ([[intrinsic exchange rate]]). BioFeaturisers calls it without the meter-to-pD correction, so the pH supplied is taken as the final pD, and the rates are converted from per second to per minute (`hdxrate.py`). Chains without exchangeable residues are skipped.
- **Dense and chunked kernels.** The dense kernel builds the full probe-by-atom distance matrices. A chunked kernel (`chunk_size > 0`) evaluates the same sums in blocks to save memory, and an experimental spatial-truncation path is slower than the dense one. The dense path is the reference.
- **Exclusions in the experiments.** The BPTI experiment compares $m = 0$ and $m = 2$ ([[bf-bpti]]). The ±0 setting is used there to generate diverse starts, and ±2 is the exclusion set for the production runs.
- **What the smoothing changes.** At steepness 5 Å$^{-1}$ a contact switches over about 1 Å around its cutoff (a 10 to 90 % width of $2\ln 9 / b$, about 0.9 Å), so atoms near the boundary carry fractional counts that the hard model assigns to zero or one. Fitted $\beta$ coefficients calibrated for the hard cutoff are therefore not guaranteed to transfer, and ValDX's mismatch tests used a switch-function target with a hard-cutoff fit by design ([[Best–Vendruscolo model]]).
- **Limit of the map.** The model predicts residue-wise protection from one structure, then averages over the ensemble. It cannot represent a residue whose exchange runs through a rare opening that the structures do not contain ([[HDX protection-factor model]]).
