---
type: paper
citekey: skinnerEstimatingConstraintsProtection2019
year: 2019
read: false
pdf: kb/_pdf/@skinnerEstimatingConstraintsProtection2019.pdf
extraction: auto
needs_review: true
review_reason: "ValDX 6_methods_omc.tex L624 cites this paper for the switch-function BV model; it describes no such model and cites Radou et al. 2014, so the manuscript citation should change."
---

# Estimating Constraints for Protection Factors from HDX-MS Data (2019)

## Main point

Peptide-level HDX-MS centroid uptake fixes residue protection factors only up to a family of solutions. The method searches at random for sets of protection factors that reproduce all overlapping peptides through the EX2 uptake sum (Eq. 4), then groups the solutions with a Gaussian mixture model. Some residues end up uniquely determined and others take a few discrete values, depending on peptide overlap, length and time range. The output is a set of data-side constraints on protection factors, which the authors argue validate structural models more stringently than uptake alone.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The uptake of a peptide is fixed by the exchange rates of its amides, but the rates generally cannot be recovered from the uptake. ^c1
  - page: 1
  - quote: "depends uniquely on the rate of exchange of its amide hydrogens, but determining the latter from the former is generally not possible"
  - quote_check: pass
  - reviewed: false
- How degenerate the solution is depends on the number and overlap of peptides and on their length. ^c2
  - page: 2
  - quote: "depends on the number of peptides and overlap (the more the better), on their length (the shorter the better)"
  - quote_check: pass
  - reviewed: false
- For a single peptide that is long relative to the number of time points, infinitely many sets of protection factors minimise the cost. ^c3
  - page: 3
  - quote: "at which the experiment has been performed, an infinite number of sets of protection factors that minimize C exist"
  - quote_check: pass
  - reviewed: false
- Sets of protection factors compatible with the measured uptake are found by repeated random search. ^c4
  - page: 3
  - quote: "To determine sets of protection factors compatible with the experimental deuterium uptakes, we opted to perform a random search a number of times"
  - quote_check: pass
  - reviewed: false
- The number of distinct solution sets for a covered region is chosen by the lowest Bayesian information criterion. ^c5
  - page: 3
  - quote: "The number of solutions L was chosen based on the lowest Bayesian information criteria value"
  - quote_check: pass
  - reviewed: false
- The protection factor estimated for one residue is linked to those of its neighbours. ^c6
  - page: 4
  - quote: "the estimate of the protection factor for a given residue is linked to those of neighboring residues"
  - quote_check: pass
  - reviewed: false
- When each peptide is fitted on its own, the residue protection factors are severely underdetermined. ^c7
  - page: 7
  - quote: "in which case, the protection factors of individual residues are severely underdetermined"
  - quote_check: pass
  - reviewed: false
- A residual misfit may mean the model assumptions fail, for example that each residue has one protection factor, which is false when several conformers are populated. ^c8
  - page: 7
  - quote: "such as that the protection factor of each residue is uniquely defined (which is not the case if populations of different conformers exist)"
  - quote_check: pass
  - reviewed: false
- Residue protection factors can be converted into structural information and used to generate or validate protein models. ^c9
  - page: 9
  - quote: "Protection factors for each residue can be converted structural information (37–40) and used to generate or validate models of proteins"
  - quote_check: pass
  - reviewed: false
- Deuterium uptake alone can validate structural models, but protection factors give a much more stringent test. ^c10
  - page: 9
  - quote: "Although deuterium uptake alone can be used to validate structural models (42), the information contained in protection factors provides a much more stringent validation tool"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The data-side alternative to a structural forward model: infer constraints on protection factors from uptake instead of predicting them from structure (^c4, ^c5, ^c9). [[protection factor]], [[HDX protection-factor model]]
- Non-uniqueness of the residue-level [[inverse problem]] from peptide data, and what reduces it (^c1, ^c2, ^c3, ^c6, ^c7).
- The single-conformer assumption behind residue protection factors breaks down for ensembles (^c8). This is the case for averaging protection factors over an ensemble rather than inverting to one profile.
- The claim that protection factors validate models more stringently than uptake (^c10), with ref. 42 (Radou et al. 2014) as the uptake-based example. ^c9 cites the structure-based models in refs 37–41, including Best and Vendruscolo (2006) as ref. 41. [[Best–Vendruscolo model]]
- The EX2 relation $k_\text{obs} = k_\text{int}/P$ (Eq. 3, p. 2) and the peptide uptake sum over residues $m_j+1$ to $m_j+n_j-1$, which skips the first residue (Eq. 4, p. 3).

## Disagreements / limitations

- **No structure-based model.** The paper describes no switch function, contact-count or Best–Vendruscolo model. It mentions structure-based conversion only in one sentence citing refs 37–41 (^c9), and ref. 41 is Best and Vendruscolo (2006). If ValDX credits this paper with a "switch-function BV model", that citation needs correcting.
- **Not Bayesian sampling.** The method is random search followed by least-squares minimisation (sequential least-squares quadratic programming, bounds 0 ≤ ln P ≤ 20), then Gaussian-mixture clustering by expectation maximisation. "Bayesian" enters only through the information criterion used to pick the number of clusters (^c5). There is no prior or posterior over protection factors. Saltzberg et al. (2017, ref. 26) is the Bayesian method.
- The uptake model assumes EX2 exchange and one protection factor per residue. The authors note both may fail (^c8).
- Back exchange is handled only as a uniform correction. Site-specific back exchange is set aside "at the expense of overall accuracy" (p. 3), and a per-peptide back-exchange factor is suggested but not used (p. 8).
- The C3d application gives no ground truth, so it shows how ambiguous the problem is, not whether the solutions are accurate. Peptides exchanging much faster than 10 s or slower than 10^4 s carry little or no information (p. 8).
- Uncertainty comes from the spread of solutions, not from replicate error. The authors say statistical error "could be easily included" by inverse-SD weighting but do not report doing so (p. 8).
