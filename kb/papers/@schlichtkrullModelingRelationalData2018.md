---
type: paper
citekey: schlichtkrullModelingRelationalData2018
year: 2018
read: false
pdf: kb/_pdf/@schlichtkrullModelingRelationalData2018.pdf
extraction: auto
needs_review: false
review_reason:
---

# Modeling Relational Data with Graph Convolutional Networks (2018)

## Main point

R-GCN extends graph convolution to multi-relational graphs by transforming each neighbour's message with a weight matrix specific to the edge's relation type and direction, plus a self-connection. Basis and block-diagonal decompositions limit the parameter growth that many relation types cause.

## Claims

- Unlike standard GCNs, R-GCN uses relation-specific transformations that depend on the type and direction of each edge. ^c1
  - page: 2
  - quote: "Different from regular GCNs, we introduce relation-specific transformations, i.e. depending on the type and direction of an edge."
  - quote_check: pass
  - reviewed: false
- With many relations, the number of parameters grows rapidly with the number of relation types. ^c2
  - page: 2
  - quote: "the rapid growth in number of parameters with the number of relations in the graph"
  - quote_check: pass
  - reviewed: false
- Each node gets a self-connection of a special relation type, so its next-layer representation also depends on its current one. ^c3
  - page: 2
  - quote: "we add a single self-connection of a special relation type to each node in the data"
  - quote_check: pass
  - reviewed: false
- The layer update accumulates transformed neighbour features through a normalised sum. ^c4
  - page: 2
  - quote: "accumulates transformed feature vectors of neighboring nodes through a normalized sum"
  - quote_check: pass
  - reviewed: false
- The basis decomposition is a form of weight sharing between relation types. ^c5
  - page: 3
  - quote: "The basis function decomposition (3) can be seen as a form of effective weight sharing between different relation types"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c3 are the precedent for jax-Ka's separate key/value projection per relation type (spatial, ±1, ±2 sequence edges). ^c2, ^c5 explain why a few relation types need no decomposition.

## Disagreements / limitations
