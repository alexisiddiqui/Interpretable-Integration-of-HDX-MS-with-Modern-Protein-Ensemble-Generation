---
type: concept
aliases:
  - hyperparameter selection
  - selection bias
  - nested cross-validation
  - test set
  - evaluation set
  - external validation
  - free R value
  - Rfree
notation: []
sources:
  - "[[@burnleyModellingDynamicsProtein2012#^c1]]"
  - "[[@burnleyModellingDynamicsProtein2012#^c2]]"
  - "[[@burnleyModellingDynamicsProtein2012#^c3]]"
  - "[[@bmsb2012ch13#^c6]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c16]]"
  - "[[@bradshawInterpretationHDXData2020#^c20]]"
---

## Definition

Model selection chooses between fitted models, or between settings of a hyperparameter such as the fitting strength, by a score. When the score is the error on held-out data, the chosen model is the one that happened to do best on that particular held-out set, so the same error overstates how well it will do on new data. Estimating performance therefore needs data that played no part in selection. That can be a separate test set, or a nested procedure in which selection happens inside an outer loop of held-out evaluation. The general source for this statement is standard statistical learning, which the vault does not yet hold (see Gaps in [[02-background]]).

## In integrative practice

- Crystallography has selected refinement parameters on held-out reflections since the free R value. Ensemble refinement of X-ray data chooses its parameters by Rfree and reads a lower Rfree as a better fit of the ensemble to the data ([[@burnleyModellingDynamicsProtein2012#^c1]], [[@burnleyModellingDynamicsProtein2012#^c2]], [[@burnleyModellingDynamicsProtein2012#^c3]]). Rfree withholds a random subset of reflections, which are not overlapping measurements of the same residues.
- In ensemble reweighting the fitting strength is usually chosen by a χ² target or an elbow heuristic, or inferred as a hyperparameter ([[@bmsb2012ch13#^c6]], [[nuisance parameter]]). Evidence ranking is the Bayesian alternative ([[BICePs]], [[Bayes' theorem#^eq-bayes-factor]]).
- HDXer's authors note that time points could be split into training and validation sets to cross-validate the data themselves ([[@bradshawInterpretationHDXData2020#^c20]]). Withholding time points asks whether the kinetic model generalises in time, which is a different question from withholding peptides ([[data splitting]]).

## Why it matters here

- ValDX chooses the fitting strength within each split replicate by a knee criterion on the training sweep, and reports validation error and Work Done at that choice (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L473). Validation error is therefore not used for selection, which keeps it an evaluation. On experimental data the baseline Random and Sequential splits added no discrimination beyond training error ([[@siddiquiFrameworkTestingStructural2026#^c16]]), so only the structured splits carry an evaluation.
- jaxENT's current policy selects each split replicate on its HDX-MS validation data and evaluates against the HDX-NMR-derived reference or the synthetic truth, which never enter selection ([[Evaluation design (jaxENT)]]). That is selection separated from evaluation, nested in structure with one outer evaluation rather than a resampled outer loop. The manuscript's "selected by test error minimisation" (`projects/2-jaxENT/manuscript/report/experiments/protocols.tex` L325) describes the legacy path and needs updating.
- "Nested cross-validation" is reserved in this thesis for a resampled outer loop. Having two modalities does not by itself make a procedure nested.

Claims that use this term: [[Selecting a model by its validation error makes that error optimistic, so performance must be estimated on data unused in selection.]], [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]], [[Withholding a time point, a peptide, a sequence region or a structural region asks different predictive questions.]].
