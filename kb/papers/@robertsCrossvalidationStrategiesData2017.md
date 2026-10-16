---
type: paper
citekey: robertsCrossvalidationStrategiesData2017
year: 2017
read: false
pdf: kb/_pdf/@robertsCrossvalidationStrategiesData2017.pdf
extraction: auto
needs_review: false
review_reason:
---

# Cross-Validation Strategies for Data with Temporal, Spatial, Hierarchical, or Phylogenetic Structure (2017)

## Main point

Review and simulations from ecology. Structured data carry dependence that persists into model residuals, so random cross-validation underestimates predictive error and rewards overfitting. Block cross-validation, which splits along the dependence structure, is recommended wherever such structure exists. The choice of block matters, because blocking can also force extrapolation and so overestimate interpolation error.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- When cross-validation ignores dependence structure in the data, predictive error is seriously underestimated. ^c1
  - page: 1
  - quote: "these structures are regularly ignored, resulting in serious underestimation of predictive error"
  - quote_check: pass
  - reviewed: false
- Block cross-validation is recommended wherever dependence structures exist in a dataset. ^c2
  - page: 1
  - quote: "block cross-validation be used wherever dependence structures exist in a dataset"
  - quote_check: pass
  - reviewed: false
- Blocking can force extrapolation by restricting the predictor ranges available for training, so the blocking strategy must match the prediction intended. ^c3
  - page: 1
  - quote: "may also unwittingly induce extrapolations by restricting the ranges or combinations of predictor variables available for model training"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The layer 1b source for dependence-aware [[data splitting]] (^c1, ^c2).
- ^c3 is why each partition asks a different predictive question: withholding a sequence or structural region tests extrapolation to unseen parts of the protein, not interpolation.

## Disagreements / limitations

- Ecological data (spatial, temporal, phylogenetic). Overlapping peptides are a further case it does not treat, in which observations share the same residues rather than being nearby.
