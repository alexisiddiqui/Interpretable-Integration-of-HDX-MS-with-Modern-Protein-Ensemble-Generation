---
type: paper
citekey: bmsb2012ch3
year: 2012
read: false
pdf: kb/_pdf/@bmsb2012ch3.pdf
extraction: auto
needs_review: false
review_reason:
---

# On the Physical Relevance and Statistical Interpretation of Knowledge-Based Potentials

Chapter 3 of Hamelryck, Mardia and Ferkinghoff-Borg (eds), *Bayesian Methods in Structural Bioinformatics*, Springer 2012 (DOI 10.1007/978-3-642-27225-7). Author(s): Borg, Mikael; Hamelryck, Thomas; Ferkinghoff-Borg, Jesper. Printed pages 97–124.

PDF note: the PDF holds this chapter only, so PDF page = printed page − 96. The book prints one shared reference list at the end, which is not in this PDF. Use this chapter for mathematical definitions and derivations; quote the sentence that introduces an equation and give the equation number in the citing note's body.


## Main point

Knowledge-based potentials are ratios of observed to reference-state statistics. They are physical potentials of mean force only under strict conditions, and are otherwise statistical constructs whose meaning depends on the reference state. With a prior or sampler for fine-grained structure, the proper reference is the prior's own marginal: the reference ratio.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- The probability of a conformation and its momenta is given by the Boltzmann distribution (Eq. 3.1). ^c1
  - page: 3
  - quote: "The probability that a molecule with N atoms adopts a specific conformation"
  - quote_check: pass
  - reviewed: false
- The thermodynamic potential associated with the partition function is the Helmholtz free energy (Eq. 3.7). ^c2
  - page: 4
  - quote: "The thermodynamic potential associated with Z is the Helmholtz free energy"
  - quote_check: pass
  - reviewed: false
- The free energy is a sum of contributions from the average energy and the entropy (Eq. 3.9). ^c3
  - page: 5
  - quote: "the free energy can be viewed as a sum of contributions from the average energy and entropy"
  - quote_check: pass
  - reviewed: false
- A free energy along a coarse variable includes an entropy contribution, so it is not strictly a potential of mean force (Eq. 3.30). ^c4
  - page: 9
  - quote: "and from the entropy profile, and it can therefore strictly speaking no longer be"
  - quote_check: pass
  - reviewed: false
- Eq. 3.33, a ratio of observed to reference-state probabilities, is the basis of many knowledge-based potentials. ^c5
  - page: 10
  - quote: "This equation forms the basis for many KBPs that follow"
  - quote_check: pass
  - reviewed: false
- Knowledge-based potentials are built by statistical analysis of known structures, the 'inverse Boltzmann law'. ^c6
  - page: 11
  - quote: "referred to as the ‘inverse Boltzmann law’"
  - quote_check: pass
  - reviewed: false
- The 'energy' of a knowledge-based potential differs from the physical energy of the state. ^c7
  - page: 14
  - quote: "‘energy’ differs from the physical energy of the particular state s, as we have no"
  - quote_check: pass
  - reviewed: false
- Knowledge-based potentials are typically only crude approximations of physical potentials of mean force. ^c8
  - page: 21
  - quote: "suggests that KBPs are typically only crude approximations."
  - quote_check: pass
  - reviewed: false
- There is no a priori reason to think a particular knowledge-based potential is a physical free energy. ^c9
  - page: 23
  - quote: "there is no a priori reason to believe that a particular"
  - quote_check: pass
  - reviewed: false
- Knowledge-based potentials can only be assessed by using them in a full canonical calculation. ^c10
  - page: 23
  - quote: "KBPs and free energies can in general only be assessed by using the KBPs in"
  - quote_check: pass
  - reviewed: false
- Given a prior or sampler for the fine-grained structure, the reference state is uniquely determined. ^c11
  - page: 25
  - quote: "the reference state is uniquely determined"
  - quote_check: pass
  - reviewed: false
- The explicit construction with the prior's marginal as reference is called the reference ratio method (Eqs. 3.66-3.72). ^c12
  - page: 26
  - quote: "We refer to this explicit construction as the reference ratio"
  - quote_check: pass
  - reviewed: false
- The reference free energy is the free energy associated with the prior. ^c13
  - page: 27
  - quote: "the reference free energy is the free energy associated with the prior"
  - quote_check: pass
  - reviewed: false
- Knowledge-based potentials are generally not free energies or potentials of mean force in the statistical mechanics sense. ^c14
  - page: 28
  - quote: "free energies or potentials of mean force in the ordinary statistical mechanics sense."
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $r$ | atomic positions | $x$ |  |
| $E(r)$ | conformational energy | $U(x)$ |  |
| $\beta$ | inverse temperature $1/k_BT$ | — | write $1/k_BT$ |
| $\beta_s$ | scaling factor of a knowledge-based potential | — |  |
| $Z$ | configurational partition function | $Z$ |  |
| $F$ | free energy | $F$ |  |
| $S$ | entropy; also a structure database | $S$ | the database has no canonical symbol |
| $\lambda$ | coarse-grained variable (Eqs. 3.30-3.76) | $\xi(x)$ | pdftotext drops this symbol |
| $\Delta F(\lambda)$ | free energy relative to the reference state | $\Delta F(\xi)$ |  |
| $p_\beta(\lambda)$ | Boltzmann marginal of the coarse variable | $P(\xi)$ |  |
| $\tilde p(\lambda)$ | reference-state distribution | $\tilde P(\xi)$ |  |
| $n_\text{obs}$ | observed counts | $n_\text{obs}(\xi)$ |  |
| $n_\text{exp}$ | counts expected in the reference state | $n_\text{exp}(\xi)$ |  |
| $q(r \mid a)$ | prior or sampler for structure given sequence | $P_0(x)$ |  |
| $\tilde q(\lambda \mid a)$ | the sampler's marginal on the coarse variable, the reference | $P_0(\xi)$ |  |
| $p(\lambda \mid a)$ | target distribution of the coarse variable | $P^*(\xi)$ |  |
| $p(r \mid a)$ | reference-ratio distribution (Eq. 3.72) | $\hat P(x)$ |  |
| $w_{(n)}$ | potential of mean force | — | not a weight; $w_j$ are conformer weights |
| $s$ | a database state $(r, a)$ | — | $s_i$ is an observable |
| $U_s$ | knowledge-based potential | — | $U$ is the physical potential energy |
| $g(r)$ | radial distribution function | — |  |
| $a$ | amino-acid sequence | — |  |

## What I use from it

The Boltzmann distribution and free energies (Eqs. 3.1, 3.7, 3.9), the inverse Boltzmann relation (Eq. 3.33), why knowledge-based potentials are not free energies, and the reference ratio derivation (Eqs. 3.66-3.72). Used in [[Boltzmann distribution]], [[knowledge-based potential]] and [[reference ratio method]].

## Disagreements / limitations
