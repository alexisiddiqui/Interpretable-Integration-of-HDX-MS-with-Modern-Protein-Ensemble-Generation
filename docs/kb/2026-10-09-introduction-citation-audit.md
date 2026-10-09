# Introduction citation audit (2026-10-09)

This audit came from extracting the two existing introductions into `kb/`: the ValDX manuscript and the confirmation-of-status report. 219 citations in 5 files resolve to 81 papers and 128 claim notes. Every claim was checked against the cited PDF by the lint (quotes) and by per-file fidelity reviews (meaning). The live view is `kb/review-queue.md`; this file is a snapshot for revising the introduction text.

## Summary

- Claims: 27 `supported` (directly stated by verified passages; usable without re-reading) and 101 `draft`.
- Review queue:
  - 74 Support is partial or indirect
  - 20 Cited paper does not support the claim
  - 7 No PDF for any cited paper
  - 10 papers have no PDF in Zotero
  - 1 paper has an unreadable PDF
  - 2 mis-cited papers sit inside supported claims
- The draft count is high because many introduction sentences generalise beyond the papers cited for them: a general statement backed by a single-system example. Mostly the citations need adjusting, not the science.

## Papers, PDFs and duplicates

### Papers without a readable PDF

- @MISATOMachineLearning (No PDF in Zotero)
- @baiHowCryoEMRevolutionizing2015 (No PDF in Zotero)
- @jaynesInformationTheoryStatistical1957 (No PDF in Zotero)
- @karplusMolecularDynamicsSimulations2002 (No PDF in Zotero)
- @kayNMRStudiesProtein2011 (No PDF in Zotero)
- @liConformationalAnalysisProteincoupled2015 (No PDF in Zotero)
- @massonOverviewHydrogenDeuterium2017 (No PDF in Zotero)
- @mcallisterChallengesInterpretationProtein2015 (No PDF in Zotero)
- @mukherjeeProteinMisfoldingAmyloid2024 (No PDF in Zotero)
- @standerEpitopeMappingPolyclonal2021 (No PDF in Zotero)
- @hollingsworthMolecularDynamicsSimulation2018 (PDF in Zotero has no readable text (damaged or scanned))

Also, 7 claims whose every cited paper has no PDF sit under the heading "No PDF for any cited paper" (their citations stay unverified).

### Zotero duplicates to merge

- jamesAdvancesHydrogenDeuterium2022 (duplicate key: jamesAdvancesHydrogenDeuterium2022a)
- leeInterpretingHydrogenDeuteriumExchange2021 (duplicate key: leeInterpretingHydrogenDeuteriumExchange2021a)
- massonRecommendationsPerformingInterpreting2019 (duplicate key: massonRecommendationsPerformingInterpreting2019a)

### Likely mis-citations

Two lists. List 1 gives every claim where the check pass flagged a citation as likely mis-cited or named a likely intended source. List 2 gives every citation marked "no passage supporting this claim found" (a superset: includes cases where the paper is real but the passage was not found, and the intended source is not named). Source line is the claim's `origin`.

#### List 1: flagged as likely mis-citation / intended source named

- **A complete picture of dynamics requires sampling in between these states.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L72`
  - cited paper(s) with no supporting passage: @heninEnhancedSamplingMethods2022
  - flag: No passage making this point was found in Henin et al. (a likely mis-citation), and no better source was found.
- **AlphaFold2 is a deep-learning-based protein structure model developed by DeepMind.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L37`
  - cited paper(s) with no supporting passage: @abramsonAccurateStructurePrediction2024
  - flag: Varadi et al. call AlphaFold an AI system developed by DeepMind and do not use the term deep learning. @casadevallAlphaFold2DeepLearning2023 p1 (^c1) calls AF2 a deep-learning algorithm but is not cited for this sentence. Abramson et al. is a likely mis-citation here, since it describes AlphaFold 3 and mentions AF2 only as the model it evolved from.
- **By combining physics-based and statistics-based simulations we can fill in gaps in sampling and accuracy.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L48`
  - cited paper(s) with no supporting passage: @heninEnhancedSamplingMethods2022
  - flag: Likely intended source: @zhengMachineLearningGeneration2023 p1 (^c4), which says machine learning can drive additional MD sampling or directly generate conformations. Henin et al. is a likely mis-citation here and has no passage on combining physics-based and statistics-based simulations.
- **By providing multiple plausible starting structures, deep learning has bridged the gap for diverse physics-based sampling.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L72`
  - cited paper(s) with no supporting passage: @heninEnhancedSamplingMethods2022
  - flag: Likely intended source: @zhengMachineLearningGeneration2023 p9 (^c5), which says autoencoder-based generation may suit producing new initial structures to seed additional MD simulations. Henin et al. is a likely mis-citation here and has no such passage.
