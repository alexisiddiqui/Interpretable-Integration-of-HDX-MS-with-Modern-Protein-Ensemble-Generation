---
type: paper
citekey: parraFrustrationPhysiologyMolecular2025
year: 2025
read: false
pdf: kb/_pdf/@parraFrustrationPhysiologyMolecular2025.pdf
extraction: manual
needs_review: true
review_reason: Bib entry hand-added, not from Zotero; import into Zotero and confirm the Better BibTeX citekey matches
---

# Frustration in physiology and molecular medicine (2025)

Parra, Komives, Wolynes & Ferreiro, *Mol. Aspects Med.* 103, 101362. doi:10.1016/j.mam.2025.101362. Review, 29 pp. Same group as [[@galpernProbingDarkEnergy2026]] and [[@galpernInformationtheoreticArgumentRestriction2026]].

## Main point

Proteins fold by minimising conflicts between residues, but folded structures keep some conflicts: they stay *locally frustrated*. The Frustratometer finds these conflicts by comparing each native contact energy (AWSEM, or Rosetta in the all-atom version) with decoys that mutate or move the residues. About 40% of contacts are minimally frustrated (the core), 50% neutral, and 10% highly frustrated (surface patches). The review argues the leftover frustration is kept on purpose. It marks binding interfaces, catalytic sites and allosteric switches, and it drives interconversion within the native [[structural ensemble]]. Disease mutations retune frustration in either direction, and changing how frustration is distributed between states shifts populations. The last sections stretch the idea to gene networks and the brain, speculatively.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Folded proteins do not resolve all conflicting interactions, so the structure remains locally frustrated. ^c1
  - page: 1
  - quote: "even when completely folded, not all conflicting interactions have been resolved so the structure remains ‘locally frustrated’"
  - quote_check: pass
  - reviewed: false
- About 40% of native contacts are minimally frustrated; these make up the core. ^c2
  - page: 4
  - quote: "These interactions are typically shielded from solvent, constituting the core of the globules."
  - quote_check: pass
  - reviewed: false
- About 10% of contacts are highly frustrated, and they cluster in surface patches. ^c3
  - page: 4
  - quote: "These interactions typically occur in patches in the surface of the globules."
  - quote_check: pass
  - reviewed: false
- Specific binding regions are enriched in highly frustrated patches when the partners are separated. ^c4
  - page: 4
  - quote: "those regions involved in specific binding were found generally to be enriched in highly frustrated patches when the partners in the complexes are artificially separated"
  - quote_check: pass
  - reviewed: false
- Catalytic sites are often highly frustrated whatever the enzyme's oligomeric state, topology or class. ^c5
  - page: 4
  - quote: "the catalytic sites themselves are often highly frustrated regardless of the protein oligomeric state, overall topology, and enzymatic class"
  - quote_check: pass
  - reviewed: false
- A second shell of weaker frustration usually surrounds the catalytic site. ^c6
  - page: 4
  - quote: "a secondary shell of more weakly frustrated interactions usually surrounds the catalytic site itself"
  - quote_check: pass
  - reviewed: false
- In allosteric proteins, regions that change structure between states are enriched in high frustration. ^c7
  - page: 5
  - quote: "the regions of the proteins that undergo structural changes are indeed enriched in highly frustrated regions"
  - quote_check: pass
  - reviewed: false
- The review links local frustration to protein dynamics. ^c8
  - page: 5
  - quote: "Local frustration must be somehow related to the dynamics of protein molecules."
  - quote_check: pass
  - reviewed: false
- NFκB keeps moving after binding DNA, which is attributed to frustration left unresolved in its linkers. ^c9
  - page: 5
  - quote: "The continued dynamics of the DNA-bound state is most likely due to incomplete satisfaction of the frustration within the linkers"
  - quote_check: pass
  - reviewed: false
- In thrombin, nanosecond dynamics do not correlate with catalysis, which happens on millisecond-to-second timescales. Frustration tracks slow-motion order parameters (RDC plus accelerated MD), not nanosecond ones. ^c10
  - page: 6
  - quote: "nanosecond time scale dynamics do not correlate with protein enzyme catalysis, which occurs on the millisecond to seconds timescale"
  - quote_check: pass
  - reviewed: false
- In thrombin's proposed allosteric mechanism, the regulator engages frustrated contacts at the allosteric site. The change in dynamics then travels through the minimally frustrated core to the active site. ^c11
  - page: 7
  - quote: "frustrated contacts at the allosteric site are engaged by the binding of the allosteric regulator"
  - quote_check: pass
  - reviewed: false
