---
type: paper
citekey: yimDiffusionModelsProtein2024
year: 2024
read: false
pdf: kb/_pdf/@yimDiffusionModelsProtein2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# Diffusion Models in Protein Structure and Docking (2024)

## Main point

A tutorial review of diffusion models for structural biology: forward noising SDE, reverse SDE via the score, denoising score matching, diffusion on Riemannian manifolds, and applications to protein structure generation and docking.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Diffusion models have achieved state-of-the-art results on protein 3D structure generation and small molecule docking. ^c1
  - page: 1
  - quote: "they have achieved state-of-the-art results on protein 3D structure generation and small molecule docking"
  - quote_check: pass
  - reviewed: false
- A diffusion process progressively modifies noisy samples toward clean examples. ^c2
  - page: 3
  - quote: "process consists of progressively modifying noisy samples toward clean examples"
  - quote_check: pass
  - reviewed: false
- The forward noising process from data to noise is characterised by an SDE (Eq. 1). ^c3
  - page: 4
  - quote: "from data to noise is then characterized by the following SDE"
  - quote_check: pass
  - reviewed: false
- Anderson showed the forward SDE can be reversed by another SDE that starts from noise and reconstitutes the same marginals (Eq. 2). ^c4
  - page: 4
  - quote: "showed that Equation (1) can be reversed by another SDE that starts from noise and reconstitutes the same"
  - quote_check: pass
  - reviewed: false
- The gradient of the log marginal density is known as the Stein score. ^c5
  - page: 5
  - quote: "is known as the stein score of the marginal density"
  - quote_check: pass
  - reviewed: false
- Diffusion models are learned by corrupting examples with additive noise and training a neural network to reverse the corruption steps. ^c6
  - page: 3
  - quote: "sequentially corrupting examples with additive noise until samples are just noise. A deep neural network is then trained to reverse such corruption steps"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $t$ | diffusion time | $\tau$ | $t$ is labelling time |
| $f(x,t)$ | drift of the forward SDE | $f(x,\tau)$ |  |
| $g(t)$ | diffusion coefficient | $g(\tau)$ |  |
| $\nabla \log p_t(x)$ | score of the marginal density | $\nabla_x \log p_\tau(x)$ |  |
| $s_\theta(x,t)$ | learned score network with weights $\theta$ | — | $s_i$ and $\theta$ are taken; write $\hat\nabla_x \log p_\tau(x)$ |
| $B$ | Brownian motion | — |  |

## What I use from it

Introduction §1.3 and [[diffusion model]]: training corrupts structures with noise and learns to reverse it (^c6); generation progressively denoises (^c2). The SDE pair (^c3, ^c4) is Chapter 2 material.

## Disagreements / limitations
