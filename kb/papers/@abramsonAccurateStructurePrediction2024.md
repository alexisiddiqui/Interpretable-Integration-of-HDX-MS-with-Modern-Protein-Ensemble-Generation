---
type: paper
citekey: abramsonAccurateStructurePrediction2024
year: 2024
read: false
pdf: kb/_pdf/@abramsonAccurateStructurePrediction2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# Accurate Structure Prediction of Biomolecular Interactions with AlphaFold 3 (2024)

## Main point

AlphaFold 3 replaces AF2's structure module with a diffusion module and predicts complexes of nearly all molecular types in the PDB. The authors state that it still predicts static, PDB-like structures, and that repeated random seeds do not approximate the solution ensemble.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- AlphaFold 3 is a single model that predicts the structure of complexes containing nearly all molecular types in the Protein Data Bank with high accuracy. ^c1
  - page: 1
  - quote: "a model that is capable of high-accuracy prediction of complexes containing nearly all molecular types present in the Protein Data Bank"
  - quote_check: pass
  - reviewed: false
- The introduction of AlphaFold 2 spurred a revolution in modelling the structure of proteins and their interactions. ^c2
  - page: 1
  - quote: "has spurred a revolution in modelling the structure of proteins and their interactions"
  - quote_check: pass
  - reviewed: false
- AlphaFold 3 predicts protein-ligand interactions with far greater accuracy than state-of-the-art docking tools. ^c3
  - page: 1
  - quote: "far greater accuracy for protein–ligand interactions compared with state-of-the-art docking tools"
  - quote_check: pass
  - reviewed: false
- Substantial challenges remain in achieving highly accurate predictions across all interaction types. ^c4
  - page: 7
  - quote: "there are still substantial challenges to achieve highly accurate predictions across all interaction types"
  - quote_check: pass
  - reviewed: false
- AlphaFold 3's diffusion-based training is a generative procedure that produces a distribution of answers. ^c5
  - page: 3
  - quote: "this is a generative training procedure that produces a distribution of answers"
  - quote_check: pass
  - reviewed: false
- Structure prediction models typically predict static PDB-like structures, not the dynamical behaviour of biomolecular systems in solution. ^c6
  - page: 6
  - quote: "typically predict static structures as seen in the PDB, not the dynamical behaviour of biomolecular systems in solution"
  - quote_check: pass
  - reviewed: false
- In AF3, multiple random seeds for the diffusion head or the whole network do not approximate the solution ensemble. ^c7
  - page: 6
  - quote: "multiple random seeds for either the diffusion head or the overall network do not produce an approximation of the solution ensemble"
  - quote_check: pass
  - reviewed: false

## What I use from it

Introduction §1.3: a diffusion-based structure predictor is generative but is not an ensemble sampler (^c5, ^c7). This is the precise limitation to cite in place of "no approaches generate ensembles". See [[diffusion model]], [[MSA subsampling]].

## Disagreements / limitations
