---
type: concept
aliases:
  - cross-validation
  - held-out validation
  - validation split
  - training and validation split
  - structured split
  - validation leakage
  - peptide overlap
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c12]]"
---

## Definition

Data splitting fits a model to part of the data (training) and tests it on the rest (validation), to measure how well it generalises ([[overfitting]]). The test is only fair if the validation data carry information the training data do not.

HDX-MS peptides overlap, so the same residues appear in several peptides. A random split therefore puts peptides in the validation set whose uptake is predictable from training peptides covering similar regions ([[@siddiquiFrameworkTestingStructural2026#^c8]]). This leakage inflates apparent validation performance. ValDX uses structured splits instead: redundancy-aware splits that group peptides by sequence position, and spatial splits. Repeated splits test how much the result depends on which peptides and time points were used ([[@siddiquiFrameworkTestingStructural2026#^c12]]; [[replicate uncertainty]]).

## Assumptions and limits

- Structured splits reduce dependence between the sets but do not guarantee independence (revised ValDX, `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L37; `6_methods_omc.tex` L52). Posted v1 says they "ensure" that validation error reflects true predictive performance; do not reuse that wording.
- Overlap also correlates the errors of neighbouring peptides, which most likelihoods treat as independent ([[forward model]]).
- Withholding peptides reduces the data available for fitting. With few peptides the validation error itself is noisy.
- Validation tests prediction of uptake. It does not test populations directly, which is why ValDX adds [[Work Done]] and reference benchmarks.

## Why it matters here

Introduction §1.5, paragraph 4, and the ValDX chapter's splitting protocol. Bayesian model comparison by evidence is the alternative for choosing a regularisation weight ([[Bayes' theorem#^eq-bayes-factor]], [[regularisation]]).

Claims that use this term: [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]], [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]], [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]].
