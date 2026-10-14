---
type: concept
aliases:
  - Bayesian Inference of Conformational Populations
  - BICePs score
notation:
  - {symbol: 'f^{(k)}', meaning: 'BICePs score of model k, minus the log ratio of its evidence to that of a uniform-population null model', units: null}
sources:
  - "[[@wanReconcilingSimulatedEnsembles2020#^c2]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c3]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c4]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c5]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c6]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c7]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c8]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c9]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c10]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c11]]"
  - "[[@raddiAutomaticForwardModel2025#^c1]]"
  - "[[@raddiAutomaticForwardModel2025#^c2]]"
  - "[[@raddiAutomaticForwardModel2025#^c3]]"
  - "[[@raddiAutomaticForwardModel2025#^c5]]"
  - "[[@raddiAutomaticForwardModel2025#^c6]]"
  - "[[@raddiAutomaticForwardModel2025#^c7]]"
  - "[[@raddiAutomaticForwardModel2025#^c8]]"
  - "[[@raddiAutomaticForwardModel2025#^c9]]"
---

## Definition

BICePs (Bayesian Inference of Conformational Populations) estimates conformational populations by combining a theoretical prior, usually from simulation, with ensemble-averaged experimental observables ([[@wanReconcilingSimulatedEnsembles2020#^c3]]). It samples a posterior over populations and over nuisance parameters $\sigma$ that represent the unknown experimental uncertainty and ensemble heterogeneity ([[@wanReconcilingSimulatedEnsembles2020#^c4]]). It belongs to the same family as ISD and [[metainference]] ([[@wanReconcilingSimulatedEnsembles2020#^c5]]).

Its distinctive use is model selection. Each candidate prior, for example one Markov state model per simulation condition, is ranked by how well its populations agree with the data ([[@wanReconcilingSimulatedEnsembles2020#^c6]]). The BICePs score is a [[Bayes' theorem#^eq-bayes-factor|Bayes factor]] of the model's total evidence against a null model with uniform populations ([[@wanReconcilingSimulatedEnsembles2020#^c7]]). It can be read as a free energy of each model, and lower is better ([[@wanReconcilingSimulatedEnsembles2020#^c8]], [[@wanReconcilingSimulatedEnsembles2020#^c9]]). Raddi et al. describe it as the free energy of turning on the experimental restraints ([[@raddiAutomaticForwardModel2025#^c3]]).

Later versions infer every source of error by MCMC ([[@raddiAutomaticForwardModel2025#^c5]]). With replica averaging, BICePs becomes a MaxEnt reweighting method that needs no adjustable regularisation parameter ([[@raddiAutomaticForwardModel2025#^c6]]). Forward-model parameters can then be learned with the ensemble, either sampled as nuisance parameters ([[@raddiAutomaticForwardModel2025#^c1]]) or optimised by minimising the BICePs score ([[@raddiAutomaticForwardModel2025#^c2]], [[@raddiAutomaticForwardModel2025#^c7]]).

## Equations

$$ f^{(k)} = -\ln \frac{Z^{(k)}}{Z_0}, \qquad Z^{(k)} = \int P^{(k)}(x, \sigma \mid s^\text{exp})\, dx\, d\sigma $$
^eq-biceps-score

Source: [[@wanReconcilingSimulatedEnsembles2020#^c7]], Eqs. (14)–(15), p. 25. Wan et al. write conformational states as $X$, data as $D$ and the unnormalised posterior under prior $P^{(k)}(X)$, so $Z^{(k)}$ is the evidence of model $k$; $Z_0$ is the evidence with uniform populations. The score is computed with free-energy estimators (MBAR, p. 26).

## Assumptions and limits

- **Ranks priors, does not identify populations.** The score orders the candidate models supplied. A missing state stays missing, and the ranking is conditional on the forward model and the error model ([[identifiability]], [[sampling coverage]]).
- **The error scale is inferred, not set.** $\sigma$ has an uninformative Jeffreys prior and is marginalised ([[@wanReconcilingSimulatedEnsembles2020#^c11]]). HDXer and ValDX instead fix the error scale and tune the fitting strength $\gamma$ ([[nuisance parameter]]).
- **Its "free energy" is an evidence.** The score is a statement about a model given data. It is not a conformational free energy, and its thermodynamic name is an analogy ([[statistical potential]]).
- **Three objects to keep apart.**
  - The HDXer loss is a fitting objective. With $\sigma$ fixed and the posterior mode taken in place of the evidence integral, it has the form of a MAP posterior energy.
  - [[Work Done]] is a diagnostic distance in protection-factor space computed after fitting. It is not an objective and not an evidence, so "Work equals BICePs log-evidence" does not hold.
  - The BICePs score is an evidence ratio over the full posterior.
  - The derivation and its limits are worked through in `projects/1-ValDX/manuscript/assessments/BiCePs_positioning_handoff.md` (§§2–3; working note, not evidence).
- **HDX coverage.** Wan et al. used BICePs with an HDX protection-factor predictor to choose among apomyoglobin ensembles ([[@wanReconcilingSimulatedEnsembles2020#^c2]]). They first inferred that predictor's parameters, including BV-like $\beta_c$ and $\beta_h$, by sampling a posterior trained on ubiquitin and [[BPTI]] protection factors ([[@wanReconcilingSimulatedEnsembles2020#^c10]]). That work uses residue protection factors, not peptide uptake. No BICePs study benchmarks HDX-MS uptake through the Best–Vendruscolo model against held-out peptides.
- **Forward-model learning is shown for Karplus only.** Raddi et al. refine Karplus-relation parameters ([[@raddiAutomaticForwardModel2025#^c8]]) and state that the method generalises to any differentiable forward model ([[@raddiAutomaticForwardModel2025#^c9]]). No BV or uptake model is fitted, so it is the closest published analogue to jaxENT's joint weight and BV-coefficient fitting, not a benchmark against it.
- **gap.** BICePs v2.0 (Raddi, Ge & Voelz 2023) is in Zotero but not yet in the KB. Its live item has the key `raddiBICePsV20Software2023c` because trashed copies hold the base key; seed it once the key is clean.

## Why it matters here

Chapter 2 and Chapter 3. BICePs is the clearest existing method for Bayesian evidence-based ranking of competing structural hypotheses, so ValDX is positioned against it (`projects/1-ValDX/manuscript/report/7_results_omc.tex` L220; manuscript pointer). The two address different parts of the same inference problem. BICePs asks which prior the data favour under a full error model, whereas ValDX asks whether a fit generalises across leakage-aware splits and how much fitting changed the protection profile. Chapter 3 has to define the Work metrics, HDXer apparent work and the BICePs score side by side (`thesis/chapters/03-valdx.tex` L9).

Claims that use this term: [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]], [[BICePs ranks candidate priors by an evidence ratio while inferring the experimental uncertainty as a nuisance parameter.]].
