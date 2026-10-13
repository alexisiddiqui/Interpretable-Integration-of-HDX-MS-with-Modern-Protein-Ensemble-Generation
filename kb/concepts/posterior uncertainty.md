---
type: concept
aliases:
  - inferential ensemble
  - posterior ensemble
  - structural uncertainty
  - MAP estimate
  - maximum a posteriori
notation: []
sources:
  - "[[@bmsb2012ch12#^c2]]"
  - "[[@bmsb2012ch12#^c3]]"
  - "[[@bmsb2012ch12#^c4]]"
  - "[[@bmsb2012ch12#^c5]]"
  - "[[@bmsb2012ch12#^c7]]"
  - "[[@bmsb2012ch12#^c6]]"
  - "[[@bmsb2012ch12#^c16]]"
  - "[[@bmsb2012ch1#^c3]]"
  - "[[@bmsb2012ch1#^c5]]"
---

## Definition

Posterior uncertainty is the spread of a posterior distribution over structures or parameters. It measures what the data and prior leave undetermined. It is not the same quantity as the physical heterogeneity of a protein, the spread of conformations it actually populates. A set of structures sampled from a posterior is an *inferential* ensemble: a description of uncertainty. A protein's *physical* ensemble is a set of conformations with populations. An NMR bundle from repeated structure calculations is neither of these. It is not an experimentally determined thermodynamic ensemble, and its spread is not evidence of dynamics.

## Assumptions and limits

- **Probability is about knowledge.** "A probability quantifies our ignorance about a parameter, it does not relate to a physical propensity or fluctuation" ([[@bmsb2012ch12#^c7]], p. 5).
- **NMR bundles.** Standard calculations treat NMR data as instantaneous measurements on a single structure ([[@bmsb2012ch12#^c2]], p. 3), although the data are time- and ensemble-averaged ([[@bmsb2012ch12#^c4]]). The bundle is therefore not a thermodynamic ensemble ([[@bmsb2012ch12#^c3]]). Claims that it reflects dynamics do not follow from how the data were modelled ([[@bmsb2012ch12#^c5]], p. 4).
- **Sampling the posterior.** In Bayesian structure determination, the posterior over structures is represented by sampling an ensemble of structures ([[@bmsb2012ch1#^c3]], p. 4). Such an ensemble shows how precisely the structure is determined.
- **Point estimates.** A MAP or minimum-energy structure finds one optimum but says nothing about its quality ([[@bmsb2012ch12#^c6]], p. 4; [[@bmsb2012ch12#^c16]], p. 13). Point estimates make most sense when the posterior is sharply peaked and unimodal ([[@bmsb2012ch1#^c5]], p. 11).
- **Two layers for ensemble-averaged data** (ours). When the data are ensemble averages, as in HDX-MS, the physical heterogeneity is in the weights $w_j$ of a [[structural ensemble]]. Posterior uncertainty is then a distribution over those weights and over the forward-model parameters. A wide posterior over $w$ means the data do not determine the populations, not that the protein is more dynamic.
- A third quantity is the spread across replicate fits to different data selections. It measures sensitivity to the data chosen; it is neither posterior uncertainty under one model nor physical heterogeneity ([[replicate uncertainty]]).

## Why it matters here

This distinction runs through the thesis argument. It is the caution in introduction §1.1, that an ensemble's spread can reflect incomplete data or the method rather than motion. In §1.5, it is why a good fit does not make the inferred populations uniquely correct. It also shapes how jaxENT reports replicate-based uncertainty: as uncertainty in the populations, not as additional dynamics. The same applies to generators. Diverse samples from a model are not evidence of equilibrium populations ([[importance sampling]], [[Markov chain Monte Carlo]]).

Claims that use this term: [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]], [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]], [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]], [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]].
