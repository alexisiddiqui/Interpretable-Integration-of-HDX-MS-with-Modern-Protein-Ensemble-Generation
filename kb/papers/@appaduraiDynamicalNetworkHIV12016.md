---
type: paper
citekey: appaduraiDynamicalNetworkHIV12016
year: 2016
read: false
pdf: kb/_pdf/@appaduraiDynamicalNetworkHIV12016.pdf
extraction: auto
needs_review: false
review_reason:
---

# Dynamical Network of HIV-1 Protease Mutants Reveals the Mechanism of Drug Resistance and Unhindered Activity (2016)

## Main point

MD and network analysis of HIV-1 protease mutants suggest that non-active-site resistance mutations act through opening of the flaps, communicated to the active site through residue networks that are more indirect in the mutants.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- MD simulations suggest that secondary resistance mutations in HIV-1 protease act mainly through opening of the flaps. ^c1
  - page: 1
  - quote: "Results from molecular dynamics simulations suggest that the primary mechanism of drug resistance of the secondary mutations involves opening"
  - quote_check: pass
  - reviewed: false
- The dynamic cross-correlation map was computed from the MD trajectories with CPPTRAJ. ^c2
  - page: 2
  - quote: "Trajectory analysis of B factors, distances, and the dynamic cross-correlation map (DCCM) was performed"
  - quote_check: pass
  - reviewed: false
- Dynamic cross-correlation analysis attributed the change in flexibility to decoupled motions of the active site and other regions. ^c3
  - page: 5
  - quote: "Dynamic cross-correlation analysis revealed that this was due to the decoupling of the motions of the active site"
  - quote_check: pass
  - reviewed: false
- Negative or weak correlation is read as opposite or independent motion of the two regions. ^c4
  - page: 5
  - quote: "negative or weak correlation implies opposite or independent motions of the two"
  - quote_check: pass
  - reviewed: false

## What I use from it

An applied example of a dynamic cross-correlation map used to read coupling and decoupling between regions ([[positional covariance]], [[allostery]]).

## Disagreements / limitations

Correlation maps are read as communication paths. That reading is an interpretation of equilibrium fluctuations, not a measured pathway ([[conformational kinetics]]).
