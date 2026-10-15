---
type: paper
citekey: reisPKPDBProteinData2022
year: 2022
read: false
pdf: kb/_pdf/@reisPKPDBProteinData2022.pdf
extraction: auto
needs_review: false
review_reason:
---

# pKPDB: A Protein Data Bank Extension Database of pKa and pI Theoretical Values (2022)

## Main point

pKPDB is a database of about 12.5 million theoretical pKa values (and pI values) computed with PypKa at default settings over roughly 120k PDB structures. The authors present it as a precomputed resource that covers environments, such as buried residues, that experiments under-sample.

## Claims

- pKPDB is a database of theoretical pKa values computed over the structures in the PDB. ^c1
  - page: 1
  - quote: "pKPDB is a database of theoretical pKa values calculated over the structures found in the PDB"
  - quote_check: pass
  - reviewed: false
- At publication it held about 12.5 million pKa values from 120k protein structures. ^c2
  - page: 1
  - quote: "At the moment, it is comprised of about 12.5 million pKa values estimated from 120k protein structures"
  - quote_check: pass
  - reviewed: false
- The pKa and pI values were computed with PypKa at its default parameters. ^c3
  - page: 2
  - quote: "In order to calculate pKa and pI values PypKa was used with default parameters"
  - quote_check: pass
  - reviewed: false
- The database does not yet include protein–nucleic acid complexes. ^c4
  - page: 2
  - quote: "The database does not yet include structures with complexes of protein and nucleic acids"
  - quote_check: pass
  - reviewed: false
- The authors argue the database adds information on buried residues, which are under-represented among experimental measurements. ^c5
  - page: 1
  - quote: "can also provide crucial information regarding buried residues that are under-represented in experimental measurements"
  - quote_check: pass
  - reviewed: false
- The authors expect pKPDB predictions to be about as accurate as PypKa was on its published benchmark. ^c6
  - page: 2
  - quote: "thus, the predictions featured in pKPDB should have a comparable accuracy"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1–^c3 define the jax-Ka pretraining labels: PypKa pKas across the PDB, so the model learns PB/MC behaviour, not experiment.
- ^c5 is the case for computed labels (coverage of buried residues); ^c6 means label error is inherited from PypKa ([[@reisPypKaFlexiblePython2020#^c4]]).

## Disagreements / limitations
