---
type: paper
citekey: galpernInformationtheoreticArgumentRestriction2026
year: 2026
read: false
pdf: kb/_pdf/@galpernInformationtheoreticArgumentRestriction2026.pdf
extraction: manual
needs_review: true
review_reason: Bib entry hand-added, not from Zotero; import into Zotero and confirm the Better BibTeX citekey matches
---

# An information-theoretic argument for the restriction of the current biological alphabets to 4 nucleotides and 20 amino acids (2026)

Galpern, Ferreiro & Sánchez, *Sci. Rep.* 16:10751. doi:10.1038/s41598-026-46009-8. It cites the dark-energy paper, [[@galpernProbingDarkEnergy2026]], for function needing information beyond folding.

## Main point

Molecular information theory postulates that the information gained when a chain folds equals the information gained when evolution selects foldable sequences: $\log_2(N_{unfolded}/N_{native}) = \log_2(\text{Alphabet}/N_{evolved})$ (Eq. 1, p. 2). The random-energy-model feasibility condition is $N_{evolved} > N_{unfolded}$ (Eq. 3). Taken at its limit, this gives $N_{unfolded}^2 = \text{Alphabet}\cdot N_{native}$ (Eq. 4), and for well-folded polymers ($N_{native} \approx 1$), $\text{Alphabet} \approx N_{unfolded}^2$ (Eq. 5). Empirical per-site numbers agree: proteins have $N_{unfolded} = 5.38$ and $N_{evolved} = 4.82$ against $\sqrt{20} = 4.47$; RNA has 2.54 and 2.35 against 2. Because $N_{native}\cdot\text{Alphabet}$ is fixed, smaller early alphabets imply more native heterogeneity. On this view, early proteins (about 7 amino acids, $N_{native} \approx 3$) were [[intrinsically disordered protein|intrinsically disordered]], and folds became better defined as the code grew to 20.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- One effective sequence letter maps to one effective monomer conformation. ^c1
  - page: 1
  - quote: "one effective digital alphabet letter in the sequence landscape maps to one effective analog monomer configuration in the conformational landscape"
  - quote_check: pass
  - reviewed: false
- Primitive genetic codes with smaller amino-acid alphabets may have produced mostly intrinsically disordered proteins. ^c2
  - page: 1
  - quote: "primitive genetic systems coding for smaller amino acid alphabets may have led to a prominent presence of intrinsically disordered proteins"
  - quote_check: pass
  - reviewed: false
- The equality between the information gained by folding and by sequence selection is a postulate of molecular information theory. ^c3
  - page: 2
  - quote: "Molecular information theory also postulates that the information gained by finding the native state by folding matches the information gained"
  - quote_check: pass
  - reviewed: false
- Viable foldable sequences exist only if the sequence-space entropy for the target structure is positive. ^c4
  - page: 2
  - quote: "There are viable sequences if the entropy in sequence space for a given target structure is positive."
  - quote_check: pass
  - reviewed: false
- Folded biopolymers are approximated as one reference structure with small fluctuations, so $N_{native} \approx 1$. ^c5
  - page: 2
  - quote: "Extant folded biopolymers can be usually well described using a single reference structure and small fluctuations around it."
  - quote_check: pass
  - reviewed: false
- The measured $N_{unfolded}$ for proteins and RNA is close to the square root of each alphabet size. ^c6
  - page: 3
  - quote: "The values of Nunfolded for both proteins and RNA are close to the square root of the respective Alphabet size"
  - quote_check: pass
  - reviewed: false
- With a seven-letter early alphabet, evolved proteins would have about 3 native conformations per monomer, which is consistent with intrinsic disorder. ^c7
  - page: 5
  - quote: "the mean value for Nnative in evolved proteins would be around 3 conformations per monomer for proteins"
  - quote_check: pass
  - reviewed: false
