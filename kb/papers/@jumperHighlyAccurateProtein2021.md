---
type: paper
citekey: jumperHighlyAccurateProtein2021
year: 2021
read: false
pdf: kb/_pdf/@jumperHighlyAccurateProtein2021.pdf
extraction: auto
needs_review: false
review_reason:
---

# Highly Accurate Protein Structure Prediction with AlphaFold (2021)

## Main point

AlphaFold2 predicts the 3D coordinates of a protein from its sequence and an MSA of homologues. In CASP14 it reached near-experimental accuracy, and its per-residue confidence (pLDDT) tracks the true local accuracy. It is trained on PDB chains and returns the structure most likely to appear in the PDB, with the best of five models picked by confidence. The paper makes no claim about dynamics or alternative states.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- AlphaFold2 is presented as the first method to regularly predict structures with atomic accuracy, even without a similar known structure. ^c1
  - page: 1
  - quote: "the first computational method that can regularly predict protein structures with atomic accuracy even in cases in which no similar structure is known"
  - quote_check: pass
  - reviewed: false
- In CASP14 the median backbone accuracy was 0.96 Å r.m.s.d.95, against 2.8 Å for the next best method. ^c2
  - page: 2
  - quote: "AlphaFold structures had a median backbone accuracy of 0.96 Å r.m.s.d.95"
  - quote_check: pass
  - reviewed: false
- The pLDDT confidence score reliably predicts the lDDT-Cα accuracy of the prediction it comes with. ^c3
  - page: 2
  - quote: "our confidence measure, the predicted local-distance difference test (pLDDT), reliably predicts the Cα local-distance difference test (lDDT-Cα) accuracy"
  - quote_check: pass
  - reviewed: false
- The network takes the sequence and aligned homologous sequences as input and outputs coordinates for all heavy atoms. ^c4
  - page: 3
  - quote: "predicts the 3D coordinates of all heavy atoms for a given protein using the primary amino acid sequence and aligned sequences of homologues as inputs"
  - quote_check: pass
  - reviewed: false
- Training used PDB structures released up to 30 April 2018. ^c5
  - page: 8
  - quote: "To train, we use structures from the PDB with a maximum release date of 30 April 2018"
  - quote_check: pass
  - reviewed: false
- Accuracy falls sharply when the median MSA depth is below about 30 sequences. ^c6
  - page: 6
  - quote: "the accuracy decreases substantially when the median alignment depth is less than around 30 sequences"
  - quote_check: pass
  - reviewed: false
- AlphaFold2 is trained to output the single structure most likely to appear in the PDB. ^c7
  - page: 6
  - quote: "AlphaFold is trained to produce the protein structure most likely to appear as part of a PDB structure"
  - quote_check: pass
  - reviewed: false
- At inference the five trained models are run and the confidence score picks one best model per target. ^c8
  - page: 9
  - quote: "We inference the five trained models and use the predicted confidence score to select the best model per target"
  - quote_check: pass
  - reviewed: false
- The structure module represents each residue's backbone as an independent rotation and translation (the "residue gas"), which encodes the geometry of its N, Cα and C atoms. ^c9
  - page: 4
  - quote: "independent rotations and translations, each with respect to the global frame (residue gas) (Fig. 3e). These rotations and translations—representing the geometry of the N-Cα-C"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c4, ^c5 set out what a [[protein structure predictor]] learns from. It is supervised on static PDB chains and reads coevolution from the MSA.
- ^c1, ^c2 give the accuracy claim, which is accuracy against a deposited structure.
- ^c3 defines pLDDT as a self-estimate of local accuracy. It is not a population or free-energy score (compare [[@wayment-steelePredictingMultipleConformations2024#^c6]]).
- ^c7, ^c8 support the statement that default AlphaFold2 gives one structure per target, not a [[structural ensemble]].
- ^c6 is the depth dependence that [[MSA subsampling]] methods exploit.

## Disagreements / limitations

The paper never discusses dynamics, alternative states or populations. Any claim that AlphaFold2 "cannot" predict multiple conformations must be cited to later work, not to this paper. What it does say (^c7) is that the training target is the most PDB-like structure. That target inherits whatever states were solved and deposited, which the paper does not discuss.

PAE is not described in the main text. The main text names pTM only (Fig. 2d), and PAE sits in the Supplementary Methods. Cite a PAE definition from the supplement or from [[@mirditaColabFoldMakingProtein2022]].

MSA subsampling is already part of training (self-distillation with sub-sampled MSAs) and of the CASP14 ensembling, where cluster centres are drawn at random. Later "subsampling" methods push this existing stochasticity further. They do not add a new physical ingredient.
