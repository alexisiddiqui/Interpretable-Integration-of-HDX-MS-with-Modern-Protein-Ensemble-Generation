---
type: paper
citekey: monteirodasilvaHighthroughputPredictionProtein2024
year: 2024
read: false
pdf: kb/_pdf/@monteirodasilvaHighthroughputPredictionProtein2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# High-Throughput Prediction of Protein Conformational Distributions with Subsampled AlphaFold2 (2024)

## Main point

Lowering AlphaFold2's max_seq and extra_seq settings, and running many seeds with dropout, gives a spread of predicted structures. The fraction of models in each state is read as a relative population. For Abl1 kinase, its relatives and point mutants, and for GMCSF mutants, the direction of population change matched NMR in over 80% of cases. The authors limit the claim to qualitative changes in well-populated states. They say it is not shown that the method gives Boltzmann ratios.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The authors claim subsampling MSAs lets AlphaFold2 directly predict the relative populations of protein conformations. ^c1
  - page: 1
  - quote: "we demonstrate how AlphaFold 2 can directly predict the relative populations of different protein conformations by subsampling multiple sequence alignments"
  - quote_check: pass
  - reviewed: false
- Tested against NMR on Abl1 and GMCSF, changes in relative state populations were predicted with over 80% accuracy. ^c2
  - page: 1
  - quote: "predicted changes in their relative state populations with more than 80% accuracy"
  - quote_check: pass
  - reviewed: false
- The method worked best for qualitative prediction of how mutations or evolution shift the landscape and well-populated states. ^c3
  - page: 1
  - quote: "Our subsampling approach worked best when used to qualitatively predict the effects of mutations or evolution on the conformational landscape"
  - quote_check: pass
  - reviewed: false
- Earlier work showed that cutting max_seq and extra_seq well below their defaults gives ensemble predictions. ^c4
  - page: 2
  - quote: "a significant reduction in the values of max_seq and extra_seq from their default values achieves ensemble prediction"
  - quote_check: pass
  - reviewed: false
- The predicted ground-state fraction for the ancestral kinase Anc-AS (93%) fell between Src (97%) and Abl1 (89%), matching the experimental order. ^c5
  - page: 4
  - quote: "Anc-AS was predicted to be in the ground state 93% of the time, in-between the frequencies predicted for Src"
  - quote_check: pass
  - reviewed: false
- Low-occupancy states, such as I2 in Src, can be missed entirely. ^c6
  - page: 4
  - quote: "conformations with very low occupancy such as I2 in Src might be missed by the algorithm in its current implementation"
  - quote_check: pass
  - reviewed: false
- It remains to be shown whether the method can predict Boltzmann ratios of states quantitatively. ^c7
  - page: 10
  - quote: "remains to be shown whether it is capable of directly predicting Boltzmann ratios of states quantitatively"
  - quote_check: pass
  - reviewed: false
- For some systems, such as LAT1, the predicted ground-state population depended on the level of subsampling. ^c8
  - page: 10
  - quote: "for which the ground state population was dependent on the level of subsampling"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1 is the strongest published claim that [[MSA subsampling]] yields relative populations. Cite it as their claim, paired with ^c3 and ^c7.
- ^c2, ^c5 are the evidence. It is a correct sign or rank order of population change against NMR and known kinase biochemistry, not a match of absolute populations.
- ^c4 describes the mechanism. Shallower max_seq and extra_seq, plus many seeds and dropout, widen the spread of outputs.
- ^c6, ^c8 are limits on [[sampling coverage]] and on how stable the population estimate is. Rare states are missed, and the estimate moves with the subsampling depth.
- ^c7 is the authors' own statement that a quantitative link to a [[conformational free-energy landscape]] is not established.

## Disagreements / limitations

What is shown is a qualitative match. The direction of population change was right in over 80% of a small set (eight Abl1 mutants plus kinase relatives), and a rank order held for three related kinases. GMCSF was judged on which histidine mutants changed the RMSD distributions most, compared with NMR chemical shift perturbations. GMCSF had no measured populations to compare against. M290L was predicted in the wrong direction, and the double mutants were wrongly ranked (p. 5).

What is asserted goes further. The abstract says "directly predict the relative populations" (^c1), and the discussion speaks of AF2 "decoding information regarding conformational distributions from sequence data alone" (p. 10). The same discussion concedes ^c7. It also says "it remains to understand exactly how AF2 is gathering and interpreting signals about state populations" (p. 10).

The population read-out also depends on choices that are not physical. These are max_seq and extra_seq tuned per protein for maximum diversity, the state-binning thresholds, and the training set. The authors link missed Src I2 to a PDB training set dominated by ground-state structures (p. 4). Aggressive subsampling gave unfolded models with no experimental analogue for GMCSF and AkrB (pp. 7, 10). There is a detection floor between 2% and 6% population (p. 10). Note that [[@wayment-steelePredictingMultipleConformations2024#^c7]] argues the opposite view of what model counts mean.
