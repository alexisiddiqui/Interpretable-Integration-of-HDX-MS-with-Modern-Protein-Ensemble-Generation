---
type: concept
aliases:
  - structural ensembles
  - conformational ensemble
  - conformational ensembles
notation: []
sources:
  - "[[@bmsb2012ch12#^c3]]"
  - "[[@bmsb2012ch12#^c7]]"
---

## Definition

A structural ensemble is a set of conformations, each with a weight, used to describe a protein that samples more than one state. Experimental observables such as HDX data are averages over such an ensemble, so no single structure is the right comparison object.

A physical ensemble, whose weights are populations, is different from an inferential one, whose spread describes uncertainty. A bundle of structures sampled from a posterior or from repeated structure calculations is the second kind: an NMR bundle "is not an experimentally determined thermodynamic ensemble" ([[@bmsb2012ch12#^c3]], p. 3), and "a probability quantifies our ignorance about a parameter" ([[@bmsb2012ch12#^c7]], p. 5). See [[posterior uncertainty]]. A generator's output is a third kind: samples from its own distribution, which become populations only after reweighting against experiment ([[importance sampling]]).

## Why it matters here

Claims that use this term: [[Interpreting dynamics measurements in structural terms is a grand challenge, as they can be indirect or ensemble-averaged.]], [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]], [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]].
