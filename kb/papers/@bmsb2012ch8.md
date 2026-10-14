---
type: paper
citekey: bmsb2012ch8
year: 2012
read: false
pdf: kb/_pdf/@bmsb2012ch8.pdf
extraction: auto
needs_review: false
review_reason:
---

# Likelihood and Empirical Bayes Superposition of Multiple Macromolecular Structures

Chapter 8 of Hamelryck, Mardia and Ferkinghoff-Borg (eds), *Bayesian Methods in Structural Bioinformatics*, Springer 2012 (DOI 10.1007/978-3-642-27225-7). Author(s): Theobald, Douglas L.. Printed pages 191–208.

PDF note: the PDF holds this chapter only, so PDF page = printed page − 190. The book prints one shared reference list at the end, which is not in this PDF. Use this chapter for mathematical definitions and derivations; quote the sentence that introduces an equation and give the equation number in the citing note's body.


## Main point

Least-squares superposition assumes every atom has the same variance and that atoms move independently. Neither holds for proteins, and a maximum-likelihood superposition with a full atomic covariance matrix gives more accurate superpositions and covariance estimates.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Ordinary least-squares superposition can be inaccurate when atoms have heterogeneous variances or correlated positions. ^c1
  - page: 1
  - quote: "the ordinary unweighted least-squares (OLS) criterion can produce inaccurate results when the atoms have heterogeneous variances"
  - quote_check: pass
  - reviewed: false
- In MD simulations some regions undergo large conformational changes, which violates the equal-variance assumption of least-squares superposition. ^c2
  - page: 4
  - quote: "In molecular dynamics simulations, particular regions of a macromolecule may undergo relatively large conformational changes"
  - quote_check: pass
  - reviewed: false
- Adjacent main-chain atoms covary strongly through covalent bonds, so atomic positions are not independent. ^c3
  - page: 4
  - quote: "Adjacent atoms in a protein main chain covary strongly due to covalent chemical bonds"
  - quote_check: pass
  - reviewed: false
- In practice, different superpositions result depending on which variable regions are excluded. ^c4
  - page: 4
  - quote: "Different superpositions result depending on which pieces of data are discarded."
  - quote_check: pass
  - reviewed: false
- The likelihood model estimates a global covariance matrix giving the variance and correlations of each atom. ^c5
  - page: 4
  - quote: "a global covariance matrix describing the variance and correlations for each atom in the structures"
  - quote_check: pass
  - reviewed: false
- The matrix Gaussian model allows heterogeneous variances and correlations among atoms. ^c6
  - page: 5
  - quote: "We allow heterogeneous variances and correlations among the atoms in the structures"
  - quote_check: pass
  - reviewed: false
- Covariance estimated after least-squares superposition is biased and shows an artefactual pattern of correlation. ^c7
  - page: 17
  - quote: "The least-squares estimate is markedly biased and shows a strong artifactual pattern of correlation"
  - quote_check: pass
  - reviewed: false

- Least squares is corrected for uneven variances and correlated observations by weighting with the inverse of the covariance matrix. ^c8
  - page: 5
  - quote: "for uneven variances and correlations by weighting by the inverse of the covariance matrix"
  - quote_check: pass
  - reviewed: false
## What I use from it

Atomic covariance and correlation as the general frame for RMSF and dynamic cross-correlation, and the warning that the superposition used to remove rigid-body motion can itself create apparent correlations ([[positional covariance]]).

## Disagreements / limitations

The chapter is about superposition, not about MD analysis metrics. Its evidence on artefactual correlation comes from simulated structures (§8.10.1).
