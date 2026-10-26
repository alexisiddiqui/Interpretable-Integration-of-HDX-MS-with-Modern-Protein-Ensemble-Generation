# 01 Introduction

Chapter hub: the argument in order, one claim per line. Sections follow `thesis/chapters/01-introduction.tex`.

## 1.1 Proteins as Dynamic Ensembles

**Argument.** Protein function depends on the conformations a protein occupies and on the transitions between them. Folding constrains the accessible conformational landscape, while local frustration at functional sites supports interconversion between native conformations. Disease-associated changes can alter their populations without changing the overall fold, or favour partially unfolded and aggregation-prone states. Understanding these effects requires descriptions of conformational ensembles under the conditions in which the protein functions.

**Section structure.** Why [[population shift|conformational populations]] matter for function and disease. The arc follows `01-introduction.tex` L7 in six groups: proteins are dynamic polypeptides → folding constrains the landscape globally → function frustrates it locally, and the consequence is dynamics → disease as a perturbation of populations → what structural methods record → the thesis problem. Folding versus function is the organising argument. Galpern and Parra supply its abstract anchors, allostery shows its dynamic consequence, and the three disease cases read as perturbations of one principle rather than as a list. The ValDX opener ("understanding protein dynamics is crucial to understanding biological function, and therefore disease", `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L8) closes group C, and the jaxENT synthesis belongs in group F. Each later section answers a need this section exposes, so a limitation is developed once, in its home section, and only reminded elsewhere.

**A. Proteins are dynamic polypeptides.** Proteins are polypeptide chains whose sequences govern folding and conformational behaviour. Even in the folded state, they occupy ensembles of conformations and undergo [[protein dynamics|motions]] spanning picoseconds to days. A crystal structure describes a conformation or averaged structural features of this ensemble, without specifying its full distribution in solution.

**Section structure.** The calmodulin example belongs in group E, where it shows what crystallography misses.

- [[Proteins are linear polymers whose sequences encode structures that fold rapidly and spontaneously.]]
- [[The rigid view of proteins has given way to one in which motions spanning picoseconds to days are essential to function.]]
- [[Even a folded protein is an ensemble of structures, and distinct crystal structures can be time-averaged members of one ensemble.]]

**B. Folding constrains the landscape globally.** Folding is an entropic search (Levinthal) that evolved sequences solve because they are minimally frustrated and fold down a rough funnel ([[conformational free-energy landscape]]). Accurate structure prediction does not establish the populations of alternative conformations or the rates of transitions between them. Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.

**Section structure.** Use Galpern for two conclusions only, that function needs information beyond folding ([[@galpernInformationtheoreticArgumentRestriction2026#^c9]]) and that folded and disordered proteins lie on one axis. The information-theoretic derivation (Eqs. 1 to 5, bits per site) stays in the paper note and does not enter the chapter.

- [[Folding poses an entropic search problem, and evolved sequences carry just enough information to solve it.]]
- [[Folding is possible because evolved sequences are minimally frustrated, giving a rough, funnel-shaped energy landscape.]]
- [[X-ray crystallography, cryo-EM and NMR provide high-resolution structures of proteins.]]
- [[Leveraging large structure and sequence corpora, protein structure models predict structures rapidly and with high accuracy.]] (also in §1.3 group 4). For the scale of sequences against solved structures, cite the 2022 snapshot in Varadi ^c5.
- [[Despite structure prediction, the dynamics of folding remains a formidable problem that predictors and most experiments cannot resolve.]]
- [[AlphaFold2 can predict individual domains accurately while missing their relative motion.]]
- [[Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.]]

**C. Function frustrates the landscape locally, and the consequence is dynamics.** Minimal frustration is a global property. Interactions required for binding, catalysis and allosteric switching can conflict with those that stabilise the fold, producing local frustration at functional sites. The same sites drive interconversion between native conformations, so function depends on how the native [[structural ensemble]] is populated, often through slow, sparsely populated states. For an [[intrinsically disordered protein]] the ensemble is the principal structural description, and folded and disordered proteins sit at two ends of one landscape. [[allostery|Allostery]] is the demonstration, and it acts by two routes. A [[population shift]] among conformations the protein already visits changes function without a new fold, and a weighted ensemble can show it (D1). Altered motions without a large rearrangement, as in IGPS, where activation is driven by millisecond dynamics ([[@lisiAllosteryEnzymeCatalysis2017#^c7]]), need kinetic evidence, and this second route sets the boundary the thesis works within. Weighted ensembles describe which states are occupied; the order, rates and pathways of transitions need kinetic evidence ([[conformational kinetics]]).

**Section structure.** State the boundary here, once; Q4 reminds in one line.

- [[Folded proteins retain a minority of highly frustrated contacts, clustered at the surface.]]
- [[Highly frustrated sites mark where proteins bind partners, catalyse reactions and switch allosteric states.]]
- [[Function conflicts with folding, so sequences encode function locally at sites that sacrifice stability.]]
- [[Local frustration drives interconversion between native conformations, coupling function to slow, high-energy states.]]
- [[Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles.]]
- [[Long-range contacts within intrinsically disordered protein ensembles may contribute to function.]]
- [[Intrinsically disordered proteins require an ensemble description rather than a single structure.]]
- [[Folded proteins have well-defined free-energy minima, whereas intrinsically disordered proteins sample relatively flat landscapes.]]
- [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]] (own; its home is here)

**D. Disease as a perturbation of populations.** Disease-associated changes in conformational populations can alter function while preserving the overall fold ([[dynamic disease mechanism]]).

**Section structure.** Three cases, ordered by how much a single structure can show, each establishing one distinction. A population shift shows function changing while the structure is preserved. α-Synuclein shows a solution ensemble that only makes sense as a whole. The prion protein shows partially unfolded intermediates that the endpoint structures cannot reveal, and introduces pH as a condition of the populations. The general misfolding discussion is folded into the D2 and D3 leads; no further example is added unless it establishes another distinction.

*D0. Framing.*
- [[Disease mutations can destabilise functional states or over-stabilise states that impair function.]]
- [[Disease-associated variants perturb local frustration more than benign variants.]]
- [[Conformational dynamics can inform therapeutic strategies for allosteric regulation and protein aggregation.]]

*D1. Population shift: structure preserved, function changed* ([[allostery]]). Mutations reshape the [[conformational free-energy landscape]] without changing the fold. PKA is the structure-preserved illustration, not a disease case ([[@lisiAllosteryEnzymeCatalysis2017#^c6]]), and EGFR carries the disease link. That resistance arises without a steric clash holds for T790M as Sutto interprets it ([[@suttoEffectsOncogenicMutations2013#^c3]]), not for PKA.
- [[A single mutation can leave the crystal structure unchanged yet strongly alter function.]]
- [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]]
- [[Kinases and their inhibitor resistance mutations often preserve drug-binding sites while shifting conformational equilibria.]]
- [[EGFR L858R and T790M mutations rigidify sub-domains and shift equilibria toward active states, preserving active-site geometry.]]
- [[EGFR T790M inhibitor resistance can arise through active-state stabilisation without steric obstruction of the inhibitor-binding site.]]

*D2. α-Synuclein: the heterogeneous solution ensemble behind a solved fibril.* Open with the shared-transition claim as the bridge from D1 to the aggregation diseases. In [[alpha-synuclein]] the fibril is solved ([[@yanCryoEMStructuresInfectious2026#^c1]], [[@dhavaleStructureAlphasynucleinFibrils2024#^c1]]), but the protective state is a disordered ensemble whose protection lies in an autoinhibitory N- to C-terminal contact ([[@mukherjeeProteinMisfoldingAmyloid2024#^c6]]). One paragraph.
- [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]] (the bridge sentence)
- [[Heterogeneous, rapidly interconverting misfolded oligomers are difficult to characterise at high structural resolution.]]
- [[Differences in conformational dynamics can influence aggregation of amyloidogenic immunoglobulin light chains.]]
- [[These neurodegenerative diseases involve transient oligomeric intermediates that never crystallize.]]
- [[Differences in conformational dynamics relate to the aggregation of amyloidogenic light chains.]]
- [[Alpha-synuclein is an unfolded monomer, yet cryo-EM has solved its Lewy body fibril structures at atomic resolution.]]
- [[Cryo-EM fibrils are helical but the solution state is disordered, so aggregation-prone states can escape standard methods.]]
- [[Soluble alpha-synuclein adopts an autoinhibitory conformation in which N- to C-terminal contacts protect the aggregation-prone NAC domain.]]
- [[Disrupting alpha-synuclein's autoinhibitory conformation exposes the NAC domain and is likely to lower the nucleation barrier for aggregation.]]
- [[In soluble alpha-synuclein, an electrostatic interaction between the N- and C-termini protects the aggregation-prone NAC domain, and disrupting it is likely to lower the nucleation barrier.]]

*D3. Prion protein: partially unfolded intermediates, and pH as a condition.* The endpoints are solved and the path between them is not. The intermediates on that path are sparsely populated, so what is needed is the intermediates and their populations, not only the endpoints, and [[prion protein|MoPrP]] populates its β-rich intermediate only at acidic pH. This is where pH enters the biological motivation. §1.2 group 2 carries it to the measurement, §1.3 group 2 to the simulation, [[02-background]] §2.2 supplies the chemistry, and chapters 4 to 6 use MoPrP at pH 4 and pH 7.
- [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]]
- [[A familial prion-disease variant populates a more heterogeneous ensemble with thermally accessible misfolded states.]]
- [[Conformational conversion of oligomeric intermediates can limit the rate of protein aggregation.]]
- [[High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.]]
- [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]]
- [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]]
- [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]] (own framing)
- [[Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH, and urea is needed to populate it substantially.]] (the pH condition)
- [[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]]. State the protonation half here; the HDX-MS half is the MoPrP example in §1.2 group 3.

**E. What structural methods record, method by method.** This is the home of the structural-method limitations, so each method gets its own limitation and one example rather than a shared generic sentence. The disease cases in D already show some of these; recall them in a clause rather than re-explaining.
- *[[X-ray crystallography]].* A crystal structure is a time average of an ordered lattice ([[@lisiAllosteryEnzymeCatalysis2017#^c5]]). Example: [[NMR relaxation showed the central helix of calmodulin is flexible in solution, though it appears rigid in crystal structures.]]. The PKA time-average reading ([[@lisiAllosteryEnzymeCatalysis2017#^c5]]) is already in group A, and the unchanged crystal structure under a functional mutation is D1.
- *[[cryo-EM]].* It removes the need for a crystal but still reconstructs well-populated end states. Example: the α-synuclein fibril against its disordered solution state (D2, one clause).
- *[[NMR]].* It works in solution and across timescales, so it is the one of the three that reports motion in solution directly, but sensitivity and spectral complexity limit the size of system it can study, and its deposited structural ensembles are not thermodynamic ensembles.
  - [[NMR works in solution like HDX-MS but also gives structural information and is sensitive over a wide range of timescales.]]
  - [[NMR typically needs larger samples and is limited to smaller proteins or domains by sensitivity and spectral complexity.]]
  - An NMR ensemble is not a thermodynamic ensemble ([[@bmsb2012ch12#^c3]]). Cross-reference §1.5 group 1: [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]].
- *What all three find hardest.* Transient, sparsely populated intermediates under the conditions that populate them, which are the states D3 needs.
  - [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]]; its second citation, [[@biancanielloStructureDynamicsMisfolding2025#^c9]], states for the T183A prion variant that integrative approaches are needed because X-ray crystallography, NMR and cryo-EM cannot capture its dynamic intermediate species. Biancaniello ^c2 (techniques mainly target rigid states) is further support not yet on the note.
  - [[Linking fast molecular motions to slow pathological processes requires conformational dynamics that static structures cannot capture.]]
  - [[Time-averaged crystal structures do not resolve the motions within a protein's conformational ensemble.]]
- *Scale of the gap*, one sentence: [[Only about 12,000 experimental structural ensembles exist, covering 21% of CATH superfamilies, so dynamic data are scarce.]] or [[Tools to estimate protein dynamics are decades old, but public datasets hold only thousands to tens of thousands of entries.]] (use one). The NMR caveat above means the count overstates what is known about populations.
- *Conditions.* [[Conformational populations depend on molecular context, so they are defined only for a stated environment.]]. This sets up the requirement in F that a measurement work under stated conditions.
- Framing claims, if a summary sentence is needed at all: [[Relating protein structures to function and disease requires information about conformational dynamics.]] or [[Static structures alone cannot explain many biological phenomena; dynamics underlie disease mechanisms and drug response.]] (use one). They add no example, so they cannot replace the method-by-method limitations.
- Other method-specific support: Pelikan ^c4 (disorder and heterogeneity obstruct classical methods), Li ^c1 (GPCR signalling is hard for crystallography and NMR, and HDX-MS could help), James ^c6 (cryo-EM has outpaced the modelling of disordered regions).

**F. What a measurement must offer, and the thesis problem.** Estimating the contribution of each conformational state to an experimental observable requires its relative population ([[structural ensemble]]). Constraining these populations requires measurements made in solution, under stated conditions, on systems of realistic size, and sensitive to sparsely populated states. [[HDX-MS]] meets these requirements, which is why it is the measurement the thesis integrates. Frustration analysis, by its authors' own account, also needs generated ensembles rather than one structure (Parra ^c25, ^c27). Generated ensembles can be constrained by solution measurements, and the question the thesis takes up is how to assess the explanation that results.

**Section structure.** Name HDX-MS here with what it can see; §1.2 explains how. End on the problem as the thesis's own statement, with no claim behind it. §1.2 asks what the measurement records, §1.3 where the candidates come from, §1.4 how they are fitted, and §1.5 what the fit can be trusted to mean.

- [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]
- [[Quantifying state populations requires experimental measurements of protein dynamics.]] or [[Without experimental measurements of protein dynamics, the biological mechanism of misfunction can remain unclear.]] (use one)
- [[Allosteric communication remains poorly characterised in most biological systems.]]
- The thesis problem, from jaxENT (`projects/2-jaxENT/manuscript/report/introduction.tex` ¶1): "Protein conformational dynamics govern biological function and modulate disease-associated conformational states, necessitating their representation as diverse structural ensembles rather than single static models" (cite `moulickPartiallyUnfoldedForms2015`, `bonomiPrinciplesProteinStructural2017`).
- What HDX-MS offers against E:
  - scope: [[HDX-MS can study many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools.]] ([[@jamesAdvancesHydrogenDeuterium2022#^c2]]);
  - rare states: exchange of otherwise inaccessible amides needs rarely populated open conformations, so hydrogen exchange reports on them ([[@vendruscoloRareFluctuationsNative2003#^c7]]), which links back to [[Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.]] in group B;
  - ensembles: [[HDX data report on ensembles and can reveal conformational landscapes that differ from the crystal structure.]]

**Drafting sources.**
- Anchors:
  - [[@galpernInformationtheoreticArgumentRestriction2026]] for B (conclusions only);
  - [[@parraFrustrationPhysiologyMolecular2025]] for B to E; its gene-network and psychiatry analogies (§§13–14) are analogies, its hemoglobin sentence (^c33) is a framing image, and specific disease results cite their primary study where the KB has it;
  - [[@galpernProbingDarkEnergy2026]] for B and C;
  - [[@lisiAllosteryEnzymeCatalysis2017]] for the allostery demonstration in C;
  - the [[dynamic disease mechanism]] concept for D and E.
- Confirmation `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex`:
  - the database-size figure (`figures/database_sizes.png`) fits group B or E;
  - its disease paragraphs map onto D;
  - reorder its material; do not reuse its opening.

### Gaps (1.1)
- A citation for cryo-EM reconstructing well-populated end states.
- A citation for allostery acting by population shift.

## 1.2 Measuring Protein Dynamics

**Argument.** Hydrogen–deuterium exchange mass spectrometry ([[HDX-MS]]) probes protein behaviour in solution by measuring the exchange of backbone amide hydrogens with solvent deuterium. Exchange depends on intrinsic chemistry and on protection associated with hydrogen bonding, burial and conformational opening. Peptide uptake curves are therefore sensitive to changes in the conformational ensemble, but do not uniquely identify the structures responsible. Structural interpretation requires candidate conformations and a model that relates them to the measured uptake.

**Thread for 1.2–1.5.** Sections 1.2 to 1.5 share one thread: HDX-MS constrains ensembles only through an indirect [[forward model]], so the inferred populations depend on the candidate ensemble, the forward model and their uncertainties. The grounding for 1.3–1.5 comes mainly from BMSB (Hamelryck et al. 2012) chapters 1–4, 12 and 13.

**Section structure.** Six steps, strengths before limits. Exchange theory stays in Chapter 2 (see below).

**1. What is recorded.** Backbone amides exchange with solvent deuterium, and MS reads this as a mass increase of peptides over labelling time ([[deuterium uptake]]).
- [[Different methods can measure protein dynamics, depending on the system, timescale and experimental conditions.]]
- [[HDX-MS measures protein conformational dynamics in solution.]]
- [[HDX-MS measures the exchange of backbone amide hydrogens with deuterium in the solvent.]]
- [[Measuring the mass increase of peptides over time lets HDX-MS report on protein dynamics and conformational changes.]]

**2. What sets the rate.** Intrinsic chemistry ([[intrinsic exchange rate]]) and local protection from hydrogen bonding, burial and transient opening ([[Linderstrøm–Lang model]], [[protection factor]]). The intrinsic rate depends on pH and temperature, so uptake, and the populations later inferred from it, hold for the stated pD and temperature. This is the measurement's side of the pH thread opened in §1.1 D3.
- [[Amide exchange rates depend on intrinsic chemistry and on local protection from hydrogen bonding, burial and transient opening.]]
- [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]]
- [[The HDX rate depends on the local environment of the amide hydrogen, including solvent accessibility and hydrogen bonding.]] (read it with the second caution in group 5)
- [[His, Asp and Glu neighbours change intrinsic exchange rates with pH through their own ionisation.]] (the neighbour half of the pH dependence)
- The intrinsic exchange rate depends on pH and temperature through its acid-, base- and water-catalysed terms, so uptake is defined for the stated pD and temperature ([[intrinsic exchange rate]]; source [[@baiPrimaryStructureEffects1993#^c2]]). The jaxENT MoPrP data were taken at pD 4.
- $P_f$ is a ratio of rates ([[protection factor]]).

**3. What it can show.** Strengths come before limits, so the reader knows what the measurement is for before learning where it stops. Two examples, one general and one on the thesis's own system. Group F of §1.1 has already named the scope and the rare-state sensitivity; recall them in a clause, not again in full.
- [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]] (the one disease example that only HDX-MS supplies)
- [[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]]. The HDX-MS half. It shows a pH-dependent change in protection on MoPrP, the system of chapters 4 to 6, and carries the pH thread from group 2.
- [[The primary benefits of HDX-MS are sensitivity, flexibility and low sample needs compared with other biophysical techniques.]]
- [[HDX-MS flexibility and increasing throughput make it well suited to challenging targets such as GPCRs, antibodies and IDPs.]]
- [[Orthogonal to X-ray, cryo-EM and NMR, HDX-MS probes protein dynamics in solution under diverse conditions.]] (solution conditions only; peptide resolution sets a size limit, James p16, so breadth is the scope claim in §1.1 F)
- Reminder only: [[HDX-MS can study many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools.]] (stated in §1.1 F)

**4. What the readout resolves.** Overlapping peptides, not residues or atoms. This is the price of the strengths in group 3.
- [[Conventional peptide-level HDX-MS reports uptake averaged over the exchangeable amides within each fragment.]]
- [[HDX-MS data alone do not give the atomic positions that NMR, crystallography and cryo-EM provide.]]

**5. Why interpretation is ambiguous.** Different local environments or populations can give the same uptake. A change in uptake shows a change in protection, not a mechanism.
- [[Under matched exchange conditions, an HDX-MS uptake change identifies altered protection but does not identify the structural event responsible.]]
- [[Under matched exchange conditions, greater deuterium uptake indicates less protection from exchange, not directly greater flexibility.]] (own)
- [[Under EX2, labelling time measures accumulated exchange rather than the duration of a conformational motion.]] (own)
- Non-uniqueness is developed in §1.5 group 1 ([[Ensembles generally have far more degrees of freedom than observables, so a single data source leaves them underdetermined.]]); here, one sentence at most.

**6. Why simulations are the complement, and the handoff to §1.3–1.4.** The limits in groups 4 and 5 are exactly what an atomic model supplies. Protection is a property of the ensemble, not of one structure, so a residue whose environment differs between conformers needs those conformers, and peptide uptake cannot pin residue protection down on its own. Connecting uptake to structure therefore needs candidate conformations and a model that predicts exchange from them ([[forward model]]), which makes interpretation an [[inverse problem]]. Others have already combined the two, mainly for simpler systems, so the open question is where the candidates come from (§1.3) and how they are weighted (§1.4).
- Equilibrium protection factors are a property of a Boltzmann ensemble, so no single conformation is expected to satisfy all of them ([[@vendruscoloRareFluctuationsNative2003#^c5]]).
- [[A single protection factor per residue cannot describe a residue whose environment differs between populated conformers.]]
- [[Residue protection factors are generally underdetermined by peptide-level uptake.]]
- [[To quantitatively connect measurements of dynamics to biological mechanisms, they must be interpreted in structural terms.]]
- [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]]
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]]
- [[Several groups have restrained simulations or pruned ensembles post hoc with HDX-MS data, mainly for simpler systems.]] (the precedent, and its "simpler systems" is the opening for the thesis)
- [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]]

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

## 1.3 Estimating Protein Dynamics

**Argument.** Computational methods provide candidate conformations with which to interpret experimental measurements. Their value depends on which states they sample, how accurately they estimate their populations and whether they describe the transitions between them. These are distinct requirements. Molecular dynamics, enhanced sampling and learned generators address them in different ways, and greater structural diversity does not by itself establish accurate populations. Experimental measurements provide constraints against which the resulting ensemble hypotheses can be assessed.

**Section structure.** Distinguish coverage, populations and kinetics throughout ([[sampling coverage]]). Five paragraphs, as in the outline; equations and algorithms stay in Chapter 2.

**1. Candidate ensembles.** A [[structural ensemble]] is a set of candidate conformations. A sampler can get coverage, populations and kinetics right or wrong separately ([[conformational free-energy landscape]]).
- [[Deep-learning methods can predict protein structures across entire proteomes.]]
- [[Characterising transitions between generated conformations requires sampling the intervening states.]]
- Already in §1.1 group F: [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

**2. MD and its limits.** [[molecular dynamics]] gives physically grounded trajectories, but only for its approximate [[force field]] and only once sampling has converged ([[equilibration and convergence]]). Five claims and one line on protonation, the simulation's side of the pH thread.
- [[MD simulations numerically integrate Newton's equations of motion, giving atomistic insight into protein dynamics over time.]]
- [[MD simulations can model varied conditions such as temperature, pressure, pH and the presence of ligands or other biomolecules.]]
- [[MD is computationally expensive and may only approximate true dynamics due to force-field inaccuracies and limited sampling.]]
- [[MD lets researchers study how proteins respond to different environments, giving insight into functional mechanisms.]]
- [[Physics-based methods are useful for detailed analysis but limited by the computational cost of equilibration.]]
- [[Sampling is limited because equilibration must be repeated for each new system or starting conformational state.]]
- [[Sufficiently sampled equilibrium MD targets the Boltzmann distribution of its approximate force field, not the protein's true distribution.]] (own)
- [[Until MD has converged, its statistics depend on the starting structures; reproducibility across independent starts is the basic check.]]
- [[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]. A pH 4 ensemble is only as good as the states assigned; chapter 6 takes this up ([[02-background]] §2.2). The thesis's own case, [[Our candidate ensembles were protonated once at pH 7 or 7.4, so a pH 4 ensemble depends on protonation states that were not assigned for pH 4.]], belongs in §1.7 and chapter 6, not here.

**3. Enhanced sampling.** Two families ([[enhanced sampling]]). Biasing the energy recovers equilibrium probabilities by reweighting but usually loses kinetics. Adaptive seeding broadens exploration, but pooled frames are not populations. Broader sampling does not by itself establish equilibrium populations.
- [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]]
- [[The metadynamics bias encourages exploring new states by discouraging revisits to previously sampled configurations.]]
- [[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]]
- [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]]
- [[Frontier Expansion Sampling restarts simulations from low-density regions of the sampled conformational space.]]
- [[Frontier Expansion Sampling selects seeds from Cartesian coordinates and can be extended to simulations with different topologies.]]
- Optional detail: [[Online analysis of collective variables can adaptively guide sampling towards underexplored regions of conformational space.]]
- [[Adaptive seeding can select starting structures using collective variables or coordinates obtained by dimensionality reduction.]]

**4. Learned generators, including diffusion.** Three kinds of model, which the confirmation runs together:
- **Structure predictors adapted for diversity.** Perturb the input ([[MSA subsampling]]) or the seed. Output frequencies have no defined target distribution.
  - [[Protein structure models predict three-dimensional structures from amino-acid sequences.]]
  - [[Leveraging large structure and sequence corpora, protein structure models predict structures rapidly and with high accuracy.]]
  - [[As protein structure models are primarily trained on static structures, their ability to predict dynamics is limited.]]
  - [[AlphaFold2 is trained on PDB structures to predict the structure most likely to appear in the PDB.]] (the reason the adaptations below are needed)
  - [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]]
  - [[Sub-sampling multiple sequence alignments alters the contacts described to the model, leading to diverse structural predictions.]]
  - [[MSA subsampling generates candidate conformations whose relative probabilities require further estimation.]]
  - [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]]
- **Generators trained to sample a distribution.** A [[diffusion model]] learns the training-data distribution by learning to denoise; a [[Boltzmann generator]] is trained toward the Boltzmann distribution and reweighted to it.
  - [[Deep-learning models rapidly generate structures and ensembles by sampling a learned distribution of conformational space.]]
  - [[Deep-learning models trained on large structural datasets learn conformation distributions, and sampling them yields ensembles.]]
  - [[Diffusion models are trained to reverse a noising process and generate structures by progressively denoising random samples.]]
  - [[PDB-trained diffusion models learn conformations represented in a structural database rather than equilibrium populations under specified solution conditions.]] (what the learned distribution is, and why it is a prior)
  - [[Diffusion steps are not physical simulation time.]] (own)
  - [[Diffusion models generate protein structures through iterative denoising.]]
  - [[Learning the physical landscape can reduce the cost of sampling new states while retaining the accuracy of the underlying physics.]] (Boltzmann generators only)
- **Learned force fields inside MD.** An MLFF improves the [[force field]], not the sampling.
  - [[Machine-learned force fields learn energies and forces for simulation, whereas Boltzmann generators generate configurations and reweight them to the Boltzmann distribution.]]
  - [[Ensembles can be generated by learning the physical landscape of protein systems directly from existing simulations.]]
- **Combining generators with MD.** Generators broaden coverage and MD relaxes the candidates; whether the result is representative still has to be assessed.
  - [[Learned generators are used to seed MD simulations, combining broad coverage with physics-based sampling.]]
  - [[Deep-learning generators can supply diverse starting structures for MD simulations.]]
  - [[Learned conformational representations can guide MD sampling as well as generate candidate structures.]]
  - [[Hierarchical ensemble generation uses learned structures to seed MD and enhanced sampling.]]

**5. Handoff to §1.4: populations need experimental constraints.** Sampling frequencies define the reference distribution used in fitting; whether they approximate physical populations depends on the sampling method and its convergence ([[importance sampling]]). Experimental measurements constrain these weights. Generators and simulations supply atomic candidates whose populations require assessment, and HDX-MS constrains protection in solution without atomic positions, so each supplies what the other lacks. Integration (§1.4) is the operation that joins them.

**Section structure.** This is the mirror of §1.2 group 6, and the section should close on the two halves together.

- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]]
- [[A knowledge-based potential is not a thermodynamic free energy unless its probabilistic model and reference distribution are defined.]]
- [[The emerging bottleneck is scoring generated structures against in vitro and in vivo behaviour.]]
- [[Integrating measurements of protein dynamics with simulations constrains structural ensembles.]] (moved from §1.1 F)
- The generated-diversity point is developed in §1.5 group 4; do not state it here.

**Drafting sources.**
- ValDX methods: `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L85. Ensembles are framed as competing structural hypotheses, and the concrete examples are single-start MD, multiple-start MD, T-FES, and filtered and unfiltered AF2.
- jaxENT intro: `projects/2-jaxENT/manuscript/report/introduction.tex` L6. MD recovers dominant states for folded proteins but cannot guarantee representativeness. AF2 sub-sampling includes implausible structures. Wider sampling creates opportunities for integration.
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex` L15–84, which has most of the explanatory prose. Where it differs from groups 3 and 4 on what metadynamics loses (L76), what seeding preserves (L80–82) and learned force fields against Boltzmann generators (L67), the groups are right, and the AF3 seeds claim replaces its L42.

**Kept for Chapter 2:**
- diffusion SDEs and score matching ([[diffusion model]]);
- bias potentials, reweighting estimators and MSMs ([[enhanced sampling]]);
- detailed balance ([[Markov chain Monte Carlo]]);
- Boltzmann-generator weights ([[Boltzmann generator#^eq-bg-weight]]);
- force-field functional forms;
- knowledge-based potentials and the [[reference ratio method]].

## 1.4 Integrating Experiment and Ensembles

**Argument.** Candidate ensembles can be tested against HDX-MS data by predicting uptake and adjusting the contributions of the sampled conformations. This requires a forward model that relates structural features to exchange, together with a treatment of experimental uncertainty and prior information. Ensemble reweighting balances agreement with the data against changes to the reference ensemble, while calibration adjusts the parameters of the forward model. The fitted ensemble is a structural hypothesis whose interpretation depends on both choices.

**1. From candidate structures to a testable hypothesis.** Pick up the handoff from §1.3: the candidates need relative contributions before they can explain a solution measurement. Frame the task as an [[inverse problem]]: infer an ensemble from its measured effects. Recall the ambiguity from §1.2 briefly; use it to motivate forward prediction rather than repeating the measurement limitations.
- [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]]
- [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]]

**2. Predict what the experiment would measure.** Define a [[forward model]] as the link from a proposed ensemble to an observable. Give the HDX example in words. Counts of hydrogen bonds and heavy-atom contacts at each amide, weighted by two empirical coefficients, give the log protection factor of each conformer; the weighted average over conformers gives the ensemble log protection factor; exchange rates under EX2 and peptide averaging then give uptake. Introduce the [[Best–Vendruscolo model]] as the concrete example shared by the research chapters. The prediction depends on ensemble weights and empirical model parameters.
- [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]]
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]]
- BV/HDXer averages log protection factors before calculating uptake. Averaging separate conformer uptake curves would describe a different model; see [[Best–Vendruscolo model#^eq-bv-ensemble]] and [[deuterium uptake#^eq-uptake-peptide]].

**3. Fit the contributions of the sampled conformations.** Explain [[ensemble reweighting]] physically: each candidate contributes to the ensemble-average log protection factor, uptake is computed from that average, and fitting adjusts how much each candidate contributes so the predicted uptake agrees better with experiment. The initial weights define the reference ensemble. Reweighting changes contributions within the sampled candidates; states absent from that set require further sampling ([[importance sampling]]). Name HDXer as an established implementation after explaining the operation.
- [[Ensemble reweighting adjusts structural contributions so proposed conformational states can be tested against experiment.]]
- [[HDXer is a Python package that implements a MaxEnt reweighting scheme to fit simulated ensembles to experimental HDX-MS data.]]

**4. Balance experimental agreement with the reference ensemble.** The data generally permit several fits, so explain why closeness to a prior matters ([[regularisation]]). Introduce relative [[maximum entropy principle|MaxEnt]] as seeking agreement with minimal departure from the reference weights, accounting for uncertainty. Give the Bayesian reading briefly: the prior and an error-model likelihood jointly determine inference. Equal initial frame weights preserve the sampled distribution as the reference; they do not establish its physical accuracy.
- [[MaxEnt reweighting seeks new weights that minimise the discrepancy with experimental uptake while staying close to the prior.]]
- [[In a Bayesian description, a prior and a likelihood combine into a posterior over unknown structures and parameters.]]

**5. Fit the ensemble and calibrate its forward model.** Distinguish the two adjustable parts of an ensemble model: frame weights determine structural contributions, while the BV coefficients calibrate the mapping from structural features to protection. Either can improve uptake agreement, a change in weights by moving population between conformers and a change in coefficients by rescaling every conformer's protection, so agreement alone does not say which changed. Introduce fixed-parameter, staged and joint fitting as choices about these unknowns ([[nuisance parameter]]). This motivates the unified fitting problem addressed by jaxENT; detailed objectives and results belong in its research chapter.
- Source: ValDX `6_methods_omc.tex` L356–465 (weights and BV parameters fitted against uptake) and jaxENT `introduction.tex` L4, L10 (unified weight–parameter fitting).
- HDXer already optimises BV parameters. BICePs learns forward-model parameters within the posterior for Karplus J-couplings, not for BV uptake (`7_results_omc.tex` L220). jaxENT's contribution is one optimisation in which fixed, staged and joint fits and added constraints can be compared, not parameter fitting itself.

**6. What established integration provides, and what it leaves open.** First credit what the existing tools do. HDXer and MaxEnt refinement reweight candidates against a reference, fit forward-model parameters, and test sensitivity by omitting data or varying parameters ([[02-background]] §2.5, layer 2 of the layered-validation decision). Then name the two problems they leave, one sentence each. Agreement with uptake supports consistency under the chosen candidates, forward model and fitting assumptions, and no existing HDX study partitions the data around peptide dependence, so assessment without ground truth is unresolved (§1.5, Q1). For HDX-MS with the BV model, weights and forward-model parameters have been fitted in stages, with plausibility fixed by the method (HDXer), so a joint fit whose constraint can be chosen for candidates whose sampling frequencies are not Boltzmann weights, such as MSA-subsampled AF2, is unresolved (Q2). Parameter fitting itself is not new; the gap is the comparison of fixed, staged and joint fits and added constraints within one optimisation, and its assessment. Let §1.5 develop identifiability, model error, overfitting, uncertainty and interpretability.

Close §1.4 on why agreement can mislead, which sets §1.5's order. One kind of risk is common to any model fitted to finite data and is answered by standard statistics (held-out data, partitions that respect dependence, selection kept apart from evaluation). The other is specific to integration, because the forward model that links structure to uptake is itself approximate, and a fit can absorb its errors into the weights.
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]
- [[HDXer is a Python package that implements a MaxEnt reweighting scheme to fit simulated ensembles to experimental HDX-MS data.]] (reminder; introduced in group 3)

**Drafting sources, in trust order.**
- ValDX: `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L11–20 (inverse problem, reweighting and model dependence); `2_hdx_theory_omc.tex` (EX2 assumption); `6_methods_omc.tex` L356–465 (weight/parameter fitting, BV averaging, regularisation and Bayesian interpretation).
- jaxENT: `projects/2-jaxENT/manuscript/report/introduction.tex` L4 and L10 (prior dependence and unified weight–parameter fitting).
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex` L83 onward (expository sequence and equations).
- KB papers: [[@bradshawInterpretationHDXData2020]] and [[@leeInterpretingHydrogenDeuteriumExchange2021]] for HDXer; [[@berlinRecoveringRepresentativeConformational2013]] and [[@hummerBayesianEnsembleRefinement2015]] for underdetermination; [[@cesariUsingMaximumEntropy2018]] for relative MaxEnt and treatment of error; [[@bmsb2012ch12]] for forward/error models and parameter inference.

**Kept for Chapter 2:** BV and uptake equations, the likelihood, KL divergence and Lagrange-multiplier derivations, importance-sampling diagnostics, and comparisons with experimentally restrained simulations. The [[reference ratio method]] is an optional conceptual precedent there; [[The meaning of a statistical correction depends on the reference distribution implied by the model or sampling procedure.]] is supported but need not carry the introductory argument.

## 1.5 Trusting Integrative Ensemble Models

**Argument.** Agreement with experimental uptake is insufficient to establish the accuracy of inferred conformational populations. Assessment must also examine prediction of held-out data, the modification required during fitting and sensitivity to the candidate ensemble, forward model and data selection. These comparisons can distinguish hypotheses that achieve similar uptake agreement. They do not, by themselves, identify the cause of a discrepancy. Structural conclusions must therefore be assessed through comparisons that test their dependence on specific modelling assumptions.

**Section structure.** The section follows the two risks named at the end of §1.4. After the non-uniqueness that motivates everything (group 1), group 2 takes the risks shared by any fitted model, which established statistics answers, and group 3 the risk specific to integration, a poor forward model. Groups 2 and 3 each open on the established principle, stated once with one general citation, then give its upshot for HDX-MS, then say what integrative practice does with it ([[2026-10-14 layered presentation of validation and uncertainty]]; full treatment in [[02-background]] §2.5). Candidates (group 4), what a comparison then supports (group 5) and cost (group 6) follow. jaxENT adds joint fitting and mapped uncertainty, but has no citable version yet.

**1. Non-uniqueness.** Pick up the §1.4 handoff. Different populations can produce the same uptake, so a good fit does not identify the ensemble ([[inverse problem]], identifiability). Keep posterior spread apart from physical populations ([[posterior uncertainty]]).
- [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]]
- [[Ensembles generally have far more degrees of freedom than observables, so a single data source leaves them underdetermined.]]
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]] (prefer the first claim)
- Different ensembles can fit the same averages ([[@bonomiPrinciplesProteinStructural2017#^c8]]), and noise and heterogeneity are hard to tell apart in the data ([[@bonomiPrinciplesProteinStructural2017#^c1]]).
- [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]]
- Revised ValDX only (`1_introduction_omc.tex` L17, not in v1): this holds even with a perfect forward model. Present it as the thesis's own statement.

**2. Standard statistics: generalisation, dependence and selection.** Training error is insufficient ([[overfitting]]). Regularisation and error models reduce overfitting but leave a validation problem ([[regularisation]], [[maximum entropy principle]]). Comparing predictions with held-out observations tests whether the fitted ensemble generalises beyond the data used to determine its weights (ValDX `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L23). Agreement supports predictive ability but does not establish that the conformational populations are correct (own; the underdetermination stated in ValDX `1_introduction_omc.tex` L17). This test is informative only as far as the partition respects the dependence between observations ([[data splitting]]). For HDX-MS the dependence comes first from overlapping peptides and then from cooperative unfolding, which couples residues that share no peptide, so structured splits reduce dependence without removing it. A validation error used to select a fit is no longer an unbiased estimate of performance ([[model selection]]), and replicate spread reflects the partition, not repeat measurement ([[replicate uncertainty]]). The divergence from practice is specific. Integrative HDX studies test robustness by omitting peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions built around peptide dependence; crystallographic ensemble refinement already selects its parameters by the cross-validated free R value ([[@burnleyModellingDynamicsProtein2012#^c1]]), so the gap is in the HDX setting, not in structural biology as a whole.
- Principle, layer 1b: [[When observations are dependent, a random partition gives optimistic validation error, so the partition should follow the dependence.]]
- [[Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is expected to be a good choice when the prior is reasonable.]]
- [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]]
- [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]]
- [[Cooperative unfolding couples exchange at residues that share no peptide, so removing peptide overlap does not make training and validation peptides independent.]] (own; the bridge between the two fields)
- [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]]
- [[Selecting a model by its validation error makes that error optimistic, so performance must be estimated on data unused in selection.]] (one sentence, with the jaxENT HDX-NMR evaluation as the instance, see [[Evaluation design (jaxENT)]])
- [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]]
- Practice: [[In the HDX ensemble-integration studies examined, robustness is assessed by removing selected peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions designed around peptide dependence.]] (own; keep the scope "studies examined")
- Optional, if consensus fitting is named here rather than in ch. 3: [[Averaging fitted models reduces their variance but retains any error they share.]]
- [[With a uniform-weight MD ensemble as the prior, MaxEnt reweighting that models experimental error reduces overfitting and keeps the resulting ensemble close to the prior.]]

