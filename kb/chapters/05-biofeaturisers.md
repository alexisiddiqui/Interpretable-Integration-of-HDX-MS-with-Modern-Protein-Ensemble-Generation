# 05 BioFeaturisers

Chapter hub for `thesis/chapters/05-biofeaturisers.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. The contribution that can be claimed now is the library and the pipeline. The case results are in progress and are written as what each case tests, in order of decreasing ground truth ([[examples]] 7).

Status sentence: work in progress. Preliminary experiments; metadiffusion working on TeaA. Due 28 Nov ("metadynamics" in `DEADLINES.md`).

## Detail moved from §1.7

- A library of differentiable forward models (JAX, with PyTorch wrappers): a Heaviside-contact BV model with usable gradients and an FFT SAXS model. One forward-model definition serves reweighting (jaxENT), restrained sampling (metadynamics–metainference) and guided generation (metadiffusion). Stub.
- [[BPTI]] against the 1 ms Anton trajectory, by metainference–metadynamics. MI+PB with ±0 residue exclusions first generates a diverse ensemble; four structures selected across that ensemble seed sampling with the correct ±2 exclusions, with matched MI+PB, MI-only and unbiased conditions. Each stage uses four 250 ns replicas, so one two-stage route totals 2 μs, 500-fold less aggregate production simulation than the 1 ms reference. The restraints use experimental HDX-NMR protection factors, and Anton supplies the controlled structural reference. The experiment tests whether restrained sampling recovers the basins and populations a long reference simulation shows; the existing PCA comparison establishes basin coverage and retention from the diverse starts. Protocol and comparison in [[bf-bpti]].
- MoPrP at pH 4 and pH 7: candidates from metadynamics–metainference, then unrestrained short apo simulations from decorrelated structures: tests whether pH-dependent partially unfolded states appear. Reading a pathway from them needs the trajectories, not the weights ([[conformational kinetics]]). Mechanistic question; depends on protonation (ch. 6).
- TeaA (two lobes joined by a hinge) against a synthetic HDX target built from MD frames at 40 % open : 60 % closed, by metadiffusion with a well-tempered bias along a hinge coordinate taken from Boltz-2's own fluctuations, then late-stage HDX guidance and MaxEnt reweighting: tests whether the open:closed populations are recovered with no MD reference in any run. The bias gives coverage of the hinge angle and the populations come from the reweighting. In the seed-43 run the refined ensemble puts 0.459 of the weight on the open state against a target of 0.40, and its strict recovery of 74.7 % compares with 54.0 % for the unguided control, though the forward model cannot separate 0.40 from 0.50 open. Known populations, synthetic data; protocol in `kb/experiments/bf-teaa.md`.
- Boundary (from the §2.4 hub): [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]], and a restraint is only as good as the forward model where the data are.
- "heavy-side" (tex comments) is Heaviside.

## BPTI figures

- [biofeat-bpti-matched-starts](../../figures/biofeat-bpti-matched-starts/fig.png) is the main-text BPTI figure. It compares the ±0 source with the subsequent ±2 MI+PB, ±2 MI and matched unbiased ensembles against Anton, showing recovery of basin coverage with 2 μs of aggregate production simulation per two-stage route.
- [biofeat-bpti-replica-retention](../../figures/biofeat-bpti-replica-retention/fig.png) goes in the appendix. It follows each selected start through the three conditions, distinguishing retention of starting diversity from visits by other replicas.
- [biofeat-bpti-seq0-controls](../../figures/biofeat-bpti-seq0-controls/fig.png) is retained in the experiment record. It shows that the ±0 MI+PB source covers the two principal Anton basins across the original sampling controls.
- [biofeat-bpti-seq2-controls](../../figures/biofeat-bpti-seq2-controls/fig.png) is retained in the experiment record. It shows that ±2 MI and MI+PB from the original starts remain concentrated in the main basin, motivating the diversity stage.

## Drafting sources

- Chapter tex comments (`05-biofeaturisers.tex`); the README project table and `DEADLINES.md` for status.
- [[02-background]] §2.4 for restraints, guidance and the missing HDX collective variable.

## Gaps
- The TeaA case has no MD metadynamics run with the same forward model, so the comparison planned for the metadiffusion case is open: drop it or run it.
- No published pH 4 against pH 7 simulation of mouse PrP was found (human and bovine only); check again before calling the MoPrP runs the first mouse-specific comparison.
