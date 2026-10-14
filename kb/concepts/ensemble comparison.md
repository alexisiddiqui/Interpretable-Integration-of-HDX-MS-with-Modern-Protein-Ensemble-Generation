---
type: concept
aliases:
  - ensemble similarity
  - ensemble similarity measures
  - comparing ensembles
  - Jensen–Shannon divergence
  - Jensen-Shannon divergence
  - JSD
  - D_JS
  - harmonic ensemble similarity
  - ENCORE
notation:
  - {symbol: 'D_\text{JS}', meaning: 'Jensen–Shannon divergence between two distributions', units: null}
sources:
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c1]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c2]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c3]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c5]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c6]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c7]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c10]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c1]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c2]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c3]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c5]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c6]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c8]]"
  - "[[@tibertiENCORESoftwareQuantitative2015#^c10]]"
  - "[[@wangProteinConformationGeneration2024#^c9]]"
---

## Definition

Once a state is represented by an ensemble, comparing states means comparing ensembles rather than single conformations ([[@tibertiENCORESoftwareQuantitative2015#^c1]]). An RMSD between ensembles is a poor measure: it is generally non-zero even for two identical ensembles ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c1]]). Comparing estimated probability densities instead tests both whether the same conformations occur and whether they occur with the same frequency ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c2]]).

Each method therefore has two steps. First, derive a probability distribution from each ensemble. Then compare the distributions with a symmetrised Kullback–Leibler divergence ([[@tibertiENCORESoftwareQuantitative2015#^c2]]). ENCORE's three methods differ mainly in the first step ([[@tibertiENCORESoftwareQuantitative2015#^c3]]):
- harmonic: a multivariate normal, using only the first two moments ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c7]]);
- clustering-based: cluster populations ([[clustering]]);
- dimensionality-reduction-based: densities in a projected space.

## Equations

$$ D_\text{JS}(P_A, P_B) = \tfrac12 \left[ D_\text{KL}\!\left(P_A \,\Vert\, M\right) + D_\text{KL}\!\left(P_B \,\Vert\, M\right) \right], \qquad M = \tfrac12 (P_A + P_B) $$
^eq-jsd

Source: [[@lindorff-larsenSimilarityMeasuresProtein2009#^c5]], Eq. (2), p. 2. The source writes $D_{JS}(p_A, p_B)$ with a comma for each KL argument pair; canonical KL is [[Kullback–Leibler divergence#^eq-kl]].

## Assumptions and limits

- **Why JSD rather than KL.** KL is not a true metric ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c3]]). JSD is symmetric and is the square of a metric ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c5]]). It stays defined where one density is zero and the other is not ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c6]]), and with natural logs it lies between 0 and ln 2 ([[@tibertiENCORESoftwareQuantitative2015#^c5]]). In base 2 it lies between 0 and 1, so always state the base. jaxENT's recovery score $100(1-\sqrt{D_\text{JS}})$ reaches 0 only in base 2 ([[Ground-truth recovery (jaxENT)]]).
- **The representation is a modelling choice.** The harmonic score assumes normality, and only approximately normal ensembles may explain why it disagrees with the other scores ([[@tibertiENCORESoftwareQuantitative2015#^c8]]). PCA and MDS assume a linear conformational space ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c10]]), so a projection can hide differences.
- **Equilibrium only.** Changes in dynamics or transition rates are not captured ([[@tibertiENCORESoftwareQuantitative2015#^c6]]). The scores lack a simple geometric meaning and are best read relative to each other ([[@tibertiENCORESoftwareQuantitative2015#^c10]]).
- **Other measures.** Per-residue flexibility (RMSF) and correlated motion are summaries of [[positional covariance]], and the [[Wasserstein distance]] compares distributions using the geometry of the variable. ValDX's constructions from them are in [[Structural comparison metrics (ValDX)]]. ConfDiff uses Jensen–Shannon distance to reference MD as its fidelity metric ([[@wangProteinConformationGeneration2024#^c9]]).
- Comparing two ensembles is not validating either one against experiment. It needs a reference, which is itself a model ([[sampling coverage]]).

## Why it matters here

Chapter 2, "Ensemble Comparison and Interpretable Representations". The thesis compares ensembles at four levels, and each answers a different question.
- **Structural distributions.** PCA of pair distances, per-residue pair-distance [[Wasserstein distance]], RMSF and correlated motion ([[positional covariance]]) ask where two ensembles differ in geometry and fluctuation (ValDX).
- **Populations.** JSD between state or cluster populations asks whether the same states are occupied with the same frequency (jaxENT recovery, [[Ground-truth recovery (jaxENT)]]).
- **Change induced by fitting.** [[Work Done]] and apparent work ([[Kullback–Leibler divergence]]) ask how far fitting moved the ensemble from its prior, which is a different question from how far it is from the truth.
- **Compact representations.** [[clustering]] and rule-based or shape-space states make the result inspectable at a chosen resolution. The [[Kullback–Leibler divergence]] measures change between prior and fitted weights; JSD compares two ensembles symmetrically, so the direction question does not arise.

Claims that use this term: [[Comparing ensembles requires comparing probability distributions over conformations, not single-structure RMSD.]], [[The Jensen–Shannon divergence is a symmetric, bounded measure of ensemble similarity that stays defined where one ensemble has no density.]], [[Dimensionality reduction by PCA or MDS assumes a linear conformational space.]], [[Ensemble similarity scores compare equilibrium distributions and do not capture changes in dynamics or transition rates.]], [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]], [[Agreement of per-residue pair-distance distributions does not establish that two ensembles share the same joint conformational distribution.]].
