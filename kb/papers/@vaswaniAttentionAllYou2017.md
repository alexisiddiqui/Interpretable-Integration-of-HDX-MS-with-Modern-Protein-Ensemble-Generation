---
type: paper
citekey: vaswaniAttentionAllYou2017
year: 2017
read: false
pdf: kb/_pdf/@vaswaniAttentionAllYou2017.pdf
extraction: auto
needs_review: false
review_reason:
---

# Attention Is All You Need (2017)

## Main point

The Transformer replaces recurrence with attention. Its scaled dot-product attention weights values by the softmax of query–key dot products divided by √d_k, and multi-head attention runs several such functions in parallel on learned projections.

## Claims

- An attention function maps a query and a set of key–value pairs to an output. ^c1
  - page: 3
  - quote: "An attention function can be described as mapping a query and a set of key-value pairs to an output"
  - quote_check: pass
  - reviewed: false
- The authors name their attention scaled dot-product attention and define it in Eq. 1 as softmax(QKᵀ/√d_k)V. ^c2
  - page: 4
  - quote: "We call our particular attention "Scaled Dot-Product Attention" (Figure 2)."
  - quote_check: pass
  - reviewed: false
- Multi-head attention projects queries, keys and values h times with different learned linear projections and attends in parallel. ^c3
  - page: 4
  - quote: "we found it beneficial to linearly project the queries, keys and values h times with different, learned linear projections"
  - quote_check: pass
  - reviewed: false
- The output is a weighted sum of the values, each weight given by a compatibility function of the query with that value's key. ^c4
  - page: 4
  - quote: "where the weight assigned to each value is computed by a compatibility function of the query with the corresponding key"
  - quote_check: pass
  - reviewed: false
- Multiple heads let the model attend jointly to different representation subspaces at different positions. ^c5
  - page: 5
  - quote: "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c4, ^c2 define the attention used in each jax-Ka layer; ^c3, ^c5 define multi-head attention. jax-Ka changes where keys and values come from (per-relation projections), not the attention itself.

## Disagreements / limitations