- Chaperones are proposed to recognise local frustrated sites in clients rather than sequence motifs. ^c12
  - page: 7
  - quote: "chaperones do not recognize specific sequence motifs but instead recognize and bind to local frustrated sites in their client proteins"
  - quote_check: pass
  - reviewed: false
- Local frustration drives interconversion between native-state conformations at the bottom of the folding landscape. ^c13
  - page: 9
  - quote: "Local frustration drives the interconversion between such conformations at the bottom of the folding energy landscape."
  - quote_check: pass
  - reviewed: false
- In metamorphic RfaH, AlphaFold2 predicts that adding frustrating mutations at interface residues drives the switch from α-hairpin to β-barrel. ^c14
  - page: 11
  - quote: "Structure predictions using AlphaFold2 supported the hypothesis that introducing highly frustrated mutations at these residues could drive the"
  - quote_check: pass
  - reviewed: false
- Sub-sampling AlphaFold2 MSAs by frustration energy gives a continuous range of adenylate kinase conformations between open and closed (Guan et al. 2024). ^c15
  - page: 12
  - quote: "Using a series of increasing values of W produces a continuous range of conformations between the open and closed conformations"
  - quote_check: pass
  - reviewed: false
- Frustration conservation across a family (FrustraEvo) sorts aligned positions into four classes: folding, flexibility buffer, function, and free to vary. ^c16
  - page: 17
  - quote: "quantifying local frustration conservation in protein families can classify aligned residues in MSAs into 4 classes"
  - quote_check: pass
  - reviewed: false
- The balance between global stability and local instability can be dysregulated by mutations. ^c17
  - page: 19
  - quote: "This delicate equilibrium can be dysregulated by the occurrence of mutations in the sequences of proteins"
  - quote_check: pass
  - reviewed: false
- AADC P330L makes the open catalytic loop less frustrated. That shifts the loop towards open and impairs catalysis. ^c18
  - page: 20
  - quote: "the P330L mutation leads to a less frustrated open catalytic loop"
  - quote_check: pass
  - reviewed: false
- The desmin Glu353dup mutation creates a minimally frustrated, over-stabilised dimer interface that impairs polymerisation. ^c19
  - page: 20
  - quote: "The disease-causing mutation induces the formation of a minimally frustrated interface between the monomers, presumably stabilizing the dimer"
  - quote_check: pass
  - reviewed: false
- In p53 R248Q, increased frustration goes with more conformational heterogeneity and higher aggregation propensity. ^c20
  - page: 22
  - quote: "increased frustration correlates with an increased propensity for the protein to adopt multiple conformations and seems related to an increased aggregation propensity"
  - quote_check: pass
  - reviewed: false
- The cardiomyopathy variant cTnC C84Y remotely alters N-domain dynamics and reduces its rigidity. ^c21
  - page: 22
  - quote: "remotely alters conformational dynamics of the N-domain, compromising its structural rigidity"
  - quote_check: pass
  - reviewed: false
- Cancer mutations in kinases may raise frustration in the inactive state and lower it in the active state, favouring activation. ^c22
  - page: 23
  - quote: "cancer mutations may increase local frustration in the inactive state of kinases while reducing frustration in the active state"
  - quote_check: pass
  - reviewed: false
- Disease-related SNVs change local frustration more than non-disease variants (Kumar et al. 2016). ^c23
  - page: 23
  - quote: "disease-related single-nucleotide variants cause more substantial changes in localized frustration compared to non-disease related variants"
  - quote_check: pass
  - reviewed: false
- Oncogene mutations can cause gain of function by relieving frustration and disrupting allosteric communication. ^c24
  - page: 23
  - quote: "oncogene-associated mutations displayed the opposite effect, creating gain-of-function events, sometimes by alleviating frustration and interfering with proper allosteric communication"
  - quote_check: pass
  - reviewed: false
- The Frustratometer needs an input structure. ^c25
  - page: 25
  - quote: "Current limitations include the requirement for an input structure"
  - quote_check: pass
  - reviewed: false
- The Frustratometer does not capture every biologically relevant energetic conflict. ^c26
  - page: 26
  - quote: "the Frustratometer does not capture all biologically relevant energetic conflicts"
  - quote_check: pass
  - reviewed: false
- The authors propose extending frustration analysis to native conformational diversity using ML ensemble generators (citing Lewis et al. 2024, BioEmu). ^c27
  - page: 26
  - quote: "explicitly consider the conformational diversity of the native state using machine learning methods to generate conformational ensembles"
  - quote_check: pass
  - reviewed: false
