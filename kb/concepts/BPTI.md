---
type: concept
aliases:
  - bovine pancreatic trypsin inhibitor
  - aprotinin
notation: []
sources:
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c11]]"
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c12]]"
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c13]]"
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c14]]"
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c15]]"
---

## Definition

Bovine pancreatic trypsin inhibitor (BPTI) is a small, compact globular protein that has been studied extensively, including by hydrogen exchange ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c11]]). Its exchange data were measured by NMR as rate constants for individual backbone amides ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c12]]), so they are residue-level [[protection factor|protection factors]] rather than peptide uptake. They do not cover every residue ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c14]]). The HDXer tutorial converts them into residue fractional deuteration as if they had been recorded by HDX-MS ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c13]]) and reweights five 500 ns MD replicas against them ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c15]]).

## Assumptions and limits

- **Residue-level, NMR-derived.** Converted uptake is not measured peptide uptake. There is no peptide overlap to leak between splits, although exchange at neighbouring residues can still be correlated through shared structure ([[data splitting]]).
- **Small and folded.** BPTI tests whether a method recovers local, rare opening in a stable fold. It says little about disordered or multidomain systems.
- **gap.** Kim et al. 1993, the native-state HX study of BPTI, is in the bib but has no PDF, so no block from it supports this note.

## Why it matters here

BPTI appears in three chapters, each asking a different question of the same protein.
- ValDX (ch. 3) compares AF2-Filtered and MD-1Start ensembles under global and local splits. AF2 MSA subsampling captures a rare hairpin-opening state, and Work Done asks whether the candidates represent local opening differently at similar uptake agreement (`projects/1-ValDX/manuscript/report/7_results_omc.tex` L68–93; NMR conversion in `6_methods_omc.tex` L36–52). Manuscript pointer, not evidence.
- BioFeaturisers (ch. 5) restrains sampling against the 1 ms Anton trajectory as a controlled reference.
- Lee et al. use it as the HDXer reference system, which is why it is a convenient common benchmark.

Claims that use this term: [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]].
