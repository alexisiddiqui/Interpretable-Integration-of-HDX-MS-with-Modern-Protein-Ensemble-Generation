---
type: paper
citekey: leeInterpretingHydrogenDeuteriumExchange2021
year: 2021
read: false
pdf: kb/_pdf/@leeInterpretingHydrogenDeuteriumExchange2021.pdf
extraction: auto
needs_review: false
review_reason:
---

# Interpreting Hydrogen-Deuterium Exchange Experiments with Molecular Simulations: Tutorials and Applications of the HDXer Ensemble Reweighting Software [Article v1.0] (2021)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- In HDX-MS the measured local exchange rates are averaged over oligopeptide fragments. ^c1
  - page: 2
  - quote: "averaged over oligopeptide fragments as in the case of HDX-MS data"
  - quote_check: pass
  - reviewed: false
- HDXer reweights the conformational populations in a candidate ensemble, for example from molecular simulations, to conform to experimental exchange data. ^c2
  - page: 1
  - quote: "to objectively reweight the conformational populations present in a candidate ensemble to conform to experimental exchange data"
  - quote_check: pass
  - reviewed: false
- Next-generation HDX studies need to derive objective structural ensembles directly from the measurements, which motivated the development of HDXer. ^c3
  - page: 2
  - quote: "enable high-resolution, quantitative, robust, and objective structural ensembles to be derived directly from the experimental measurements"
  - quote_check: pass
  - reviewed: false
- Using single structures to interpret HDX data underutilizes the information encoded in the measurement. ^c4
  - page: 2
  - quote: "limitation of using single structures to interpret HDX data, however, is that this approach underutilizes the information inherently encoded in the experimental measurement"
  - quote_check: pass
  - reviewed: false
- The connection between deuterium exchange and structural flexibility offers the possibility to interpret HDX data in a structural context. ^c5
  - page: 2
  - quote: "The connection between deuterium exchange and structural flexibility offers the possibility to interpret HDX in a structural context"
  - quote_check: pass
  - reviewed: false
- HDXer is classified as a post-hoc maximum entropy ensemble reweighting method. ^c6
  - page: 5
  - quote: "We classify HDXer itself as a post-hoc maximum entropy ensemble reweighting method"
  - quote_check: pass
  - reviewed: false
- HDXer minimally biases the relative populations of frames in a previously generated candidate structural ensemble. ^c7
  - page: 5
  - quote: "HDXer minimally biases the relative populations of frames in a previously-generated candidate structural ensemble"
  - quote_check: pass
  - reviewed: false
- The HDXer software is a Python 3.7 package. ^c8
  - page: 16
  - quote: "The HDXer software itself is a Python 3.7 package"
  - quote_check: pass
  - reviewed: false
- HDXer's protection factors can be translated into an overall H-D exchange rate and fractional deuteration for peptide segments, allowing direct comparison to HDX-MS data. ^c9
  - page: 3
  - quote: "These values can then be translated into an overall H-D exchange rate and fractional deuteration, for any combination of residues in a peptide segment"
  - quote_check: pass
  - reviewed: false
- HDXer iteratively minimises a distance function that balances the bias applied to the ensemble, quantified as an apparent work, against an error distribution. ^c10
  - page: 9
  - quote: "HDXer iteratively minimizes a distance function that balances the bias applied, quantified across the whole ensemble as an apparent work"
  - quote_check: pass
  - reviewed: false
- BPTI, the tutorial system, is a small, compact globular protein that has been studied extensively, including by HDX. ^c11
  - page: 16
  - quote: "BPTI is a small and compact globular protein and has been studied extensively, including using HDX methodologies"
  - quote_check: pass
  - reviewed: false
- The BPTI exchange data were first measured by NMR as rate constants for individual backbone amides. ^c12
  - page: 17
  - quote: "first reported as observed H-D exchange rate constants for discrete backbone amides, measured by NMR"
  - quote_check: pass
  - reviewed: false
- The tutorial converts the NMR protection factors into residue fractional deuteration, as if the data were HDX-MS. ^c13
  - page: 18
  - quote: "we will further convert the experimental protection factors into fractional deuteration values for each residue, as if the data had been recorded by HDX-MS experiments"
  - quote_check: pass
  - reviewed: false
- The experimental protection factors do not cover every residue of BPTI. ^c14
  - page: 18
  - quote: "the experimental HDX protection factor data for BPTI does not cover every residue in the protein"
  - quote_check: pass
  - reviewed: false
- The candidate ensemble is five 500 ns MD replicas of BPTI in solution. ^c15
  - page: 19
  - quote: "five replica trajectories, each 500 ns long, from five separate simulations of BPTI in solution"
  - quote_check: pass
  - reviewed: false

## What I use from it

## Disagreements / limitations
