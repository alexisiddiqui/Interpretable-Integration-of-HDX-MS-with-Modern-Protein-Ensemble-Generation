# 01 Introduction

Chapter hub: the argument in order, one claim per line. Sections follow `thesis/chapters/01-introduction.tex`.

Markers:
- **supported**: lint-verified evidence.
- **partial**: flagged for review because support is partial or indirect.
- **gap**: the cited paper does not support the claim, so it needs a new source or rewording.
- Unmarked claims are drafts that have not been flagged.

## 1.1 Proteins as Dynamic Ensembles

Why [[population shift|conformational populations]] matter for function and disease. The order follows the confirmation intro (`biological_dynamics.tex`). The ValDX opener ("understanding protein dynamics is crucial to understanding biological function, and therefore disease") and the jaxENT synthesis map onto groups 1 and 9.

**1. Static structures are not enough.** Function, disease and drug response depend on [[protein dynamics]], and the tools have mostly frozen proteins in time.
- [[Static structures alone cannot explain many biological phenomena; dynamics underlie disease mechanisms and drug response.]]
- [[Mounting evidence suggests that understanding dynamics is the key to novel therapeutic strategies.]]
- [[There is a persistent, critical gap in our ability to predict and understand protein dynamics.]]
- [[Tools have been dominated by methods that freeze proteins in time, hiding links between structure, dynamics, function and disease.]]

**2. The gap is one of scale.** Dynamic structural data are scarce next to static structures.
- [[Only about 12,000 experimental structural ensembles exist, covering 21% of CATH superfamilies, so dynamic data are scarce.]]
- [[Tools to estimate protein dynamics are decades old, but public datasets hold only thousands to tens of thousands of entries.]] (supported)

**3. Mutations shift populations, not structures.** Disease mutations can leave the crystal structure unchanged while reshaping the [[conformational free-energy landscape]].
- [[Cancer-causing p53 mutants have crystal structures nearly identical to wild type but very different DNA binding and pathologies.]] (gap)
- [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]]
- [[Mutations create neither steric clashes nor new folds but shift conformational ensembles, which needs sampling of many distributions.]] (partial)

**4. Static methods and their limits.** [[X-ray crystallography]], [[cryo-EM]] and [[NMR]] have transformed structural biology, but they restrict understanding to what they can measure.
- [[Structural biology has made tremendous strides in solving static protein structures by X-ray crystallography, cryo-EM and NMR.]]
- [[The fundamental limitations of these methods restrict our understanding to what can be measured experimentally.]]
- [[Across disease categories, high-resolution structures exist but mechanisms remain unclear.]] (gap)

**5. Kinases: drug sites preserved, equilibria shifted.** An example of [[allostery]] and [[population shift]].
- [[Kinases and their inhibitor resistance mutations often preserve drug-binding sites while shifting conformational equilibria.]]
- [[Shifted conformational equilibria are a major reason why most kinases are still undruggable.]] (gap)
- [[EGFR L858R and T790M mutations rigidify sub-domains and shift equilibria toward active states, preserving active-site geometry.]]

**6. Misfolding diseases share a dynamic mechanism.** [[protein misfolding and aggregation|Misfolding]] runs through transient [[high-energy intermediate|intermediates]].
- [[Diseases involving protein misfolding are prime case studies that highlight the limitations of structural biology.]]
- [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]]
- [[The conformational dynamics underlying pathogenic aggregation are central to understanding these diseases.]] (partial)
- [[These neurodegenerative diseases involve transient oligomeric intermediates that never crystallize.]] (partial)
- [[High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.]] (partial)

**7. α-Synuclein: dynamics hidden in plain sight.** In [[alpha-synuclein]], the fibril is solved but the protective solution state is an ensemble.
- [[Alpha-synuclein is an unfolded monomer, yet cryo-EM has solved its Lewy body fibril structures at atomic resolution.]] (partial)
- [[Cryo-EM fibrils are helical but the solution state is disordered, so aggregation-prone states can escape standard methods.]] (partial)
- [[Soluble alpha-synuclein stays compact through transient long-range contacts between its charged C-terminus and hydrophobic centre.]] (gap)
- [[Conformational heterogeneity from pathogenic mutations fundamentally alters alpha-synuclein's protective intramolecular interactions.]] (gap)
- [[NMR showed protective picosecond intramolecular interactions in soluble alpha-synuclein, whose disruption starts aggregation.]] (partial)
- [[Linking fast molecular motions to slow pathological processes requires conformational dynamics that static structures cannot capture.]]

**8. IDPs: heterogeneity is the function.** For an [[intrinsically disordered protein]], the ensemble is the description.
- [[For intrinsically disordered proteins, the failure of static structural biology becomes apparent.]]
- [[Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles.]] (supported)
- [[The conformational heterogeneity of IDPs is not a limitation but the functional mechanism by which they carry out their roles.]]

**9. Prion protein: the full ensemble is needed.** The [[prion protein]] case study links to the MoPrP test system used in jaxENT.
- [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]] (partial)
- [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]] (partial)
- [[High-energy intermediates with enhanced conformational heterogeneity precede aggregation but resist crystallization.]] (partial)
- [[Sparsely populated intermediates act as critical gateway states that control the kinetics of pathological conversion.]]
- [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]] (supported)
- [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]] (partial)

