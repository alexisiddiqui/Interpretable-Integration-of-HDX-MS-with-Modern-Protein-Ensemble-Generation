---
type: paper
citekey: ingrahamGenerativeModelsGraphbased2019
year: 2019
read: false
pdf: kb/_pdf/@ingrahamGenerativeModelsGraphbased2019.pdf
extraction: auto
needs_review: false
review_reason:
---

# Generative Models for Graph-Based Protein Design (2019)

## Main point

The Structured Transformer designs sequences for a fixed backbone by attending over a k-nearest-neighbour residue graph whose edges carry rotation- and translation-invariant features. Each edge encodes the distance, direction and relative orientation between the two residues' local backbone frames, plus a relative positional encoding of their sequence gap.

## Claims

- Edges are kept only within the k-nearest-neighbour graph of the backbone coordinates, with k = 30. ^c1
  - page: 5
  - quote: "We only include edges in the k-nearest neighbors graph of X , with k = 30 for all experiments"
  - quote_check: pass
  - reviewed: false
- The rigid-body transformation between two residues' frames is decomposed into distance, direction and orientation features. ^c2
  - page: 4
  - quote: "While this transformation has 6 degrees of freedom, we decompose it into features for distance, direction, and orientation"
  - quote_check: pass
  - reviewed: false
- Positional embeddings are a sinusoidal function of the sequence gap between residues. ^c3
  - page: 5
  - quote: "we obtain the position embedding as a sinusoidal function of the gap"
  - quote_check: pass
  - reviewed: false
- The graph features are required to be invariant to rotations and translations. ^c4
  - page: 3
  - quote: "Invariance. The features are invariant to rotations and translations."
  - quote_check: pass
  - reviewed: false
- Each residue's point is given an orientation that defines a local coordinate system there. ^c5
  - page: 4
  - quote: "augmenting the points xi with ‘orientations’ Oi that define a local coordinate system at each point"
  - quote_check: pass
  - reviewed: false
- The direction feature is the direction of residue j expressed in the reference frame of residue i. ^c6
  - page: 4
  - quote: "the second vector is a direction encoding that corresponds to the relative direction of xj in the reference frame of (xi , Oi )"
  - quote_check: pass
  - reviewed: false
- Unlike the standard Transformer, the model feeds edge features into the attention to embed spatial and positional dependencies. ^c7
  - page: 3
  - quote: "unlike the standard Transformer, we also include edge features to embed the spatial and positional dependencies in deriving the attention"
  - quote_check: pass
  - reviewed: false
- Queries come from the embedding of node i, while keys and values come from the relational information at neighbouring nodes. ^c8
  - page: 5
  - quote: "The queries are derived from the current embedding at node i while the keys and values from the"
  - quote_check: pass
  - reviewed: false
- The authors speculate that attention overfits, since a simple MLP aggregation performed best in their comparison. ^c9
  - page: 8
  - quote: "We speculate that this is due to potential overfitting by the attention mechanism."
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c2, ^c5, ^c6 are the template for the jax-Ka spatial graph and its local-frame direction and orientation edge features; ^c3 for sequence-gap encodings; ^c4 for invariance.
- ^c7, ^c8 are the query-from-node, key/value-from-edge attention that jax-Ka extends with per-relation projections.

## Disagreements / limitations
