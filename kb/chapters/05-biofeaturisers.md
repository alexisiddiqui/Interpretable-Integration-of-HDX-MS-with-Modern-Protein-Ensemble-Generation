# 05 BioFeaturisers

Chapter hub for `thesis/chapters/05-biofeaturisers.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. The contribution that can be claimed now is the library and the pipeline. The case results are in progress and are written as what each case tests, in order of decreasing ground truth ([[examples]] 7).

Status sentence: work in progress. Preliminary experiments; metadiffusion working on TeaA. Due 28 Nov ("metadynamics" in `DEADLINES.md`).

## Detail moved from §1.7

- A library of differentiable forward models (JAX, with PyTorch wrappers): a Heaviside-contact BV model with usable gradients and an FFT SAXS model. One forward-model definition serves reweighting (jaxENT), restrained sampling (metadynamics–metainference) and guided generation (metadiffusion). Stub.
- [[BPTI]] against the 1 ms Anton trajectory, by metainference–metadynamics. MI+PB with ±0 residue exclusions first generates a diverse ensemble; four structures selected across that ensemble seed sampling with the correct ±2 exclusions, with matched MI+PB, MI-only and unbiased conditions. Each stage uses four 250 ns replicas, so one two-stage route totals 2 μs, 500-fold less aggregate production simulation than the 1 ms reference. The restraints use experimental HDX-NMR protection factors, and Anton supplies the controlled structural reference. The experiment tests whether restrained sampling recovers the basins and populations a long reference simulation shows; the existing PCA comparison establishes basin coverage and retention from the diverse starts. Protocol and comparison in [[bf-bpti]].
- MoPrP at pH 4 and pH 7: candidates from metadynamics–metainference, then unrestrained short apo simulations from decorrelated structures: tests whether pH-dependent partially unfolded states appear. Reading a pathway from them needs the trajectories, not the weights ([[conformational kinetics]]). The closest match to PUF1 is β1, the loop and α1 N displaced together (MSM ΔG 2.60 kcal/mol at pH 4 against 2.2 ± 0.2). The closest match to PUF2 lies in the same detached β1–α1 set with α1 and β2 also shifted (3.35 against 3.1 ± 0.5), although β2 shifts and does not detach. Both candidates rest on the 12 pH 7 #3 seeds, and MaxCal does not preserve this agreement (3.90 and 3.47, with the order inverted). The campaign shows pH differences in the MSM, where core distortion is 2.3–2.8 times and the α1–β2 unit shift 7–10 times more populated at pH 4 at both lags. These results depend on seeding, and constant-pH simulations are required to resolve these ambiguities. Mechanistic question; depends on protonation (ch. 6). Protocol and results in [[bf-moprp]].
- TeaA (two lobes joined by a hinge) against a synthetic HDX target built from MD frames at 40 % open : 60 % closed, by metadiffusion with a well-tempered bias along a hinge coordinate taken from Boltz-2's own fluctuations, then late-stage HDX guidance and MaxEnt reweighting: tests whether the open:closed populations are recovered with no MD reference in any run. The bias gives coverage of the hinge angle and the populations come from the reweighting. In the seed-43 run the refined ensemble puts 0.459 of the weight on the open state against a target of 0.40, and its strict recovery of 74.7 % compares with 54.0 % for the unguided control, though the forward model cannot separate 0.40 from 0.50 open. Known populations, synthetic data; protocol in `kb/experiments/bf-teaa.md`.
- Boundary (from the §2.4 hub): [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]], and a restraint is only as good as the forward model where the data are.
- "heavy-side" (tex comments) is Heaviside.

## BPTI figures

- [biofeat-bpti-matched-starts](../../figures/biofeat-bpti-matched-starts/fig.png) is the main-text BPTI figure. It compares the ±0 source with the subsequent ±2 MI+PB, ±2 MI and matched unbiased ensembles against Anton, showing recovery of basin coverage with 2 μs of aggregate production simulation per two-stage route.
- [biofeat-bpti-replica-retention](../../figures/biofeat-bpti-replica-retention/fig.png) goes in the appendix. It follows each selected start through the three conditions, distinguishing retention of starting diversity from visits by other replicas.
- [biofeat-bpti-seq0-controls](../../figures/biofeat-bpti-seq0-controls/fig.png) is retained in the experiment record. It shows that the ±0 MI+PB source covers the two principal Anton basins across the original sampling controls.
- [biofeat-bpti-seq2-controls](../../figures/biofeat-bpti-seq2-controls/fig.png) is retained in the experiment record. It shows that ±2 MI and MI+PB from the original starts remain concentrated in the main basin, motivating the diversity stage.

## MoPrP figures and section plan

- [biofeat-moprp-basins](../../figures/biofeat-moprp-basins/moprp_basins_101.png) shows the MI+PB basins on the Cartesian PCA at each pH, with renders of representative frames. The seeds of the unbiased runs come from these circles.
- [biofeat-moprp-paths-ext12](../../figures/biofeat-moprp-paths-ext12/seeded_paths_ext12_pca.png), with `seeded_paths_ext12_dih`, follows the seeded runs on the PCA plane and on the dRMSD–β1-deviation plane.
- [biofeat-moprp-msm-ext12](../../figures/biofeat-moprp-msm-ext12/msm_ext12_main_fes.png) gives the stationary MSM free energy on both planes at each pH.
- [biofeat-moprp-flow-ext12](../../figures/biofeat-moprp-flow-ext12/seeded_flow_ext12_tau1ns_pca_contours.png) gives the drift, with speed contours on the PCA plane, direction arrows on the dihedral plane and the pH 7 minus pH 4 change.

Paragraph order, one finding each:

1. Restrained sampling at pH 4 and pH 7 uses one HDX target vector, so the comparison changes only protonation and buffer. Restrained frame frequencies do not give populations, so unbiased runs are seeded from the sampled basins (12 per basin and pH, 12.48 μs) and built into MSMs.
2. Basins figure. At pH 4 restrained sampling extends along the β1-detached arm, and at pH 7 it reaches the core-distorted lobe and the detached β1–α1 set.
3. Basins figure. The arm is mostly β1 detached alone. The lobe keeps β1 and distorts the core (0.17–0.20 against 0.09 nm). The detached β1–α1 set displaces β1, the loop and α1 N, and it holds both PUF candidates. The PUF1 text rule, α3 C disorder with β1 detached, has no frames.
4. Paths figure. β1 alone exchanges with the detached β1–α1 set, which almost never connects directly to Folded, and the lobe is a separate branch off Folded. The dihedral plane separates β1 detachment from the rest.
5. MSM figure. At pH 4 the PUF1 candidate lies at 2.60 against 2.2 ± 0.2 kcal/mol and the PUF2 candidate at 3.35 against 3.1 ± 0.5. Both rest on the pH 7 #3 seeds, and MaxCal does not keep the agreement (3.90 and 3.47). The MSM makes β1 opening too easy (0.52 against 2.2 kcal/mol).
6. MSM figure. pH 7 has a metastable state with PUF2-like character on the arm at PC (87.5, 17.5), at 0.65 against 1.7 kcal/mol at pH 4, where 72 % of the MSM weight meets the PUF2 text rule (0 % at pH 4). It only just meets the PUF2 candidate definition, because β2 shifts by 0.28–0.33 nm against a 0.25 nm threshold rather than detaching, and it rests on the pH 7 #3 seeds. Core distortion (2.3–2.8 times) and the unit shift (7–10 times) are more populated at pH 4.
7. Flow figure. pH 7 has one clear slow corridor from Folded towards that metastable state on the arm, whereas pH 4 has a flat slow region that splits into two routes, towards the lobe and along the arm. These are the parallel pathways. Drift is measured in the projection, and early and late drift agree (median cosine 0.89–0.94), so runs of different lengths can be pooled.
8. Seeding from the detached β1–α1 set cannot show Folded opening into it. These results depend on seeding, and constant-pH simulations are required to resolve these ambiguities, together with better paired experiments.

## Drafting sources

- Chapter tex comments (`05-biofeaturisers.tex`); the README project table and `DEADLINES.md` for status.
- [[02-background]] §2.4 for restraints, guidance and the missing HDX collective variable.

## Gaps
- The TeaA case has no MD metadynamics run with the same forward model, so the comparison planned for the metadiffusion case is open: drop it or run it.
- No published pH 4 against pH 7 simulation of mouse PrP was found (human and bovine only); check again before calling the MoPrP runs the first mouse-specific comparison.
