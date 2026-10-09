---
type: claim
chapter: 01-introduction
project:
basis: stated
confidence: high
status: supported
origin: milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L30
source_state: current
needs_review: false
review_reason:
figures: []
cites:
  - "[[@varadiAlphaFoldProteinStructure2022#^c1]]"
  - "[[@varadiAlphaFoldProteinStructure2022#^c3]]"
  - "[[@varadiAlphaFoldProteinStructure2022#^c4]]"
  - "[[@varadiAlphaFoldProteinStructure2022#^c5]]"
code: []
---

## Argument

Varadi et al. describe the accuracy and speed of AlphaFold as unprecedented. Their acknowledgements say experimentally determined structures archived in the PDB enabled the training of AlphaFold and that public protein sequence archives (UniProt, BFD, MGnify) supplied the sequence data used for predicting structures.
The scale of these corpora is given on p1 of the same paper: almost 220 million unique protein sequences in UniProt and just over 180,000 structures in the PDB.

## Caveats

Varadi et al. state the corpus sizes but describe the PDB figure as "only" just over 180,000 structures, set against 220 million sequences, so "large" holds clearly for the sequence data and relatively for the structure data. The cited paper is about AlphaFold specifically, so the plural "protein structure models" rests on AlphaFold as the example.
