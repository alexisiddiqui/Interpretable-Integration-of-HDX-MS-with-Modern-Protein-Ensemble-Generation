---
type: paper
citekey: cawleyOverfittingModelSelection2010
year: 2010
read: false
pdf: kb/_pdf/@cawleyOverfittingModelSelection2010.pdf
extraction: auto
needs_review: false
review_reason:
---

# On Over-Fitting in Model Selection and Subsequent Selection Bias in Performance Evaluation (2010)

## Main point

A model selection criterion estimated on finite data has variance, so optimising it can over-fit at the level of hyperparameters, just as training over-fits at the level of parameters. When the same data serve selection and performance evaluation, the reported performance is optimistically biased, often by as much as the differences between learning algorithms. Selection must be repeated inside each evaluation trial (nested cross-validation), which costs repeated fitting.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Common performance-evaluation practices are susceptible to selection bias from over-fitting in model selection. ^c1
  - page: 1
  - quote: "some common performance evaluation practices are susceptible to a form of selection bias"
  - quote_check: pass
  - reviewed: false
- To avoid this bias, model selection must be repeated as part of fitting whenever a model is fitted to a new sample of data. ^c2
  - page: 2
  - quote: "model selection must be treated as an integral part of the model fitting process and performed afresh every time a model is fitted"
  - quote_check: pass
  - reviewed: false
- The findings apply to any selection criterion optimised over a finite sample, including the Bayesian evidence. ^c3
  - page: 1
  - quote: "including maximisation of the Bayesian evidence and optimisation of performance bounds"
  - quote_check: pass
  - reviewed: false
- Rigorous performance evaluation requires substantial computation, because models must be refitted over many partitions with selection repeated in each. ^c4
  - page: 25
  - quote: "Rigorous performance evaluation therefore requires a substantial investment of processor time"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The layer 1b source for [[model selection]]: a validation error used to choose a model overstates its performance, so evaluation needs data unused in selection (^c1, ^c2).
- ^c3 extends the point to evidence-based ranking, which bears on [[BICePs]].
- ^c4 is the general statement that assessment costs repeated fitting (§1.5 group 6).

## Disagreements / limitations

- Kernel classifiers on benchmark datasets with independent samples. Dependence between observations, as between overlapping HDX-MS peptides, is outside its scope ([[data splitting]]).
