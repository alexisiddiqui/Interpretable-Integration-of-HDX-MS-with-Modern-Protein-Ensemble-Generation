---
type: paper
citekey: mirditaColabFoldMakingProtein2022
year: 2022
read: false
pdf: kb/_pdf/@mirditaColabFoldMakingProtein2022.pdf
extraction: auto
needs_review: false
review_reason:
---

# ColabFold: Making Protein Folding Accessible to All (2022)

## Main point

ColabFold replaces the HMMer and HHblits homology search of AlphaFold2 with MMseqs2. Search is 40–60 times faster, and prediction quality on CASP14 matches AlphaFold2. It runs free on Google Colaboratory or locally. It also exposes internal settings (recycles, random seeds, dropout at inference) that later ensemble methods use to make AlphaFold2 return varied structures.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- ColabFold speeds up prediction by pairing the fast MMseqs2 homology search with AlphaFold2 or RoseTTAFold. ^c1
  - page: 1
  - quote: "ColabFold offers accelerated prediction of protein structures and complexes by combining the fast homology search of MMseqs2 with AlphaFold2 or RoseTTAFold"
  - quote_check: pass
  - reviewed: false
- Faster search and model reuse allow close to 1,000 structures per day on one GPU. ^c2
  - page: 1
  - quote: "40−60-fold faster search and optimized model utilization enables prediction of close to 1,000 structures per day"
  - quote_check: pass
  - reviewed: false
- ColabFold beats AlphaFold-Colab and matches AlphaFold2 on CASP14 targets. ^c3
  - page: 1
  - quote: "We show that ColabFold outperforms AlphaFold-Colab and matches AlphaFold2 on CASP14 targets"
  - quote_check: pass
  - reviewed: false
- Prediction quality depends on the MSA, but about 30 diverse sequences are often enough. ^c4
  - page: 2
  - quote: "often an MSA with only a few (~30) sufficiently diverse sequences is enough to produce high-quality predictions"
  - quote_check: pass
  - reviewed: false
- Extra recycling iterations can rescue difficult targets and designed proteins without known homologues. ^c5
  - page: 2
  - quote: "For difficult targets as well as for designed proteins without known homologs, additional recycling iterations can result in a high-quality prediction"
  - quote_check: pass
  - reviewed: false
- Turning on dropout at inference activates the stochastic part of the model, so predictions can differ. ^c6
  - page: 5
  - quote: "This activates the stochastic part of the model and can result in different predictions"
  - quote_check: pass
  - reviewed: false
- Because AlphaFold2 subsamples the MSA, a new random seed can pick different cluster centres and give a different structure. ^c7
  - page: 6
  - quote: "Changing the random seed can result in different cluster centers and thus different structure predictions"
  - quote_check: pass
  - reviewed: false
- Dropout sampling is offered to give an ensemble of models for the uncertain parts of a prediction. ^c8
  - page: 6
  - quote: "Enabling the latter can be used to sample an ensemble of models for the uncertain parts of the structure prediction"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1–^c3 are the citation for ColabFold as the standard fast route to AlphaFold2 predictions.
- ^c4 explains why shallow or subsampled MSAs can still give folded models, which [[MSA subsampling]] methods rely on.
- ^c6–^c8 list the stochastic knobs (seeds, dropout, recycles in ^c5) behind most AlphaFold2 "ensembles". The paper frames the spread as model uncertainty, not as a [[structural ensemble]] with populations.

## Disagreements / limitations

ColabFold is a speed and access paper. It makes no claim that seed or dropout diversity reflects conformational populations or a [[conformational free-energy landscape]]. The word "ensemble" in ^c8 means a set of models that spans uncertainty. The same notebook also says seed diversity may reflect the "ambiguity of co-evolution constraints derived from the input MSA" (p. 5). That is the hook later papers build on, but here it is stated, not tested.

The 512 cluster-centre and 1,024 extra-sequence limits (p. 6) are the max_seq and extra_seq settings that [[@monteirodasilvaHighthroughputPredictionProtein2024]] reduces. CF-random in [[@schaferSequenceClusteringConfounds2024]] runs on ColabFold with shallow random MSAs.
