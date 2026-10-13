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
---

## Definition

Ensemble reweighting changes the weights (populations) of the conformers in an existing ensemble so that ensemble averages agree better with experimental data, without generating new structures.

Statistically, reweighting is [[importance sampling]]: the conformers are samples of a prior, and the new weights are importance weights towards the posterior ([[@bmsb2012ch2#^c5]], p. 8). It therefore inherits the limits of importance sampling. If the prior covers the posterior poorly, a few conformers take most of the weight and the effective sample size becomes much smaller than the number of conformers ([[@bmsb2012ch2#^c8]], p. 9). The [[maximum entropy principle]] supplies the weights; [[Bayes' theorem]] and [[regularisation]] supply the trade-off between data and prior.

## Why it matters here

Reweighting is how the relative populations of generated states are determined against HDX-MS data, which is the step that turns a set of generated structures into an ensemble that can be tested against experiment in ValDX and JaxENT.

Claims that use this term: [[Ensemble reweighting adjusts structural contributions so proposed conformational states can be tested against experiment.]], [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]].
