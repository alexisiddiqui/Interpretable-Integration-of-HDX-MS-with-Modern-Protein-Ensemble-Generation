---
type: paper
citekey: crookEmpiricalBayesFunctional2022
year: 2022
read: false
pdf: kb/_pdf/@crookEmpiricalBayesFunctional2022.pdf
extraction: auto
needs_review: false
review_reason:
---

# Empirical Bayes Functional Models for Hydrogen Deuterium Exchange Mass Spectrometry (2022)

## Main point

A functional data analysis of differential HDX-MS in which each peptide's uptake curve is modelled as a smooth function of labelling time and tested for differences between conditions with empirical Bayes shrinkage of the variance. The method is applied to HOIP-RBR with single-domain antibodies to locate epitopes and allosteric effects. The limitations section states that correlations between overlapping peptides are not modelled and show up as clustered p-values.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The model does not account for correlations between overlapping peptides, which the authors call the spatial domain of HDX data. ^c1
  - page: 6
  - quote: "we do not model correlations in the spatial domain of HDX data"
  - quote_check: pass
  - reviewed: false
- Unmodelled overlap correlation shows up as clustering of p-values for overlapping peptides. ^c2
  - page: 6
  - quote: "This manifests as clustering of pvalues for overlapped peptides"
  - quote_check: pass
  - reviewed: false

## What I use from it

- Field practice for [[error covariance]] and [[data splitting]]: the dependence between overlapping peptides is recognised in HDX-MS statistics and left unmodelled (^c1, ^c2). The clustering of p-values is the hypothesis-testing counterpart of validation leakage.

## Disagreements / limitations

- Differential HDX-MS hypothesis testing, not ensemble integration. Nothing here concerns reweighting or validation of structural hypotheses.
- Only the limitations paragraph has been read closely. The modelling details are not yet extracted.
