---
type: paper
citekey: wayment-steelePredictingMultipleConformations2024
year: 2024
read: false
pdf: kb/_pdf/@wayment-steelePredictingMultipleConformations2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# Predicting Multiple Conformations via Sequence Clustering and AlphaFold2 (2024)

## Main point

AF-Cluster clusters an MSA by sequence similarity and runs AlphaFold2 on each cluster. For fold switchers (KaiB, RfaH, MAD2) this returns both known states with high pLDDT, where the full MSA returns one. NMR confirmed two predictions: a KaiB variant stabilised in the fold-switched state, and a triple mutant that flips the KaiB equilibrium. The authors state that pLDDT is not a free energy and that model counts are not Boltzmann weights.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Clustering the MSA by sequence similarity lets AlphaFold2 sample alternative states of known metamorphic proteins with high confidence. ^c1
  - page: 1
  - quote: "clustering a multiple-sequence alignment by sequence similarity enables AlphaFold2 to sample alternative states of known metamorphic proteins with high confidence"
  - quote_check: pass
  - reviewed: false
- An ideal ensemble predictor would both generate the whole landscape and score conformations by their Boltzmann distribution. ^c2
  - page: 1
  - quote: "generate conformations encompassing the complete landscape and (2) score these conformations in accordance with the underlying Boltzmann distribution"
  - quote_check: pass
  - reviewed: false
- MSA Transformer found evolutionary couplings for both KaiB states in the clusters. ^c3
  - page: 3
  - quote: "these clusters contained evolutionary couplings for both states"
  - quote_check: pass
  - reviewed: false
- NMR confirmed the AF-Cluster prediction that a KaiB variant from T. elongatus vestitus favours the fold-switched state. ^c4
  - page: 3
  - quote: "Using nuclear magnetic resonance (NMR) spectroscopy, we could indeed verify our AF-Cluster prediction"
  - quote_check: pass
  - reviewed: false
- By NMR peak intensities, the designed triple mutant of R. sphaeroides KaiB is 86% fold-switched, against 11% for wild type. ^c5
  - page: 4
  - quote: "the mutant occupies the FS state with a population of 86% (versus 11% in the WT)"
  - quote_check: pass
  - reviewed: false
- The authors state that pLDDT cannot be used as a measure of free energy. ^c6
  - page: 6
  - quote: "the pLDDT metric itself cannot be used as a measure of free energy"
  - quote_check: pass
  - reviewed: false
- The number of models per state reflects how common each state is across the family, not its Boltzmann weight. ^c7
  - page: 6
  - quote: "will reflect the abundance of constructs reflecting different states across the protein family, which cannot be interpreted as that state’s Boltzmann weight"
  - quote_check: pass
  - reviewed: false
- The authors expect such methods, developed with experiments, to have an impact on predicting energy landscapes. ^c8
  - page: 1
  - quote: "will probably have a considerable impact on predicting protein energy landscapes, essential for illuminating biological function"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1 is the main citation for AF-Cluster as an [[MSA subsampling]] method that reaches alternative states.
- ^c2 states the two requirements of an ensemble generator, [[sampling coverage]] and correct weights. AF-Cluster addresses only the first.
- ^c6, ^c7 are the strongest caution passages. Counts of AF-Cluster models are not populations, and pLDDT is not an energy. Use these whenever the thesis describes MSA-derived sets as a [[structural ensemble]].
- ^c4, ^c5 are what is experimentally shown. The prediction gives the dominant state, and NMR measures the populations. The 86% figure is an NMR measurement, not an AF-Cluster output.
- ^c8 is the "energy landscape" aspiration, stated as an outlook in the abstract. Cite it as a hope, not a result, alongside [[conformational free-energy landscape]].
- ^c3 is the proposed mechanism (deconvolved couplings), which [[@schaferSequenceClusteringConfounds2024]] disputes.

## Disagreements / limitations

What the paper shows is that clustered MSAs make AlphaFold2 return both known states of a few fold switchers, and that predicted dominant states matched NMR for two tested KaiB constructs. What it asserts is broader. The mechanism (clustering "deconvolving conflicting sets of couplings", p. 5) rests on the RfaH pLDDT comparison and MSA Transformer contacts (^c3). [[@schaferSequenceClusteringConfounds2024]] challenges both. They report that the full-MSA pLDDT control was run in ColabFold rather than AF2, that random subsampling beats clustering, and that KaiB predictions are reproducible from single sequences.

Population claims rest on NMR, not on AF-Cluster. The authors themselves say model counts track family abundance (^c7) and pLDDT ranks the disfavoured KaiB state above the ground state (p. 6). Seeds, dropout and the five models gave no fold-switched KaiB models without an MSA (p. 6). They also note that "conformational substates not present in the evolutionary signal may require alternative methods" (p. 7). The paper's own caveats therefore rule out reading AF-Cluster output as an energy landscape.

Schafer et al. flag KaiB-TV4 (^c4) as a case where AF-Cluster also predicts a ground state that NMR does not show.
