---
type: paper
citekey: burnleyModellingDynamicsProtein2012
year: 2012
read: false
pdf: kb/_pdf/@burnleyModellingDynamicsProtein2012.pdf
extraction: auto
needs_review: false
review_reason:
---

# Modelling Dynamics in Protein Crystal Structures by Ensemble Refinement (2012)

## Main point

Ensemble refinement of X-ray data by time-averaged restrained molecular dynamics, with large-scale disorder partitioned into a TLS model. Twenty datasets at 1.1 to 3.1 Å resolution refined to ensembles with cross-validated Rfree improved by 0.3 to 4.9 % over single structures. The refinement parameters are selected by Rfree, and the paper notes that earlier ensemble methods were exposed as over-fitted once cross-validation was introduced into crystallography.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The ensemble-refinement parameters are chosen by the cross-validated Rfree. ^c1
  - page: 5
  - quote: "Optimum parameters are selected by Rfree"
  - quote_check: pass
  - reviewed: false
- Ensemble models improved Rfree for every dataset tested. ^c2
  - page: 3
  - quote: "The ensemble models yield improved Rfree values for all datasets"
  - quote_check: pass
  - reviewed: false
- A better cross-validated Rfree is read as the ensemble fitting the X-ray data better than a single structure. ^c3
  - page: 1
  - quote: "indicating that ensemble models fit the X-ray data better than single structures"
  - quote_check: pass
  - reviewed: false

## What I use from it

- Field practice for [[model selection]]: crystallography has selected ensemble-refinement parameters on held-out reflections since the free R value (^c1), which is the nearest established precedent for choosing a fitting strength by held-out data.
- A counter-example to the statement that integrative structural biology never holds out data ([[data splitting]]).

## Disagreements / limitations

- Rfree withholds a fixed random subset of reflections. Reflections are not overlapping measurements of the same residues, so the leakage problem of HDX-MS peptides does not arise, and the precedent does not transfer to dependence-aware partitioning.
- Improvement in Rfree shows better fit to the data, not that the ensemble populations are physical.
