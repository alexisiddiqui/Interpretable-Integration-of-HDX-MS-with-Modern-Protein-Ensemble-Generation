---
type: paper
citekey: galpernProbingDarkEnergy2026
year: 2026
read: false
pdf: kb/_pdf/@galpernProbingDarkEnergy2026.pdf
extraction: manual
needs_review: true
review_reason: Bib entry hand-added, not from Zotero; import into Zotero and confirm the Better BibTeX citekey matches
---

# Probing the dark energy in the functional protein universe (2026)

Galpern, Bueno, Sánchez, Wolynes & Ferreiro, *PNAS* 123(4), e2531111123. doi:10.1073/pnas.2531111123. Companion theory paper from the same group: [[@galpernInformationtheoreticArgumentRestriction2026]].

## Main point

Within energy landscape theory, a sequence's evolutionary likelihood is its folding energy rescaled by a folding selection temperature $T_{sel}^{fold}$. The paper defines "dark energy" as the remainder, $E^{dark} = k_B T_{sel}^{fold}\Psi^{evo} - E^{fold}$ (Eq. 5, p. 3). For single mutants, $\Delta\Psi^{evo}$ comes from ESM-2 masked marginals and $\Delta E^{fold}$ from mega-scale $\Delta\Delta G$ or AWSEM. Dark energy is the part of evolutionary constraint that folding does not explain, i.e. the functional constraint. It is concentrated at functional and frustrated sites, forms a halo around enzyme active sites, and covers about 25–35% of positions. When the function is binding, a binding selection temperature can be estimated, and it comes out similar to the folding one.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Dark energy is defined as the difference between physical folding free energies and evolutionary free energies inferred from sequences. ^c1
  - page: 1
  - quote: "The difference between the physical folding free energies and the evolutionary free energies can be called a “dark energy.”"
  - quote_check: pass
  - reviewed: false
- Dark energy is largely localised at functional sites, which are often energetically frustrated with respect to folding. ^c2
  - page: 1
  - quote: "dark energy is largely localized at functional sites, which are also often energetically frustrated from the point of view of folding"
  - quote_check: pass
  - reviewed: false
- About a quarter of positions in folded globular proteins carry significant dark energy. ^c3
  - page: 1
  - quote: "about 25% of the positions of the folded globular proteins display some significant dark energy"
  - quote_check: pass
  - reviewed: false
- Across 64 mega-scale domains the folding selection temperature averages 156 ± 9 K. Because this is below the folding temperature, it satisfies the minimal frustration principle. ^c4
  - page: 4
  - quote: "which being below Tf clearly satisfies the minimal frustration principle and is within the expected theoretical range"
  - quote_check: pass
  - reviewed: false
- A two-component Gaussian mixture splits single-site variants into mainly folding-related (74.7%) and mainly function-related (25.3%) groups. ^c5
  - page: 5
  - quote: "We propose to use this threshold to separate those variants that affect mainly folding stability (74.7% of this dataset)"
  - quote_check: pass
  - reviewed: false
- In enzymes, high dark energy is enriched around active sites and decays with distance from the catalytic centre. ^c6
  - page: 6
  - quote: "high dark energy changes (red) also are enriched around the active sites, decaying as one moves away from the catalytic center"
  - quote_check: pass
  - reviewed: false
- Across the Catalytic Site Atlas, the fraction of function-related variants rises from about 39% in the outer shells to 61%, 67% and 88% towards the active sites. ^c7
  - page: 7
  - quote: "60.7% of them the Inner Shell 2, 66.8% for the Inner Shell 1 and 87.6% for the active sites"
  - quote_check: pass
  - reviewed: false
- The fixation of functional sites compromises folding, giving a function–folding trade-off. ^c8
  - page: 8
  - quote: "there is often a trade-off between function and folding, where the fixation of functional sites compromises folding"
  - quote_check: pass
  - reviewed: false
- Folding is encoded globally across the structure, whereas function can be coded locally. ^c9
  - page: 8
  - quote: "Folding is encoded globally across the structure, while coding for function can be done locally."
  - quote_check: pass
  - reviewed: false
