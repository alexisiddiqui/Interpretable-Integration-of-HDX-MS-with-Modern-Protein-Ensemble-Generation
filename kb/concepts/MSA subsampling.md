---
type: concept
aliases:
  - MSA-based ensemble generation
  - MSA sub-sampling
  - reduced MSA
  - AF2 subsampling
  - AF2-MSAss
  - SPEACH_AF
  - AlphaFold2-RAVE
notation: []
sources:
  - "[[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c1]]"
  - "[[@steinSPEACH_AFSamplingProtein2022#^c1]]"
  - "[[@steinSPEACH_AFSamplingProtein2022#^c2]]"
  - "[[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c2]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c6]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c7]]"
  - "[[@mccaffertyDoesAlphaFold2Model2023#^c1]]"
  - "[[@zhengMachineLearningGeneration2023#^c5]]"
---

## Definition

MSA subsampling turns a structure predictor into a source of diverse structures by changing its input. AlphaFold2 reads co-evolution from a multiple sequence alignment (MSA). Reducing the MSA increases the conformational diversity of its predictions ([[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c1]]), and mutating the MSA in silico reveals conformations the default MSA does not give ([[@steinSPEACH_AFSamplingProtein2022#^c1]]). Running many such predictions gives a set of candidate structures.

This is different from a generator trained to sample a distribution, such as a [[diffusion model]] or a [[Boltzmann generator]]. The predictor was trained to return one structure per input; the diversity comes from perturbing the input, so there is no defined distribution that the output frequencies estimate (ours).

## Assumptions and limits

- Output frequencies are not populations. They depend on how the MSA was cut or mutated, not on free energies (ours). The same holds for repeated seeds: in AF3 they do not approximate the solution ensemble ([[@abramsonAccurateStructurePrediction2024#^c7]]), and predictors typically return static, PDB-like states ([[@abramsonAccurateStructurePrediction2024#^c6]]).
- Stein et al. read their results as AF2 generating conformations rooted in physical principles ([[@steinSPEACH_AFSamplingProtein2022#^c2]]). That is a claim about which states appear, not how populated they are ([[sampling coverage]]).
- Predictions can be right per domain and wrong about relative domain motion ([[@mccaffertyDoesAlphaFold2Model2023#^c1]]), and sub-sampled ensembles include implausible structures (jaxENT intro L6), hence ValDX's filtered AF2 ensembles.
- The usual use is seeding MD, which adds physics but not populations ([[@vaniAlphaFold2RAVESequenceBoltzmann2023#^c2]], [[@zhengMachineLearningGeneration2023#^c5]]; [[enhanced sampling]]).

## Why it matters here

ValDX's AF2-MSAss and AF2-Filtered ensembles are this method. They test whether HDX-MS can choose between coverage obtained from evolutionary information and coverage from simulation, and why their frame counts are a prior, not populations ([[importance sampling]]).

Claims that use this term: [[Sub-sampling multiple sequence alignments alters the contacts described to the model, leading to diverse structural predictions.]], [[Generating many sub-sampled predictions creates a conformational ensemble that captures the protein's dynamic nature.]], [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]], [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]], [[Learned generators are used to seed MD simulations, combining broad coverage with physics-based sampling.]], [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]].
