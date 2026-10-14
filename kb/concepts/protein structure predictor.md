---
type: concept
aliases:
  - protein structure predictors
  - structure predictor
  - learned structure predictor
  - protein structure model
  - structure prediction
  - AlphaFold
  - AlphaFold2
  - AlphaFold 3
  - ColabFold
notation: []
sources:
  - "[[@jumperHighlyAccurateProtein2021#^c1]]"
  - "[[@jumperHighlyAccurateProtein2021#^c3]]"
  - "[[@jumperHighlyAccurateProtein2021#^c4]]"
  - "[[@jumperHighlyAccurateProtein2021#^c5]]"
  - "[[@jumperHighlyAccurateProtein2021#^c6]]"
  - "[[@jumperHighlyAccurateProtein2021#^c7]]"
  - "[[@jumperHighlyAccurateProtein2021#^c8]]"
  - "[[@mirditaColabFoldMakingProtein2022#^c1]]"
  - "[[@mirditaColabFoldMakingProtein2022#^c2]]"
  - "[[@mirditaColabFoldMakingProtein2022#^c7]]"
  - "[[@mirditaColabFoldMakingProtein2022#^c8]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c6]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c7]]"
  - "[[@wayment-steelePredictingMultipleConformations2024#^c6]]"
  - "[[@yimDiffusionModelsProtein2024#^c8]]"
---

## Definition

A protein structure predictor is a network trained to map a sequence, usually with an alignment of homologues, to one structure. AlphaFold2 takes the sequence and aligned homologous sequences and outputs coordinates for all heavy atoms ([[@jumperHighlyAccurateProtein2021#^c4]]). It was the first method to regularly reach atomic accuracy even when no similar structure is known ([[@jumperHighlyAccurateProtein2021#^c1]]). Its confidence score, pLDDT, reliably predicts the local accuracy of the prediction ([[@jumperHighlyAccurateProtein2021#^c3]]). ColabFold pairs a much faster MSA search with AlphaFold2, at close to 1,000 structures per day on one GPU ([[@mirditaColabFoldMakingProtein2022#^c1]], [[@mirditaColabFoldMakingProtein2022#^c2]]).

The training target sets what the output means. AlphaFold2 is trained on PDB structures ([[@jumperHighlyAccurateProtein2021#^c5]]) to produce the structure most likely to appear in the PDB ([[@jumperHighlyAccurateProtein2021#^c7]]). Those structures capture proteins in their lowest-energy states, although proteins are highly dynamic ([[@yimDiffusionModelsProtein2024#^c8]]). At inference five models are run, and the confidence score picks one ([[@jumperHighlyAccurateProtein2021#^c8]]).

## Assumptions and limits

- **Confidence is not population.** pLDDT measures expected accuracy. It cannot be used as a measure of free energy ([[@wayment-steelePredictingMultipleConformations2024#^c6]]).
- **Diversity is a side effect of the input.** Accuracy drops sharply below about 30 MSA sequences ([[@jumperHighlyAccurateProtein2021#^c6]]). A new seed can pick different MSA cluster centres and give a different structure ([[@mirditaColabFoldMakingProtein2022#^c7]]). Dropout gives an ensemble "for the uncertain parts" ([[@mirditaColabFoldMakingProtein2022#^c8]]), which is model uncertainty, not conformational heterogeneity. Deliberate input changes are [[MSA subsampling]].
- **Seeds do not give the solution ensemble.** AF3 predictions are static, PDB-like states ([[@abramsonAccurateStructurePrediction2024#^c6]]), and repeated seeds do not approximate the solution ensemble ([[@abramsonAccurateStructurePrediction2024#^c7]]).
- **"Statistical potential" is an analogy here.** ValDX writes that AF2 generates structures according to a statistical potential (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L176). AF2 exposes no normalised density, so no [[statistical potential]] can be computed from its output. The phrase describes learned, data-derived preferences, not an energy.
- Jumper et al. say nothing about dynamics or alternative states. A claim that AF2 "cannot predict multiple states" needs later sources (above).

## Why it matters here

Chapter 2, "Learned Structure Predictors and Ensemble Generators". Predictors supply candidate structures, not populations. ValDX's AF2-MSAss and AF2-Filtered ensembles use ColabFold with subsampled MSAs (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L169–172), and the filter removes implausible structures. HDX-MS then tests whether such candidates can be weighted to match experiment ([[sampling coverage]], [[ensemble reweighting]]). Sampling-based generators, such as the [[diffusion model]] and the [[Boltzmann generator]], are different: they are trained to sample a distribution.

Claims that use this term: [[A structure predictor's confidence score measures expected accuracy, not the free energy or population of a conformation.]], [[Structure predictors are trained to return the single structure most likely to appear in the PDB.]], [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]], [[Subsampled AlphaFold2 can predict the direction of population shifts qualitatively, but quantitative Boltzmann ratios have not been shown.]], [[Frequencies of states in MSA-clustered AlphaFold2 predictions reflect family abundance, not Boltzmann weights.]].