- IκBα is more frustrated as an isolated monomer than in its complex with NFκB, because the partner's compensating interactions are missing. ^c28
  - page: 9
  - quote: "displayed higher frustration due to the absence of compensatory interactions provided by its binding partner"
  - quote_check: pass
  - reviewed: false
- Frustration depends on the protein's context within a biological system. ^c29
  - page: 9
  - quote: "These findings underscore the dynamic nature of frustration and its dependency on the protein’s context within a biological system."
  - quote_check: pass
  - reviewed: false
- The Ca2+-binding Asp residues in calmodulin look highly frustrated to the coarse-grained Frustratometer only because the ion is not modelled to compensate them. ^c30
  - page: 14
  - quote: "the highly frustrated signal that is observed comes from the fact that the Ca2+ ion is not in place to compensate the energetics"
  - quote_check: pass
  - reviewed: false
- Energy landscape theory postulates that natural proteins navigate a rough, funnel-shaped energy landscape. ^c31
  - page: 3
  - quote: "the energy landscape navigated by natural proteins has the form of a rough funnel"
  - quote_check: pass
  - reviewed: false
- The folded state is still a large ensemble of structures. ^c32
  - page: 3
  - quote: "This folded state is still a large ensemble of structures, resembling a hazy memory recall."
  - quote_check: pass
  - reviewed: false
- A completely frozen hemoglobin, like its crystal structure, could not let oxygen in to bind. ^c33
  - page: 3
  - quote: "if hemoglobin were a completely frozen structure like the one revealed by X-ray crystallography, oxygen couldn’t get in to bind"
  - quote_check: pass
  - reviewed: false

## What I use from it

My reading, not the review's claims:

- **The timescale finding points to HDX.** Frustration tracks slow motions in thrombin, not nanosecond ones (^c10). [[HDX-MS]] protection comes from slow, rare opening events, so HDX should match frustration better than nanosecond NMR order parameters do. Testable prediction: highly frustrated contacts line up with low [[protection factor|protection factors]].
- **The authors' future direction (^c27) is this thesis.** Frustration computed on a generated ensemble is better than on one structure. Frustration computed on an HDX-reweighted ensemble ([[ensemble reweighting]]) is the experimentally grounded version, and it addresses the input-structure limitation (^c25).
- **The disease mechanisms are [[population shift|population shifts]].** AADC open/closed loop (^c18), cTnC primed state (^c21) and kinase active/inactive (^c22) are state equilibria that HDX-informed ensemble reweighting can quantify. Losing frustration can be as harmful as gaining it (^c19, ^c24). Disease isn't only destabilisation; it can be the wrong state becoming too stable.
- **A source of alternative states.** Frustration-filtered AF2 MSA sub-sampling (^c15) is another way to generate candidate conformations for reweighting.
- **The same picture as the Galpern papers, at three levels.** The catalytic frustration halo (^c5, ^c6) is the structural counterpart of the dark-energy halo in [[@galpernProbingDarkEnergy2026]]. Frustration-driven native interconversion (^c13) is the dynamic counterpart of $N_{native} > 1$ in [[@galpernInformationtheoreticArgumentRestriction2026]].
- Background framing for [[allostery]], [[protein dynamics]], [[intrinsically disordered protein|IDP]] fuzziness and [[protein misfolding and aggregation]] (chaperones handling leftover frustration, ^c12).

## Disagreements / limitations

- Frustration is computed from a single static structure, or frames picked from MD, so dynamics is inferred, not measured. The authors list the limits: an input structure is required, cost scales as N², AWSEM ignores cofactors, post-translational modifications and non-standard residues, and expected frustrated regions are sometimes missed (^c25, ^c26).
- The disease section collects mostly computational, correlational case studies, many by other groups using the server. Some sources are preprints (desmin, Research Square) or undated (Troussicot et al., n.d.). For p53 R273H the mechanism is called unclear. **Cite the primary studies, not this review, for disease examples.**
- Miscitation: "Cai et al. 2015", cited for p53 R273H and autophagy (p. 22), resolves to a graphene field-effect-transistor microRNA biosensor paper.
- The thrombin text cites "Fig. 2B" for the S²_AMD comparison, which is in Fig. 3B (p. 6).
- In the AADC passage (p. 20), the description of closed-state frustration is internally inconsistent (first "increases", then "stays the same"). The open-loop decrease is the consistent part (^c18).
- Gene-network and psychiatry sections (13–14) are analogy and speculation, not evidence about proteins.
