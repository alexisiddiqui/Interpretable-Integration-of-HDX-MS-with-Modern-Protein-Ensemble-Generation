---
type: paper
citekey: atilganAnisotropyFluctuationDynamics2001
year: 2001
read: false
pdf: kb/_pdf/@atilganAnisotropyFluctuationDynamics2001.pdf
extraction: auto
needs_review: false
review_reason:
---

# Anisotropy of Fluctuation Dynamics of Proteins with an Elastic Network Model (2001)

## Main point

The anisotropic network model (ANM) extends the Gaussian network model, which gives only fluctuation magnitudes, to the directions of residue fluctuations. Residues are nodes joined by harmonic springs of one generic force constant within a cutoff, and the Hessian's slow modes give the collective motions.

## Claims

- The ANM is a simplified normal mode analysis in which inter-residue interactions are assumed to be nonspecific. ^c1
  - page: 8
  - quote: "In principle, the ANM may be viewed as a simplified form of NMA, in which inter-residue interactions are assumed to be nonspecific."
  - quote_check: pass
  - reviewed: false
- The elastic network model is extended from fluctuation magnitudes to the directions of individual residue fluctuations. ^c2
  - page: 1
  - quote: "it becomes essential to expand this model to include the added details of the directions of individual residue fluctuations"
  - quote_check: pass
  - reviewed: false
- In the elastic network, the nodes are residues and the links are inter-residue potentials that stabilise the fold. ^c3
  - page: 1
  - quote: "the nodes are the residues, and the linkers are the inter-residue potentials stabilizing the folded conformation"
  - quote_check: pass
  - reviewed: false
- A harmonic potential with a generic force constant is assigned to all residue pairs within the cutoff distance. ^c4
  - page: 8
  - quote: "is assigned to all pairs located within rc, similar to the distance-dependent generic force constant adopted by Hinsen"
  - quote_check: pass
  - reviewed: false
- The model has a single parameter, the force constant. ^c5
  - page: 5
  - quote: "There is a single parameter in the theory, the force constant"
  - quote_check: pass
  - reviewed: false
- The ANM is presented as a simple analytical approach for estimating the mechanism of collective motions in proteins. ^c6
  - page: 8
  - quote: "A simple analytical approach (ANM) for estimating the mechanism of collective motions in proteins has been presented here."
  - quote_check: pass
  - reviewed: false

## What I use from it

- ^c1, ^c3–^c5 define the ANM used to perturb training structures in jax-Ka; ^c2, ^c6 justify ANM modes as directional, collective (not random) perturbations.

## Disagreements / limitations
