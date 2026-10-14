---
type: concept
aliases:
  - consensus
  - consensus fitting
  - consensus fit
  - replicate averaging
  - parameter averaging
  - bagging
  - bootstrap aggregation
notation: []
sources:
  - "[[@bmsb2012ch13#^c7]]"
---

## Definition

Model averaging fits one procedure to several resamples or partitions of the data and then averages the fitted predictions or parameters. Each single fit depends on which observations it saw. The average depends less on any one of them, so the variance of the result falls, and it falls most where single fits are unstable. Error that every fit shares, because every fit uses the same prior, the same forward model and the same candidate structures, is left where it was. The general source for this statement is standard statistical learning, which the vault does not yet hold (see Gaps in [[02-background]]).

The Bayesian cousin is averaging over hyperparameters, which gives an error estimate for the quantity of interest ([[@bmsb2012ch13#^c7]]). It integrates over the posterior of a parameter. Averaging over data partitions integrates over the choice of data. The two are related operations with different objects.

## Derivation

The bridging upshot for ensemble reweighting is that averaging weights is not always the same as averaging predictions (steps ours).

1. The ensemble-average log protection factor is linear in the weights, $\langle \ln P_f\rangle_w = \sum_j w_j \ln P_{f}(j)$ ([[Best–Vendruscolo model#^eq-bv-ensemble]]). Averaging the weight vectors of several fits therefore averages their predicted profiles, provided the Best–Vendruscolo coefficients are held fixed.
2. With the coefficients also fitted, the prediction is bilinear in weights and coefficients. The mean of the products differs from the product of the means by the covariance of weights and coefficients across fits. Compensation between weights and coefficients makes that covariance non-zero ([[model misspecification]]), so a consensus formed by averaging each separately is not the average prediction.
3. Peptide uptake is non-linear in the rates ([[deuterium uptake#^eq-uptake-residue]]). Averaging weights averages uptake only approximately, and the choice of what is averaged over frames is itself a forward-model choice ([[Evaluation design (jaxENT)]]).
4. The mean of weight vectors on the simplex stays on the simplex, so a consensus weight vector is a valid prior for a next stage.

## Assumptions and limits

- Report the spread before the average. The spread is the partition sensitivity ([[replicate uncertainty]]); the average is the estimate.
- Staged replicates are not independent. When each replicate of a later stage starts from the consensus of the earlier stage, their spread measures sensitivity to partitioning, not independent replication (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L693).
- Three averages share one word in this thesis. Ensemble averages are over conformations, replica averages are over simulated copies ([[restrained simulation]]), and model averages are over fits. Say which one is meant.
- Averaging cannot add a state that no fit contained ([[sampling coverage]]).

## In integrative practice

Ensemble refinement usually reports one fit at one fitting strength. Replicate fits, where they appear, are shown as a spread rather than combined into a consensus.

## Why it matters here

ValDX forms the consensus for a staged protocol by taking the arithmetic mean of frame weights and Best–Vendruscolo coefficients across split replicates, and uses it as the prior for the next stage (`6_methods_omc.tex` L659, L672; [[Peptide splitting and consensus (ValDX)]]). The results text says that averaging across replicate fits improves stability and reduces overfitting to any particular peptide subset (`7_results_omc.tex` L60). No figure in the manuscript compares the consensus with single-replicate fits, so the thesis states the principle from the general source and the ValDX consensus as the application. jaxENT selects one model per replicate and does not average ([[Evaluation design (jaxENT)]]).

Claims that use this term: [[Averaging models fitted to different subsets of the data reduces variance due to data selection, most for unstable fitting procedures.]], [[Averaging fitted models reduces their variance but retains any error they share.]], [[Averaging frame weights across fits averages their predicted log protection factors only while forward-model coefficients are held fixed.]], [[Averaging reweighting fits across split replicates stabilises the consensus and reduces overfitting to particular peptide subsets.]], [[A consensus over split replicates does not by itself make the candidate ensemble representative.]].
