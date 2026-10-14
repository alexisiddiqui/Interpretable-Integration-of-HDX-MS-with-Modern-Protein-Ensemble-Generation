---
type: concept
aliases:
  - α-synuclein
  - a-synuclein
  - aSyn
  - αSN
notation: []
sources:
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c7]]"
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c5]]"
  - "[[@ahmedRefinementASynucleinEnsembles2021#^c6]]"
  - "[[@mukherjeeProteinMisfoldingAmyloid2024#^c6]]"
  - "[[@mukherjeeProteinMisfoldingAmyloid2024#^c7]]"
---

## Definition

α-Synuclein is an [[intrinsically disordered protein]] expressed mainly in the brain. As a monomer it is disordered and populates multiple conformational states. Its aggregation into amyloid fibrils is linked to Parkinson's disease and dementia with Lewy bodies. An electrostatic interaction between its N- and C-termini gives an autoinhibitory conformation that shields the aggregation-prone NAC domain from exposure. Disrupting that conformation exposes NAC and is likely to lower the nucleation barrier.

## Why it matters here

In Section 1.1, α-synuclein is the case where dynamics hide in plain sight. The fibril has an atomic structure, but the protective solution state is a disordered [[structural ensemble]] held together by transient contacts. Only an ensemble description, constrained by solution data, can represent the state whose loss starts [[protein misfolding and aggregation|aggregation]].

The confirmation intro describes the protective contact as being between the C-terminus and the hydrophobic centre. The checked source (Mukherjee et al.) describes an N- to C-terminal interaction that protects NAC. Use the source's wording.

In jaxENT, α-synuclein in Tris buffer asks whether C-tail protection is better explained by compaction, by buffer binding or by both, and whether NAC exposure persists among the fitted conformations (`projects/2-jaxENT/manuscript/report/results.tex` L166–211, L282–284; manuscript only). That reading stays a hypothesis, bounded by sampling of a disordered protein and by how well the forward model suits it ([[sampling coverage]], [[forward model]]).


Claims that use this term: [[Alpha-synuclein is an unfolded monomer, yet cryo-EM has solved its Lewy body fibril structures at atomic resolution.]], [[Cryo-EM fibrils are helical but the solution state is disordered, so aggregation-prone states can escape standard methods.]], [[Soluble alpha-synuclein stays compact through transient long-range contacts between its charged C-terminus and hydrophobic centre.]], [[Conformational heterogeneity from pathogenic mutations fundamentally alters alpha-synuclein's protective intramolecular interactions.]], [[NMR showed protective picosecond intramolecular interactions in soluble alpha-synuclein, whose disruption starts aggregation.]].
