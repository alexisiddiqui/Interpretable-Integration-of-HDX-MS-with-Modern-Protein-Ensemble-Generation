---
type: concept
aliases:
  - free-energy landscape
  - free-energy landscapes
  - energy landscape
  - energy landscapes
  - conformational landscape
  - conformational landscapes
  - frustration
  - local frustration
notation: []
sources:
  - "[[@parraFrustrationPhysiologyMolecular2025#^c31]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c1]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c13]]"
  - "[[@fisherConstructingEnsemblesIntrinsically2011#^c4]]"
  - "[[@fisherConstructingEnsemblesIntrinsically2011#^c5]]"
  - "[[@fisherConstructingEnsemblesIntrinsically2011#^c1]]"
  - "[[@suttoEffectsOncogenicMutations2013#^c6]]"
---

## Definition

The conformational free-energy landscape gives a protein's free energy as a function of its conformation. Its topography sets the probability of each conformation: basins are the populated states, and barriers between them control how often the protein moves from one to another. Folded proteins have a well-defined global minimum. [[intrinsically disordered protein|Intrinsically disordered proteins]] have relatively flat landscapes and so sample a large, diverse set of conformations. Mutations can reshape the landscape, for example by globally altering it in oncogenic EGFR kinase mutants.

The landscape fixes three things a sampled ensemble can get right or wrong separately: which basins exist (coverage), how deep they are (populations) and how high the barriers between them are (kinetics). See [[sampling coverage]].

## Assumptions and limits

- **Frustration.** The landscape that natural proteins navigate has the form of a rough funnel ([[@parraFrustrationPhysiologyMolecular2025#^c31]]). Even a completely folded protein keeps some conflicting interactions unresolved and remains locally frustrated ([[@parraFrustrationPhysiologyMolecular2025#^c1]]). Local frustration drives interconversion between conformations at the bottom of the landscape ([[@parraFrustrationPhysiologyMolecular2025#^c13]]), which ties it to function and, through mutations, to disease ([[dynamic disease mechanism]]). Parra et al. is a review; cite its primary studies for specific mechanisms.
- **Populations are not barriers.** Reweighting against EX2 data estimates the depth of basins. Barrier heights, and the rates they set, need kinetic evidence ([[conformational kinetics]]).

## Why it matters here

A [[structural ensemble]] is a discrete sample of this landscape, and its weights stand in for the populations of the basins. Mutations and disease states act by reshaping the landscape ([[population shift]]). Both generating structures and reweighting them against [[HDX-MS]] are attempts to recover the landscape's populated regions.

Claims that use this term: [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]], [[Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles.]], [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]], [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]], [[Offline methods adaptively seed new simulations from underexplored regions, sampling efficiently without distorting the landscape.]], [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]].
