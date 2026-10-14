# 01 Introduction

Chapter hub: the argument in order, one claim per line. Sections follow `thesis/chapters/01-introduction.tex`.

Markers:
- **supported**: lint-verified evidence.
- **partial**: flagged for review because support is partial or indirect.
- **gap**: the cited paper does not support the claim, so it needs a new source or rewording.
- Unmarked claims are drafts that have not been flagged.

## 1.1 Proteins as Dynamic Ensembles

Why [[population shift|conformational populations]] matter for function and disease. The arc follows `01-introduction.tex` L7: proteins are dynamic polypeptides → the protein folding grand challenge → folding versus function → case studies showing why populations must be measured and modelled, and where structural methods fall short. The opening is deliberately broad. Energy landscape and frustration theory (Galpern et al.; Parra et al.) supply the abstract anchors, so that the disease cases read as consequences of one principle rather than as a list. The ValDX opener ("understanding protein dynamics is crucial to understanding biological function, and therefore disease", `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L8) closes group C, and the jaxENT synthesis belongs in group F.

**A. Proteins are dynamic polypeptides.** A protein is a sequence before it is a structure, and its structure is something the chain does. The rigid picture has given way to [[protein dynamics|motions]] from picoseconds to days. A crystal structure is one member, or a time average, of what the protein populates, and folded and disordered proteins sit at two ends of one [[conformational free-energy landscape|landscape]].
- [[Proteins are linear polymers whose sequences encode structures that fold rapidly and spontaneously.]]
- [[The rigid view of proteins has given way to one in which motions spanning picoseconds to days are essential to function.]]
- [[Even a folded protein is an ensemble of structures, and distinct crystal structures can be time-averaged members of one ensemble.]]
- [[NMR relaxation showed the central helix of calmodulin is flexible in solution, though it appears rigid in crystal structures.]]
- [[Folded and disordered proteins lie at two ends of one energy landscape, from a well-defined minimum to a flat surface.]] (partial)

**B. The protein folding grand challenge.** Folding is an entropic search (Levinthal) that evolved sequences carry just enough information to solve. They can solve it because they are minimally frustrated and fold down a rough funnel. Structure prediction has largely solved the static half of the problem. The dynamic half remains open, and native-state hydrogen exchange shows why it matters: partially unfolded forms are real but too sparsely populated to see in a structure.
- [[Folding poses an entropic search problem, and evolved sequences carry just enough information to solve it.]]
- [[Folding is possible because evolved sequences are minimally frustrated, giving a rough, funnel-shaped energy landscape.]]
- [[Structural biology has made tremendous strides in solving static protein structures by X-ray crystallography, cryo-EM and NMR.]]
- [[Leveraging large structure and sequence corpora, protein structure models predict structures rapidly and with high accuracy.]] (supported; also in §1.3 group 4). For the scale, Varadi ^c5 compares about 220 million sequences with just over 180,000 PDB structures.
- [[Despite huge advances in accuracy and speed, protein structure models have limitations.]] (supported)
- [[Despite structure prediction, the dynamics of folding remains a formidable problem that predictors and most experiments cannot resolve.]]
- [[Native-state hydrogen exchange reveals sparsely populated partially unfolded forms that are otherwise invisible.]]

**C. Folding versus function.** Minimal frustration is a global property; function puts frustration back locally. The frustrated sites are where proteins bind, catalyse and switch, and where the sequence pays for function in stability. The same sites drive interconversion between native conformations, so function depends on how the native [[structural ensemble]] is populated, often through slow, sparsely populated states. For an [[intrinsically disordered protein]], the ensemble is the whole description.
- [[Folded proteins retain a minority of highly frustrated contacts, clustered at the surface.]]
- [[Highly frustrated sites mark where proteins bind partners, catalyse reactions and switch allosteric states.]]
- [[Function conflicts with folding, so sequences encode function locally at sites that sacrifice stability.]]
- [[Local frustration drives interconversion between native conformations, coupling function to slow, high-energy states.]] (partial)
- [[Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles.]] (supported)
- [[The conformational heterogeneity of IDPs is not a limitation but the functional mechanism by which they carry out their roles.]]
- Alt: [[For intrinsically disordered proteins, the failure of static structural biology becomes apparent.]] (overlaps the first IDP claim; it could instead open group E)
- Summary into D: [[Static structures alone cannot explain many biological phenomena; dynamics underlie disease mechanisms and drug response.]], [[Mounting evidence suggests that understanding dynamics is the key to novel therapeutic strategies.]]

**D. Case studies: disease as a change in populations.** A [[dynamic disease mechanism]] changes which states a protein populates; it need not change the structure. The cases are ordered by how much a single structure can show. They start from a clean two-state [[population shift]] and end with ensembles that only make sense as a whole.

*D0. Framing.*
- [[Disease mutations can destabilise the functional state or over-stabilise the wrong one.]] (partial)
- [[Disease-associated variants perturb local frustration more than benign variants.]] (partial; replaces the "Across disease categories" gap claim)

*D1. Two-state shifts: structure preserved, function changed* ([[allostery]]). Mutations reshape the [[conformational free-energy landscape]] without changing the fold.
- [[A single mutation can leave the crystal structure unchanged yet strongly alter function.]] (replaces the p53 gap claim)
- [[Mutations create neither steric clashes nor new folds but shift conformational ensembles, which needs sampling of many distributions.]] (partial)
- [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]]
- [[Kinases and their inhibitor resistance mutations often preserve drug-binding sites while shifting conformational equilibria.]]
- [[EGFR L858R and T790M mutations rigidify sub-domains and shift equilibria toward active states, preserving active-site geometry.]]

*D2. Misfolding: the kinetic extreme.* [[protein misfolding and aggregation|Misfolding]] runs through sparsely populated [[high-energy intermediate|intermediates]]. Chaperones that recognise frustrated sites (Parra ^c12) are one cellular response to that risk.
- [[Diseases involving protein misfolding are prime case studies that highlight the limitations of structural biology.]]
- [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]]
- [[The conformational dynamics underlying pathogenic aggregation are central to understanding these diseases.]] (partial)
- [[High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.]] (partial)
- Alt: [[These neurodegenerative diseases involve transient oligomeric intermediates that never crystallize.]] (partial)
- [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]] (supported; moved from §1.2 group 5)
- [[Differences in conformational dynamics relate to the aggregation of amyloidogenic light chains.]]

*D3. α-Synuclein: the solution ensemble behind a solved fibril.* In [[alpha-synuclein]], the fibril is solved but the protective solution state is an ensemble. Keep this to one paragraph.
- [[Alpha-synuclein is an unfolded monomer, yet cryo-EM has solved its Lewy body fibril structures at atomic resolution.]] (partial)
- [[Cryo-EM fibrils are helical but the solution state is disordered, so aggregation-prone states can escape standard methods.]] (partial)
- [[Soluble alpha-synuclein adopts an autoinhibitory conformation in which N- to C-terminal contacts protect the aggregation-prone NAC domain.]] (replaces a gap claim)
- [[Disrupting alpha-synuclein's autoinhibitory conformation exposes the NAC domain and is likely to lower the nucleation barrier for aggregation.]] (replaces a gap claim)
- [[NMR showed protective picosecond intramolecular interactions in soluble alpha-synuclein, whose disruption starts aggregation.]] (partial)
- [[Linking fast molecular motions to slow pathological processes requires conformational dynamics that static structures cannot capture.]]

*D4. Prion protein: the full ensemble is needed.* The [[prion protein]] case study links to the MoPrP test system in jaxENT.
- [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]] (partial)
- [[A familial prion-disease variant populates a more heterogeneous ensemble with thermally accessible misfolded states.]]
- [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]] (partial)
- [[High-energy intermediates with enhanced conformational heterogeneity precede aggregation but resist crystallization.]] (partial)
- [[Sparsely populated intermediates act as critical gateway states that control the kinetics of pathological conversion.]]
- [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]] (supported)
- [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]] (partial)

**E. Where static methods fall short.** (Old group 1, moved down.) [[X-ray crystallography]], [[cryo-EM]] and [[NMR]] transformed structural biology, but they record ground states and time averages, and few dynamic data exist. Populations also depend on the molecular environment, so they have to be measured under stated conditions.
- [[There is a persistent, critical gap in our ability to predict and understand protein dynamics.]]
- [[Tools have been dominated by methods that freeze proteins in time, hiding links between structure, dynamics, function and disease.]]
- [[The fundamental limitations of these methods restrict our understanding to what can be measured experimentally.]]
- [[Only about 12,000 experimental structural ensembles exist, covering 21% of CATH superfamilies, so dynamic data are scarce.]]
- [[Tools to estimate protein dynamics are decades old, but public datasets hold only thousands to tens of thousands of entries.]] (supported)
- Cross-reference to §1.5: [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]] (supported). An NMR ensemble is not a thermodynamic ensemble ([[@bmsb2012ch12#^c3]]), so the 12,000 count overstates what is known about populations.
- [[Conformational populations depend on molecular context, so they are defined only for a stated environment.]] (partial)
- Further evidence for the limitation claims, not yet added to their notes: Biancaniello ^c2 and ^c9 (current techniques target rigid states and cannot capture intermediates), Pelikan ^c4, Li ^c1 (GPCRs), James ^c6.

**F. Bridge to §1.2: ensembles need populations, and populations need measurements.** A [[structural ensemble]] is useful only once its weights are known. HDX reports on ensembles in solution. Frustration analysis, by its authors' own account, needs generated ensembles rather than one structure (Parra ^c25, ^c27), which points ahead to §1.3–1.4.
- [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]
- [[Quantifying state populations requires experimental measurements of protein dynamics.]]
- Alt: [[Without experimental measurements of protein dynamics, the biological mechanism of misfunction can remain unclear.]]
- [[HDX data report on ensembles and can reveal conformational landscapes that differ from the crystal structure.]]
- [[Bridging the gap requires a shift toward integrative approaches combining measurements of dynamics with advanced simulations.]]

**Drafting sources.**
- Anchors:
  - [[@galpernInformationtheoreticArgumentRestriction2026]] for A and B;
  - [[@parraFrustrationPhysiologyMolecular2025]] for B to E;
  - [[@galpernProbingDarkEnergy2026]] for B and C;
  - the [[dynamic disease mechanism]] concept for D and E.
- Confirmation `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex`:
  - the database-size figure (`figures/database_sizes.png`) fits group B or E;
  - its disease paragraphs map onto D;
  - reorder its material; do not reuse its opening.

**Wording to avoid.**
- Intensifiers from the confirmation: "paradigm shift", "simply", "critical", "fundamental". Several existing claim titles use them, so reword when drafting.
- Parra's gene-network and psychiatry analogies (§§13–14). They are analogies, not evidence.
- The hemoglobin sentence as a result. It is a framing image.
- Parra as the citation for specific disease results. Cite the primary studies (see Gaps).

### Gaps
- **No claim yet** for the jaxENT synthesis: "Protein conformational dynamics govern biological function and modulate disease-associated conformational states, necessitating their representation as diverse structural ensembles rather than single static models" (`projects/2-jaxENT/manuscript/report/introduction.tex` ¶1). Two of its citations are not yet in `thesis/references.bib` or `kb/papers/`: `moulickPartiallyUnfoldedForms2015` and `bonomiPrinciplesProteinStructural2017`.
- **Folding theory has no primary sources in the KB.** There are no notes for Anfinsen, Levinthal, Bryngelson and Wolynes (1987) or Onuchic et al. (1997), so groups A and B rest on Galpern and Parra.
- **Stubs without PDFs** that would strengthen A to C: [[@vendruscoloRareFluctuationsNative2003]] (rare native fluctuations) and [[@kimHydrogenExchangeIdentifies1993]] (native-state motional domains). Add `kb/_pdf/@<citekey>.pdf` for each.
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
- **Near-duplicates.** When drafting, use one claim from each set:
  - "Static structures alone…" / "Tools have been dominated…"
  - "Only about 12,000…" / "Tools to estimate…"
  - the high-energy-intermediate claims in D2 and D4
  - "Quantifying state populations…" / "Without experimental measurements…"
  - the IDP claims
  - "Linking fast molecular motions…" / "Rate-limiting conformational changes…"
- **Mis-cited claims found in passing, not fixed here:**
  - the GPCR ¹⁹F-NMR claim cites Fan and Yen, which cover GPR52 and β1AR;
  - the HIV Vif claim cites Appadurai, which is the wrong paper;
  - the SARS-CoV-2 spike claim cites Puchades and Stander, which do not support it;
  - "With current models, most single-domain proteins…" likely mis-cites Varadi.

## 1.2 Measuring Protein Dynamics

**Thread for 1.2–1.5.** Sections 1.2 to 1.5 share one thread: HDX-MS constrains ensembles only through an indirect [[forward model]], so the inferred populations depend on the candidate ensemble, the forward model and their uncertainties. The grounding for 1.3–1.5 comes mainly from BMSB (Hamelryck et al. 2012) chapters 1–4, 12 and 13.

§1.2 says what [[HDX-MS]] measures and where measurement ends and structural inference begins. It does this in six steps. Exchange theory stays in Chapter 2 (see below).

**1. What is recorded.** Backbone amides exchange with solvent deuterium, and MS reads this as a mass increase of peptides over labelling time ([[deuterium uptake]]).
- [[Different methods can measure protein dynamics, depending on the system, timescale and experimental conditions.]]
- [[HDX-MS measures protein conformational dynamics in solution.]] (supported)
- [[HDX-MS measures the exchange of backbone amide hydrogens with deuterium in the solvent.]] (supported)
- [[Measuring the mass increase of peptides over time lets HDX-MS report on protein dynamics and conformational changes.]] (supported)

**2. What sets the rate.** Intrinsic chemistry ([[intrinsic exchange rate]]) and local protection from hydrogen bonding, burial and transient opening ([[Linderstrøm–Lang model]], [[protection factor]]).
- [[Amide exchange rates depend on intrinsic chemistry and on local protection from hydrogen bonding, burial and transient opening.]] (supported)
- [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]] (supported)
- [[The HDX rate depends on the local environment of the amide hydrogen, with more exposed and flexible regions exchanging faster.]] (supported; read it with the second caution in group 4)

**3. What the readout resolves.** Overlapping peptides, not residues or atoms.
- [[HDX-MS reports deuterium uptake at the peptide level, not the residue level.]] (supported)
- [[HDX-MS data alone do not give the atomic positions that NMR, crystallography and cryo-EM provide.]] (supported)

**4. Why interpretation is ambiguous.** Different local environments or populations can give the same uptake. A change in uptake shows a change in protection, not a mechanism. Two cautions follow.
- [[A change in HDX-MS uptake shows a change in protection but does not on its own identify the structural mechanism.]] (supported)
- [[Interpreting dynamics measurements in structural terms is a grand challenge, as they can be indirect or ensemble-averaged.]]
- [[Greater deuterium uptake indicates less protection from exchange, not directly greater flexibility.]] (partial)
- [[Labelling time measures accumulated exchange, not the duration of a conformational motion.]] (partial)
- [[Ensembles have far more degrees of freedom than observables, so any single data source leaves them underdetermined.]] (partial). The general form is in §1.5: [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]

**5. Why it is useful.** Keep this to a sentence or two.
- [[HDX-MS can study many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools.]] (supported)
- [[The primary benefits of HDX-MS are sensitivity, flexibility and low sample needs compared with other biophysical techniques.]]
- [[HDX-MS flexibility and increasing throughput make it well suited to challenging targets such as GPCRs, antibodies and IDPs.]]
- Optional example: the tau HDX-MS claim, now in §1.1 group D2 ([[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]]). Refer back to it here; do not present it twice.

**6. Handoff to §1.3–1.4.** Connecting uptake to structure needs a model that predicts exchange from candidate structures ([[forward model]]), which makes interpretation an [[inverse problem]].
- [[To quantitatively connect measurements of dynamics to biological mechanisms, they must be interpreted in structural terms.]]
- [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]] (supported)
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]] (supported)
- [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]] (partial)

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
- "without size limitations" (ValDX intro L8). Use the group 5 claim; [[Orthogonal to X-ray, cryo-EM and NMR, HDX-MS probes without size limits and uniquely unravels dynamics in diverse conditions.]] is flagged for review.

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
- [[A complete picture of dynamics requires sampling in between these states.]] (partial)
- Already in §1.1 group 10: [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

**2. MD and its limits.** [[molecular dynamics]] gives physically grounded trajectories, but only for its approximate [[force field]] and only once sampling has converged ([[equilibration and convergence]]).
- [[MD simulations numerically integrate Newton's equations of motion, giving atomistic insight into protein dynamics over time.]]
- [[MD simulations can model varied conditions such as temperature, pressure, pH and the presence of ligands or other biomolecules.]]
- [[MD lets researchers study how proteins respond to different environments, giving insight into functional mechanisms.]] (supported)
- [[MD is computationally expensive and may only approximate true dynamics due to force-field inaccuracies and limited sampling.]] (supported)
- [[Sufficiently sampled equilibrium MD targets the Boltzmann distribution of its approximate force field, not the protein's true distribution.]] (partial)
- [[Until MD has converged, its statistics depend on the starting structures; reproducibility across independent starts is the basic check.]] (supported)
- [[Physics-based methods are useful for detailed analysis but limited by the computational cost of equilibration.]]
- [[Sampling is limited because equilibration must be repeated for each new system or starting conformational state.]] (partial)

**3. Enhanced sampling.** Two families ([[enhanced sampling]]). Biasing the energy recovers equilibrium probabilities by reweighting but usually loses kinetics. Adaptive seeding broadens exploration, but pooled frames are not populations. Neither gives populations for free.
- [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]] (supported)
- [[The metadynamics bias encourages exploring new states by discouraging revisits to previously sampled configurations.]] (supported)
- [[Many enhanced sampling schemes alter kinetics; equilibrium probabilities are recovered by reweighting, which needs good overlap between biased and unbiased distributions.]] (supported)
- [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]] (supported)
- [[Frontier-Expansion Sampling is a promising avenue for enhanced sampling of conformational space.]] (supported)
- [[As FES only requires Cartesian coordinates to select new simulation seeds, it is flexible to the underlying topology.]]
- Reword before use (see Wording to avoid): [[Metadynamics is limited by the need for appropriate CVs, complex computational requirements and loss of equilibrium properties.]], [[Offline biasing methods can be used to preserve equilibria while enhancing sampling.]], [[Offline methods adaptively seed new simulations from underexplored regions, sampling efficiently without distorting the landscape.]]
- Optional detail: [[Online analysis of collective variables can adaptively guide sampling towards underexplored regions of conformational space.]], [[These methods can be sampled over specific CVs but are also compatible with generic dimensionality reduction techniques.]]

**4. Learned generators, including diffusion.** Three kinds of model, which the confirmation runs together:
- **Structure predictors adapted for diversity.** Perturb the input ([[MSA subsampling]]) or the seed. Output frequencies have no defined target distribution.
  - [[Protein structure models have recently emerged as a powerful tool for structural biology.]] (supported)
  - [[Leveraging large structure and sequence corpora, protein structure models predict structures rapidly and with high accuracy.]] (supported)
  - [[As protein structure models are primarily trained on static structures, their ability to predict dynamics is limited.]]
  - [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]] (supported)
  - [[Sub-sampling multiple sequence alignments alters the contacts described to the model, leading to diverse structural predictions.]] (partial)
  - [[Generating many sub-sampled predictions creates a conformational ensemble that captures the protein's dynamic nature.]]
  - [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]] (partial)
- **Generators trained to sample a distribution.** A [[diffusion model]] learns the training-data distribution by learning to denoise; a [[Boltzmann generator]] is trained toward the Boltzmann distribution and reweighted to it.
  - [[Deep-learning models rapidly generate structures and ensembles by sampling a learned distribution of conformational space.]] (supported)
  - [[Deep-learning models trained on large structural datasets learn conformation distributions, and sampling them yields ensembles.]]
  - [[Diffusion models are trained to reverse a noising process and generate structures by progressively denoising random samples.]] (supported)
  - [[Diffusion steps are not physical simulation time.]] (partial)
  - [[Diffusion-based PSMs have emerged as a powerful alternative to traditional structure prediction methods.]]
  - [[Learning the physical landscape can reduce the cost of sampling new states while retaining the accuracy of the underlying physics.]] (supported) (Boltzmann generators only)
- **Learned force fields inside MD.** An MLFF improves the [[force field]], not the sampling.
  - [[Machine-learned force fields learn energies and forces for simulation, whereas Boltzmann generators generate configurations and reweight them to the Boltzmann distribution.]] (supported)
  - [[Ensembles can be generated by learning the physical landscape of protein systems directly from existing simulations.]] (partial)
- **Combining generators with MD.** Generators broaden coverage and MD relaxes the candidates; whether the result is representative still has to be assessed.
  - [[Learned generators are used to seed MD simulations, combining broad coverage with physics-based sampling.]] (supported)
  - [[By providing multiple plausible starting structures, deep learning has bridged the gap for diverse physics-based sampling.]] (partial)
  - [[By combining physics-based and statistics-based simulations we can fill in gaps in sampling and accuracy.]] (partial)
  - [[The limitations of each ensemble generation scheme can be overcome by combining both approaches, in a hierarchical pipeline.]] (partial)

**5. Handoff to §1.4: populations need experimental constraints.** Every source above gives candidates whose frequencies are a prior, not populations ([[importance sampling]]). Experiment is needed to weight them.
- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]] (partial)
- [[A knowledge-based potential is not a thermodynamic free energy unless its probabilistic model and reference distribution are defined.]] (supported)
- [[The emerging bottleneck is scoring generated structures against in vitro and in vivo behaviour.]]
- Also in §1.5: [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]] (partial)

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
- **Equilibration cost:** the confirmation cites Lazim et al. (2020), but the only KB quote from it is about the cost of all-atom MD in general. The two equilibration claims in group 2 need a passage.
- **Unchecked PDFs:** Karplus, Barducci, Casadevall, Wilson, Varadi and He are cited in the confirmation for this section but not yet checked.
- **Unread papers:** Hénin, Zhang, Zheng, Stein, Vani, Unke, Noé, Abramson and Yim are all `read: false`. Their quotes pass the lint.

## 1.4 Integrating Experiment and Ensembles

**Argument:** the measurements introduced in §1.2 can constrain the candidates generated in §1.3 through a structural forward model. Integration fits their contributions relative to a starting ensemble, with assumptions about exchange and uncertainty. The resulting ensemble model is a structural hypothesis whose reliability is the subject of §1.5.

**1. From candidate structures to a testable hypothesis.** Pick up the handoff from §1.3: the candidates need relative contributions before they can explain a solution measurement. Frame the task as an [[inverse problem]]: infer an ensemble from its measured effects. Recall the ambiguity from §1.2 briefly; use it to motivate forward prediction rather than repeating the measurement limitations.
- [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]] (supported)
- [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]] (partial)

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

**6. Handoff to §1.5: fitting produces a hypothesis that needs validation.** Finish with the dependence on the candidate ensemble, the forward model and the fitting assumptions. Agreement with uptake supports consistency under those choices; it does not establish unique conformational populations. Let §1.5 develop identifiability, model error, overfitting, uncertainty and interpretability.
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]

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

ValDX supplies the central argument; jaxENT adds joint fitting and mapped uncertainty, but has no citable version yet.

**1. Non-uniqueness.** Pick up the §1.4 handoff. Different populations can produce the same uptake, so a good fit does not identify the ensemble ([[inverse problem]], identifiability). Keep posterior spread apart from physical populations ([[posterior uncertainty]]).
- [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]] (supported)
- [[Ensembles have far more degrees of freedom than observables, so any single data source leaves them underdetermined.]] (partial)
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]] (partial; prefer the first claim)
- [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]] (supported)
- Revised ValDX only (`1_introduction_omc.tex` L17, not in v1): this holds even with a perfect forward model. Present it as the thesis's own statement.

**2. Candidate coverage and decoys.** The fit can only weight what the candidates contain ([[sampling coverage]]). Missing states cannot be created; plausible but unpopulated or implausible candidates can absorb weight ([[ensemble reweighting]]).
- [[Reweighting cannot create conformational states absent from the candidate ensemble.]] (partial)
- [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]] (supported)
- [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]] (partial)
- [[Seeding simulations from rarely visited states broadens exploration but does not by itself give accurate populations.]] (supported)

**3. Compensation between model and populations.** If the forward model or the exchange assumptions are wrong, weights and parameters absorb the error ([[model misspecification]]). Calibration can restore agreement without validating kinetics or populations.
- [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]] (supported)
- [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]] (supported)
- [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]] (revised ValDX only)
- [[Uncertainty in nuisance parameters and regularisation choices can affect structural conclusions from Bayesian analyses of NMR and small-angle scattering.]] (partial)

**4. Generalisation and regularisation.** Training error is insufficient ([[overfitting]]). Regularisation and error models reduce overfitting but leave a validation problem ([[regularisation]], [[maximum entropy principle]]). Held-out peptides test prediction, but only as far as the split is independent ([[data splitting]]). [[Work Done]] adds how much fitting changed the starting hypothesis.
- [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]] (supported)
- [[Accounting for experimental error reduces overfitting in MaxEnt reweighting, and minimal correction is a good choice only when the prior is reasonable.]] (supported)
- [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]] (supported)
- [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]] (revised ValDX only)
- [[Work Done quantifies how much an ensemble must be modified to match experiment.]] (supported)
- [[Low validation error with high Work Done signals agreement reached by excessive modification of the ensemble.]] (supported)
- [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]] (revised ValDX only)
- [[MaxEnt reweighting avoids overfitting and ensures the resulting ensemble remains physically plausible.]] (partial; do not reuse)

**5. Uncertainty, interpretation and testing structural hypotheses.** Variation across replicate fits shows which conclusions depend on the data chosen ([[replicate uncertainty]]). It locates instability but does not identify its cause. Representative structures make the inferred states inspectable, if conclusions survive a change of representation. End on integration as hypothesis testing, which hands over to the research questions (§1.6).
- [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]] (supported)
- [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]] (revised ValDX only)
- [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]] (supported)
- [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]] (revised ValDX only)
- [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]] (supported)
- [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]] (jaxENT, draft)

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
- **Bib entry:** `siddiquiFrameworkTestingStructural2026` was appended by hand to `thesis/references.bib`. Add it in Zotero too, or the next Better BibTeX export will drop it.
- **Review status:** all papers are `read: false`, and all quotes are `reviewed: false`, including the ValDX ones.
- **Unused BMSB chapters:** chapters 5–11 (statistical-potential learning, directional statistics, alignment, local structure models, side chains) are not yet used. They are background or methods material if needed.

## 1.6 Research Questions and Objectives

- **Q1.** How can we reliably assess integration in cases where there is no ground-truth? How can we leverage uncertainty to identify the sources of instability in structural hypotheses?
- **Q2.** How can we integrate knowledge, statistics and physics during integration to improve the reliability of structural hypotheses?
- **Q3.** How can we improve the efficiency of integration to enable its application to larger and more complex systems?
- **Q4.** How can we build interpretable models for protein dynamics that allow us to answer mechanistic questions about their dynamics?

## 1.7 Thesis Outline and Contributions

**Argument:** the four questions in §1.6 are taken up by four research chapters that move from assessing an integration (ch. 3) to performing it jointly and quickly (ch. 4), then to letting the data act during sampling and generation (ch. 5), with a differentiable protonation model (ch. 6) that the pH-dependent cases need. One paragraph per chapter names the question it answers, the contribution, the regime that tests it, and what it leaves to the next chapter. A fixed status sentence in each paragraph separates finished work from work in progress, so the examiner knows which results the thesis is held to.

Register: jaxENT compression for contribution statements, each bounded by its validation regime ([[style]] §Registers; [[examples]] 7). There are no literature markers here. A contribution is a claim about the thesis's own results and leaves `draft` only with a figure ID, or with a quote from the posted ValDX preprint. Chapter 3's contributions already exist as §1.5 claims and are reused; chapters 4 to 6 need new claim notes (`project:` set, `figures:` filled).

**1. The arc, in one paragraph.** §1.5 named three conditions for trusting a fitted ensemble, and §1.6 turned them into questions. The chapters answer them in order of decreasing control over the candidates. ValDX scores fits to fixed candidate ensembles where references exist (Q1). jaxENT fits weights and forward-model parameters together, fast enough to repeat the fit across splits and replicates (Q2, Q3). BioFeaturisers moves the same forward models into sampling and generation, so the data can reach states the candidates lacked, which §1.5 group 2 set as the limit of reweighting (Q2, Q3, Q4). jax-Ka extends the differentiable forward-model idea to protonation (Q2, Q4). From chapter 4 onward one technical thread holds. A forward model with gradients can score, reweight, restrain and guide, so one definition serves every stage. End on the boundary: chapters 3 and 4 reweight what they are given, and only chapter 5 can add states.

**2. Chapter 2 supplies, it does not contribute.** One sentence per block on what the research chapters draw from it (exchange kinetics and forward models; generators and their sampling distributions; MaxEnt, Bayesian refinement, restraints and guidance; validation and ensemble comparison; protonation, in proportion to ch. 6). The thesis's own formulations (Work Done, linear-additive uptake, graph-Laplacian regularisation, Heaviside-contact BV, metadiffusion) stay in their chapters ([[02-background]]).

**3. Chapter 3, ValDX, answers Q1 (assessment without ground truth; uncertainty that locates instability) and opens Q4 through representative structures.** Lead with the problem the §1.5 claims set up, then the tools, the benchmark result, and the boundary.
- Tools. Overlap-aware splits and replicate fits give a validation error that reflects prediction beyond the training peptides, and reduce rather than remove dependence between splits: [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]], [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]], [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]].
- Work Done measures how much the ensemble was modified to reach agreement, independent of uptake error, and is a distance from the prior rather than from the truth: [[Work Done quantifies how much an ensemble must be modified to match experiment.]], [[Low validation error with high Work Done signals agreement reached by excessive modification of the ensemble.]], [[Work Done measures distance from the prior, not from the true ensemble, and small values can also mean too little fitting.]].
- Result. Across 22 ensembles of six proteins (58 to 480 residues), conventional error did not establish population accuracy on its own, and Work Done ranked candidate hypotheses: [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]].
- Representation. Clustering to 10 to 20% of the parent ensemble preserved performance, and smaller sets aid interpretation when the conclusion survives a change of cluster size: [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]], [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]].
- Protocol. Under an imposed kinetic mismatch, fitting forward-model parameters before reweighting limited population distortion: [[Fitted populations can compensate for errors in assumed exchange kinetics, and restoring uptake agreement by calibration does not validate kinetics or populations.]], [[When fitting points to calibration mismatch, the forward model should be recalibrated before the ensemble hypothesis is rejected.]].
- Decoys. Artificial and decoy conformations probe what the BV model can and cannot distinguish: [[Plausible but unpopulated candidate structures can absorb weight and prevent population recovery even when uptake matches.]].
- BiCePs beside Work Done (`03-valdx.tex` comment): a full Bayesian score as the comparison. Not in the preprint; stub.
- Boundary, handed to ch. 4 and 5. Conclusions are comparative across the candidates supplied, reweighting cannot add states, and replicate uncertainty does not name its cause: [[Reweighting cannot create conformational states absent from the candidate ensemble.]], [[Replicate uncertainty locates where a model is unstable but does not by itself separate sampling, structural and forward-model deficiencies.]].
- Status sentence: complete. Manuscript post-review; preprint v1 posted ([[@siddiquiFrameworkTestingStructural2026]]). The five "revised ValDX only" claims in §1.5 become supported once the revision is posted.

**4. Chapter 4, jaxENT, answers Q2 (knowledge, statistics and physics in the fit) and Q3 (efficiency), and returns to Q1 with uncertainty traced to individual structures.** Open on what ch. 3 could not do with HDXer: fit parameters and weights at once, and change the plausibility constraint. Every bullet is a stub (new claim, `project: 2-jaxENT`, figure ID needed).
- A differentiable MaxEnt engine in which plausibility constraints are loss terms rather than architecture, with splits and replicates built into the fit.
- Joint inference of weights and forward-model parameters, with an L1 penalty on the deviation of parameters from their prior values. Non-standard conditions such as low pH require this.
- A linear-additive protection-to-uptake forward model in interval-hazard form. It is an approximation, since protection factors add and uptake does not, and the frame-wise versus ensemble-average inequality remains. It holds for most cases tested and costs O(fragments × timepoints) rather than O(fragments × timepoints × frames).
- Graph-Laplacian regularisation of the weights towards the candidates' pairwise-distance distribution, for candidate sets that do not carry Boltzmann weights (statistical potentials, enhanced sampling), where the uniform-prior KL term breaks down. Any pairwise distance serves, so physics or knowledge-based terms enter the regulariser.
- Covariance-weighted and peptide-timepoint-weighted error terms.
- Validation across three regimes of decreasing ground truth, and runtime against HDXer: [[Validation should progress from synthetic data with known populations to an orthogonal experimental reference to systems without ground truth.]] (draft). The draft abstract's figures (populations within 20 to 25% of experimental precision; 1.5 to 400× faster) come from outdated experiments (project README) and are re-derived before they appear here.
- Boundary: jaxENT still reweights fixed candidates. The states it cannot reach are ch. 5's problem.
- Status sentence: analyses complete; manuscript in draft. Due 14 Nov.

**5. Chapter 5, BioFeaturisers, answers Q2 and Q3 during sampling, and Q4 through two mechanistic cases.** Open on the §1.5 limit (missing states) and the §2.3 gap (no HDX collective variable with forces is published). The contribution that can be claimed now is the library and the pipeline. The case results are in progress and are written as what each case tests, in order of decreasing ground truth ([[examples]] 7).
- A library of differentiable forward models (JAX, with PyTorch wrappers): a Heaviside-contact BV model with usable gradients and an FFT SAXS model. One forward-model definition serves reweighting (jaxENT), restrained sampling (metadynamics–metainference) and guided generation (metadiffusion). Stub.
- BPTI against the 1 ms Anton trajectory, by metainference–metadynamics: tests that restrained sampling recovers the populations a long reference simulation shows. Controlled reference.
- MoPrP at pH 4 and pH 7: candidates from metadynamics–metainference, then unrestrained short apo simulations from decorrelated structures: tests whether pH-dependent unfolding pathways appear. Mechanistic question; depends on protonation (ch. 6).
- RORγ with agonist, partial-agonist and antagonist ligands, by metadiffusion against metadynamics with the same forward models: tests that guided generation of complexes gives ligand-dependent dynamics consistent with restrained sampling. No reference.
- Boundary (from the §2.3 hub): [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]], and a restraint is only as good as the forward model where the data are.
- Status sentence: work in progress. Preliminary experiments; metadiffusion under development. Due 28 Nov ("metadynamics" in `DEADLINES.md`).

**6. Chapter 6, jax-Ka, answers Q2 and Q4 for protonation.** Its place is the pH thread. Intrinsic exchange rates and the MoPrP simulations at pH 4 both need protonation states, and a differentiable pKa model is a second forward model of the kind ch. 5 builds. Keep the paragraph proportional to the final chapter (`02-background.tex` §2.5 comment).
- A differentiable neural pKa predictor with backbone-only and all-atom representations, trained on curated complex databases annotated with pKAI, with a siamese loss for binding-induced shifts. Stub.
- What the preliminary results test: that the siamese loss improves binding-shift recovery, most at large shifts; that site-level features capture atomistic effects a backbone representation misses (Kd-ratio error under 9% all-atom against 30% backbone over pH 6.1 to 7.4, from the tex comment); that a transformer closes part of that gap (under 20% backbone-only). All preliminary.
- Status sentence: preliminary training. **decision**: full research chapter, short chapter, or appendix. `DEADLINES.md` has no entry for it.

**7. Chapter 7 returns to the questions.** The conclusion answers Q1 to Q4 with the chapter evidence, names what stays open (equilibrium weighting of guided samples; forward-model error where data are sparse; the posted ValDX revision), and places the confirmation's future work (AlphaFold3 confidence benchmarking; jaxENT with SAXS and NMR) as extensions, not chapters.

**Map.**

| Chapter | Questions | Contribution, one line | Tested on | Status |
|---|---|---|---|---|
| 3 ValDX | Q1, Q4 | Splits, replicates and Work Done make integration a comparison of candidate hypotheses | 22 ensembles, six proteins; synthetic kinetic mismatch; decoys | complete; preprint v1, revision post-review |
| 4 jaxENT | Q2, Q3, Q1 | Joint differentiable fit with plausibility as loss terms; linear-additive uptake; graph-Laplacian regularisation | synthetic, HDX-NMR reference, α-synuclein; runtime vs HDXer | analyses complete; manuscript draft |
| 5 BioFeaturisers | Q2, Q3, Q4 | Differentiable forward models shared by reweighting, restrained sampling and guided generation | BPTI (Anton), MoPrP pH 4 and 7, RORγ ligand series | in progress |
| 6 jax-Ka | Q2, Q4 | Differentiable pKa model with a siamese binding-shift loss | pKAI retraining, ablations, transformer | preliminary |

**decision**: contributions inline, one per chapter paragraph, closed by a four-sentence paragraph keyed to Q1 to Q4; or a separate bulleted list as in the confirmation and Crook §1.7. Inline is recommended; a list invites the unconditional phrasing below.
**decision**: chapter titles. The tex titles are project names; the outline reads better if each chapter carries a descriptive title that §1.7 can quote.
**decision**: one fixed status sentence per state, used verbatim across chapters ("This chapter is complete and posted as a preprint." / "This chapter reports completed analyses whose manuscript is in draft." / "This chapter reports work in progress.").

**Drafting sources.**
- Confirmation `milestones/2025-11-confirmation-of-status/introduction/thesis_outline.tex` (chapter summaries and contributions; its numbering is stale, ValDX was chapter 2) and `future_work/future_work.tex` (what moves to ch. 7).
- ValDX `0_abstract_omc.tex` and `1_introduction_omc.tex` L25–37; preprint note [[@siddiquiFrameworkTestingStructural2026]].
- jaxENT `abstract.tex`, `introduction.tex` final two paragraphs, `results.tex` L29 (validation regimes), `meta_analysis.tex` L1–10.
- Chapter tex comments (`03-valdx.tex` to `06-jax-ka.tex`) for ch. 4 to 6; the README project table and `DEADLINES.md` for status.
- Crook §1.7 "Thesis outline and contributions" (`examples/crook-map`) for the shape: chapter by chapter, each tied to the question it answers.

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