**10. Bridge to 1.2: ensembles need populations, and populations need measurements.** A [[structural ensemble]] is only useful once its weights are known.
- [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]
- [[Without experimental measurements of protein dynamics, the biological mechanism of misfunction can remain unclear.]]
- [[Quantifying state populations requires experimental measurements of protein dynamics.]]
- [[Bridging the gap requires a shift toward integrative approaches combining measurements of dynamics with advanced simulations.]]

### Gaps
- **No claim yet** for the jaxENT synthesis: "Protein conformational dynamics govern biological function and modulate disease-associated conformational states, necessitating their representation as diverse structural ensembles rather than single static models" (`projects/2-jaxENT/manuscript/report/introduction.tex` ¶1). Two of its citations are not yet in `thesis/references.bib` or `kb/papers/`: `moulickPartiallyUnfoldedForms2015` and `bonomiPrinciplesProteinStructural2017`.
- **gap** claims above need a source that supports them, or rewording to what the checked source says:
  - p53: neither cited paper covers it.
  - Kinase druggability: Lisi and Loria's remark concerns phosphatases.
  - α-synuclein contacts and mutations: Mukherjee describes an N- to C-terminal contact protecting NAC.
  - "Across disease categories": Lee et al. does not address it.

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
- Optional example: [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]] (supported)

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

Generating candidate structures and estimating their populations are different tasks. Samplers need convergence ([[Markov chain Monte Carlo]]), and a generator's distribution is a prior, not an equilibrium result ([[diffusion model]], [[knowledge-based potential]]).
- [[MD is computationally expensive and may only approximate true dynamics due to force-field inaccuracies and limited sampling.]]
- [[Deep-learning models rapidly generate structures and ensembles by sampling a learned distribution of conformational space.]]
- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]] (partial)
- [[A knowledge-based potential is not a thermodynamic free energy unless its probabilistic model and reference distribution are defined.]] (supported)

## 1.4 Integrating Experiment and Ensembles

Data update a prior ensemble; they do not determine it uniquely ([[Bayes' theorem]], [[ensemble reweighting]], [[maximum entropy principle]]). Reweighting is [[importance sampling]] from the candidate ensemble, so it cannot add missing states. The [[reference ratio method]] is a conceptual precedent: impose coarse-grained statistics while keeping a generator's fine-grained structure.
- [[In a Bayesian description, a prior and a likelihood combine into a posterior over unknown structures and parameters.]] (supported)
- [[MaxEnt reweighting seeks new weights that minimise the discrepancy with experimental uptake while staying close to the prior.]]
- [[The meaning of a statistical correction depends on the reference distribution implied by the model or sampling procedure.]] (supported)

## 1.5 Trusting Integrative Ensemble Models

A good fit does not make the inferred populations unique ([[inverse problem]], identifiability). Posterior spread is not dynamics ([[posterior uncertainty]]), and the data weight and forward-model parameters are [[nuisance parameter]]s that change the result ([[regularisation]]). Competing models can be compared by their evidence ([[Bayes' theorem#^eq-bayes-factor]]) or by validation, as in ValDX.
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]
- [[Posterior uncertainty about a structure or its parameters is not the same quantity as a protein's physical conformational populations.]] (supported)
- [[Diversity among generated structures is not on its own evidence that their frequencies represent an equilibrium ensemble.]] (partial)
- [[Uncertainty in nuisance parameters and regularisation choices can affect structural conclusions from Bayesian analyses of NMR and small-angle scattering.]] (partial)

BMSB ch13's quantitative results (Shannon channels, number of good parameters) are specific to SAXS and SANS. Cite them as an example of low-information data, not as facts about HDX-MS.

### Gaps (1.2–1.5)
- The generated-diversity sentence had no citation in the earlier draft. If it returns, BMSB ch2 supports the sampling half of it; consider `\supercite{bmsb2012ch2}`.
- The generator-distribution claim needs a source on learned generators. BMSB's example is a local fragment model (TORUSDBN).
- The nuisance-parameter claim needs a passage showing a changed structural conclusion: Habeck Fig. 12.10 (pp. 22–23) or Hansen Fig. 13.8.
- BMSB chapters 5–11 (statistical-potential learning, directional statistics, alignment, local structure models, side chains) are not yet used. They are background or methods material if needed.

## 1.6 Research Questions and Objectives

Not yet assembled.

## 1.7 Thesis Outline and Contributions

Not yet assembled.
