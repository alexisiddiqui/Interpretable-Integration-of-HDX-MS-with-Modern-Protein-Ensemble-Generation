# 02 Background and Literature Review

Chapter hub: concepts and their equations in the order of `thesis/chapters/02-background.tex`. Equation links point at single displayed equations (`#^eq-…`). Every symbol follows [[2026-10-13 canonical HDX and ensemble notation]]; `notation.md` lists them.

Markers:
- **gap**: something the chapter needs that has no verified source or manuscript form yet.
- **decision**: a choice to make before writing.

## 2.1 HDX-MS: Measurement, Exchange Kinetics, and Structural Interpretation

Introductory equations: [[protection factor#^eq-pf]] and [[deuterium uptake#^eq-uptake-residue]].

### Experimental Workflow and Measurement Limitations
- [[deuterium uptake]]: peptide averaging [[deuterium uptake#^eq-uptake-peptide]] and back-exchange correction [[deuterium uptake#^eq-uptake-corr]].
- **decision**: present back-exchange as an equation or in prose. It is commented out in the current jaxENT methods.
- [[HDX-MS reports deuterium uptake at the peptide level, not the residue level.]]

### Intrinsic Exchange Rates
- [[intrinsic exchange rate]]: [[intrinsic exchange rate#^eq-kint]], [[intrinsic exchange rate#^eq-kint-sequence]], [[intrinsic exchange rate#^eq-kint-temperature]].
- **gap**: no manuscript applies Bai's temperature correction. Bai's Eqs. (2a) and (3) are images and need checking against the PDF.

### Linderstrøm–Lang Exchange Kinetics and EX1/EX2 Regimes
- [[Linderstrøm–Lang model]]: scheme [[Linderstrøm–Lang model#^eq-ll-scheme]], steady state [[Linderstrøm–Lang model#^eq-ll-kobs]], limits [[Linderstrøm–Lang model#^eq-ex2]] and [[Linderstrøm–Lang model#^eq-ex1]], with the derivation in the note.
- Distinguish exchange kinetics from conformational timescales: [[protein dynamics]].
- **gap**: no PDF for Hvidt and Nielsen 1966 or Smith 1997. Skinner 2012 and Englander 1997 carry the sources for now.

### Protection Factors and Peptide Uptake
- [[protection factor]]: [[protection factor#^eq-pf]] and [[protection factor#^eq-dgop]] (EX2 free energy, with derivation).
- [[deuterium uptake]]: [[deuterium uptake#^eq-uptake-residue]] → [[deuterium uptake#^eq-uptake-peptide]].
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]]

### Structural Forward Models for HDX
- [[Best–Vendruscolo model]]: [[Best–Vendruscolo model#^eq-bv-feature]] and [[Best–Vendruscolo model#^eq-bv-ensemble]].
- [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]]
- [[Structure-to-uptake models rely on hydrogen bonding and solvent exposure but add systematic errors that accumulate at peptide level.]]
- **gap**: alternative forward models are not yet concept notes. Skinner 2012 and Park 2015 are seeded; the Park PDF is unreadable.

## 2.2 Protein Conformational Ensembles and Their Generation

### Molecular Dynamics and Empirical Force Fields
- [[molecular dynamics]]: [[molecular dynamics#^eq-newton]] (very light).
- [[Boltzmann distribution]]: [[Boltzmann distribution#^eq-boltzmann]].
- **gap**: a displayed-equation source for Newton's or Langevin's equation.

### Enhanced Sampling
- [[Markov chain Monte Carlo]]: detailed balance [[Markov chain Monte Carlo#^eq-detailed-balance]] and Metropolis–Hastings [[Markov chain Monte Carlo#^eq-metropolis-hastings]], if the chapter needs them. Extended ensembles and reweighting back to the target are in the note's limits.
- Claims: [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]]

### Learned Structure Predictors and Ensemble Generators
- Very light equation: **gap**. No source is chosen yet for a learned-distribution equation. The [[diffusion model]] note may cover it.
- The caution that a learned score is a statistical potential, not a free energy: [[knowledge-based potential#^eq-inverse-boltzmann]] and the [[knowledge-based potential]] derivation.

### Diffusion Models for Protein Structure Generation
- [[diffusion model]]: [[diffusion model#^eq-diffusion-forward]] and [[diffusion model#^eq-diffusion-reverse]]. The link back to MD (Boltzmann score = force / $k_BT$) is in the note's derivation.

### Sampling Coverage and Ensemble Populations
- [[conformational free-energy landscape]], [[population shift]], [[structural ensemble]].
- [[importance sampling]]: [[importance sampling#^eq-importance-sampling]]; effective sample size (**gap**: no source for the Kish formula).
- [[reference ratio method]]: [[reference ratio method#^eq-reference-ratio]] and its KL optimality [[reference ratio method#^eq-reference-ratio-kl]].
- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

## 2.3 Integrating Biophysical Data with Structural Ensembles

### The Inverse Problem and Forward Modelling
- [[Bayes' theorem]]: [[Bayes' theorem#^eq-bayes]].
- [[inverse problem]]: the posterior over structure and nuisance parameters, [[inverse problem#^eq-isd-posterior]], with the derivation in the note.
- [[forward model]]: likelihood [[forward model#^eq-likelihood]], Gaussian error model [[forward model#^eq-gaussian-error]], ensemble-averaged prediction [[forward model#^eq-ensemble-prediction]].
- [[nuisance parameter]]: marginalisation [[nuisance parameter#^eq-marginal]], hybrid energy as negative log posterior [[nuisance parameter#^eq-hybrid-energy]], data weight [[nuisance parameter#^eq-data-weight]].
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]

### Maximum-Entropy and Bayesian Ensemble Refinement
- [[maximum entropy principle]]:
  - problem: [[maximum entropy principle#^eq-maxent-problem]];
  - posterior: [[maximum entropy principle#^eq-maxent-posterior]];
  - discrete weights: [[maximum entropy principle#^eq-maxent-weights]];
  - biased potential: [[maximum entropy principle#^eq-maxent-potential]];
  - apparent work: [[maximum entropy principle#^eq-apparent-work]].
- The KL divergence derived from the Lagrangian is steps 1–7 of the MaxEnt derivation.
- [[Kullback–Leibler divergence]]: [[Kullback–Leibler divergence#^eq-kl]] and [[Kullback–Leibler divergence#^eq-kl-weights]]. State the KL direction wherever it is used.
- Reweighting as importance sampling: [[importance sampling]], derivation step 4.
- The SAXS MaxEnt regulariser is the same prior: [[regularisation#^eq-maxent-regulariser]].
- Bayesian equivalence: [[Bayes' theorem]] (derivation steps 1–2).
- [[The MaxEnt reweighting optimisation problem is solved with the method of Lagrange multipliers.]]
- [[Minimising apparent work and KL divergence gives a reweighted ensemble that satisfies the constraints with minimal deviation.]]

### Experimentally Restrained Simulations and Metainference
- Not yet assembled. The tilted landscape ([[maximum entropy principle#^eq-maxent-potential]]) is the bridge to restrained MD.

### Experimental Guidance of Diffusion Models
- Not yet assembled. This section reviews existing approaches; the project's formulation stays in its research chapter.

## 2.4 Validation, Uncertainty, and Interpretability

Grounding concepts (from BMSB): [[posterior uncertainty]]; [[regularisation]], with $\chi^2$ [[regularisation#^eq-chi2]], the regularised objective [[regularisation#^eq-regularised-objective]] and good parameters [[regularisation#^eq-good-parameters]]; model comparison with [[Bayes' theorem#^eq-bayes-factor]].

The rest is not yet assembled. Covariance-weighted MSE, Wasserstein-1, RMSF and Work Done become method notes for ValDX and jaxENT. `02-background.tex` places the new Work Done metrics in ValDX.
