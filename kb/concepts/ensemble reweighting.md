---
type: concept
aliases:
  - reweighting
  - ensemble refinement
  - reweighted ensemble
notation: []
sources:
  - "[[@bmsb2012ch2#^c5]]"
  - "[[@bmsb2012ch2#^c8]]"
  - "[[@leeInterpretingHydrogenDeuteriumExchange2021#^c7]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c4]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c2]]"
  - "[[@bradshawInterpretationHDXData2020#^c2]]"
  - "[[@bradshawInterpretationHDXData2020#^c13]]"
---

## Definition

Ensemble reweighting changes the weights (populations) of the conformers in an existing ensemble so that ensemble averages agree better with experimental data, without generating new structures.

Statistically, reweighting is [[importance sampling]]: the conformers are samples of a prior, and the new weights are importance weights towards the posterior ([[@bmsb2012ch2#^c5]], p. 8). It therefore inherits the limits of importance sampling. If the prior covers the posterior poorly, a few conformers take most of the weight and the effective sample size becomes much smaller than the number of conformers ([[@bmsb2012ch2#^c8]], p. 9). The [[maximum entropy principle]] supplies the weights; [[Bayes' theorem]] and [[regularisation]] supply the trade-off between data and prior.

## Assumptions and limits

- It cannot create states. HDXer biases the populations of frames in a previously generated candidate ensemble ([[@leeInterpretingHydrogenDeuteriumExchange2021#^c7]]); a missing state needs more sampling ([[sampling coverage]]).
- Extra candidates are not harmless. Plausible but unpopulated structures can absorb weight and prevent population recovery even when uptake matches ([[@siddiquiFrameworkTestingStructural2026#^c4]]).
- Weights compensate for forward-model error. If the [[forward model]] or its coefficients are wrong ([[@bradshawInterpretationHDXData2020#^c13]]), the fit moves weights to make up for it ([[model misspecification]]).
- A good fit is not proof of correct populations ([[@siddiquiFrameworkTestingStructural2026#^c2]]; [[overfitting]]). What a fit can do is rank candidate ensembles against the data or reveal them as inadequate ([[@bradshawInterpretationHDXData2020#^c2]]).

## Why it matters here

Reweighting is how the relative populations of generated states are determined against HDX-MS data, which is the step that turns a set of generated structures into an ensemble that can be tested against experiment in ValDX and JaxENT.

Claims that use this term: [[Ensemble reweighting adjusts structural contributions so proposed conformational states can be tested against experiment.]], [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]], [[Reweighting cannot create conformational states absent from the candidate ensemble.]], [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]], [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]].
