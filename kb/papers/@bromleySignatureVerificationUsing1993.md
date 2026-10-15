---
type: paper
citekey: bromleySignatureVerificationUsing1993
year: 1993
read: false
pdf: kb/_pdf/@bromleySignatureVerificationUsing1993.pdf
extraction: auto
needs_review: false
review_reason:
---

# Signature Verification Using a “Siamese” Time Delay Neural Network (1993)

## Main point

Bromley et al. introduce the Siamese network for signature verification. Two sub-networks with identical weights extract feature vectors from two inputs, and the cosine between those vectors measures their similarity.

## Claims

- A Siamese network consists of two identical sub-networks joined at their outputs. ^c1
  - page: 1
  - quote: "This network consists of two identical sub-networks joined at their outputs."
  - quote_check: pass
  - reviewed: false
- The two sub-networks are trained with their weights constrained to be identical. ^c2
  - page: 4
  - quote: "All weights could be learnt, but the two sub-networks were constrained to have identical weights."
  - quote_check: pass
  - reviewed: false
- The distance between the two inputs is the cosine of the angle between their feature vectors. ^c3
  - page: 4
  - quote: "the cosine of the angle between two feature vectors is calculated and this represents the distance value"
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c2 define the shared-weight (Siamese) set-up that applies wherever one network with shared weights processes a pair of inputs and compares the outputs.

## Disagreements / limitations
