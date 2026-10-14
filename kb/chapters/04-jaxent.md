# 04 jaxENT

Chapter hub for `thesis/chapters/04-jaxent.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. Every bullet is a stub (new claim, `project: 2-jaxENT`, figure ID needed).

Status sentence: analyses complete; manuscript in draft. Due 14 Nov.

## Detail moved from §1.7

- A differentiable MaxEnt engine in which plausibility constraints are loss terms rather than architecture, with splits and replicates built into the fit.
- Joint inference of weights and forward-model parameters, with an L1 penalty on the deviation of parameters from their prior values. Non-standard conditions such as low pH require this. HDXer already optimises BV parameters, so the contribution is the unified optimisation workflow and composable objectives, not parameter fitting itself.
- A linear-additive protection-to-uptake forward model in interval-hazard form. It is an approximation, since protection factors add and uptake does not, and the frame-wise versus ensemble-average inequality remains. It holds for most cases tested and costs O(fragments × timepoints) rather than O(fragments × timepoints × frames).
- Graph-Laplacian regularisation of the weights towards the candidates' pairwise-distance distribution, for candidate sets that do not carry Boltzmann weights (statistical potentials, enhanced sampling), where the uniform-prior KL term breaks down. Any pairwise distance serves, so physics or knowledge-based terms enter the regulariser.
- Covariance-weighted and peptide-timepoint-weighted error terms ([[error covariance]]).
- Validation across three regimes of decreasing ground truth, and runtime against HDXer: [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]] (draft). The draft abstract's figures (populations within 20 to 25% of experimental precision; 1.5 to 400× faster) come from outdated experiments (project README) and are re-derived before they appear in the thesis.
- Uncertainty maps localise instability. Comparisons across simulation lengths and a control ensemble are what attribute it to sampling ([[controlled perturbation]]). The α-synuclein Tris reading stays a hypothesis bounded by sampling and forward model.
- Boundary: jaxENT still reweights fixed candidates. The states it cannot reach are ch. 5's problem.

## Drafting sources

- jaxENT (`projects/2-jaxENT/manuscript/report/`): `abstract.tex`; `introduction.tex` L4–10 and the final two paragraphs; `results.tex` L29 (validation regimes), L63 and L130 (decoys), L173–197 (uncertainty maps); `meta_analysis.tex` L1–10.
- Method notes for jaxENT observation weighting, selection and evaluation design ([[02-background]] §2.4).

## Wording to avoid

- "Uncertainty distinguishes sampling from force-field limitations" (`results.tex` L203–207). This conflicts with ValDX.
- jaxENT speedups from the outdated experiments.
- "fundamental problem", "critical obstacles", "great synergy", "establish jaxENT as".
