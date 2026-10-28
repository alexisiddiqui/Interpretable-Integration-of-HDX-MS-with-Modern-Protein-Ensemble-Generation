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

The prion protein (PrP) exists in a cellular form, PrP^C, that can misfold into the scrapie fibrillar form, PrP^Sc. That misfolding is associated with the transmissible spongiform encephalopathies, the prion diseases. Conversion passes through intermediate states, which Biancaniello et al. characterised for the pathogenic T183A variant. Its partially misfolded states are thermally accessible, which explains the lack of a lag phase in that mutant's aggregation kinetics. The historical lack of high-resolution structural information for PrP^Sc limited understanding of prion strains; the current structural framing is given below.

## Why it matters here

Prions do two jobs in Section 1.1. The early example connects partially unfolded states to disease and conformational memory, before local frustration supplies the general folding–function explanation (`thesis/chapters/01-introduction.tex` L65–88). PrP returns among the disease cases to establish how solution conditions govern intermediate populations (L130). Both end states can be described, but conversion runs through [[high-energy intermediate|intermediates]], so understanding it needs the whole [[structural ensemble]]. MoPrP and its partially unfolded forms at pH 4 are also a test system in jaxENT and appear in Chapter 5. The same protein links the biological motivation to the results.

Conformational memory connects a protein's state to its history. [[At pH 4 the mouse prion protein folds along a pathway distinct from its unfolding pathway, so its kinetics depend on initial conditions.]] This is the kinetic basis of the thesis's memory interpretation ([[Because folding and unfolding follow distinct pathways at pH 4, the prion landscape can retain the history of the condition applied, which reads as a form of memory.]]). The memristor analogy explains that memory through condition-dependent switching between states. Its device-physics component is [[The crossing point of two potential-energy curves sets the barrier to a charge transition in an oxide defect.]].

The biological memory sources address complementary systems. [[Prions can encode and transmit an epigenetic record of a protein's life history between cells and individuals.]] records the yeast non-amyloid prion work. [[Prion-like proteins are proposed to act as memory molecules by turning transient environmental signals into persistent conformational states.]] concerns plant memory, while [[The cellular prion protein is proposed to contribute to memory formation and long-term memory.]] records the PrP review. These links give the early introduction its functional context.

Atomic structures exist for both PrP^C and PrP^Sc, while the intervening conformational landscape remains unresolved (`milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex` L45–49). Soto and Pritzkow’s 2018 account records the earlier structural limitation.

In jaxENT, MoPrP at pD 4 tests which partially unfolded states and populations are consistent with HDX-MS, against an HDX-NMR-derived reference (`projects/2-jaxENT/manuscript/report/results.tex` L81–116; manuscript only). The defensible output is a set of occupied states. A conversion pathway needs kinetic evidence ([[conformational kinetics]]). The reference is HDX-NMR-derived and Boltzmann-weighted (`results.tex` L97), so it depends on its own state assignments and thermodynamic assumptions. "Ground-truth recovery" there means agreement with another model, not with exact populations ([[identifiability]]). The figure caption's "misfolding progresses stepwise Folded, PUF1, PUF2" orders states by structural deviation. It is not a measured sequence of transitions.


**Acidic pH.** Lowering the pH destabilises PrP and populates non-native states, which is why MoPrP at pH 4 is a misfolding-promoting condition. Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH ([[Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH, and urea is needed to populate it substantially.]]). In MoPrP the protonation of specific residues, H186 and D201, drives misfolding ([[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]]); the buried His in hamster and rabbit PrP has a lowered pKa ([[@malevanetsInterplayBuriedHistidine2017]]), and constant-pH MD of human PrP links its protonation to subdomain separation ([[Constant-pH MD of human PrP at low pH populates a β-rich form in which His187 protonation separates the subdomains.]]). Use species numbering: mouse H186 is human and hamster H187. This is the thread that ties §2.2 and Chapter 6 to the MoPrP data ([[pKa]], [[pKa shift]]).

Claims that use this term: [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]], [[High-energy intermediates with enhanced conformational heterogeneity precede aggregation but resist crystallization.]], [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]], [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]], [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]].

## Wording history

Historical formulation in this concept's Definition: "The lack of high-resolution structural information for PrP^Sc has limited understanding of prion strains." This described the limitation recorded by Soto and Pritzkow (2018). The current wording places that limitation in the past and uses the checked confirmation introduction (`milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex` L45–49) for the resolved endpoints and unresolved conversion landscape.
