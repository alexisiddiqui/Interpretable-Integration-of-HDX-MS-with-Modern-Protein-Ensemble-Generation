---
type: concept
aliases:
  - PrP
  - PrP-C
  - PrP-Sc
  - MoPrP
  - mouse prion protein
notation: []
sources:
  - "[[@biancanielloStructureDynamicsMisfolding2025#^c7]]"
  - "[[@biancanielloStructureDynamicsMisfolding2025#^c5]]"
  - "[[@biancanielloStructureDynamicsMisfolding2025#^c10]]"
  - "[[@sotoProteinMisfoldingAggregation2018#^c6]]"
---

## Definition

The prion protein (PrP) exists in a cellular form, PrP^C, that can misfold into the scrapie fibrillar form, PrP^Sc. That misfolding is associated with the transmissible spongiform encephalopathies, the prion diseases. Conversion passes through intermediate states, which Biancaniello et al. characterised for the pathogenic T183A variant. Its partially misfolded states are thermally accessible, which explains the lack of a lag phase in that mutant's aggregation kinetics. The lack of high-resolution structural information for PrP^Sc has limited understanding of prion strains.

## Why it matters here

PrP is the case study that closes Section 1.1. Both end states can be described, but conversion runs through [[high-energy intermediate|intermediates]], so understanding it needs the whole [[structural ensemble]]. The mouse prion protein (MoPrP) and its partially unfolded forms at pH 4 are also a test system in the jaxENT chapter and appear in the Chapter 5 draft. The same protein therefore links the biological motivation to the results.

The confirmation intro says atomic structures exist for both PrP^C and PrP^Sc. Soto and Pritzkow (2018) describe PrP^Sc as lacking high-resolution structural information. Check which statement is current before using either in the thesis.

In jaxENT, MoPrP at pD 4 tests which partially unfolded states and populations are consistent with HDX-MS, against an HDX-NMR-derived reference (`projects/2-jaxENT/manuscript/report/results.tex` L81–116; manuscript only). The defensible output is a set of occupied states. A conversion pathway needs kinetic evidence ([[conformational kinetics]]). The reference is HDX-NMR-derived and Boltzmann-weighted (`results.tex` L97), so it depends on its own state assignments and thermodynamic assumptions. "Ground-truth recovery" there means agreement with another model, not with exact populations ([[identifiability]]). The figure caption's "misfolding progresses stepwise Folded, PUF1, PUF2" orders states by structural deviation. It is not a measured sequence of transitions.


**Acidic pH.** Lowering the pH destabilises PrP and populates non-native states, which is why MoPrP at pH 4 is a misfolding-promoting condition. Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH ([[Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH, and urea is needed to populate it substantially.]]). In MoPrP the protonation of specific residues, H186 and D201, drives misfolding ([[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]]); the buried His in hamster and rabbit PrP has a lowered pKa ([[@malevanetsInterplayBuriedHistidine2017]]), and constant-pH MD of human PrP links its protonation to subdomain separation ([[Constant-pH MD of human PrP at low pH populates a β-rich form in which His187 protonation separates the subdomains.]]). Use species numbering: mouse H186 is human and hamster H187. This is the thread that ties §2.2 and Chapter 6 to the MoPrP data ([[pKa]], [[pKa shift]]).

Claims that use this term: [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]], [[High-energy intermediates with enhanced conformational heterogeneity precede aggregation but resist crystallization.]], [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]], [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]], [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]].