**3. Poor forward models: compensation and calibration.** If the forward model or the exchange assumptions are wrong, weights and parameters absorb the error ([[model misspecification]]). Keep three cases apart, because each changes the advice. A parameter can be uncertain (a posterior width), miscalibrated (wrong coefficients, fixed by refitting them), or the functional form can be inadequate (no coefficients fit, as under kinetic mismatch). Recalibration addresses only the second, and restoring agreement by calibration does not validate kinetics or populations. How frame predictions are averaged is itself a forward-model choice.
- Forward models are often inaccurate ([[@bonomiPrinciplesProteinStructural2017#^c3]]), the general statement that opens the group.
- [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]]
- The uncertain case in practice. BICePs samples the BV parameters from their posterior rather than fixing them ([[@wanReconcilingSimulatedEnsembles2020#^c10]]).
- [[Structure-to-uptake models rely on hydrogen bonding and solvent exposure but add systematic errors that accumulate at peptide level.]]
- [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]]
- [[Recalibrating forward-model coefficients can correct a miscalibration but not an inadequate functional form.]] (own)
- [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]]
- [[Uncertainty in nuisance parameters and regularisation choices can affect structural conclusions from Bayesian analyses of NMR and small-angle scattering.]]
- Optional, one clause at most: [[Averaging log protection factors, exchange rates or uptake over frames are different forward models, and held-out uptake error and population recovery can favour different choices.]] (jaxENT project doc only; detail in ch. 2 and ch. 4)

**4. Candidate coverage and decoys.** The fit can only weight what the candidates contain ([[sampling coverage]]). §1.4 group 3 has already said that missing states cannot be created; remind it in one line. The finding to carry is the converse, that plausible but unpopulated candidates can absorb weight while uptake still matches ([[ensemble reweighting]]).
- Reweighting is inaccurate when the prior differs strongly from the reweighted distribution ([[@bonomiPrinciplesProteinStructural2017#^c9]]), the external statement that opens the group.
- [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]] (also carries [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], the same TeaA result)
- [[Reweighting cannot create conformational states absent from the candidate ensemble.]]
- [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]]
- [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]]

**5. What a comparison then supports: Work Done, uncertainty and hypothesis testing.** Validation error alone cannot separate a good hypothesis from one forced into agreement, so [[Work Done]] adds how much fitting changed the starting hypothesis. Variation across replicate fits shows which conclusions depend on the data chosen ([[replicate uncertainty]]). It locates instability but does not identify its cause. Changing one suspected cause at a time is how a cause is tested ([[controlled perturbation]]). Representative structures make the inferred states inspectable, if conclusions survive a change of representation. End on integration as hypothesis testing, which hands over to the research questions (§1.6).
- HDXer's apparent work is a KL divergence over frame weights ([[@bradshawInterpretationHDXData2020#^c11]]). Introduce it first, then Work Done as the general idea of how far fitting moved the starting hypothesis, of which apparent work is one form and the ValDX definition ([[03-valdx]]) another.
- [[Low validation error with high Work Done shows agreement reached by substantial modification of the prior.]]
- [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]]
- [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]] (the external precedent; its converse does not hold)
- [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]]
- [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]]
- [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]]
- [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]]
- [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]]
- [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]] (jaxENT, draft)

