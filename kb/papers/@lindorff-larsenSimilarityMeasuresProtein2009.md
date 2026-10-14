---
type: paper
citekey: lindorff-larsenSimilarityMeasuresProtein2009
year: 2009
read: false
pdf: kb/_pdf/@lindorff-larsenSimilarityMeasuresProtein2009.pdf
extraction: manual
needs_review: false
review_reason:
---

# Similarity Measures for Protein Ensembles (2009)

The PDF is the publisher's open-access version (PLoS ONE 4(1): e4203), not a Zotero copy, and the paper still has to be added to Zotero.

## Main point

Comparing ensembles should mean comparing the probability distributions behind them, not averaging RMSDs between structures. The paper estimates a density for each ensemble in three ways and compares the densities with the Kullback–Leibler or Jensen–Shannon divergence. The three estimates are a multivariate normal (harmonic ensemble similarity), cluster populations, and kernel densities in a low-dimensional projection. Each estimate has its own blind spot, so the authors recommend the harmonic score first and the other two as a check.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The inter-ensemble RMSD is generally non-zero even for two identical ensembles, which makes it hard to use quantitatively. ^c1
  - page: 1
  - quote: "One drawback of the eRMSD is that in general it is non-zero even when the two ensembles are identical"
  - quote_check: pass
  - reviewed: false
- Comparing estimated densities tests both whether the same conformations occur and whether they occur with the same frequency. ^c2
  - page: 2
  - quote: "not only able to test whether the conformations in the two ensembles are similar, but also whether they occur with the same frequency"
  - quote_check: pass
  - reviewed: false
- The Kullback–Leibler divergence is not a true metric, though it is widely used to measure the similarity of two distributions. ^c3
  - page: 2
  - quote: "While the Kullback-Leibler divergence is not a true metric it is commonly used as a measure of the similarity between two distributions"
  - quote_check: pass
  - reviewed: false
- In thermodynamic terms the Kullback–Leibler divergence can be read as a non-equilibrium free-energy difference between the two ensembles. ^c4
  - page: 2
  - quote: "the Kullback-Leibler divergence can be thought of as the (non-equilibrium) free-energy difference between the two ensembles"
  - quote_check: pass
  - reviewed: false
- The Jensen–Shannon divergence is symmetric and is the square of a metric. ^c5
  - page: 2
  - quote: "In addition to being symmetric, it can be shown that the Jensen-Shannon divergence is the square of a metric"
  - quote_check: pass
  - reviewed: false
- The authors prefer the Jensen–Shannon divergence because it stays well-defined where one density is zero and the other is not. ^c6
  - page: 2
  - quote: "prefer the Jensen-Shannon divergence because it is well-defined even in the situation where one density is zero in regions where the other is not"
  - quote_check: pass
  - reviewed: false
- The harmonic ensemble similarity uses only the first two moments of the conformational distribution. ^c7
  - page: 4
  - quote: "The harmonic ensemble similarity score only explicitly includes the first two moments of the distribution of conformations"
  - quote_check: pass
  - reviewed: false
- In the clustering method the cluster preference, and hence the number of clusters, sets the resolution of the comparison. ^c8
  - page: 5
  - quote: "In this way, the cluster preference sets the resolution of the algorithm"
  - quote_check: pass
  - reviewed: false
- Clustering ignores differences between structures in the same cluster and similarities between structures in different clusters. ^c9
  - page: 6
  - quote: "any conformational differences between structures in the same cluster are ignored. Similarly, any similarities between structures in separate clusters are also ignored"
  - quote_check: pass
  - reviewed: false
- Dimensionality reduction by PCA or MDS assumes that the conformational space is linear. ^c10
  - page: 6
  - quote: "An important underlying assumption of methods such as PCA and MDS is that the conformational space is linear"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $D_{KL}(p_A, p_B)$ | Kullback–Leibler divergence of $p_A$ from $p_B$, Eq. 1, p. 2 | $D_\text{KL}$ | source uses a comma, thesis writes $D_\text{KL}(p_A \Vert p_B)$; natural log assumed, base not stated |
| $D_{JS}(p_A, p_B)$ | Jensen–Shannon divergence, Eq. 2, p. 2 | $D_\text{JS}$ | average KL of each density from their mixture $(p_A + p_B)/2$ |
| $D_{HES}$ | harmonic ensemble similarity, the symmetrised (J-divergence) KL between two multivariate normals, Eq. 7, p. 4 | — | log-determinant terms cancel; unbounded above |
| $p_A, p_B$ | probability densities estimated from ensembles A and B | — | |

## What I use from it

- Why single-structure RMSD is not enough for ensembles, and why the eRMSD extension fails as a score (^c1, ^c2). [[ensemble comparison]]
- Properties of the divergences for the Chapter 2 section on ensemble comparison: KL is asymmetric and not a metric (^c3), it has a free-energy reading (^c4), and JSD is symmetric, square-root metric and defined where supports differ (^c5, ^c6). Equations 1 and 2 (p. 2) are the source forms. [[Kullback–Leibler divergence]]
- The three routes from ensemble to distribution, with the limit of each: harmonic keeps two moments (^c7); clustering depends on resolution and is blind within clusters (^c8, ^c9) [[clustering]]; linear projections assume a linear space (^c10).
- Context for the ValDX choice of cluster-based summaries: ^c8 and ^c9 are the reason conclusions must be checked across cluster numbers.

## Disagreements / limitations

- The paper does not discuss RMSF or any per-residue measure. Every score is global, so it says how different two ensembles are but not where.
- The authors could not derive a closed-form JSD between two normal distributions, so the harmonic score uses the J-divergence instead (p. 4). Its scale is therefore not comparable with the cluster and projection JSDs.
- The clustering method is better at showing that ensembles differ than that they are similar. At few clusters it could not separate ensembles A and B, which differ considerably in breadth (p. 9).
- The projection method (SPE plus kernel density estimation) also trades resolution against density estimation, here through the choice of dimension (p. 10). In the test, the A–C densities barely overlapped, so JSD sat near its maximum and mainly ranked the pairs.
- The Nrep = 2 result on ensemble refinement is for one synthetic GB1 dataset that the authors call possibly "unrealistically large" (p. 11).
