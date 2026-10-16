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

A structural ensemble is a set of conformations with weights specifying how much each contributes to a prediction. When those weights represent physical populations, the ensemble describes which states a protein occupies under stated conditions. A proposed weighted ensemble is a structural hypothesis whose populations require assessment ([[sampling coverage]]).

Physical populations and uncertainty about them are different quantities. A posterior over ensemble weights describes uncertainty in the inferred populations ([[posterior uncertainty]]; [[@bmsb2012ch12#^c7]]). Structures returned by conventional NMR structure calculations are solutions to a structure-determination problem and are not, by construction, a thermodynamic ensemble ([[@bmsb2012ch12#^c3]]). Their spread does not establish physical populations.

A generator's output frequencies define a reference distribution. Whether they approximate physical populations depends on the sampling method, its target and its convergence. Reweighting can adjust the contributions of sampled conformations against experiment, but fitted weights remain population estimates under the chosen candidates and [[forward model]] ([[ensemble reweighting]], [[importance sampling]]).

## Why it matters here

Its weights describe proposed conformational populations. The order, rates and pathways of transitions require kinetic evidence ([[conformational kinetics]]). Representative structures make a large ensemble inspectable ([[clustering]]).


Claims that use this term: [[Interpreting dynamics measurements in structural terms is a grand challenge, as they can be indirect or ensemble-averaged.]], [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]], [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]].

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L193`; the historical wording comes from this note before revision, and its evidence remains in the linked source notes and manuscript references.

The primary wording separates a proposed weighted ensemble, physical populations and uncertainty about those populations. Generated frequencies need assessment; experimental reweighting is one route to that assessment, rather than a prerequisite for every physical ensemble.

### Historical wording

> A structural ensemble is a set of conformations, each with a weight, used to describe a protein that samples more than one state. Experimental observables such as HDX data are averages over such an ensemble, so no single structure is the right comparison object.
>
> A physical ensemble, whose weights are populations, is different from an inferential one, whose spread describes uncertainty. A bundle of structures sampled from a posterior or from repeated structure calculations is the second kind: an NMR bundle "is not an experimentally determined thermodynamic ensemble" ([[@bmsb2012ch12#^c3]], p. 3), and "a probability quantifies our ignorance about a parameter" ([[@bmsb2012ch12#^c7]], p. 5). See [[posterior uncertainty]]. A generator's output is a third kind: samples from its own distribution, which become populations only after reweighting against experiment ([[importance sampling]]). A generated ensemble's coverage can be judged from its members, but its weights mean populations only if the sampling distribution is defined ([[sampling coverage]]).

> Its weights say which states are occupied and how much. They carry no information about the order or rates of transitions ([[conformational kinetics]]). Representative structures make a large ensemble inspectable ([[clustering]]).
