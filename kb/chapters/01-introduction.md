# 01 Introduction

Chapter hub: the argument in order, one claim per line. Sections follow `thesis/chapters/01-introduction.tex`.

Markers:
- **supported**: lint-verified evidence.
- **partial**: flagged for review because support is partial or indirect.
- **gap**: the cited paper does not support the claim, so it needs a new source or rewording.
- Unmarked claims are drafts that have not been flagged.

## 1.1 Proteins as Dynamic Ensembles

Why [[population shift|conformational populations]] matter for function and disease. The arc follows `01-introduction.tex` L7 in six groups: proteins are dynamic polypeptides → folding constrains the landscape globally → function frustrates it locally, and the consequence is dynamics → disease as a perturbation of populations → what structural methods record → the thesis problem. Folding versus function is the organising argument. Galpern and Parra supply its abstract anchors, allostery shows its dynamic consequence, and the three disease cases read as perturbations of one principle rather than as a list. The ValDX opener ("understanding protein dynamics is crucial to understanding biological function, and therefore disease", `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L8) closes group C, and the jaxENT synthesis belongs in group F. Each later section answers a need this section exposes, so a limitation is developed once, in its home section, and only reminded elsewhere.

**A. Proteins are dynamic polypeptides.** A protein is a sequence before it is a structure, and its structure is something the chain does. The rigid picture has given way to [[protein dynamics|motions]] from picoseconds to days, and a crystal structure is one member, or a time average, of what the protein populates. Three claims; the calmodulin example moved to group E, where it shows what crystallography misses.
- [[Proteins are linear polymers whose sequences encode structures that fold rapidly and spontaneously.]]
- [[The rigid view of proteins has given way to one in which motions spanning picoseconds to days are essential to function.]]
- [[Even a folded protein is an ensemble of structures, and distinct crystal structures can be time-averaged members of one ensemble.]]

**B. Folding constrains the landscape globally.** Folding is an entropic search (Levinthal) that evolved sequences solve because they are minimally frustrated and fold down a rough funnel ([[conformational free-energy landscape]]). Structure prediction has largely solved the static half of the problem. The dynamic half remains open, and native-state hydrogen exchange shows why it matters, because partially unfolded forms are real but too sparsely populated to appear in a structure. Use Galpern for two conclusions only, that function needs information beyond folding ([[@galpernInformationtheoreticArgumentRestriction2026#^c9]]) and that folded and disordered proteins lie on one axis. The information-theoretic derivation (Eqs. 1 to 5, bits per site) stays in the paper note and does not enter the chapter.
- [[Folding poses an entropic search problem, and evolved sequences carry just enough information to solve it.]]
- [[Folding is possible because evolved sequences are minimally frustrated, giving a rough, funnel-shaped energy landscape.]]
- [[Structural biology has made tremendous strides in solving static protein structures by X-ray crystallography, cryo-EM and NMR.]]
- [[Leveraging large structure and sequence corpora, protein structure models predict structures rapidly and with high accuracy.]] (supported; also in §1.3 group 4). For the scale, Varadi ^c5 compares about 220 million sequences with just over 180,000 PDB structures.
- [[Despite structure prediction, the dynamics of folding remains a formidable problem that predictors and most experiments cannot resolve.]]
- [[Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.]]

**C. Function frustrates the landscape locally, and the consequence is dynamics.** Minimal frustration is a global property. Function puts frustration back at the sites where proteins bind, catalyse and switch, and the sequence pays for it in stability. The same sites drive interconversion between native conformations, so function depends on how the native [[structural ensemble]] is populated, often through slow, sparsely populated states. For an [[intrinsically disordered protein]] the ensemble is the whole description, and folded and disordered proteins sit at two ends of one landscape. [[allostery|Allostery]] is the demonstration. Where it acts by [[population shift]], a weighted ensemble can show it. In IGPS, activation is driven by millisecond motions without any large rearrangement ([[@lisiAllosteryEnzymeCatalysis2017#^c7]]), which sets the boundary the thesis works within. Weighted ensembles describe which states are occupied; the order, rates and pathways of transitions need kinetic evidence ([[conformational kinetics]]). State the boundary here, once; Q4 reminds in one line.
- [[Folded proteins retain a minority of highly frustrated contacts, clustered at the surface.]]
- [[Highly frustrated sites mark where proteins bind partners, catalyse reactions and switch allosteric states.]]
- [[Function conflicts with folding, so sequences encode function locally at sites that sacrifice stability.]]
- [[Local frustration drives interconversion between native conformations, coupling function to slow, high-energy states.]]
- [[Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles.]] (supported)
- [[The conformational heterogeneity of IDPs is not a limitation but the functional mechanism by which they carry out their roles.]]
- [[Folded and disordered proteins lie at two ends of one energy landscape, from a well-defined minimum to a flat surface.]] (moved from A)
- [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]] (draft, inferred; its home is here)
- IGPS has no claim note. Cite the Lisi block through the [[allostery]] concept until one is written.

**D. Disease as a perturbation of populations.** A [[dynamic disease mechanism]] changes which states a protein populates; it need not change the structure. Three cases, ordered by how much a single structure can show, each establishing one distinction. A population shift shows function changing while the structure is preserved. α-Synuclein shows a solution ensemble that only makes sense as a whole. The prion protein shows partially unfolded intermediates that the endpoint structures cannot reveal, and introduces pH as a condition of the populations. The general misfolding discussion is folded into the D2 and D3 leads; no further example is added unless it establishes another distinction.

*D0. Framing.*
- [[Disease mutations can destabilise the functional state or over-stabilise the wrong one.]]
- [[Disease-associated variants perturb local frustration more than benign variants.]] (partial; replaces the "Across disease categories" gap claim)

*D1. Population shift: structure preserved, function changed* ([[allostery]]). Mutations reshape the [[conformational free-energy landscape]] without changing the fold.
- [[A single mutation can leave the crystal structure unchanged yet strongly alter function.]] (replaces the p53 gap claim)
- [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]]
- [[Kinases and their inhibitor resistance mutations often preserve drug-binding sites while shifting conformational equilibria.]]
- [[EGFR L858R and T790M mutations rigidify sub-domains and shift equilibria toward active states, preserving active-site geometry.]]
- [[Mutations create neither steric clashes nor new folds but shift conformational ensembles, which needs sampling of many distributions.]] (use only as the sentence that names sampling as the need, otherwise drop)

*D2. α-Synuclein: the heterogeneous solution ensemble behind a solved fibril.* Open with the shared-transition claim as the bridge from D1 to the aggregation diseases. In [[alpha-synuclein]] the fibril is solved, but the protective state is a disordered ensemble whose protection lies in transient contacts. One paragraph.
- [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]] (the bridge sentence)
- [[Alpha-synuclein is an unfolded monomer, yet cryo-EM has solved its Lewy body fibril structures at atomic resolution.]]
- [[Cryo-EM fibrils are helical but the solution state is disordered, so aggregation-prone states can escape standard methods.]]
- [[Soluble alpha-synuclein adopts an autoinhibitory conformation in which N- to C-terminal contacts protect the aggregation-prone NAC domain.]] (replaces a gap claim)
- [[Disrupting alpha-synuclein's autoinhibitory conformation exposes the NAC domain and is likely to lower the nucleation barrier for aggregation.]] (replaces a gap claim)
- [[In soluble alpha-synuclein, an electrostatic interaction between the N- and C-termini protects the aggregation-prone NAC domain, and disrupting it is likely to lower the nucleation barrier.]]

*D3. Prion protein: partially unfolded intermediates, and pH as a condition.* The endpoints are solved and the path between them is not. The intermediates are sparsely populated, so the full ensemble is needed, and [[prion protein|MoPrP]] populates its β-rich intermediate only at acidic pH. This is where pH enters the biological motivation. §1.2 group 2 carries it to the measurement, §1.3 group 2 to the simulation, [[02-background]] §2.5 supplies the chemistry, and chapters 4 to 6 use MoPrP at pH 4 and pH 7.
- [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]]
- [[A familial prion-disease variant populates a more heterogeneous ensemble with thermally accessible misfolded states.]]
- [[Sparsely populated intermediates act as critical gateway states that control the kinetics of pathological conversion.]] (the one high-energy-intermediate claim used in §1.1; drop "critical" when drafting)
- [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]]
- [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]] (supported)
- [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]]
- [[Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH, and urea is needed to populate it substantially.]] (supported; the pH condition)
- [[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]] (supported). State the protonation half here; the HDX-MS half is the MoPrP example in §1.2 group 3.

**E. What structural methods record, method by method.** This is the home of the structural-method limitations, so each method gets its own limitation and one example rather than a shared generic sentence. The disease cases in D already show some of these; recall them in a clause rather than re-explaining.
- *[[X-ray crystallography]].* A crystal structure is a time average of an ordered lattice. Example: [[NMR relaxation showed the central helix of calmodulin is flexible in solution, though it appears rigid in crystal structures.]] (moved from A). The PKA time-average reading ([[@lisiAllosteryEnzymeCatalysis2017#^c5]]) is already in group A, and the unchanged crystal structure under a functional mutation is D1.
- *[[cryo-EM]].* It removes the need for a crystal but still reconstructs well-populated end states. Example: the α-synuclein fibril against its disordered solution state (D2, one clause).
- *[[NMR]].* It works in solution and across timescales, so it is the closest of the three to a measurement of populations, but sensitivity and spectral complexity limit the size of system it can study, and its deposited structural ensembles are not thermodynamic ensembles.
  - [[NMR works in solution like HDX-MS but also gives structural information and is sensitive over a wide range of timescales.]] (supported)
  - [[NMR typically needs larger samples and is limited to smaller proteins or domains by sensitivity and spectral complexity.]] (draft, needs review)
  - An NMR ensemble is not a thermodynamic ensemble ([[@bmsb2012ch12#^c3]]). Cross-reference §1.5 group 1: [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]] (supported).
- *What all three miss.* Transient, sparsely populated intermediates, which are the states D3 needs.
  - [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]]; its second citation, [[@biancanielloStructureDynamicsMisfolding2025#^c9]], states that integrative approaches are needed because X-ray crystallography, NMR and cryo-EM cannot capture dynamic intermediate species. Biancaniello ^c2 (techniques mainly target rigid states) is further support not yet on the note.
- *Scale of the gap*, one sentence: [[Only about 12,000 experimental structural ensembles exist, covering 21% of CATH superfamilies, so dynamic data are scarce.]] or [[Tools to estimate protein dynamics are decades old, but public datasets hold only thousands to tens of thousands of entries.]] (supported) (use one). The NMR caveat above means the count overstates what is known about populations.
- *Conditions.* [[Conformational populations depend on molecular context, so they are defined only for a stated environment.]]. This sets up the requirement in F that a measurement work under stated conditions.
- Framing claims, if a summary sentence is needed at all: [[Tools have been dominated by methods that freeze proteins in time, hiding links between structure, dynamics, function and disease.]] or [[Static structures alone cannot explain many biological phenomena; dynamics underlie disease mechanisms and drug response.]] (use one). They add no example, so they cannot replace the method-by-method limitations.
- Other method-specific support: Pelikan ^c4 (disorder and heterogeneity obstruct classical methods), Li ^c1 (GPCR signalling is hard for crystallography and NMR, and HDX-MS could help), James ^c6 (cryo-EM has outpaced the modelling of disordered regions).

**F. What a measurement must offer, and the thesis problem.** E leaves a set of requirements. A [[structural ensemble]] is useful only once its weights are known, and the weights need a measurement made in solution, under stated conditions, on systems of realistic size, and sensitive to sparsely populated states. [[HDX-MS]] meets these requirements, which is why it is the measurement the thesis integrates. Name it here with what it can see; §1.2 explains how. Frustration analysis, by its authors' own account, also needs generated ensembles rather than one structure (Parra ^c25, ^c27). End on the problem as the thesis's own statement, with no claim behind it. Generated ensembles can be constrained by solution measurements, and the question the thesis takes up is how to assess the explanation that results. §1.2 asks what the measurement records, §1.3 where the candidates come from, §1.4 how they are fitted, and §1.5 what the fit can be trusted to mean.
- [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]
- [[Quantifying state populations requires experimental measurements of protein dynamics.]] or [[Without experimental measurements of protein dynamics, the biological mechanism of misfunction can remain unclear.]] (use one)
- What HDX-MS offers against E:
  - scope: [[HDX-MS can study many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools.]] (supported; [[@jamesAdvancesHydrogenDeuterium2022#^c2]]);
  - rare states: exchange of otherwise inaccessible amides needs rarely populated open conformations, so hydrogen exchange reports on them ([[@vendruscoloRareFluctuationsNative2003#^c7]]), which links back to [[Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.]] in group B;
  - ensembles: [[HDX data report on ensembles and can reveal conformational landscapes that differ from the crystal structure.]]
- [[Bridging the gap requires a shift toward integrative approaches combining measurements of dynamics with advanced simulations.]] moved to §1.3 group 5, where both halves of the complementarity have been shown.

**Drafting sources.**
- Anchors:
  - [[@galpernInformationtheoreticArgumentRestriction2026]] for B (conclusions only);
  - [[@parraFrustrationPhysiologyMolecular2025]] for B to E;
  - [[@galpernProbingDarkEnergy2026]] for B and C;
  - [[@lisiAllosteryEnzymeCatalysis2017]] for the allostery demonstration in C;
  - the [[dynamic disease mechanism]] concept for D and E.
- Confirmation `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex`:
  - the database-size figure (`figures/database_sizes.png`) fits group B or E;
  - its disease paragraphs map onto D;
  - reorder its material; do not reuse its opening.

**Wording to avoid.**
- Intensifiers from the confirmation: "paradigm shift", "simply", "critical", "fundamental". Several existing claim titles use them (the gateway-states claim in D3 among them), so reword when drafting.
- Parra's gene-network and psychiatry analogies (§§13–14). They are analogies, not evidence.
- The hemoglobin sentence as a result. It is a framing image.
- Parra as the citation for specific disease results. Cite the primary studies (see Gaps).
- Galpern's bits-per-site numbers and Eqs. 1 to 5. Conclusions only.

### Gaps
- **Dropped from the hub, note kept.** These claims are no longer listed in §1.1. Their notes stay in `kb/claims/` and can return if a draft needs them.
  - [[Despite huge advances in accuracy and speed, protein structure models have limitations.]] (stays in §1.3 group 4)
  - [[For intrinsically disordered proteins, the failure of static structural biology becomes apparent.]]
  - [[Mounting evidence suggests that understanding dynamics is the key to novel therapeutic strategies.]]
  - [[Diseases involving protein misfolding are prime case studies that highlight the limitations of structural biology.]]
  - [[The conformational dynamics underlying pathogenic aggregation are central to understanding these diseases.]]
  - [[High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.]] (D3 uses the gateway-states claim)
  - [[These neurodegenerative diseases involve transient oligomeric intermediates that never crystallize.]]
  - [[Differences in conformational dynamics relate to the aggregation of amyloidogenic light chains.]]
  - [[Linking fast molecular motions to slow pathological processes requires conformational dynamics that static structures cannot capture.]] (its sentence shape remains the model in [[examples]] 8)
  - [[There is a persistent, critical gap in our ability to predict and understand protein dynamics.]]
  - [[The fundamental limitations of these methods restrict our understanding to what can be measured experimentally.]]
  - [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]] moved to §1.2 group 3.
- **No claim yet** for the jaxENT synthesis: "Protein conformational dynamics govern biological function and modulate disease-associated conformational states, necessitating their representation as diverse structural ensembles rather than single static models" (`projects/2-jaxENT/manuscript/report/introduction.tex` ¶1). Its two missing citations, `moulickPartiallyUnfoldedForms2015` and `bonomiPrinciplesProteinStructural2017`, are now seeded and in `thesis/references.bib`.
- **No claim for IGPS.** Group C cites Lisi ^c7 through the [[allostery]] concept. Write a claim note once the block is reviewed.
- **Folding theory has no primary sources in the KB.** There are no notes for Anfinsen, Levinthal, Bryngelson and Wolynes (1987) or Onuchic et al. (1997), so groups A and B rest on Galpern and Parra.
- **Vendruscolo 2003 and Kim 1993 have PDFs and blocks.** Vendruscolo ^c7 is used in group F and ^c5 in §1.2 group 6. Kim ^c1 (native-state motional domains) is still free to strengthen A to C or §1.2 group 3; neither paper has a claim note yet.
- **Primary sources behind Parra-level claims**, to import into Zotero:
  - Ferreiro et al. 2007 and 2011
  - Freiberger et al. 2019
  - Fuglestad et al. 2013
  - Kumar et al. 2016
  - Bizzarri 2022
  - Bisello et al. 2022
  - Dixit and Verkhivker 2011
  - Marques et al. 2021
  - Frauenfelder et al. 1991
- **Replaced or dropped claims.** Their notes are kept, each with a "Superseded" section:
  - [[Cancer-causing p53 mutants have crystal structures nearly identical to wild type but very different DNA binding and pathologies.]] is replaced by the PKA claim. It can return once there is a primary p53 source.
  - [[Across disease categories, high-resolution structures exist but mechanisms remain unclear.]] is replaced by the frustration-variant claim.
  - [[Soluble alpha-synuclein stays compact through transient long-range contacts between its charged C-terminus and hydrophobic centre.]] and [[Conformational heterogeneity from pathogenic mutations fundamentally alters alpha-synuclein's protective intramolecular interactions.]] are replaced by the two Mukherjee rewordings.
  - [[Shifted conformational equilibria are a major reason why most kinases are still undruggable.]] is dropped, because Lisi and Loria's remark concerns phosphatases.
- **Near-duplicates still open.** When drafting, use one claim from each set:
  - "Tools have been dominated…" / "Static structures alone…" (E)
  - "Only about 12,000…" / "Tools to estimate…" (E)
  - "Quantifying state populations…" / "Without experimental measurements…" (F)
  - the IDP claims (C)
- **Mis-cited claims found in passing, not fixed here:**
  - the GPCR ¹⁹F-NMR claim cites Fan and Yen, which cover GPR52 and β1AR;
  - the HIV Vif claim cites Appadurai, which is the wrong paper;
  - the SARS-CoV-2 spike claim cites Puchades and Stander, which do not support it;
  - "With current models, most single-domain proteins…" likely mis-cites Varadi.

## 1.2 Measuring Protein Dynamics

**Thread for 1.2–1.5.** Sections 1.2 to 1.5 share one thread: HDX-MS constrains ensembles only through an indirect [[forward model]], so the inferred populations depend on the candidate ensemble, the forward model and their uncertainties. The grounding for 1.3–1.5 comes mainly from BMSB (Hamelryck et al. 2012) chapters 1–4, 12 and 13.

§1.2 says what [[HDX-MS]] measures, what it can show, and where measurement ends and structural inference begins, which is where simulation comes in. It does this in six steps, strengths before limits. Exchange theory stays in Chapter 2 (see below).

**1. What is recorded.** Backbone amides exchange with solvent deuterium, and MS reads this as a mass increase of peptides over labelling time ([[deuterium uptake]]).
- [[Different methods can measure protein dynamics, depending on the system, timescale and experimental conditions.]]
- [[HDX-MS measures protein conformational dynamics in solution.]] (supported)
- [[HDX-MS measures the exchange of backbone amide hydrogens with deuterium in the solvent.]] (supported)
- [[Measuring the mass increase of peptides over time lets HDX-MS report on protein dynamics and conformational changes.]] (supported)

**2. What sets the rate.** Intrinsic chemistry ([[intrinsic exchange rate]]) and local protection from hydrogen bonding, burial and transient opening ([[Linderstrøm–Lang model]], [[protection factor]]). The intrinsic rate depends on pH and temperature, so uptake, and the populations later inferred from it, hold for the stated pD and temperature. This is the measurement's side of the pH thread opened in §1.1 D3.
- [[Amide exchange rates depend on intrinsic chemistry and on local protection from hydrogen bonding, burial and transient opening.]] (supported)
- [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]] (supported)
- [[The HDX rate depends on the local environment of the amide hydrogen, with more exposed and flexible regions exchanging faster.]] (supported; read it with the second caution in group 5)
- [[His, Asp and Glu neighbours change intrinsic exchange rates with pH through their own ionisation.]] (supported; the neighbour half of the pH dependence)
- Claim still to write: the intrinsic exchange rate depends on pH and temperature through its acid-, base- and water-catalysed terms, so uptake is defined for the stated pD and temperature ([[intrinsic exchange rate]]; source [[@baiPrimaryStructureEffects1993#^c2]]). The jaxENT MoPrP data were taken at pD 4.

**3. What it can show.** Strengths come before limits, so the reader knows what the measurement is for before learning where it stops. Two examples, one general and one on the thesis's own system. Group F of §1.1 has already named the scope and the rare-state sensitivity; recall them in a clause, not again in full.
- [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]] (supported; the one disease example that only HDX-MS supplies)
- [[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]] (supported). The HDX-MS half. It shows a pH-dependent change in protection on MoPrP, the system of chapters 4 to 6, and carries the pH thread from group 2.
- [[The primary benefits of HDX-MS are sensitivity, flexibility and low sample needs compared with other biophysical techniques.]]
- [[HDX-MS flexibility and increasing throughput make it well suited to challenging targets such as GPCRs, antibodies and IDPs.]]
- Reminder only: [[HDX-MS can study many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools.]] (supported; stated in §1.1 F)

**4. What the readout resolves.** Overlapping peptides, not residues or atoms. This is the price of the strengths in group 3.
- [[HDX-MS reports deuterium uptake at the peptide level, not the residue level.]] (supported)
- [[HDX-MS data alone do not give the atomic positions that NMR, crystallography and cryo-EM provide.]] (supported)

**5. Why interpretation is ambiguous.** Different local environments or populations can give the same uptake. A change in uptake shows a change in protection, not a mechanism. Two cautions follow.
- [[A change in HDX-MS uptake shows a change in protection but does not on its own identify the structural mechanism.]] (supported)
- [[Greater deuterium uptake indicates less protection from exchange, not directly greater flexibility.]]
- [[Labelling time measures accumulated exchange, not the duration of a conformational motion.]]
- Non-uniqueness is developed in §1.5 group 1 ([[Ensembles generally have far more degrees of freedom than observables, so a single data source leaves them underdetermined.]]); here, one sentence at most.

**6. Why simulations are the complement, and the handoff to §1.3–1.4.** The limits in groups 4 and 5 are exactly what an atomic model supplies. Protection is a property of the ensemble, not of one structure, so a residue whose environment differs between conformers needs those conformers, and peptide uptake cannot pin residue protection down on its own. Connecting uptake to structure therefore needs candidate conformations and a model that predicts exchange from them ([[forward model]]), which makes interpretation an [[inverse problem]]. Others have already combined the two, mainly for simpler systems, so the open question is where the candidates come from (§1.3) and how they are weighted (§1.4).
- Equilibrium protection factors are a property of a Boltzmann ensemble, so no single conformation is expected to satisfy all of them ([[@vendruscoloRareFluctuationsNative2003#^c5]]).
- [[A single protection factor per residue cannot describe a residue whose environment differs between populated conformers.]] (supported)
- [[Residue protection factors are generally underdetermined by peptide-level uptake.]] (supported)
- [[To quantitatively connect measurements of dynamics to biological mechanisms, they must be interpreted in structural terms.]]
- [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]] (supported)
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]] (supported)
- [[Several groups have restrained simulations or pruned ensembles post hoc with HDX-MS data, mainly for simpler systems.]] (supported; the precedent, and its "simpler systems" is the opening for the thesis)
- [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]] (the supported claims above can carry the point without it)

**Drafting sources.**
- ValDX intro: `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L8 (scope and targets) and L14 (peptide-level ambiguity).
- ValDX theory: `2_hdx_theory_omc.tex` L5 (local environment and intrinsic rate) and L9 (labelling time).
- jaxENT intro: `milestones/2025-11-confirmation-of-status/jaxENT_paper1/report/introduction.tex` L4 (inverse problem).
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex` L9–11, a plain-language description and benefits. Its NMR and SAXS paragraphs are broader than §1.2 needs.

**Kept for Chapter 2:**
- intrinsic-rate equations ([[intrinsic exchange rate]]);
- EX1/EX2 kinetics ([[Linderstrøm–Lang model]]);
- $P_f$ and $\Delta G_\text{op}$ ([[protection factor]]);
- back-exchange and peptide averaging ([[deuterium uptake]]);
- the [[Best–Vendruscolo model]].

**Wording to avoid:**
- "chemical potential" for $P_f$ (confirmation `measuring_dynamics.tex` L22). $P_f$ is a ratio of rates ([[protection factor]]).
- "without size limitations" (ValDX intro L8). Use the group 5 claim for breadth. [[Orthogonal to X-ray, cryo-EM and NMR, HDX-MS probes protein dynamics in solution under diverse conditions.]] now states solution conditions only, since James p16 sets a size limit by peptide resolution.

### Gaps (1.2)
- The two cautions are inferred, not stated by a source:
  - [[Greater deuterium uptake indicates less protection from exchange, not directly greater flexibility.]]
  - [[Labelling time measures accumulated exchange, not the duration of a conformational motion.]]
  - Either find a source that states each one, or present it as the thesis's own reading of EX2 kinetics.
- Masson (2017, 2019), Narang, Vinciauskaite, James, Lee, Englander and Skinner are all still `read: false`. Their quotes pass the lint, but check the papers before relying on finer points.

## 1.3 Estimating Protein Dynamics

§1.3 says where candidate structures come from and what each source can and cannot tell us. Generating candidates and estimating their populations are different tasks. Keep three things apart throughout: which states are present (coverage), how much weight each has (populations) and how fast they interconvert (kinetics) ([[sampling coverage]]). Five paragraphs, as in the outline; equations and algorithms stay in Chapter 2.

**1. Candidate ensembles.** A [[structural ensemble]] is a set of candidate conformations. A sampler can get coverage, populations and kinetics right or wrong separately ([[conformational free-energy landscape]]).
- [[Modern computational methods allow protein structures to be generated at an unprecedented rate.]]
- Already in §1.1 group F: [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

**2. MD and its limits.** [[molecular dynamics]] gives physically grounded trajectories, but only for its approximate [[force field]] and only once sampling has converged ([[equilibration and convergence]]). Five claims and one line on protonation, the simulation's side of the pH thread.
- [[MD simulations numerically integrate Newton's equations of motion, giving atomistic insight into protein dynamics over time.]]
- [[MD simulations can model varied conditions such as temperature, pressure, pH and the presence of ligands or other biomolecules.]]
- [[MD is computationally expensive and may only approximate true dynamics due to force-field inaccuracies and limited sampling.]] (supported)
- [[Sufficiently sampled equilibrium MD targets the Boltzmann distribution of its approximate force field, not the protein's true distribution.]]
- [[Until MD has converged, its statistics depend on the starting structures; reproducibility across independent starts is the basic check.]] (supported)
- [[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]] (supported). A pH 4 ensemble is only as good as the states assigned; chapter 6 takes this up ([[02-background]] §2.5). The thesis's own case, [[Our candidate ensembles were protonated once at pH 7 or 7.4, so a pH 4 ensemble depends on protonation states that were not assigned for pH 4.]] (draft), belongs in §1.7 and chapter 6, not here.

**3. Enhanced sampling.** Two families ([[enhanced sampling]]). Biasing the energy recovers equilibrium probabilities by reweighting but usually loses kinetics. Adaptive seeding broadens exploration, but pooled frames are not populations. Neither gives populations for free.
- [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]] (supported)
- [[The metadynamics bias encourages exploring new states by discouraging revisits to previously sampled configurations.]] (supported)
- [[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]] (supported)
- [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]] (supported)
- [[Frontier-Expansion Sampling is a promising avenue for enhanced sampling of conformational space.]] (supported)
- [[As FES only requires Cartesian coordinates to select new simulation seeds, it is flexible to the underlying topology.]]
- Optional detail: [[Online analysis of collective variables can adaptively guide sampling towards underexplored regions of conformational space.]]

**4. Learned generators, including diffusion.** Three kinds of model, which the confirmation runs together:
- **Structure predictors adapted for diversity.** Perturb the input ([[MSA subsampling]]) or the seed. Output frequencies have no defined target distribution.
  - [[Protein structure models have recently emerged as a powerful tool for structural biology.]] (supported)
  - [[Leveraging large structure and sequence corpora, protein structure models predict structures rapidly and with high accuracy.]] (supported)
  - [[As protein structure models are primarily trained on static structures, their ability to predict dynamics is limited.]]
  - [[Structure predictors are trained to return the single structure most likely to appear in the PDB.]] (supported; the reason the adaptations below are needed)
  - [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]] (supported)
  - [[Sub-sampling multiple sequence alignments alters the contacts described to the model, leading to diverse structural predictions.]]
  - [[Generating many sub-sampled predictions creates a conformational ensemble that captures the protein's dynamic nature.]]
- **Generators trained to sample a distribution.** A [[diffusion model]] learns the training-data distribution by learning to denoise; a [[Boltzmann generator]] is trained toward the Boltzmann distribution and reweighted to it.
  - [[Deep-learning models rapidly generate structures and ensembles by sampling a learned distribution of conformational space.]] (supported)
  - [[Deep-learning models trained on large structural datasets learn conformation distributions, and sampling them yields ensembles.]]
  - [[Diffusion models are trained to reverse a noising process and generate structures by progressively denoising random samples.]] (supported)
  - [[Diffusion models trained on PDB structures learn a distribution concentrated on folded, low-energy states rather than the equilibrium distribution.]] (supported; what the learned distribution is, and why it is a prior)
  - [[Diffusion steps are not physical simulation time.]]
  - [[Diffusion-based PSMs have emerged as a powerful alternative to traditional structure prediction methods.]]
  - [[Learning the physical landscape can reduce the cost of sampling new states while retaining the accuracy of the underlying physics.]] (supported) (Boltzmann generators only)
- **Learned force fields inside MD.** An MLFF improves the [[force field]], not the sampling.
  - [[Machine-learned force fields learn energies and forces for simulation, whereas Boltzmann generators generate configurations and reweight them to the Boltzmann distribution.]] (supported)
  - [[Ensembles can be generated by learning the physical landscape of protein systems directly from existing simulations.]]
- **Combining generators with MD.** Generators broaden coverage and MD relaxes the candidates; whether the result is representative still has to be assessed.
  - [[Learned generators are used to seed MD simulations, combining broad coverage with physics-based sampling.]] (supported)

**5. Handoff to §1.4: populations need experimental constraints.** Every source above gives candidates whose frequencies are a prior, not populations ([[importance sampling]]). Experiment is needed to weight them. This is the mirror of §1.2 group 6, and the section should close on the two halves together. Generators and simulations supply atomic candidates without trustworthy populations, and HDX-MS constrains protection in solution without atomic positions, so each supplies what the other lacks. Integration (§1.4) is the operation that joins them.
- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]]
- [[A knowledge-based potential is not a thermodynamic free energy unless its probabilistic model and reference distribution are defined.]] (supported)
- [[The emerging bottleneck is scoring generated structures against in vitro and in vivo behaviour.]]
- [[Bridging the gap requires a shift toward integrative approaches combining measurements of dynamics with advanced simulations.]] (moved from §1.1 F; "bridging the gap" is the confirmation's phrase, reword)
- The generated-diversity point is developed in §1.5 group 4; do not state it here.

**Drafting sources.**
- ValDX methods: `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L85. Ensembles are framed as competing structural hypotheses, and the concrete examples are single-start MD, multiple-start MD, T-FES, and filtered and unfiltered AF2.
- jaxENT intro: `projects/2-jaxENT/manuscript/report/introduction.tex` L6. MD recovers dominant states for folded proteins but cannot guarantee representativeness. AF2 sub-sampling includes implausible structures. Wider sampling creates opportunities for integration.
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex` L15–84, which has most of the explanatory prose. Use it with the corrections below.

**Kept for Chapter 2:**
- diffusion SDEs and score matching ([[diffusion model]]);
- bias potentials, reweighting estimators and MSMs ([[enhanced sampling]]);
- detailed balance ([[Markov chain Monte Carlo]]);
- Boltzmann-generator weights ([[Boltzmann generator#^eq-bg-weight]]);
- force-field functional forms;
- knowledge-based potentials and the [[reference ratio method]].

**Wording to avoid** (confirmation `ensemble_generators.tex`):
- "no approaches to generate conformational ensembles" (L42). Use the AF3 seeds claim instead.
- "loss of equilibrium properties" for metadynamics (L76). Biased sampling loses kinetics, and recovers equilibrium by reweighting.
- "preserve equilibria", "without distorting the landscape" or "preserving the equilibrium distribution" for adaptive seeding and FES (L80–82). Seeding broadens exploration; pooled frames still need a model or reweighting.
- Unke and Noé cited together as "learned force fields" (L67). An MLFF is a force field; a Boltzmann generator is a sampler.

### Gaps (1.3)
- **Inferred claims:** [[Sufficiently sampled equilibrium MD targets the Boltzmann distribution of its approximate force field, not the protein's true distribution.]] and [[Diffusion steps are not physical simulation time.]] need a source, or should be presented as the thesis's own statements.
- **Dropped from the hub, note kept** (2026-10-15): [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]] The cited passage is about MSA mutagenesis, not sub-sampling. The qualitative population claim in the ch. 2 hub carries the point.
- **Dropped from the hub, note kept** (2026-10-14): [[MD lets researchers study how proteins respond to different environments, giving insight into functional mechanisms.]], [[Physics-based methods are useful for detailed analysis but limited by the computational cost of equilibration.]], [[Sampling is limited because equilibration must be repeated for each new system or starting conformational state.]]. If the equilibration pair returns, it needs a passage: the confirmation cites Lazim et al. (2020), but the only KB quote from it is about the cost of all-atom MD in general.
- **Removed** (2026-10-15): five claims whose cited papers did not support them. They said a complete picture of dynamics needs sampling between states, that deep learning supplies diverse starting structures for physics-based sampling, that physics-based and statistics-based simulation fill each other's gaps, that a hierarchical pipeline overcomes the limits of each scheme, and that seeding methods work over specific or generic CVs. The hybrid point now rests on [[Learned generators are used to seed MD simulations, combining broad coverage with physics-based sampling.]] alone. Each would need a new source to return.
- **Unchecked PDFs:** Karplus, Barducci, Casadevall, Wilson, Varadi and He are cited in the confirmation for this section but not yet checked.
- **Unread papers:** Hénin, Zhang, Zheng, Stein, Vani, Unke, Noé, Abramson and Yim are all `read: false`. Their quotes pass the lint.

## 1.4 Integrating Experiment and Ensembles

**Argument:** the measurements introduced in §1.2 can constrain the candidates generated in §1.3 through a structural forward model. Integration fits their contributions relative to a starting ensemble, with assumptions about exchange and uncertainty. The resulting ensemble model is a structural hypothesis whose reliability is the subject of §1.5.

**1. From candidate structures to a testable hypothesis.** Pick up the handoff from §1.3: the candidates need relative contributions before they can explain a solution measurement. Frame the task as an [[inverse problem]]: infer an ensemble from its measured effects. Recall the ambiguity from §1.2 briefly; use it to motivate forward prediction rather than repeating the measurement limitations.
- [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]] (supported)
- [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]]

**2. Predict what the experiment would measure.** Define a [[forward model]] as the link from a proposed ensemble to an observable. Give the HDX example in words: structural hydrogen bonding and burial features → predicted residue protection factors → exchange rates under EX2 → peptide uptake. Introduce the [[Best–Vendruscolo model]] as the concrete example shared by the research chapters. The prediction depends on ensemble weights and empirical model parameters.
- [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]]
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]] (supported)
- Drafting caution: BV/HDXer averages log protection factors before calculating uptake. Averaging separate conformer uptake curves would describe a different model; see [[Best–Vendruscolo model#^eq-bv-ensemble]] and [[deuterium uptake#^eq-uptake-peptide]].

**3. Fit the contributions of the sampled conformations.** Explain [[ensemble reweighting]] physically: adjust how much each candidate contributes so the ensemble prediction agrees better with experiment. The initial weights define the reference ensemble. Reweighting changes contributions within the sampled candidates; states absent from that set require further sampling ([[importance sampling]]). Name HDXer as an established implementation after explaining the operation.
- [[Ensemble reweighting adjusts structural contributions so proposed conformational states can be tested against experiment.]]
- [[HDXer is a Python package that implements a MaxEnt reweighting scheme to fit simulated ensembles to experimental HDX-MS data.]]

**4. Balance experimental agreement with the reference ensemble.** The data generally permit several fits, so explain why closeness to a prior matters ([[regularisation]]). Introduce relative [[maximum entropy principle|MaxEnt]] as seeking agreement with minimal departure from the reference weights, accounting for uncertainty. Give the Bayesian reading briefly: the prior and an error-model likelihood jointly determine inference. Equal initial frame weights preserve the sampled distribution as the reference; they do not establish its physical accuracy.
- [[MaxEnt reweighting seeks new weights that minimise the discrepancy with experimental uptake while staying close to the prior.]] (draft; its current citations establish the general principle, so use Bradshaw or Lee for the HDX application)
- [[In a Bayesian description, a prior and a likelihood combine into a posterior over unknown structures and parameters.]] (supported)
- Do not identify a fitted optimum with a full posterior uncertainty distribution, or say that MaxEnt guarantees physical plausibility or prevents overfitting.

**5. Fit the ensemble and calibrate its forward model.** Distinguish the two adjustable parts of an ensemble model: frame weights determine structural contributions, while the BV coefficients calibrate the mapping from structural features to protection. Introduce fixed-parameter, staged and joint fitting as choices about these unknowns ([[nuisance parameter]]). This motivates the unified fitting problem addressed by jaxENT; detailed objectives and results belong in its research chapter.
- Ground this paragraph in ValDX's optimisation protocols and jaxENT's introduction; a dedicated claim note for the joint fitting motivation has not yet been assembled.
- HDXer already optimises BV parameters. Describe jaxENT's contribution through its unified optimisation workflow and composable objectives, rather than claiming parameter fitting itself is new.

**6. What established integration provides, and what it leaves open.** First credit what the existing tools do. HDXer and MaxEnt refinement reweight candidates against a reference, fit forward-model parameters, and test sensitivity by omitting data or varying parameters ([[02-background]] §2.4, layer 2 of the layered-validation decision). Then name the two problems they leave, one sentence each. Agreement with uptake supports consistency under the chosen candidates, forward model and fitting assumptions, and no existing HDX study partitions the data around peptide dependence, so assessment without ground truth is unresolved (§1.5, Q1). Weights and forward-model parameters are fitted in stages with plausibility fixed by the method, so a joint fit under a plausibility constraint that suits candidates without Boltzmann weights is unresolved (Q2). Parameter fitting itself is not new; the gap is the unified fit and its assessment. Let §1.5 develop identifiability, model error, overfitting, uncertainty and interpretability.

Close §1.4 on why agreement can mislead, which sets §1.5's order. One kind of risk is common to any model fitted to finite data and is answered by standard statistics (held-out data, partitions that respect dependence, selection kept apart from evaluation). The other is specific to integration, because the forward model that links structure to uptake is itself approximate, and a fit can absorb its errors into the weights.
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]
- [[HDXer is a Python package that implements a MaxEnt reweighting scheme to fit simulated ensembles to experimental HDX-MS data.]] (reminder; introduced in group 3)

**Drafting sources, in trust order.**
- ValDX: `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L11–20 (inverse problem, reweighting and model dependence); `2_hdx_theory_omc.tex` (EX2 assumption); `6_methods_omc.tex` L356–465 (weight/parameter fitting, BV averaging, regularisation and Bayesian interpretation).
- jaxENT: `projects/2-jaxENT/manuscript/report/introduction.tex` L4 and L10 (prior dependence and unified weight–parameter fitting). Check the broader novelty claims at L8 against the earlier HDXer literature before reusing them.
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex` L83 onward (expository sequence and equations). Reuse its explanations with the qualifications above.
- KB papers: [[@bradshawInterpretationHDXData2020]] and [[@leeInterpretingHydrogenDeuteriumExchange2021]] for HDXer; [[@berlinRecoveringRepresentativeConformational2013]] and [[@hummerBayesianEnsembleRefinement2015]] for underdetermination; [[@cesariUsingMaximumEntropy2018]] for relative MaxEnt and treatment of error; [[@bmsb2012ch12]] for forward/error models and parameter inference.

**Kept for Chapter 2:** BV and uptake equations, the likelihood, KL divergence and Lagrange-multiplier derivations, importance-sampling diagnostics, and comparisons with experimentally restrained simulations. The [[reference ratio method]] is an optional conceptual precedent there; [[The meaning of a statistical correction depends on the reference distribution implied by the model or sampling procedure.]] is supported but need not carry the introductory argument.

### Gaps (1.4)
- Assemble a claim note for why both ensemble weights and forward-model parameters must be considered during fitting, using the ValDX/jaxENT formulations and the relevant primary literature.
- The existing reweighting claim includes mis-cited papers; use Bradshaw and Lee for the operation described in group 3.
- Support the HDX-specific MaxEnt statement in group 4 with Bradshaw/Lee, rather than relying only on general MaxEnt or NMR sources. Use Berlin/Hummer for underdetermination instead of the confirmation introduction's Lee/Cesari citations.

## 1.5 Trusting Integrative Ensemble Models

**Argument:** matching uptake does not establish the populations. Trust in a fitted ensemble comes from three things:
- predictive performance on data it was not fitted to;
- how sensitive it is to modelling and data choices;
- interpretable evidence for the inferred states.

The section follows the two risks named at the end of §1.4. After the non-uniqueness that motivates everything (group 1), group 2 takes the risks shared by any fitted model, which established statistics answers, and group 3 the risk specific to integration, a poor forward model. Groups 2 and 3 each open on the established principle, stated once with one general citation, then give its upshot for HDX-MS, then say what integrative practice does with it and what ValDX or jaxENT adds ([[2026-10-14 layered presentation of validation and uncertainty]]; full treatment in [[02-background]] §2.4). Candidates (group 4), what a comparison then supports (group 5) and cost (group 6) follow. ValDX supplies the central argument; jaxENT adds joint fitting and mapped uncertainty, but has no citable version yet.

**1. Non-uniqueness.** Pick up the §1.4 handoff. Different populations can produce the same uptake, so a good fit does not identify the ensemble ([[inverse problem]], identifiability). Keep posterior spread apart from physical populations ([[posterior uncertainty]]).
- [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]] (supported)
- [[Ensembles generally have far more degrees of freedom than observables, so a single data source leaves them underdetermined.]]
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]] (prefer the first claim)
- [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]] (supported)
- Revised ValDX only (`1_introduction_omc.tex` L17, not in v1): this holds even with a perfect forward model. Present it as the thesis's own statement.

**2. Standard statistics: generalisation, dependence and selection.** Training error is insufficient ([[overfitting]]). Regularisation and error models reduce overfitting but leave a validation problem ([[regularisation]], [[maximum entropy principle]]). Held-out data test prediction, but only as far as the partition respects the dependence between observations ([[data splitting]]). For HDX-MS the dependence comes first from overlapping peptides and then from cooperative unfolding, which couples residues that share no peptide, so structured splits reduce dependence without removing it. A validation error used to select a fit is no longer an unbiased estimate of performance ([[model selection]]), and replicate spread reflects the partition, not repeat measurement ([[replicate uncertainty]]). The divergence from practice is specific. Integrative HDX studies test robustness by omitting peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions built around peptide dependence; crystallographic ensemble refinement already selects its parameters by the cross-validated free R value ([[@burnleyModellingDynamicsProtein2012#^c1]]), so the gap is in the HDX setting, not in structural biology as a whole.
- Principle, layer 1b: [[When observations are dependent, a random partition gives optimistic validation error, so the partition should follow the dependence.]] (draft; general source to acquire, see [[02-background]] §2.4)
- [[Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is a good choice only when the prior is reasonable.]] (supported)
- [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]] (supported)
- [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]] (supported)
- [[Cooperative unfolding couples exchange at residues that share no peptide, so removing peptide overlap does not make training and validation peptides independent.]] (draft, inferred; the bridge between the two fields)
- [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]] (revised ValDX only)
- [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]] (supported; the ValDX result that makes the principle concrete)
- [[Selecting a model by its validation error makes that error optimistic, so performance must be estimated on data unused in selection.]] (draft; one sentence, with the jaxENT HDX-NMR evaluation as the instance, see [[Evaluation design (jaxENT)]])
- [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]] (draft)
- Practice: [[In the HDX ensemble-integration studies examined, robustness is assessed by removing selected peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions designed around peptide dependence.]] (draft, inferred; keep the scope "studies examined")
- Optional, if consensus fitting is named here rather than in ch. 3: [[Averaging fitted models reduces their variance but retains any error they share.]] (draft)
- [[With a uniform-weight MD ensemble as the prior, MaxEnt reweighting that models experimental error reduces overfitting and keeps the resulting ensemble close to the prior.]]

**3. Poor forward models: compensation and calibration.** If the forward model or the exchange assumptions are wrong, weights and parameters absorb the error ([[model misspecification]]). Keep three cases apart, because each changes the advice. A parameter can be uncertain (a posterior width), miscalibrated (wrong coefficients, fixed by refitting them), or the functional form can be inadequate (no coefficients fit, as under kinetic mismatch). Recalibration addresses only the second, and restoring agreement by calibration does not validate kinetics or populations. How frame predictions are averaged is itself a forward-model choice.
- [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]] (supported)
- [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]] (supported)
- [[Recalibrating forward-model coefficients can correct a miscalibration but not an inadequate functional form.]] (draft, inferred)
- [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]] (revised ValDX only)
- [[Uncertainty in nuisance parameters and regularisation choices can affect structural conclusions from Bayesian analyses of NMR and small-angle scattering.]]
- Optional, one clause at most: [[Averaging log protection factors, exchange rates or uptake over frames are different forward models, and held-out uptake error and population recovery can favour different choices.]] (jaxENT project doc only; detail in ch. 2 and ch. 4)

**4. Candidate coverage and decoys.** The fit can only weight what the candidates contain ([[sampling coverage]]). §1.4 group 3 has already said that missing states cannot be created; remind it in one line. The finding to carry is the converse, that plausible but unpopulated candidates can absorb weight while uptake still matches ([[ensemble reweighting]]).
- [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]] (supported)
- [[Reweighting cannot create conformational states absent from the candidate ensemble.]] (reminder)
- [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]]
- [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]] (supported)

**5. What a comparison then supports: Work Done, uncertainty and hypothesis testing.** Validation error alone cannot separate a good hypothesis from one forced into agreement, so [[Work Done]] adds how much fitting changed the starting hypothesis. Variation across replicate fits shows which conclusions depend on the data chosen ([[replicate uncertainty]]). It locates instability but does not identify its cause. Changing one suspected cause at a time is how a cause is tested ([[controlled perturbation]]). Representative structures make the inferred states inspectable, if conclusions survive a change of representation. End on integration as hypothesis testing, which hands over to the research questions (§1.6).
- [[Work Done quantifies how much an ensemble must be modified to match experiment.]] (supported)
- [[Low validation error with high Work Done signals agreement reached by excessive modification of the ensemble.]] (supported)
- [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]] (revised ValDX only)
- [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]] (supported)
- [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]] (revised ValDX only)
- [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]] (supported)
- [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]] (revised ValDX only)
- [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]] (supported)
- [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]] (jaxENT, draft)

**6. What repeated assessment costs, and what it cannot reach.** Two points, and they motivate Q3 and chapter 5. First, every check in groups 2 and 5 repeats the fit. Splits, replicates, parameter settings and candidate ensembles multiply (ValDX ran 3 replicates × 2 or 4 split types per ensemble across 22 ensembles, with a γ sweep in each), so the cost of one fit bounds how much validation is affordable. Efficiency is a condition for validation, not a convenience. Second, reweighting can only redistribute weight over the candidates it is given, so where coverage fails the data have to act during sampling or generation. End the section on the hand-off to §1.6 as hypothesis testing with these two limits named.
- Claim to write (ours, `basis: inferred`, draft): validation by splits and replicates multiplies the number of fits, so the cost of a single fit bounds how much assessment is affordable. Origin `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L473 and L619; leaves draft with a jaxENT runtime figure ID.
- [[Reweighting cannot create conformational states absent from the candidate ensemble.]] (stated in group 4, reminded here as the motivation for ch. 5)

**Drafting sources.**
- ValDX revised manuscript (`projects/1-ValDX/manuscript/report/`):
  - `1_introduction_omc.tex` L11–37;
  - `7_results_omc.tex` L4–30 (the Work Done framework), L42–60 (TeaA), L189–211 and L248 (kinetic misspecification), L235–248 (clustering and limitations);
  - `6_methods_omc.tex` L52, L70, L510.
- ValDX posted v1: [[@siddiquiFrameworkTestingStructural2026]]. This is the version to cite; its wording differs from the revision.
- jaxENT (`projects/2-jaxENT/manuscript/report/`): `introduction.tex` L4–10; `results.tex` L29 (validation regimes), L63 and L130 (decoys), L173–197 (uncertainty maps).
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex` L87–95. Most of it belongs in §1.4. Here it explains why regularisation still leaves a validation problem.

**Wording to avoid:**
- "Small Work Done means the ensemble is correct". v1 p. 4 reads it that way; the revision says it is distance from the prior, not to the truth.
- "Structured splits give independent validation" or "ensure that validation error reflects true predictive performance" (v1; revised `1_introduction_omc.tex` L26, `7_results_omc.tex` L28).
- "Uncertainty distinguishes sampling from force-field limitations" (jaxENT Fig. 5 caption, `results.tex` L203–207). This conflicts with ValDX.
- "Work Done allows precise statements about structural hypotheses" (v1).
- "Systematic errors accumulate at the peptide level" (ValDX `1_introduction_omc.tex` L20). Its four citations do not support it; use the BV-coefficient claim.
- "MaxEnt avoids overfitting and ensures physical plausibility" (confirmation L95).
- BMSB ch13's quantitative results (Shannon channels, number of good parameters) are specific to SAXS and SANS. Cite them as an example of low-information data, not as facts about HDX-MS.

### Gaps (1.5)
- **Revised-only claims:** five claims and the perfect-forward-model sentence are only in the revised ValDX manuscript. They become supported once a revised preprint is posted and its PDF replaces v1 in `kb/_pdf/`.
- **jaxENT:** no citable version, so the decoy, joint-uncertainty and validation-regime points stay draft.
- **Missing-state claim:** it is inferred from how reweighting works (Lee ^c7, Bradshaw ^c7). The revised ValDX states it without a citation.
- **Nuisance-parameter claim:** it still needs a passage showing a changed structural conclusion, from Habeck Fig. 12.10 (pp. 22–23) or Hansen Fig. 13.8.
- **Generated-diversity sentence:** it had no citation in the earlier draft. If it returns, BMSB ch2 supports the sampling half of it; consider `\supercite{bmsb2012ch2}`. The generator-distribution claim needs a source on learned generators; BMSB's example is a local fragment model (TORUSDBN).
- **Efficiency claim (group 6):** no note yet. It needs a jaxENT runtime figure ID or a quote from a posted jaxENT version before it leaves draft.
- **Bib entry:** `siddiquiFrameworkTestingStructural2026` was appended by hand to `thesis/references.bib`. Add it in Zotero too, or the next Better BibTeX export will drop it.
- **Review status:** all papers are `read: false`, and all quotes are `reviewed: false`, including the ValDX ones.
- **Unused BMSB chapters:** chapters 5–11 (statistical-potential learning, directional statistics, alignment, local structure models, side chains) are not yet used. They are background or methods material if needed.

## 1.6 Research Questions and Objectives

**Argument.** §1.5 named three conditions for trusting a fitted ensemble. Each question turns one of them into a problem the research chapters can test. Under each, list the Chapter 2 concepts it draws on, the claims it rests on, and what stays open. §1.7 maps the chapters to the questions, and ch. 7 answers them.

- **Q1.** How can we reliably assess integration in cases where there is no ground-truth? How can we leverage uncertainty to identify the sources of instability in structural hypotheses?
  - Raised by §1.5 groups 2 and 5. Held-out validation is only as honest as the partition, and replicate spread locates instability without naming its cause.
  - Concepts. [[inverse problem]], [[data splitting]], [[Work Done]], [[replicate uncertainty]], [[posterior uncertainty]], [[controlled perturbation]].
  - [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]] (supported)
  - [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]] (supported)
  - [[Work Done quantifies how much an ensemble must be modified to match experiment.]] (supported)
  - [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]] (supported)
  - [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]] (supported)
  - [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]] (revised ValDX only)
  - Open. Uncertainty localises instability. Attributing it to sampling, structure or the forward model needs controlled perturbations, one suspected cause at a time.
- **Q2.** How can we integrate knowledge, statistics and physics during integration to improve the reliability of structural hypotheses?
  - Raised by §1.5 group 3 and §1.4 group 6. Weights can absorb forward-model error, and established tools fit weights and forward-model parameters in stages.
  - Concepts. [[maximum entropy principle]], [[Bayes' theorem]], [[nuisance parameter]], [[regularisation]], [[forward model]], [[knowledge-based potential]], [[force field]], [[metainference]].
  - Roles. Physics proposes candidate conformations and sets the exchange assumptions. Knowledge supplies prior weights, parameter ranges and structural filters. Statistics models data errors and their correlations, balances fit against modification, and tests generalisation. The forward model connects structure to the observable, and its parameters are inferred with the weights.
  - [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]] (supported)
  - [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]] (supported)
  - [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]] (revised ValDX only)
  - [[Metainference infers an uncertainty for each datum alongside the structures, so the restraint weakens where data or forward model are unreliable.]] (supported)
  - Open. When an added constraint improves structural inference rather than absorbing error. Fitting order is conditional on the suspected mismatch.
- **Q3.** How can we improve the efficiency of integration to enable its application to larger and more complex systems?
  - Raised by §1.5 group 6. Every check repeats the fit, and reweighting cannot reach states the candidates lack.
  - Concepts. [[clustering]], [[enhanced sampling]], [[Boltzmann generator]], [[guided diffusion]], [[importance sampling]].
  - Three costs, each reduced differently. Representation (fewer structures to fit and inspect), fitting (differentiable, compiled joint optimisation), and sampling (effort spent where it adds information).
  - [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]] (supported)
  - [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]] (supported)
  - [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]] (draft, inferred)
  - Open. Efficiency of the whole workflow, from feature calculation through generation to validation and uncertainty. jaxENT's speedups are provisional until re-run on the current code.
- **Q4.** How can we build interpretable models for protein dynamics that allow us to answer mechanistic questions about their dynamics?
  - Raised by §1.1 group C and §1.5 group 5. Weighted ensembles say which states are occupied, and the mechanistic questions of §1.1 D need to know which conclusions those states can carry.
  - Concepts. [[population shift]], [[conformational free-energy landscape]], [[high-energy intermediate]], [[allostery]], [[clustering]], [[conformational kinetics]]. Systems [[BPTI]], [[prion protein]], [[alpha-synuclein]].
  - [[Ensemble similarity scores compare equilibrium distributions and do not capture changes in dynamics or transition rates.]] (supported)
  - [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]] (supported)
  - Reminder of §1.1 group C, one line only: [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]] (draft, inferred; its home is §1.1 C)
  - Open. Weighted states support statements about what is occupied and what it looks like. Causal mechanisms, transition order and rates need kinetic evidence.

**Wording to avoid.**
- "Uncertainty distinguishes sampling from force-field limitations" (jaxENT `results.tex` L203–207).
- A recommended fitting order stated without its condition.
- Pathways, transition order or rates read off fitted weights.
- The α-synuclein Tris interpretation as an established mechanism.
- jaxENT speedups from the outdated experiments.

### Gaps (1.6)
- The questions are draft wording. Keep the numbers if they are reworded.
- BPTI's primary HDX source, [[@kimHydrogenExchangeIdentifies1993]], now has a PDF and blocks but no claim note.
- jaxENT's observation weighting and selection now have method notes ([[Observation weighting and selection (jaxENT)]], [[Evaluation design (jaxENT)]]). The parameter penalty, interval-hazard uptake, graph-Laplacian regulariser and uncertainty maps still have none, so for those the Q2 and Q3 bullets point to manuscript and code.
- No source on Markov state models or other kinetic methods supports the Q4 boundary from the kinetic side.

## 1.7 Thesis Outline and Contributions

**Argument:** the four questions in §1.6 are taken up by four research chapters that move from assessing an integration (ch. 3) to performing it jointly and quickly (ch. 4), then to letting the data act during sampling and generation (ch. 5), with a differentiable protonation model (ch. 6) that the pH-dependent cases need. Each research chapter gets one paragraph with four fixed elements: the problem it answers (the §1.1 or §1.5 point that exposed it), the contribution, the validation regime, and the limitation it hands to the next chapter. A fixed status sentence closes each paragraph, so the examiner knows which results the thesis is held to. Architecture, loss-function and training detail stays out of the outline; it lives in the research-chapter hubs ([[03-valdx]], [[04-jaxent]], [[05-biofeaturisers]], [[06-jax-ka]]).

Register: jaxENT compression for contribution statements, each bounded by its validation regime ([[style]] §Registers; [[examples]] 7). There are no literature markers here. A contribution is a claim about the thesis's own results and leaves `draft` only with a figure ID, or with a quote from the posted ValDX preprint. Chapter 3's contributions already exist as §1.5 claims and are reused; chapters 4 to 6 need new claim notes (`project:` set, `figures:` filled).

**1. The arc, in one paragraph.** §1.5 named three conditions for trusting a fitted ensemble, and §1.6 turned them into questions. The chapters answer them in order of decreasing control over the candidates. ValDX scores fits to fixed candidate ensembles where references exist (Q1). jaxENT fits weights and forward-model parameters together, fast enough to repeat the fit across splits and replicates (Q2, Q3). BioFeaturisers moves the same forward models into sampling and generation, so the data can reach states the candidates lacked, which §1.5 groups 4 and 6 set as the limit of reweighting (Q2, Q3, Q4). jax-Ka extends the differentiable forward-model idea to protonation (Q2, Q4). From chapter 4 onward one technical thread holds. A forward model with gradients can score, reweight, restrain and guide, so one definition serves every stage. End on the boundary: chapters 3 and 4 reweight what they are given, and only chapter 5 can add states.

**2. Chapter 2 supplies, it does not contribute.** One sentence per block on what the research chapters draw from it (exchange kinetics and forward models; generators and their sampling distributions; MaxEnt, Bayesian refinement, restraints and guidance; validation and ensemble comparison; protonation, in proportion to ch. 6). The thesis's own formulations (Work Done, linear-additive uptake, graph-Laplacian regularisation, Heaviside-contact BV, metadiffusion) stay in their chapters ([[02-background]]).

**3. Chapter 3, ValDX, answers Q1 and opens Q4.**
- Problem (§1.5 groups 1 and 2). Agreement with uptake does not identify populations, and random splits leak through overlapping peptides, so a fitted ensemble has no honest validation error.
- Contribution. Overlap-aware splits, replicate fits and Work Done make integration a comparison of candidate hypotheses, with Work Done read as a distance from the prior rather than from the truth: [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]], [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]], [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]], [[Work Done quantifies how much an ensemble must be modified to match experiment.]], [[Low validation error with high Work Done signals agreement reached by excessive modification of the ensemble.]], [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]]. The result: [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]]. Representation and protocol, one sentence each: [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]], [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]], [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]].
- Regime. 22 ensembles of six proteins (58 to 480 residues); a synthetic kinetic mismatch; decoy conformations.
- Limitation handed on. Conclusions are comparative across the candidates supplied, reweighting cannot add states, replicate uncertainty does not name its cause, and each assessment repeats the fit many times (§1.5 group 6): [[Reweighting cannot create conformational states absent from the candidate ensemble.]], [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]].
- Status sentence: complete. Manuscript post-review; preprint v1 posted ([[@siddiquiFrameworkTestingStructural2026]]). The five "revised ValDX only" claims in §1.5 become supported once the revision is posted. The BiCePs comparison and other detail are in [[03-valdx]].

**4. Chapter 4, jaxENT, answers Q2 and Q3, and returns to Q1.**
- Problem (§1.4 group 6, §1.5 group 6). Established tools fit weights and forward-model parameters in stages with plausibility fixed by the method, and a validation protocol of splits and replicates multiplies the cost of every fit.
- Contribution. A differentiable MaxEnt engine that fits weights and Best–Vendruscolo parameters together, with plausibility constraints as loss terms (including a regulariser for candidates that carry no Boltzmann weights) and with splits and replicates built into the fit. Stub claim, `project: 2-jaxENT`, figure ID needed. HDXer already fits BV parameters; the contribution is the unified, composable fit, not parameter fitting itself.
- Regime. [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]] (draft): synthetic, an HDX-NMR reference, α-synuclein; runtime against HDXer. The draft abstract's figures come from outdated experiments and are re-derived before they appear.
- Limitation handed on. jaxENT still reweights fixed candidates, and its uncertainty maps localise instability without naming the cause; attribution needs a [[controlled perturbation]]. The α-synuclein Tris reading stays a hypothesis bounded by sampling and forward model.
- Status sentence: analyses complete; manuscript in draft. Due 14 Nov. Loss terms, the interval-hazard uptake form, the graph-Laplacian regulariser and the error weighting are in [[04-jaxent]].

**5. Chapter 5, BioFeaturisers, answers Q2 and Q3 during sampling, and Q4 through two mechanistic cases.**
- Problem (§1.5 group 6, §2.3). States absent from the candidates cannot be reweighted into existence, and no HDX collective variable with forces is published.
- Contribution. A library of differentiable forward models, so that one definition serves reweighting (jaxENT), restrained sampling (metadynamics–metainference) and guided generation (metadiffusion). Stub; the library and pipeline are what can be claimed now.
- Regime, in order of decreasing ground truth ([[examples]] 7). [[BPTI]] against the 1 ms Anton trajectory, a controlled reference. MoPrP at pH 4 and pH 7, a mechanistic question that depends on protonation (ch. 6). RORγ with agonist, partial-agonist and antagonist ligands, with no reference. Each case is written as what it tests.
- Limitation handed on. [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]]; a restraint is only as good as the forward model where the data are; and a pathway read from the MoPrP simulations needs the trajectories, not the weights (§1.1 group C, [[conformational kinetics]]).
- Status sentence: work in progress. Preliminary experiments; metadiffusion under development. Due 28 Nov ("metadynamics" in `DEADLINES.md`). Forward-model and case protocols are in [[05-biofeaturisers]].

**6. Chapter 6, jax-Ka, answers Q2 and Q4 for protonation.**
- Problem (the pH thread: §1.1 D3, §1.2 group 2, §1.3 group 2). The MoPrP data were taken at pD 4, the ch. 5 simulations run at pH 4 and pH 7, and our ensembles were protonated once at neutral pH, so which groups are protonated is an unverified input to every pH-dependent case.
- Contribution. A backbone-only pKa predictor whose readout differentiates through coordinates, a second forward model of the kind ch. 5 builds. Stub.
- Regime. pKPDB and PINDER bound and free states for training, PKAD for testing; application to which MoPrP sites change protonation between pH 4 and pH 7, and whether they sit in the regions that unfold.
- Limitation handed on. Interface experiments are open, and the MoPrP application is untested. Keep the paragraph proportional to the final chapter; [[02-background]] §2.5 is short and the titration models are introduced in the ch. 6 preface.
- Status sentence: in progress. **decision**: full research chapter, short chapter, or appendix. `DEADLINES.md` has no entry for it. Architecture, training sets and current numbers are in [[06-jax-ka]].

**7. Chapter 7 returns to the questions.** The conclusion answers Q1 to Q4 with the chapter evidence, names what stays open (equilibrium weighting of guided samples; forward-model error where data are sparse; the posted ValDX revision; and one item per question from §1.6, namely attributing instability, when added constraints help, whole-workflow efficiency, and kinetic or causal interpretation), and places the confirmation's future work (AlphaFold3 confidence benchmarking; jaxENT with SAXS and NMR) as extensions, not chapters.

**Map.**

| Chapter | Questions | Contribution, one line | Tested on | Status |
|---|---|---|---|---|
| 3 ValDX | Q1, Q4 | Splits, replicates and Work Done make integration a comparison of candidate hypotheses | 22 ensembles, six proteins; synthetic kinetic mismatch; decoys | complete; preprint v1, revision post-review |
| 4 jaxENT | Q2, Q3, Q1 | Joint differentiable fit with plausibility as loss terms; linear-additive uptake; graph-Laplacian regularisation | synthetic, HDX-NMR reference, α-synuclein; runtime vs HDXer | analyses complete; manuscript draft |
| 5 BioFeaturisers | Q2, Q3, Q4 | Differentiable forward models shared by reweighting, restrained sampling and guided generation | BPTI (Anton), MoPrP pH 4 and 7, RORγ ligand series | in progress |
| 6 jax-Ka | Q2, Q4 | Backbone-only relational oGQT pKa model, differentiable through coordinates | pKPDB, PINDER bound/free, PKAD; MoPrP pH 4 and 7 | in progress |

**decision**: contributions inline, one per chapter paragraph, closed by a four-sentence paragraph keyed to Q1 to Q4; or a separate bulleted list as in the confirmation and Crook §1.7. Inline is recommended; a list invites the unconditional phrasing below.
**decision**: chapter titles. The tex titles are project names; the outline reads better if each chapter carries a descriptive title that §1.7 can quote.
**decision**: one fixed status sentence per state, used verbatim across chapters ("This chapter is complete and posted as a preprint." / "This chapter reports completed analyses whose manuscript is in draft." / "This chapter reports work in progress.").

**Drafting sources.**
- Confirmation `milestones/2025-11-confirmation-of-status/introduction/thesis_outline.tex` (chapter summaries and contributions; its numbering is stale, ValDX was chapter 2) and `future_work/future_work.tex` (what moves to ch. 7).
- ValDX `0_abstract_omc.tex` and `1_introduction_omc.tex` L25–37; preprint note [[@siddiquiFrameworkTestingStructural2026]].
- jaxENT `abstract.tex`, `introduction.tex` final two paragraphs, `results.tex` L29 (validation regimes), `meta_analysis.tex` L1–10.
- Chapter tex comments (`03-valdx.tex` to `06-jax-ka.tex`) for ch. 4 to 6; the README project table and `DEADLINES.md` for status.
- Crook §1.7 "Thesis outline and contributions" (`examples/crook-map`) for the shape: chapter by chapter, each tied to the question it answers.
- The research-chapter hubs for the detail that was moved out of this section on 2026-10-14.

**Wording to avoid** (confirmation `thesis_outline.tex` and the jaxENT draft):
- "comprehensive workflow", "rigorous uncertainty quantification", "thermodynamically grounded", "robust indicators", "key innovation", "significantly improve", "high-performance".
- "Proof that differential HDX-MS experiments are no longer strictly required" and "absolute dynamics can be quantified from a single experiment". ValDX supports ranking candidates, not absolute dynamics.
- "Successful recovery of MoPrP misfolding intermediates and their populations". MoPrP is now a ch. 5 case in progress.
- "fundamental problem", "critical obstacles", "great synergy", "establish jaxENT as" (jaxENT draft).
- "4D visualisation" as a contribution. No chapter carries it.
- "heavy-side" (tex comments) is Heaviside.
- Stale chapter numbers from the confirmation.

### Gaps (1.7)
- §1.6 is draft wording, now numbered Q1 to Q4 so that §1.7 can map to it. If the questions are reworded, keep the numbers.
- No claim notes exist for the thesis's own ch. 4 to 6 results. Every stub above stays draft until a claim note with a figure ID exists. Ch. 3 reuses the §1.5 ValDX claims, five of which are "revised ValDX only".
- jaxENT's quantitative figures are from outdated experiments.
- Ch. 5 and 6 results are not yet obtained; their paragraphs claim the method and name what each case tests.
- jax-Ka scope is undecided and has no deadline.
- `thesis/frontmatter/abstract.tex` is empty; the abstract should reuse the four closing sentences.
- Publications and data collaborations: whether to list the preprint and collaborator data here or in the front matter.
- The research-chapter hubs ([[03-valdx]] to [[06-jax-ka]]) hold moved detail only; their argument order is not yet set.
