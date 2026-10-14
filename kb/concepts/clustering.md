---
type: concept
aliases:
  - conformational clustering
  - representative structures
  - cluster size
  - clustering-based comparison
notation: []
sources:
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c8]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c9]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c13]]"
---

## Definition

Clustering groups the structures of an ensemble by similarity and replaces each group with a representative and its population. It serves two purposes. In interpretation, it gives compact ensembles that can be inspected: in ValDX, clustering gives compact, interpretable ensembles with little loss of accuracy ([[@siddiquiFrameworkTestingStructural2026#^c13]]). In comparison, cluster populations turn an ensemble into a discrete distribution that can be compared with another ([[ensemble comparison]]).

## Assumptions and limits

- **Resolution is a choice.** The clustering preference, and so the number of clusters, sets the resolution ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c8]]).
- **Information is lost at both ends.** Differences between structures in the same cluster are ignored, and so are similarities between structures in different clusters ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c9]]).
- **Conclusions should not depend on the number of clusters.** The revised ValDX manuscript asks for stability across cluster sizes (`projects/1-ValDX/manuscript/report/7_results_omc.tex` L235). This is not in posted v1, so the claim stays draft.
- **Size is set by sensitivity analysis.** For parent ensembles of 10,000 to 12,700 structures, retaining 10 to 20% (about 1,000 to 2,000 representatives) caused minimal change in performance, and 10 to 100 representatives can aid interpretation if conclusions hold across cluster sizes (revised ValDX, `7_results_omc.tex` L234, draft). These numbers belong to the systems tested and are not defaults. How an ensemble responds to clustering is itself a [[controlled perturbation]]; valid ensembles degraded only slightly, while AF2-MSAss improved.
- Representatives inherit the coverage of the ensemble they summarise. They cannot show a state that was never sampled ([[sampling coverage]]).

## Why it matters here

Chapter 2, "Ensemble Comparison and Interpretable Representations". ValDX clusters candidate ensembles by k-means on PCA, both before fitting and to present results. jaxENT uses rule-based structural classes and GMM clustering in a ternary shape space (manuscript only). Stability under a change of representation is the same test as [[replicate uncertainty]], applied to the representation instead of the data split.

Claims that use this term: [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]], [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]], [[Clustering sets the resolution of an ensemble comparison and ignores differences within clusters and similarities across them.]].
