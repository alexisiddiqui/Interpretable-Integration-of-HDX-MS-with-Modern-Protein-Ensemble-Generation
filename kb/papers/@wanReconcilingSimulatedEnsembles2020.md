---
type: paper
citekey: wanReconcilingSimulatedEnsembles2020
year: 2020
read: false
pdf: kb/_pdf/@wanReconcilingSimulatedEnsembles2020.pdf
extraction: auto
needs_review: false
review_reason:
---

# Reconciling Simulated Ensembles of Apomyoglobin with Experimental Hydrogen/Deuterium Exchange Data Using Bayesian Inference and Multiensemble Markov State Models (2020)

## Main point

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Refining MD-derived structural ensembles against HDX data requires restraining structural observables in simulations so that the ensembles are consistent with experimental measurements. ^c1
  - page: 1
  - quote: "restraining these observables in molecular simulations to model ensembles consistent with experimental measurements"
  - quote_check: pass
  - reviewed: false
- The BICePs algorithm is used with an HDX protection factor predictor to infer which thermodynamic ensemble agrees best with experiment and to estimate the populations of each conformational state. ^c2
  - page: 2
  - quote: "to infer which thermodynamic ensemble agrees best with experiment, and estimate populations of each conformational state in the MSM"
  - quote_check: pass
  - reviewed: false
- BICePs aims to estimate conformational populations by combining theoretical predictions, here simulations, with ensemble-averaged experimental observables. ^c3
  - page: 24
  - quote: "The purpose of BICePs is to make unbiased estimates of conformational populations by optimally combining information from theoretical predictions"
  - quote_check: pass
  - reviewed: false
- BICePs models the unknown experimental uncertainty and ensemble heterogeneity with nuisance parameters σ and samples their posterior as well (Eq. 12). ^c4
  - page: 24
  - quote: "modeling the (unknown) uncertainty of the experimental measurements and heterogeneity in the conformational ensemble using nuisance parameters"
  - quote_check: pass
  - reviewed: false
- BICePs is similar to other Bayesian ensemble-inference methods such as ISD, MELD and metainference. ^c5
  - page: 24
  - quote: "BICePs is similar to other Bayesian methods for the inference of structural ensembles, including ISD"
  - quote_check: pass
  - reviewed: false
- BICePs is used to evaluate how well a model's populations agree with experiment and to rank it against competing models. ^c6
  - page: 25
  - quote: "we wish to objectively evaluate the extent to which it agrees with experimental observables, and be able to rank it against other models"
  - quote_check: pass
  - reviewed: false
- The BICePs score is a Bayes factor of each model's total evidence against a null model with uniform populations (Eqs. 14–15). ^c7
  - page: 25
  - quote: "To facilitate the assignment of a unique score to each model, we compute a Bayes factor"
  - quote_check: pass
  - reviewed: false
- The BICePs score can be thought of as a free energy of each model. ^c8
  - page: 26
  - quote: "can be thought of as a “free energy” of each model"
  - quote_check: pass
  - reviewed: false
- A lower BICePs score means better agreement with the experimental data. ^c9
  - page: 26
  - quote: "the better the model agrees with the experimental data"
  - quote_check: pass
  - reviewed: false
- The six parameters of the protection-factor model (βc, βh, β0 and the contact, H-bond and sharpness parameters) are inferred by sampling their full posterior rather than optimised to one value. ^c10
  - page: 9
  - quote: "Bayesian approaches aim to sample the entire posterior distribution of parameters"
  - quote_check: pass
  - reviewed: false
- The unknown error σ is a nuisance parameter with an uninformative Jeffreys prior (Eq. 7). ^c11
  - page: 10
  - quote: "chosen to be an uninformative Jeffreys prior"
  - quote_check: pass
  - reviewed: false

## What I use from it

## Disagreements / limitations