- **Ensembles have far more degrees of freedom than observables, so any single data source leaves them underdetermined.**
  - source line: `projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L11`
  - cited paper(s) with no supporting passage: @leeInterpretingHydrogenDeuteriumExchange2021, @cesariUsingMaximumEntropy2018
  - flag: Lee et al. (2021) is likely mis-cited at milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex L87: it describes HDXer reweighting but does not discuss inverting measurements or its intractability. Likely intended source for L87 and L93: Berlin ^c2 here, and Hummer and Koefinger p2 (@hummerBayesianEnsembleRefinement2015 ^c6, inverse problems are typically ill-conditioned and underdetermined).
  - flag: Cesari et al. (2018) never uses "ill-posed" or "underdetermined" and is likely mis-cited at milestones/2025-11-confirmation-of-status/introduction/connect_simulation_experiment.tex L93.
- **High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L32`
  - flag: The passage does not mention high-energy or sparsely populated intermediates. Likely intended source: @biancanielloStructureDynamicsMisfolding2025 p1 (^c1, ^c3), which says elusive high-energy species often play critical roles in folding and aggregation and are hard to study because of their reduced population. It is not in this claim's cites; the author decides.
- **Mutations create neither steric clashes nor new folds but shift conformational ensembles, which needs sampling of many distributions.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L19`
  - flag: The Lisi passages cover two enzymes and do not mention steric clashes or the need to sample multiple structural distributions. Likely intended source: @suttoEffectsOncogenicMutations2013 p4 (^c3), which says the T790M mutation does not act by steric hindrance but by stabilizing the active conformation. It is not in this claim's cites; the author decides.
- **Offline biasing methods can be used to preserve equilibria while enhancing sampling.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80`
  - cited paper(s) with no supporting passage: @liEnhancedSamplingProtein2025
  - flag: Henin et al. do not use the term offline biasing or state that these methods preserve equilibria. Li and Ma (2025) is a likely mis-citation here, since it is about biasing true reaction coordinates, which is an online biasing method.
- **The design of the AF2 architecture is heavily biased towards learning physical and geometric constraints of protein folding.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L37`
  - cited paper(s) with no supporting passage: @varadiAlphaFoldProteinStructure2022
  - flag: Likely intended source: @casadevallAlphaFold2DeepLearning2023 p1 (^c1), which says AF2's network architectures are based on the evolutionary, physical and geometric constraints of protein structures. Varadi et al. is a likely mis-citation here and has no passage on this.
- **The limitations of each ensemble generation scheme can be overcome by combining both approaches, in a hierarchical pipeline.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L15`
  - cited paper(s) with no supporting passage: @heninEnhancedSamplingMethods2022
  - flag: Likely intended source: @zhengMachineLearningGeneration2023 p1 (^c4), which says machine learning can learn low-dimensional representations of conformational space to drive additional MD sampling or directly generate conformations. That passage supports combining machine learning with MD sampling but does not state that each scheme's limitations are overcome by the combination. The cited Henin review has no such passage and is a likely mis-citation.
- **These methods can be sampled over specific CVs but are also compatible with generic dimensionality reduction techniques.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80`
  - cited paper(s) with no supporting passage: @liEnhancedSamplingProtein2025
  - flag: Likely intended source: @zhangFrontierExpansionSampling2020 p7 (^c3), which says various coordinate systems could describe the conformational space before dimensionality reduction by PCA or other methods in a seeding method (FEXS). Li and Ma is a likely mis-citation here and has no passage on this.
- **With current models, most single-domain proteins can be predicted to near-experimental accuracy in hours on consumer-grade hardware.**
  - source line: `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L30`
  - cited paper(s) with no supporting passage: @varadiAlphaFoldProteinStructure2022
  - flag: Varadi et al. is a likely mis-citation here and describes the accuracy and speed of AlphaFold only qualitatively. No passage on runtime, consumer hardware or single-domain accuracy was found in it. He et al. (@heAlphaFold2ExperimentalStructures2023 p1) mention near experimental accuracy in many cases but give no runtime.

(12 claims)

#### List 2: all citations with "no passage supporting this claim found"

