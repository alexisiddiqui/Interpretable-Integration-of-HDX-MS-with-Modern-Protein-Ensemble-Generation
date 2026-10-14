---
type: concept
aliases:
  - foldon
  - foldons
  - cooperative unit
  - cooperative units
  - subglobal unfolding
  - cooperative substructure
notation: []
sources:
  - "[[@englanderHydrogenExchangeModern1997#^c6]]"
  - "[[@englanderHydrogenExchangeModern1997#^c7]]"
  - "[[@englanderHydrogenExchangeModern1997#^c4]]"
  - "[[@englanderHydrogenExchangeModern1997#^c3]]"
  - "[[@moulickPartiallyUnfoldedForms2015#^c1]]"
  - "[[@moulickPartiallyUnfoldedForms2015#^c2]]"
---

## Definition

A cooperative unfolding unit is a group of residues that unfolds together in one equilibrium opening reaction, so that their amides exchange through the same high-energy state. Native proteins are composed of such units, and they are smaller than the whole protein ([[@englanderHydrogenExchangeModern1997#^c6]]). Native-state hydrogen exchange identifies them because all the amides of a unit share one unfolding isotherm ([[@englanderHydrogenExchangeModern1997#^c4]]). A unit can join segments that are far apart in sequence. In cytochrome c the N- and C-terminal helices lie on the global unfolding isotherm together ([[@englanderHydrogenExchangeModern1997#^c7]]). In the mouse prion protein at pH 4, segments of both β-strands and all three helices exchange through subglobal unfolding events of different extent, and the data are modelled as the native state in equilibrium with at least two partially unfolded forms ([[@moulickPartiallyUnfoldedForms2015#^c1]], [[@moulickPartiallyUnfoldedForms2015#^c2]]). The later term foldon comes from work after 1997 and is not needed for the argument here. The partially unfolded forms themselves are [[high-energy intermediate|high-energy intermediates]].

## Assumptions and limits

- Under EX2 a unit is a thermodynamic grouping, residues whose opening free energies move together with denaturant. The grouping does not show the order or mechanism of unfolding ([[Linderstrøm–Lang model]], [[conformational kinetics]]).
- Which units are open in a given high-energy state can be ambiguous from exchange data alone ([[@englanderHydrogenExchangeModern1997#^c3]]).
- Units are identified at residue resolution by NMR. Peptide-level HDX-MS averages over them ([[deuterium uptake]]).

## Why it matters here

Shared openings couple exchange at residues that no peptide shares. Two peptides from different parts of the sequence can therefore report the same opening reaction. Removing peptide overlap between training and validation sets removes the direct route of dependence and leaves this one in place, which is why structured [[data splitting]] reduces dependence without guaranteeing independence (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L52). For MoPrP the units are known from the HDX-NMR study that also supplies jaxENT's reference populations ([[prion protein]]).

Claims that use this term: [[Native proteins contain cooperative unfolding units smaller than the whole protein, which hydrogen exchange can identify.]], [[Cooperative unfolding couples exchange at residues that share no peptide, so removing peptide overlap does not make training and validation peptides independent.]], [[Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.]].
