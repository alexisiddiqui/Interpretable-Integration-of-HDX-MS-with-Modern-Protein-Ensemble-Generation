---
type: concept
aliases:
  - transition rates
  - transition pathway
  - transition pathways
  - transition order
  - kinetic interpretation
  - causal mechanism
notation: []
sources:
  - "[[@tibertiENCORESoftwareQuantitative2015#^c6]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c3]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c5]]"
  - "[[@lisiAllosteryEnzymeCatalysis2017#^c7]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c10]]"
---

## Definition

Conformational kinetics describes how a protein moves between states, including transition rates, their order and the pathways connecting them. A weighted [[structural ensemble]] describes proposed populations. Its weights alone do not establish transition order, rates or pathways, and comparisons of equilibrium distributions do not capture changes in transition rates ([[@tibertiENCORESoftwareQuantitative2015#^c6]]).

Under EX2, the observed exchange rate combines intrinsic chemistry with the fraction of time an amide is exchange-competent ([[@skinnerProteinHydrogenExchange2012#^c3]]). Slow exchange can therefore reflect a rarely populated opening without that opening itself being slow. Under this regime, labelling time measures accumulated exchange rather than the duration of a conformational motion. Under EX1, the observed rate instead approaches the opening rate ([[@skinnerProteinHydrogenExchange2012#^c5]]; [[Linderstrøm–Lang model]]).

## Assumptions and limits

- **Function can depend on rates as well as states.** In IGPS, activation without large structural rearrangement is driven by millisecond dynamics that propagate the allosteric signal ([[@lisiAllosteryEnzymeCatalysis2017#^c7]]). Nanosecond dynamics do not correlate with catalysis on millisecond to second timescales ([[@parraFrustrationPhysiologyMolecular2025#^c10]]). A population shift alone may then miss the mechanism ([[allostery]], [[population shift]]).
- **What weights can support.** Weighted conformations support statements about which states are occupied and what they look like. They do not on their own establish transition order, rates or causal pathways.
- **Where kinetic evidence comes from.** Trajectories (MD, Markov state models), EX1 exchange or time-resolved experiments. Unrestrained simulations started from fitted states can suggest a pathway, but the evidence for it is the trajectory, not the weights. No source on Markov state models is in the KB yet.

## Why it matters here

Q4 asks for interpretable models that answer mechanistic questions. This note marks how far an ensemble fitted to EX2 data can go towards a mechanism. It also bounds the MoPrP and α-synuclein cases ([[prion protein]], [[alpha-synuclein]]), where the tempting reading is a pathway and the defensible one is a set of occupied states. Chapter 2 §2.5, "Ensemble Comparison and Interpretable Representations" ([[ensemble comparison]]).

Claims that use this term: [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]], [[Ensemble similarity scores compare equilibrium distributions and do not capture changes in dynamics or transition rates.]], [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]].

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L66`; the historical wording comes from this note before revision, and its evidence remains in the linked source notes and manuscript references.

The primary wording states what weights can support without treating every weighted ensemble as an equilibrium distribution. It also places the EX2 condition alongside the interpretation of labelling time.

### Historical wording

> Conformational kinetics describes how a protein moves between states, meaning the rates of transitions, their order, and the pathways that connect states. It is distinct from the populations of those states. A [[structural ensemble]] with weights is an equilibrium distribution, and comparisons between such distributions do not capture changes in dynamics or in the rates of transitions between states ([[@tibertiENCORESoftwareQuantitative2015#^c6]]).
>
> HDX sets the same boundary from the data side. Under EX2, the measured exchange rate is the chemical rate multiplied down by the fraction of time the amide is open ([[@skinnerProteinHydrogenExchange2012#^c3]]). That fraction is an equilibrium quantity. Only in the EX1 case does the exchange rate reach the opening rate itself ([[@skinnerProteinHydrogenExchange2012#^c5]]). Labelling time therefore measures accumulated exchange, not the duration of a conformational motion, and slow exchange can mean a low population of open states rather than slow motion ([[Linderstrøm–Lang model]]).