- 19F-NMR of beta2-adrenergic receptors showed biased agonists give distinct shift patterns, linking dynamics to signalling bias. | `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L20` | cited: @fanAllostericCouplingGprotein2023, @yenMassSpectrometryCaptures2022
- A complete picture of dynamics requires sampling in between these states. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L72` | cited: @heninEnhancedSamplingMethods2022
- Across disease categories, high-resolution structures exist but mechanisms remain unclear. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L26` | cited: @leeInterpretingHydrogenDeuteriumExchange2021
- AlphaFold2 is a deep-learning-based protein structure model developed by DeepMind. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L37` | cited: @abramsonAccurateStructurePrediction2024
- By combining physics-based and statistics-based simulations we can fill in gaps in sampling and accuracy. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L48` | cited: @heninEnhancedSamplingMethods2022 | intended: @zhengMachineLearningGeneration2023
- By providing multiple plausible starting structures, deep learning has bridged the gap for diverse physics-based sampling. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L72` | cited: @heninEnhancedSamplingMethods2022 | intended: @zhengMachineLearningGeneration2023
- Cancer-causing p53 mutants have crystal structures nearly identical to wild type but very different DNA binding and pathologies. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L19` | cited: @suttoEffectsOncogenicMutations2013, @lisiAllosteryEnzymeCatalysis2017
- Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L49` | cited: @leeInterpretingHydrogenDeuteriumExchange2021
- Conformational heterogeneity from pathogenic mutations fundamentally alters alpha-synuclein's protective intramolecular interactions. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L36` | cited: @ahmedRefinementASynucleinEnsembles2021
- Ensemble reweighting adjusts structural contributions so proposed conformational states can be tested against experiment. | `projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L17` | cited: @mohammadiaraniInterpretingHydrogenDeuteriumExchange2018, @puchadesEpitopeMappingDiverse2019, @jiaHydrogendeuteriumExchangeMass2020
- Ensembles have far more degrees of freedom than observables, so any single data source leaves them underdetermined. | `projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L11` | cited: @leeInterpretingHydrogenDeuteriumExchange2021, @cesariUsingMaximumEntropy2018
- HDX-MS mapped ACE2 and antibody binding sites on the SARS-CoV-2 spike protein to predict immune escape mechanisms. | `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L13` | cited: @puchadesEpitopeMappingDiverse2019
- HDX-MS mapped binding sites on HIV-1 Vif and enabled inhibitor screening where traditional structural characterisation failed. | `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L13` | cited: @appaduraiDynamicalNetworkHIV12016
- High-energy intermediates with enhanced conformational heterogeneity precede aggregation but resist crystallization. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L47` | cited: @hummerBayesianEnsembleRefinement2015
- Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L40` | cited: @wanReconcilingSimulatedEnsembles2020
- NMR relaxation showed the central helix of calmodulin is flexible in solution, though it appears rigid in crystal structures. | `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L20` | cited: @klecknerIntroductionNMRbasedApproaches2011, @lisiAllosteryEnzymeCatalysis2017
- NMR showed protective picosecond intramolecular interactions in soluble alpha-synuclein, whose disruption starts aggregation. | `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L20` | cited: @ahmedRefinementASynucleinEnsembles2021, @sapienzaUsingNMRStudy2010
- Offline biasing methods can be used to preserve equilibria while enhancing sampling. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80` | cited: @liEnhancedSamplingProtein2025
- SAXS has been integrated with cross-linking MS and HDX-MS to constrain conformational ensembles across length scales. | `milestones/2025-11-confirmation-of-status/introduction/measuring_dynamics.tex#L28` | cited: @yangAdvancesMassSpectrometry2023
- Shifted conformational equilibria are a major reason why most kinases are still undruggable. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L28` | cited: @lisiAllosteryEnzymeCatalysis2017
- Soluble alpha-synuclein stays compact through transient long-range contacts between its charged C-terminus and hydrophobic centre. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L36` | cited: @ahmedRefinementASynucleinEnsembles2021
- Structure-to-uptake models rely on hydrogen bonding and solvent exposure but add systematic errors that accumulate at peptide level. | `projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L20` | cited: @skinnerEstimatingConstraintsProtection2019, @sorensenOptimizedWorkflowSelecting2018, @wollenbergAvoidingScramblingMinimal2020, @fangHighthroughputHydrogenDeuterium2021
- Successful reweighting shows which conformations fit experiment, giving pseudo-structural models of solution behaviour. | `projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L17` | cited: @jiaHydrogendeuteriumExchangeMass2020
- The design of the AF2 architecture is heavily biased towards learning physical and geometric constraints of protein folding. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L37` | cited: @varadiAlphaFoldProteinStructure2022 | intended: @casadevallAlphaFold2DeepLearning2023
- The limitations of each ensemble generation scheme can be overcome by combining both approaches, in a hierarchical pipeline. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L15` | cited: @heninEnhancedSamplingMethods2022 | intended: @zhengMachineLearningGeneration2023
- These methods can be sampled over specific CVs but are also compatible with generic dimensionality reduction techniques. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L80` | cited: @liEnhancedSamplingProtein2025 | intended: @zhangFrontierExpansionSampling2020
- These neurodegenerative diseases involve transient oligomeric intermediates that never crystallize. | `milestones/2025-11-confirmation-of-status/introduction/biological_dynamics.tex#L32` | cited: @mukhtasimovaDetectionTrappingIntermediate2009
- To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses. | `projects/1-ValDX/manuscript/report/1_introduction_omc.tex#L17` | cited: @puchadesEpitopeMappingDiverse2019
- With current models, most single-domain proteins can be predicted to near-experimental accuracy in hours on consumer-grade hardware. | `milestones/2025-11-confirmation-of-status/introduction/ensemble_generators.tex#L30` | cited: @varadiAlphaFoldProteinStructure2022

(39 citations)
