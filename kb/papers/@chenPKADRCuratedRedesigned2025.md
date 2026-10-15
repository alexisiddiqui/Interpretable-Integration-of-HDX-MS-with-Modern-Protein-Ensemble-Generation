---
type: paper
citekey: chenPKADRCuratedRedesigned2025
year: 2025
read: false
pdf: kb/_pdf/@chenPKADRCuratedRedesigned2025.pdf
extraction: auto
needs_review: false
review_reason:
---

# PKAD-R: Curated, Redesigned and Expanded Database of Experimental pKa Values in Proteins (2025)

## Main point

PKAD-R rebuilds PKAD-2 by removing erroneous entries, correcting mismatched structures, choosing one representative ("Main") pKa and PDB structure per unique residue, adding sequence-identity information and 214 new literature entries. It currently holds 877 unique wild-type and 147 mutant pKa entries, arranged so that machine-learning users can remove redundancy.

## Claims

- PKAD-R is a curated database of experimentally determined protein pKa values that builds on PKAD and PKAD-2 through curation, redesign and expansion. ^c1
  - page: 1
  - quote: "We present a new version of PKAD, named PKAD-R, which is a curated database of experimentally determined protein pKa values."
  - quote_check: pass
  - reviewed: false
- It currently contains 877 unique pKa entries for wild-type structures and 147 for mutant structures, after adding 214 new (128 non-redundant) entries from the literature. ^c2
  - page: 1
  - quote: "The database currently contains 877 unique pKa entries for wild type structures and 147 for mutant structures"
  - quote_check: pass
  - reviewed: false
- Curation removed duplicates, entries based on calculated rather than measured pKa values, entries whose pKa was absent from the cited literature, and pKa values that could not be assigned to a specific residue. ^c3
  - page: 4
  - quote: "These included: duplicates, entries based on calculated rather than experimentally determined pKa values, entries where the pKa was absent in the original literature"
  - quote_check: pass
  - reviewed: false
- In 187 entries the mutations in the PDB structure did not match the protein used for the measurement; 46 were reassigned to the correct PDB and the other 141 were excluded to a separate list. ^c4
  - page: 4
  - quote: "187 entries were identified in which the mutations in the PDB structures did not match those in the structures used for their pKa measurements"
  - quote_check: pass
  - reviewed: false
- For each unique residue a single "Main" entry was chosen, preferring NMR-measured values (13C over 1H) obtained under moderate conditions of about 298 K and 0.1 M salt; other values are kept as alternative entries. ^c5
  - page: 5
  - quote: "Values obtained under moderate experimental conditions, typically around 298 K and 0.1 M salt concentration, were prioritized."
  - quote_check: pass
  - reviewed: false
- Sequence identity is computed for all entries so that machine-learning users can keep entries at a 30% or 90% similarity threshold and avoid train–test overlap. ^c6
  - page: 4
  - quote: "a user can choose a threshold at which they want to keep pKa entries (30% similar or 90% similar)"
  - quote_check: pass
  - reviewed: false

## What I use from it

PKAD-R as the cleaned experimental pKa reference, and its list of errors in PKAD-2 (calculated values, mismatched mutant structures, duplicates) as a reason to treat older experimental test sets with care.

## Disagreements / limitations

Choosing one "Main" value per residue is a manual, case-by-case judgement; 213 pKa values without a suitable PDB structure are held in a separate list.
