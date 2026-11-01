# 05 BioFeaturisers

Chapter hub for `thesis/chapters/05-biofeaturisers.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. The contribution that can be claimed now is the library and the pipeline. The case results are in progress and are written as what each case tests, in order of decreasing ground truth ([[examples]] 7).

Status sentence: work in progress. Preliminary experiments; metadiffusion working on TeaA. Due 28 Nov ("metadynamics" in `DEADLINES.md`).

## Detail moved from §1.7

- A library of differentiable forward models (JAX, with PyTorch wrappers): a Heaviside-contact BV model with usable gradients and an FFT SAXS model. One forward-model definition serves reweighting (jaxENT), restrained sampling (metadynamics–metainference) and guided generation (metadiffusion). Stub.
- [[BPTI]] against the 1 ms Anton trajectory, by metainference–metadynamics: tests that restrained sampling recovers the populations a long reference simulation shows. Controlled reference.
- MoPrP at pH 4 and pH 7: candidates from metadynamics–metainference, then unrestrained short apo simulations from decorrelated structures: tests whether pH-dependent partially unfolded states appear. Reading a pathway from them needs the trajectories, not the weights ([[conformational kinetics]]). Mechanistic question; depends on protonation (ch. 6).
- TeaA (two lobes joined by a hinge) against a synthetic HDX target built from MD frames at 40 % open : 60 % closed, by metadiffusion with a well-tempered bias along a hinge coordinate taken from Boltz-2's own fluctuations, then late-stage HDX guidance and MaxEnt reweighting: tests whether the open:closed populations are recovered with no MD reference in any run. The bias gives coverage of the hinge angle and the populations come from the reweighting; the closed-side angle is resolved and the open-side angle is not. Known populations, synthetic data; protocol in `kb/experiments/bf-teaa.md`.
- Boundary (from the §2.4 hub): [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]], and a restraint is only as good as the forward model where the data are.
- "heavy-side" (tex comments) is Heaviside.

## Drafting sources

- Chapter tex comments (`05-biofeaturisers.tex`); the README project table and `DEADLINES.md` for status.
- [[02-background]] §2.4 for restraints, guidance and the missing HDX collective variable.

## Gaps
- The TeaA case has no MD metadynamics run with the same forward model, so the comparison planned for the metadiffusion case is open: drop it or run it.
- No published pH 4 against pH 7 simulation of mouse PrP was found (human and bovine only); check again before calling the MoPrP runs the first mouse-specific comparison.
