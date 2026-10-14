---
type: paper
citekey: meloGeneralizedCorrelationbasedDynamical2020
year: 2020
read: false
pdf: kb/_pdf/@meloGeneralizedCorrelationbasedDynamical2020.pdf
extraction: auto
needs_review: false
review_reason:
---

# Generalized Correlation-Based Dynamical Network Analysis: A New High-Performance Approach for Identifying Allosteric Communications in Molecular Dynamics Trajectories (2020)

## Main point

A high-performance implementation of dynamical network analysis for MD trajectories, built on generalised correlation coefficients from mutual information rather than Pearson correlation.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Dynamical network analysis was developed to identify important residues and information pathways in molecular complexes. ^c1
  - page: 1
  - quote: "In order to identify important residues and information pathways within molecular complexes, the Dynamical Network Analysis method was developed"
  - quote_check: pass
  - reviewed: false
- Pearson correlation misses non-linear contributions and correlations between perpendicular atomic motions. ^c2
  - page: 2
  - quote: "Pearson correlation does not account for non-linear contributions to correlations, and fails to asses correlations in perpendicular motion of atoms"
  - quote_check: pass
  - reviewed: false
- Generalised correlation coefficients based on Shannon mutual information avoid these limits. ^c3
  - page: 2
  - quote: "generalized correlation coefficients, using the well-known Shannon mutual information"
  - quote_check: pass
  - reviewed: false

## Notation

<!-- Only for sources whose equations a concept uses. One row per symbol the concepts rely on or that clashes with the thesis notation.
| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $E(x)$ | force-field energy | $U(x)$ | |
| $\beta$ | inverse temperature | — | write 1/k_BT |
Canonical is one $symbol$ declared by a concept, or —. Delete this section if unused. -->

## What I use from it

The limit of linear displacement correlation ([[positional covariance]]): Pearson-type DCC misses non-linear and perpendicular coupled motion.

## Disagreements / limitations

The local PDF is the bioRxiv preprint. The project bibliographies also hold the keys `meloGeneralizedCorrelationbasedDynamical` and `meloGeneralizedCorrelationbasedDynamicala` (Melo and Bernardi only). They are not in the current Zotero library, so treat them as stale and cite the 2020 key.
