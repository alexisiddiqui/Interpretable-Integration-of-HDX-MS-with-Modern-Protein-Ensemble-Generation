---
type: paper
citekey: schaferSequenceClusteringConfounds2024
year: 2024
read: false
pdf: kb/_pdf/@schaferSequenceClusteringConfounds2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# Sequence Clustering Confounds AlphaFold2 (2024)

## Main point

A short critique of AF-Cluster ([[@wayment-steelePredictingMultipleConformations2024]]). Random MSA subsampling in ColabFold (CF-random) predicts the fold switchers KaiB, RfaH and MAD2 more accurately and with fewer runs than sequence clustering. AF-Cluster also gives confident false positives for single-fold KaiB variants. So clustering is not shown to be what produces alternative states, and the deconvolved-couplings explanation is called into question.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Random sequence sampling outperforms sequence clustering, which challenges the claim that AF-Cluster works by deconvolving couplings. ^c1
  - page: 1
  - quote: "random sequence sampling outperforms sequence clustering, challenging the claim that AF-cluster works by"
  - quote_check: pass
  - reviewed: false
- AF-Cluster predicts some single-fold KaiB homologs to be fold switchers. ^c2
  - page: 1
  - quote: "AF-cluster mistakes some single-folding KaiB homologs for fold switchers, a critical flaw bound to mislead users"
  - quote_check: pass
  - reviewed: false
- AF-Cluster gives low confidence to many correct structures and similar confidence to some unobserved and observed conformations. ^c3
  - page: 1
  - quote: "AF-cluster predicts many correct structures with low confidence and some experimentally unobserved conformations with confidences similar to experimentally observed ones"
  - quote_check: pass
  - reviewed: false
- In the cluster giving the most confident autoinhibited RfaH model, MSA Transformer found no contacts unique to the autoinhibited form. ^c4
  - page: 2
  - quote: "no amino acid contacts unique to the autoinhibited a-helical form were observed"
  - quote_check: pass
  - reviewed: false
- For RfaH, 5 of 21 models from randomly sampled MSAs had accurate CTDs (24%), against 10 of 250 for AF-Cluster (4%). ^c5
  - page: 2
  - quote: "among the 21 models that AF2 generated from randomly sampled MSAs, five had accurately predicted CTDs, a 24% success rate"
  - quote_check: pass
  - reviewed: false
- All the KaiB predictions can also be reproduced from single sequences. ^c6
  - page: 3
  - quote: "All KaiB predictions can be reproduced from single sequences also"
  - quote_check: pass
  - reviewed: false
- These errors mean AF2-based predictions of mutational effects need caution. ^c7
  - page: 4
  - quote: "These predictive errors indicate that AF2-based predictions of mutational effects should be interpreted with caution"
  - quote_check: pass
  - reviewed: false
- Neither CF-random nor AF-Cluster predicts fold switching reliably, especially in harder cases. ^c8
  - page: 5
  - quote: "neither CF-random nor AF-cluster predicts fold switching reliably, especially in more difficult cases"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c4, ^c6 are the counter-evidence to the coevolution mechanism. If random subsampling or a single sequence gives the same states, the alternative states need not come from cluster-specific couplings.
- ^c2, ^c3 show that pLDDT does not separate real alternative states from false ones. This supports caution on any [[MSA subsampling]] set used as a [[structural ensemble]].
- ^c5 gives numbers for the random-versus-clustering comparison.
- ^c7, ^c8 support a careful sentence that MSA manipulation finds some alternative states but does not reliably predict fold switching or mutational effects.

## Disagreements / limitations

This is a bioRxiv preprint (posted 9 January 2024) and not peer reviewed in this form. It tests only the three families in the Wayment-Steele paper. Its alternative, CF-random, uses depths tuned per protein (max-seq 1, 8 and 64; p. 5), so it is not prior-free either.

The critique concerns which states are found and how confidence is scored. It does not test populations, and it does not discuss energy landscapes. Its implication for landscape claims is indirect. If the states come from stochastic MSA subsampling or from the sequence alone, the frequency of each state reflects sampling settings and memorised folds, not a Boltzmann weight. That agrees with Wayment-Steele's own caveat ([[@wayment-steelePredictingMultipleConformations2024#^c7]]).

The two papers disagree on mechanism (deconvolved couplings against plain subsampling noise) and on reliability (KaiB-TV4 confirmed versus also falsely predicted in the ground state). They agree that default AlphaFold2 misses alternative states. They also agree that predictions need orthogonal checks, and Schafer et al. close by saying AF2's "current ability to accurately predict alternative conformations is limited" (p. 5).