**6. What repeated assessment costs, and what it cannot reach.** Two points, and they motivate Q3 and chapter 5. First, every check in groups 2 and 5 repeats the fit. Because validation requires repeated fitting across data partitions, parameter settings and candidate ensembles, the cost of each fit limits the extent of the assessment. Second, reweighting can only redistribute weight over the candidates it is given, so where coverage fails the data have to act during sampling or generation. End the section on the hand-off to §1.6 as hypothesis testing with these two limits named.
- Rigorous evaluation repeats fitting across partitions with selection in each, at substantial computational cost ([[@cawleyOverfittingModelSelection2010#^c4]]).
- Validation by splits and replicates multiplies the number of fits, so the cost of a single fit bounds how much assessment is affordable (own; `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L473 and L619).
- [[Reweighting cannot create conformational states absent from the candidate ensemble.]] (stated in group 4, reminded here as the motivation for ch. 5)

**Drafting sources.**
- ValDX revised manuscript (`projects/1-ValDX/manuscript/report/`):
  - `1_introduction_omc.tex` L11–37;
  - `7_results_omc.tex` L4–30 (the Work Done framework), L42–60 (TeaA), L189–211 and L248 (kinetic misspecification), L235–248 (clustering and limitations);
  - `6_methods_omc.tex` L52, L70, L510.
- ValDX posted v1: [[@siddiquiFrameworkTestingStructural2026]]. Cited in [[03-valdx]]; not cited in this section. Where v1 and the revision differ, on what small Work Done means, on what structured splits guarantee and on how precise a structural statement Work Done supports, the revision's reading in groups 2 and 5 holds (revised `1_introduction_omc.tex` L26, `7_results_omc.tex` L28).
- jaxENT (`projects/2-jaxENT/manuscript/report/`): `introduction.tex` L4–10; `results.tex` L29 (validation regimes), L63 and L130 (decoys), L173–197 (uncertainty maps). The Fig. 5 caption (L203–207) reads uncertainty as separating sampling from force-field limitations, which group 5 and ValDX do not support.
- BMSB ch13: its Shannon-channel and good-parameter counts are for SAXS and SANS, an example of low-information data rather than facts about HDX-MS.
- Confirmation: `milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex` L87–95. Most of it belongs in §1.4. Here it explains why regularisation still leaves a validation problem.

### Gaps (1.5)
- jaxENT has no citable version, so the decoy, joint-uncertainty and validation-regime points cite the manuscript.
- Efficiency claim (group 6) needs a jaxENT runtime figure.

## 1.6 Research Questions and Objectives

**Argument.** This thesis examines how HDX-MS integration can support interpretable structural hypotheses when conformational populations are not known independently. Four questions address the assessment of fitted ensembles, the combination of physical and statistical constraints, the computational cost of fitting and sampling, and the mechanistic conclusions that the resulting models support.

**Section structure.** Under each question, list the Chapter 2 concepts it draws on, the claims it rests on, and what stays open. §1.7 maps the chapters to the questions, and ch. 7 answers them.

- **Q1.** How can we assess fitted ensembles when conformational populations are not independently known? How can variation across fits guide controlled comparisons of possible causes of instability?
  - Raised by §1.5 groups 2 and 5. Held-out validation is only as honest as the partition, and replicate spread locates instability without naming its cause.
  - Concepts. [[inverse problem]], [[data splitting]], [[Work Done]], [[replicate uncertainty]], [[posterior uncertainty]], [[controlled perturbation]].
  - [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]]
  - [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]]
  - [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]]
  - [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]]
  - [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]]
  - Open. Uncertainty localises instability. Attributing it to sampling, structure or the forward model needs controlled perturbations, one suspected cause at a time.
- **Q2.** How can we integrate knowledge, statistics and physics during integration to improve the reliability of structural hypotheses?
  - Raised by §1.5 group 3 and §1.4 group 6. Weights can absorb forward-model error, and established tools fit weights and forward-model parameters in stages.
  - Concepts. [[maximum entropy principle]], [[Bayes' theorem]], [[nuisance parameter]], [[regularisation]], [[forward model]], [[knowledge-based potential]], [[force field]], [[metainference]].
  - Roles. Physics proposes candidate conformations and sets the exchange assumptions. Knowledge supplies prior weights, parameter ranges and structural filters. Statistics models data errors and their correlations, balances fit against modification, and tests generalisation. The forward model connects structure to the observable, and its parameters are inferred with the weights.
  - [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]]
  - [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]]
  - [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]]
  - [[Metainference infers an uncertainty for each datum alongside the structures, so the restraint weakens where data or forward model are unreliable.]]
  - Open. When an added constraint improves structural inference rather than absorbing error. Fitting order is conditional on the suspected mismatch.
- **Q3.** How can we improve the efficiency of integration to enable its application to larger and more complex systems?
  - Raised by §1.5 group 6. Every check repeats the fit, and reweighting cannot reach states the candidates lack.
  - Concepts. [[clustering]], [[enhanced sampling]], [[Boltzmann generator]], [[guided diffusion]], [[importance sampling]].
  - Three costs, each reduced differently. Representation (fewer structures to fit and inspect), fitting (differentiable, compiled joint optimisation), and sampling (effort spent where it adds information).
  - [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]]
  - [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]]
  - [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]] (own)
  - Open. Efficiency of the whole workflow, from feature calculation through generation to validation and uncertainty. jaxENT's speedups are provisional until re-run on the current code.
- **Q4.** How can we build interpretable models for protein dynamics that allow us to answer mechanistic questions about their dynamics?
  - Raised by §1.1 group C and §1.5 group 5. Weighted ensembles say which states are occupied, and the mechanistic questions of §1.1 D need to know which conclusions those states can carry.
  - Concepts. [[population shift]], [[conformational free-energy landscape]], [[high-energy intermediate]], [[allostery]], [[clustering]], [[conformational kinetics]]. Systems [[BPTI]], [[prion protein]], [[alpha-synuclein]].
  - [[Ensemble similarity scores compare equilibrium distributions and do not capture changes in dynamics or transition rates.]]
  - [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]]
  - Reminder of §1.1 group C, one line only: [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]] (own; its home is §1.1 C)
  - Open. Weighted states support statements about what is occupied and what it looks like. Causal mechanisms, transition order and rates need kinetic evidence.

## 1.7 Thesis Outline and Contributions

**Argument.** The research chapters develop methods for assessing, fitting and generating conformational ensembles using experimental constraints. Following the theoretical background in Chapter 2, Chapter 3 presents ValDX for comparing candidate ensembles through predictive agreement, changes induced by fitting and sensitivity across data partitions. Chapter 4 introduces jaxENT for joint optimisation of ensemble weights and forward-model parameters. Chapter 5 develops differentiable forward models for use during sampling and generation, and Chapter 6 examines differentiable prediction of protonation for pH-dependent applications. Chapter 7 returns to the research questions and considers the conclusions supported by the evidence from each chapter.

**Section structure.** Each research chapter gets one paragraph with four fixed elements: the problem it answers (the §1.1 or §1.5 point that exposed it), the contribution, the validation regime, the limitation it hands to the next chapter, and the state of its evidence, stated as what exists (a posted preprint, completed analyses, an implemented method), so the examiner knows which results the thesis is held to. Architecture, loss-function and training detail stays out of the outline; it lives in the research-chapter hubs ([[03-valdx]], [[04-jaxent]], [[05-biofeaturisers]], [[06-jax-ka]]).

Register: jaxENT compression for contribution statements, each bounded by its validation regime ([[style]] §Registers; [[examples]] 7). Chapter 3's contributions already exist as §1.5 claims and are reused; chapters 4 to 6 state the method and what each case tests until their results exist.

**1. The arc, in one paragraph.** §1.5 named three conditions for trusting a fitted ensemble, and §1.6 turned them into questions. The chapters answer them in order of decreasing control over the candidates. ValDX scores fits to fixed candidate ensembles where references exist (Q1). jaxENT fits weights and forward-model parameters together, fast enough to repeat the fit across splits and replicates (Q2, Q3). BioFeaturisers moves the same forward models into sampling and generation, so the data can reach states the candidates lacked, which §1.5 groups 4 and 6 set as the limit of reweighting (Q2, Q3, Q4). jax-Ka extends the differentiable forward-model idea to protonation (Q2, Q4). From chapter 4 onward one technical thread holds. A forward model with gradients can score, reweight, restrain and guide, so one definition serves every stage. End on the boundary: chapters 3 and 4 reweight what they are given, and only chapter 5 can add states.

**2. What Chapter 2 supplies (synthesis and critical review).** One sentence per block on what the research chapters draw from it (exchange kinetics and forward models; generators and their sampling distributions; MaxEnt, Bayesian refinement, restraints and guidance; validation and ensemble comparison; protonation, in proportion to ch. 6). The thesis's own formulations (Work Done, linear-additive uptake, graph-Laplacian regularisation, Heaviside-contact BV, metadiffusion) stay in their chapters ([[02-background]]).

**3. Chapter 3, ValDX, answers Q1 and opens Q4.**
- Problem (§1.5 groups 1 and 2). Agreement with uptake does not identify populations, and random splits leak through overlapping peptides, so validation error from random splits is optimistic.
- Contribution. Overlap-aware splits, replicate fits and Work Done make integration a comparison of candidate hypotheses, with Work Done read as a distance from the prior rather than from the truth: [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]], [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]], [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]], [[Work Done quantifies changes in the ensemble-average protection-factor profile during fitting.]], [[Low validation error with high Work Done shows agreement reached by substantial modification of the prior.]], [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]]. The result: [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]]. Representation and protocol, one sentence each: [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]], [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]], [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]].
- Regime. 22 ensembles of six proteins (58 to 480 residues); a synthetic kinetic mismatch; decoy conformations.
- Limitation handed on. Conclusions are comparative across the candidates supplied, reweighting cannot add states, replicate uncertainty does not name its cause, and each assessment repeats the fit many times (§1.5 group 6): [[Reweighting cannot create conformational states absent from the candidate ensemble.]], [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]].
- Status. The analyses in this chapter are reported in a posted preprint ([[@siddiquiFrameworkTestingStructural2026]]), and the revised manuscript is post-review. The BICePs comparison and other detail are in [[03-valdx]].

**4. Chapter 4, jaxENT, answers Q2 and Q3, and returns to Q1.**
- Problem (§1.4 group 6, §1.5 group 6). Established tools fit weights and forward-model parameters in stages with plausibility fixed by the method, and a validation protocol of splits and replicates multiplies the cost of every fit.
- Contribution. A differentiable MaxEnt engine that fits weights and Best–Vendruscolo parameters together, with plausibility constraints as loss terms, including a regulariser for candidates whose sampling frequencies are not Boltzmann weights, and with splits and replicates built into the fit. HDXer and the ValDX protocols fit weights and BV parameters in stages; the contribution is that fixed, staged and joint fits and added constraints are compared within one optimisation, not parameter fitting itself.
- Regime. [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]]: synthetic, an HDX-NMR reference, α-synuclein; runtime against HDXer. The draft abstract's figures come from outdated experiments and are re-derived before they appear.
- Limitation handed on. jaxENT still reweights fixed candidates, and its uncertainty maps localise instability without naming the cause; attribution needs a [[controlled perturbation]]. The α-synuclein Tris reading stays a hypothesis bounded by sampling and forward model.
- Status. The analyses are complete; their manuscript is in draft, due 14 Nov. Loss terms, the interval-hazard uptake form, the graph-Laplacian regulariser and the error weighting are in [[04-jaxent]].

**5. Chapter 5, BioFeaturisers, answers Q2 and Q3 during sampling, and Q4 through two mechanistic cases.**
- Problem (§1.5 group 6, §2.4). States absent from the candidates cannot be reweighted into existence, and no HDX collective variable with forces is published.
- Contribution. A library of differentiable forward models, so that one definition serves reweighting (jaxENT), restrained sampling (metadynamics–metainference) and guided generation (metadiffusion). The library and pipeline are what can be claimed now.
- Regime, in order of decreasing ground truth ([[examples]] 7). [[BPTI]] against the 1 ms Anton trajectory, a controlled reference. MoPrP at pH 4 and pH 7, a mechanistic question that depends on protonation (ch. 6). RORγ with agonist, partial-agonist and antagonist ligands, with no reference. Each case is written as what it tests.
- Limitation handed on. [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]]; a restraint is only as good as the forward model where the data are; and a pathway read from the MoPrP simulations needs the trajectories, not the weights (§1.1 group C, [[conformational kinetics]]).
- Status. The forward-model library is implemented; the cases are under way and metadiffusion is under development, due 28 Nov ("metadynamics" in `DEADLINES.md`). Forward-model and case protocols are in [[05-biofeaturisers]].

**6. Chapter 6, jax-Ka, answers Q2 and Q4 for protonation.**
- Problem (the pH thread: §1.1 D3, §1.2 group 2, §1.3 group 2). The MoPrP data were taken at pD 4, the ch. 5 simulations run at pH 4 and pH 7, and our ensembles were protonated once at neutral pH, so which groups are protonated is an unverified input to every pH-dependent case.
- Contribution. A backbone-only pKa predictor whose readout differentiates through coordinates, a second forward model of the kind ch. 5 builds.
- Regime. Training labels are computed, PypKa values via pKPDB and pKAI values on PINDER bound and free states, and experiment enters only at test, on PKAD ([[06-jax-ka]]). The planned application asks which MoPrP sites change protonation between pH 4 and pH 7, and whether they sit in the regions that unfold.
- Limitation handed on. Interface experiments are open, and the MoPrP application is untested. Keep the paragraph proportional to the final chapter; [[02-background]] §2.2 is short and the titration models are introduced in the ch. 6 preface.
- Status. The method is implemented; the cases are under way, and `DEADLINES.md` has no entry for it. Architecture, training sets and current numbers are in [[06-jax-ka]].

**7. Chapter 7 returns to the questions.** The conclusion answers Q1 to Q4 with the chapter evidence, names what stays open (equilibrium weighting of guided samples; forward-model error where data are sparse; the posted ValDX revision; and one item per question from §1.6, namely attributing instability, when added constraints help, whole-workflow efficiency, and kinetic or causal interpretation), and places the confirmation's future work (AlphaFold3 confidence benchmarking; jaxENT with SAXS and NMR) as extensions, not chapters.

**Map.**

| Chapter | Questions | Contribution, one line | Tested on | Status |
|---|---|---|---|---|
| 3 ValDX | Q1, Q4 | Splits, replicates and Work Done make integration a comparison of candidate hypotheses | 22 ensembles, six proteins; synthetic kinetic mismatch; decoys | preprint posted; revision post-review |
| 4 jaxENT | Q2, Q3, Q1 | Joint differentiable fit with plausibility as loss terms; linear-additive uptake; graph-Laplacian regularisation | synthetic, HDX-NMR reference, α-synuclein; runtime vs HDXer | analyses complete; manuscript in draft |
| 5 BioFeaturisers | Q2, Q3, Q4 | Differentiable forward models shared by reweighting, restrained sampling and guided generation | BPTI (Anton), MoPrP pH 4 and 7, RORγ ligand series | method implemented; cases under way |
| 6 jax-Ka | Q2, Q4 | Backbone-only relational oGQT pKa model, differentiable through coordinates | pKPDB, PINDER bound/free, PKAD; MoPrP pH 4 and 7 | method implemented; cases under way |

Contributions are stated inline, one per chapter paragraph, with no closing paragraph keyed to Q1 to Q4, because chapter 7 answers the questions. A separate bulleted list, as in the confirmation and Crook §1.7, invites unconditional phrasing.

**Drafting sources.**
- Confirmation `milestones/2025-11-confirmation-of-status/introduction/thesis_outline.tex` (chapter summaries and contributions; its numbering is stale, ValDX was chapter 2, and its 4D visualisation has no chapter) and `future_work/future_work.tex` (what moves to ch. 7).
- ValDX `0_abstract_omc.tex` and `1_introduction_omc.tex` L25–37; preprint note [[@siddiquiFrameworkTestingStructural2026]].
- jaxENT `abstract.tex`, `introduction.tex` final two paragraphs, `results.tex` L29 (validation regimes), `meta_analysis.tex` L1–10.
- Chapter tex comments (`03-valdx.tex` to `06-jax-ka.tex`) for ch. 4 to 6, where "heavy-side" is Heaviside; the README project table and `DEADLINES.md` for status.
- Crook §1.7 "Thesis outline and contributions" (`examples/crook-map`) for the shape: chapter by chapter, each tied to the question it answers.
- The research-chapter hubs for the detail that was moved out of this section on 2026-10-14.

### Gaps (1.7)
- No results or claim notes yet for the thesis's own ch. 4 to 6 contributions; their paragraphs state the method and what each case tests.
- jaxENT's quantitative figures are from outdated experiments.
- jax-Ka scope is undecided (full research chapter, short chapter or appendix) and has no deadline.
- Chapter titles: the tex titles are project names, and §1.7 needs descriptive titles it can quote.
- `thesis/frontmatter/abstract.tex` is empty.
- Publications and data collaborations: whether to list the preprint and collaborator data here or in the front matter.