- High-dark-energy sites far from catalytic residues are proposed, but not tested, to contribute to enzyme dynamics and allostery. ^c10
  - page: 8
  - quote: "Presumably these sites contribute to important enzyme dynamics and allostery"
  - quote_check: pass
  - reviewed: false
- Selection for binding at functional sites is about as strong as selection for folding. ^c11
  - page: 8
  - quote: "the strength of the sequence restrictions for binding in functional sites are similar to that for folding"
  - quote_check: pass
  - reviewed: false
- Binding fully accounts for the dark energy in only about a third of the protein–protein systems analysed. ^c12
  - page: 8
  - quote: "only in a third of the analyzed systems can the dark energy be accounted entirely for by their “binding function”"
  - quote_check: pass
  - reviewed: false
- The AWSEM folding-energy changes are computed on a single fixed native structure. ^c13
  - page: 9
  - quote: "we compute the energy difference given by the sequence change in the forcefield, assuming the tertiary native structure is conserved"
  - quote_check: pass
  - reviewed: false

## What I use from it

My reading, not the paper's claims:

- **Dark energy absorbs native-ensemble effects.** $\Delta E^{fold}$ is a global two-state $\Delta\Delta G$, or an AWSEM energy on a single structure (^c13). Any mutation that shifts populations within the native basin will therefore show up as "dark": a [[population shift]] between substates, a change in local opening, or [[allostery]], all without changing global stability. Some of the ~25% may be functional [[protein dynamics]], not static chemistry. The paper only suggests this, for distal sites (^c10).
- **HDX as the missing middle layer.** Site-resolved opening free energies from [[protection factor|protection factors]] ([[Linderstrøm–Lang model]], EX2) sit between global $\Delta\Delta G$ and function. Replacing $\Delta E^{fold}$ with residue-level $\Delta\Delta G_{op}$ would split dark energy into a local-stability part and a residual part. That turns the hypothesis in ^c10 into a test.
- **Eq. 6 has a maximum-entropy form.** $p(\sigma) \propto \exp[-E^{fold}/k_BT_{sel}^{fold} - E^{func}/k_BT_{sel}^{func}]$ is a [[Boltzmann distribution]] tilted by one term per constraint, each with its own inverse temperature acting as a Lagrange multiplier ([[maximum entropy principle]]). Setting $T_{sel}$ by matching spreads, $k_BT_{sel}^{fold} = \mathrm{sd}(\Delta\Delta G)/\mathrm{sd}(\Delta\Psi^{evo})$, works like calibrating a reweighting strength in [[ensemble reweighting]].
- **A prior for where generators fail.** Positions with high dark energy are where structure- or stability-trained generators ([[diffusion model|diffusion models]], AF2-style sampling) should differ most from experimental [[structural ensemble|ensembles]]. They are candidate regions for HDX reweighting to correct.
- **The structural counterpart is local frustration.** The dark-energy halo around active sites (^c6, ^c7) matches the catalytic frustration halo reviewed in [[@parraFrustrationPhysiologyMolecular2025]]. Both approaches flag the same sites, one from evolutionary data and one from the energetics of a single structure.

## Disagreements / limitations

- The ~25% figure depends on a two-component Gaussian-mixture cutoff (1.03 kcal/mol with experimental $\Delta\Delta G$, 1.36 kcal/mol with AWSEM). The method-dependent range is 25–35%.
- ESM-2 masked marginals are treated as a Boltzmann-like evolutionary potential. They are a learned approximation, not a fitted Potts model.
- Misfolded-state statistics use the random-energy-model approximation (the paper cites its limits).
- AWSEM reproduces experimental $\Delta\Delta G$ only moderately (r = 0.63).
- ESM-2 likelihoods probably already encode some ensemble information (alternative states, coevolution with partners). The split is therefore not purely physics versus function: some native-ensemble physics is in $\Psi^{evo}$ but in neither version of $E^{fold}$.
- SKEMPI binding data are sparse (5 or more single mutants per complex), so $T_{sel}^{bind}$ estimates are noisy (60–186 K).