- As the alphabet grew, $N_{native}$ fell and native states became better defined. ^c8
  - page: 5
  - quote: "we hypothesize that Nnative became smaller and the native states of the average protein progressively became better determined"
  - quote_check: pass
  - reviewed: false
- Twenty amino acids sits at the low end of the predicted range (20–39). This may reflect functional conformational substates and the need to code information beyond folding. ^c9
  - page: 5
  - quote: "the multiple conformational substates involved in protein function and that further information besides folding needs to be coded for function"
  - quote_check: pass
  - reviewed: false
- The theory accounts for present-day IDPs keeping substantial conformational entropy under native conditions. ^c10
  - page: 5
  - quote: "current intrinsically disordered proteins retain a significant amount of conformational entropy under native conditions"
  - quote_check: pass
  - reviewed: false
- Since $N_{native}$ can reach 1 with 20 amino acids, the authors argue that the genetic code will not expand further. ^c11
  - page: 5
  - quote: "the evolution of the genetic code may be seen as largely complete"
  - quote_check: pass
  - reviewed: false

## What I use from it

My reading, not the paper's claims:

- **The paper's own numbers imply $N_{native} > 1$.** Rearranging Eq. 2 gives $N_{native} = N_{unfolded}N_{evolved}/\text{Alphabet}$: about 1.3 for proteins ($5.38 \times 4.82/20$) and about 1.5 for RNA ($2.54 \times 2.35/4$). Both are within error of 1, but both point the same way. That is roughly 0.4–0.6 bits per site of residual native entropy, i.e. a small [[structural ensemble]] rather than one structure. RNA coming out higher fits its known alternative folds. Relatedly, both measured $N_{evolved}$ values sit slightly *below* $N_{unfolded}$, which strictly breaks Eq. 3. Native heterogeneity is one way to reconcile the numbers.
- **HDX gives a residue-resolved estimate of $N_{native}$.** Treat a residue as closed or open with $p_{open} = 1/(1+P_f)$ ([[protection factor]], [[Linderstrøm–Lang model]]). Its effective number of states is $\exp(H)$, where $H$ is the Shannon entropy of that two-state split: $P_f = 1$ gives 2, $P_f = 10$ gives about 1.36, and $P_f \geq 10^3$ gives about 1. This is a lower bound, since the open state is itself many conformations. It would test where the "$N_{native} \approx 1$" assumption (^c5) breaks down, and whether residual native entropy collects at the dark-energy sites of [[@galpernProbingDarkEnergy2026]].
- **Framing for the introduction.** Folded and [[intrinsically disordered protein|disordered]] proteins sit at two ends of one $N_{native}$ axis, not in separate categories. This is an information-theoretic argument for modelling [[protein dynamics]] at the ensemble level.
- **Read with the dark-energy paper, there is an information budget.** Folding uses about 2.1 bits per site. Function needs extra, site-local information (^c9), and functional conformational substates are part of what has to be paid for.
- **What moves the residual $N_{native}$.** [[@parraFrustrationPhysiologyMolecular2025]] proposes that local frustration drives interconversion between native conformations. That gives a mechanism for $N_{native} > 1$ and predicts where it should concentrate: at highly frustrated sites.

## Disagreements / limitations

- The equality in Eq. 1 is a postulate (^c3). The data are consistent with it but do not derive it.
- Sites are treated as independent (correlations are said not to change $N_{evolved}$ much).
- $N_{unfolded}$ for proteins is an average over six very different estimators; RNA uses three.
- "Conformation" is a coarse effective state (backbone or secondary-structure class), so motion within a basin is ignored by construction.
- The time axis in Fig. 2 is Trifonov's semi-quantitative "ad hoc" scale, and the Fig. 2 dashed line uses $\sqrt{20} = 4.47$ rather than the measured 5.38.
- "The code is complete" (^c11) is a strong extrapolation from $N_{native} = 1$.
- Eq. 6 gives $\log_2\sqrt{20} = 2.16$ bits per site for proteins; the text says 2.26 (p. 2), which looks like a typo.
