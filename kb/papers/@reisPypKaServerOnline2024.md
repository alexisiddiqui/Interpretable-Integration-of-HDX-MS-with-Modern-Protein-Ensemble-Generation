---
type: paper
citekey: reisPypKaServerOnline2024
year: 2024
read: false
pdf: kb/_pdf/@reisPypKaServerOnline2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# PypKa Server: Online pKa Predictions and Biomolecular Structure Preparation with Precomputed Data from PDB and AlphaFold DB (2024)

## Main point

The PypKa server runs the physics-based PypKa predictor, or the ML models pKAI and pKAI+ for large systems, to return pKa values, titration curves and force-field-ready structures with pH-dependent protonation states. Results for over 200k PDB and AlphaFold DB structures are precomputed in pKPDB and can be retrieved without new calculations.

## Claims

- The server runs physics-based and ML-accelerated methods to obtain pKa values, isoelectric points, titration curves and structures with representative pH-dependent protonation states for AMBER, CHARMM and GROMOS. ^c1
  - page: 1
  - quote: "we present the PypKa server, which allows users to run physics-based, as well as ML-accelerated methods suitable for larger systems"
  - quote_check: pass
  - reviewed: false
- Results for over 200k structures from the PDB and the AlphaFold DB are precomputed and retrievable without extra calculation. ^c2
  - page: 1
  - quote: "The results for over 200k structures taken from the Protein Data Bank and the AlphaFold DB have been precomputed"
  - quote_check: pass
  - reviewed: false
- The pKPDB database has been extended with more than 100k AlphaFold DB structures from model-organism and global-health proteomes, giving over 200k structures and 20M pKa values in total. ^c3
  - page: 2
  - quote: "continuously adding more proteomes to the over 200k structures and 20M pKa values available currently"
  - quote_check: pass
  - reviewed: false
- pKAI is an ML model trained to reproduce PypKa predictions at much lower cost, and the server uses it by default for structures above 1500 residues. ^c4
  - page: 3
  - quote: "pKAI is an ML model trained to reproduce PypKa predictions at a much lower computational cost."
  - quote_check: pass
  - reviewed: false
- pKAI+ penalises large pKa shifts to offset the use of a single structure; it gives smaller errors against experimental pKa values, but pKAI and PypKa are better at choosing the representative protonation state at physiological pH. ^c5
  - page: 3
  - quote: "while pKAI+ yields a smaller error compared to pKAI or PypKa at predicting experimental pKa values, the latter methods perform better"
  - quote_check: pass
  - reviewed: false

## What I use from it

The source for precomputed PypKa pKa values on PDB and AlphaFold DB structures (pKPDB) and for the pKAI versus pKAI+ trade-off between experimental pKa error and protonation-state assignment.

## Disagreements / limitations

pKAI titration curves and protonation states are approximated from its predicted pKa values, whereas PypKa obtains them from Monte Carlo sampling; all predictions use a single static structure.
