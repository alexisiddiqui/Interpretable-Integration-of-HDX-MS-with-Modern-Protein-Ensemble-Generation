---
type: paper
citekey: kovtunPINDERProteinInteraction2024
year: 2024
read: false
pdf: kb/_pdf/@kovtunPINDERProteinInteraction2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# PINDER: The Protein Interaction Dataset and Evaluation Resource (2024)

## Main point

PINDER is a dataset of 2.3 million dimeric protein–protein interaction systems from the PDB, with holo, apo and AlphaFold2-predicted monomers paired to each complex and train, validation and test splits built from structural clustering of interfaces. Docking performance measured on leaky test sets is overestimated, and training on the interface-clustered splits generalises better.

## Claims

- PINDER contains 2,319,564 dimeric PPI systems (up to 25 million with augmentation) and 1,955 high-quality test PPIs with interface leakage removed, plus a 180-dimer subset free of leakage against AlphaFold-Multimer's training set. ^c1
  - page: 1
  - quote: "PINDER consists of 2,319,564 dimeric PPI systems (and up to 25 million augmented PPIs) and 1,955 high-quality test PPIs"
  - quote_check: pass
  - reviewed: false
- The dataset includes holo (bound), apo (unbound) and computationally predicted structures, so docking can be tested from unbound or predicted monomers against the holo complex. ^c2
  - page: 1
  - quote: "includes holo (bound), apo (unbound), and computationally predicted structures"
  - quote_check: pass
  - reviewed: false
- PINDER limits train–test leakage by clustering on structure and sequence similarity of interface residues. ^c3
  - page: 1
  - quote: "PINDER mitigates potential leakage between training and test sets by utilizing structure and sequence similarity-based clustering, specifically targeting interface residues"
  - quote_check: pass
  - reviewed: false
- Apo monomers matched by UniProt accession gave a corresponding apo system for 172,577 holo systems and an apo monomer for at least one chain in 335,709 holo systems, drawn from 47,717 unique apo structures. ^c4
  - page: 3
  - quote: "the procedure resulted in pairing 172,577 holo systems with a corresponding apo system and 335,709 holo systems with at least one chain paired"
  - quote_check: pass
  - reviewed: false
- The interface-based split built on structural similarity outperforms a sequence-similarity split; DiffDock-PP trained on the sequence split overestimated performance on a leaky test set and underperformed on a de-leaked one. ^c5
  - page: 1
  - quote: "interface-based splitting method, which uses structural similarity, is superior to the splits obtained using sequence similarity"
  - quote_check: pass
  - reviewed: false
- The benchmark shows that the performance of existing docking models is highly overestimated when they are evaluated on leaky test sets. ^c6
  - page: 1
  - quote: "the performance of existing docking models is highly overestimated when evaluated on leaky test sets"
  - quote_check: pass
  - reviewed: false

## What I use from it

PINDER as an example of leakage-aware splitting by interface structure rather than sequence identity, and of benchmarking from apo and predicted monomers rather than holo structures.

## Disagreements / limitations

A bioRxiv preprint (version of 13 August 2024). Apo pairing covers only a minority of the 2.3 million holo systems.
