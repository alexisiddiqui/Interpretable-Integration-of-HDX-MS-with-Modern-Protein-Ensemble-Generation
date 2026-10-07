"""Hand-written node annotations. Every statement is tied to printed pages that were read in the PDF.
N[id] = dict(summary=..., quote=(text, printed_page) | None, type=..., template=..., pub=..., collab=...)
Types: background / method / result / discussion / appendix  (+ front-matter, references for non-body parts)."""

N = {}
def a(i, summary, quote=None, **kw):
    N[i] = dict(summary=summary, quote=quote, **kw)

# ------------------------------------------------------------------ Chapter 1
a('ch1', "Background chapter. Explains how small-molecule drug discovery works, introduces the ML tools used later (supervised learning, CNNs, GNNs/EGNNs, diffusion models), reviews ML for structure prediction, cryo-EM model building, virtual screening, generative design and fragment-based design, and outlines the thesis.",
  ("it must master two fundamental challenges", "4"), type='background',
  template="Background & motivation → Drug discovery → Machine learning → ML in early-stage drug discovery → Thesis outline",
  pub="Not stated (background chapter; no publication listed).")
a('s1.1', "Traces drug discovery from trial and error to rational and structure-based design, then states the cost problem (>10 years, median $1.3bn; lack of efficacy causes >50% of Phase II failures and safety ~20-25%). Argues for DL to improve the quality of early candidates and names two challenges that organise the thesis: intramolecular bonding (Chs 3-4) and intermolecular binding (Ch 2), with structure availability (Ch 5) as a prerequisite.",
  ("the use of deep learning (DL) algorithms to screen and design drugs in the early stages of development", "4"))
a('s1.2', "Overview of small-molecule drugs and the discovery pipeline. The thesis falls within target validation, hit identification and hit-to-lead.")
a('s1.2.1', "Small molecules (<1000 Da) dominate approvals: 32 of 50 novel FDA approvals in 2024.")
a('s1.2.2', "Pipeline: target identification and validation, hit identification, hit-to-lead / lead optimisation, preclinical and clinical trials; iterative with high attrition.")
a('s1.2.2.1', "Target identification and validation, and why structural characterisation (X-ray, cryo-EM) enables structure-based design.")
a('s1.2.2.1~cryo-em', "Short primer on cryo-EM: flash-frozen samples, 2D images, 3D density map. Building an atomic model into the map is not fully automated and is the bottleneck Ch 5 targets.",
  ("remains a major bottleneck", "8"))
a('s1.2.2.2', "Hit identification: HTS, virtual screening and fragment-based drug design (growing, linking, merging) as screening vs designing strategies.")
a('s1.2.2.3', "Hit-to-lead and lead optimisation, driven by the design-make-test-analyse cycle, with ligand-based and structure-based variants.")
a('s1.3', "Compact ML primer covering only the architectures used later.")
a('s1.3.1', "Supervised learning as loss minimisation over labelled data (eq. 1.1).")
a('s1.3.2', "Neural networks and deep learning: neurons, activation, backpropagation (eq. 1.2).")
a('s1.3.3', "Convolutional networks for grid-like data (eq. 1.3).")
a('s1.3.4', "Graph neural networks and message passing (eq. 1.4); E(n)-equivariant GNNs that update features and coordinates (eq. 1.5), the basis of PointVS and of the EDM-type diffusion models. Points to Appendix A.1 for equivariance.")
a('s1.3.5', "Diffusion models: a fixed noising (forward) process and a learned denoising (reverse) process; basis for Chs 3-5.")
a('s1.4', "How ML is applied in the early pipeline, organised as target structure resolution, virtual screening, generative design and fragment-based design.")
a('s1.4.1', "Target structure resolution: in silico prediction and ML-assisted cryo-EM model building.")
a('s1.4.1.1', "AlphaFold2, AlphaFold3 and open-source relatives (OpenFold, Boltz-1, Boltz-2). Caveat: subtle binding-site errors can mislead downstream screening and design, and many predictions for novel targets deviate >2 Å.",
  ("over 50% of predictions may deviate more than 2Å", "21"))
a('s1.4.1.1~alphafold2', "AF2: MSA, single and pair representations, evoformer, then a frame-based structure module.")
a('s1.4.1.1~alphafold3', "AF3: pairformer plus a diffusion module that denoises an atom cloud; handles proteins, nucleic acids and ligands.")
a('s1.4.1.1~open-source-models-and-extensions', "OpenFold (retrainable AF2 reimplementation), Boltz-1 (AF3 replication) and Boltz-2 (adds affinity and experiment-type bias).")
a('s1.4.1.2', "Cryo-EM model building: direct map-interpretation tools versus AlphaFold-based hybrids.")
a('s1.4.1.2~direct-map-interpretation-methods', "CNN and GNN tools (DeepTracer, ModelAngelo) build models from density; accuracy drops at intermediate-to-low resolution (≈4-8 Å) and ModelAngelo degrades beyond ~3.5 Å.")
a('s1.4.1.2~alphafold-based-methods', "ROCKET (conditions OpenFold) and CryoBoltz (conditions Boltz-2) are the two existing methods that Ch 5 builds on.")
a('s1.4.2', "Virtual screening: docking, then ML scoring functions (voxel CNNs, GNNs, equivariant nets). ML scoring functions are sensitive to dataset bias; only interpretability can say if a model learns binding physics.",
  ("only interpretability methods can come close to establishing whether a model is truly learning the physics of binding", "26"))
a('s1.4.3', "Generative molecular design, split into unconditional and conditional generation.")
a('s1.4.3.1', "Unconditional generation: 1D/2D models, then 3D models (equivariant nets, diffusion) that implicitly solve conformer generation.")
a('s1.4.3.2', "Conditional de novo generation: pocket-representation trade-offs, evaluation by docking score, and untested generalisation.",
  ("a self-referential loop where models are optimised to satisfy a flawed benchmark", "29"))
a('s1.4.4', "Fragment-based design with ML: elaboration (growing), linking and merging.")
a('s1.5', "Chapter-by-chapter outline: PointVS and hotspot-guided elaboration (Ch 2), negative data for diffusion (Ch 3), block-based diffusion (Ch 4), cryo-EM conditioning of AlphaFold models (Ch 5).",
  ("ensuring that ML outputs are not only accurate but also physically realistic and practically useful", "31"))

# ------------------------------------------------------------------ Chapter 2
a('ch2', "PointVS: an E(n)-equivariant GNN scoring function trained and tested on filtered data after CASF16 was found to leak. Edge-attention attribution is checked against PLIP, then applied to fragment-screen structures to extract hotspots that guide STRIFE fragment elaboration; elaborations are scored by docking.",
  ("was found to suffer from information leakage concerning almost every test structure", "34"), type='result',
  template="Preface → Contributions → Introduction → Methods (model, datasets, filtering, attribution, elaboration) → Results (scoring, attribution, hotspots, elaboration) → Conclusions",
  pub="Published: Scantlebury J*, Vost L* et al., J Chem Inf Model, 22 May 2023 (*equal contribution).",
  collab="Joint first-author work with Jack Scantlebury, who designed PointVS, filtered datasets and assessed it as a scoring function; Vost prepared the other attribution methods and ran attribution and fragment-elaboration tests (p. 35).")
a('s2.1', "Frames the aim: find hotspots (pocket regions contributing disproportionately to binding) to guide fragment growth. Summarises the chapter: CASF16 leakage, debiasing, edge-attention attribution, hotspots, better docking scores than a data-driven baseline.")
a('s2.2', "States who did what: Scantlebury designed PointVS, filtered data and assessed it as a scoring function; Vost did the other attribution methods, attribution tests and elaboration tests.",
  ("designed PointVS, carried out the dataset filtering, and conducted all assessments of PointVS as an MLBSF", "35"))
a('s2.3', "Motivation: MLBSFs tend to learn dataset bias; interpretability could show whether they learn interactions, and could supply structural information for FBDD. Introduces PointVS and releases the code and splits on GitHub.")
a('s2.4', "Methods: model, datasets, training-set filtering, attribution methods and the hotspot-to-elaboration pipeline.", type='method')
a('s2.4.1', "PointVS: 48 EGNN layers over a protein pocket (atoms within 6 Å of the ligand), edges built on the fly (10 Å ligand-protein, 2 Å intramolecular), plus a learned edge-attention score.")
a('s2.4.2', "Datasets: Redocked2020 for pose classification, PDBBind General for affinity regression, Core set as test.")
a('s2.4.2.1', "Redocked2020: Vina-redocked Pocketome ligands, <2 Å poses active; 52,385 active and 734,417 inactive poses.")
a('s2.4.2.2', "gninaSetPose: 441 PDBBind refined-set complexes held out to compare with gnina 1.0.")
a('s2.4.2.3', "PDBBind v2020 General set (training) and the 285-structure Core set (CASF16 test).")
a('s2.4.3', "Filtering: drop training ligands with Morgan Tanimoto >0.8 or proteins with >0.8 sequence identity to any test item; size-matched random subsets control for training-set size (Table 2.1).")
a('s2.4.4', "Three attribution routes: atom masking (any model), bond masking (graph models) and edge attention (PointVS). Compared across gnina, InteractionGraphNet and PointVS.")
a('s2.4.5', "From attribution to elaboration: extract hotspots from bound fragments, obtain fragments, elaborate with STRIFE, score by docking.")
a('s2.4.5.1', "Hotspot maps from PointVS edge attention versus the data-driven Hotspots API (details in Appendix A.2).")
a('s2.4.5.2', "Targets: SARS-CoV-2 Mpro (152 bound structures, includes curated follow-up compounds), Mac1 (58) and NSP14 (19) from fragalysis.")
a('s2.4.5.3', "Fragments obtained by enumerating acyclic single-bond cuts and placing a dummy exit atom.")
a('s2.4.5.4', "STRIFE: exploration then refinement stages; GOLD constrained docking picks 'quasi-actives' within 2 Å (API) or 3 Å (PointVS) of the hotspot. Some fragment-hotspot pairs cannot be elaborated.")
a('s2.4.5.5', "Assessment: GOLD constrained-docking score divided by heavy atoms, standardised against the ground-truth molecule, top-20 mean (ΔSLE20).")
a('s2.5', "Results across scoring performance, attribution, hotspot behaviour and fragment elaboration.", type='result')
a('s2.5.1', "Debiased training and scoring-function performance.")
a('s2.5.1.1', "Leakage in CASF16: 284/285 Core proteins have a ≥90%-identity counterpart in the General set, 273 (95.7%) identical, so a fair filtered-test comparison with other methods is impossible.",
  ("making any fair and unbiased comparison to these methods impossible", "49"))
a('s2.5.1.2', "Docking power barely changes with filtering (Top-1 70% vs 68% on gninaSetPose). Scoring power does: PCC 0.805 unfiltered, 0.803 size-matched random, 0.754 filtered, still above Vina (0.601).")
a('s2.5.2', "Does PointVS use real interactions? Compare attribution to PLIP on three Tankyrase-2 inhibitors and by distance correlation over many structures.",
  ("demonstrating that the attribution scores of PointVS relate to important binding interactions is a more direct measure", "52"))
a('s2.5.2.1', "Three Tankyrase-2 complexes (5C5P, 4J21, 4J22): PointVS edge attention ranks PLIP hydrogen-bond edges first and second in each, but misses one halogen bond; gnina atom masking and IGN bond masking agree much less.")
a('s2.5.2.2', "Over the Core set, attribution score correlates negatively with ligand-atom distance (PCC -0.766 top 5, -0.844 top 10); on a 20-structure subset PointVS (-0.710/-0.853) is far stronger than gnina (-0.233/0.094).")
a('s2.5.3', "Hotspots from PointVS on Mpro land in different places from Hotspots API hotspots (Fig 2.5).")
a('s2.5.3.1', "Control against simply counting contacts: PLIP counts yield four hotspots (146, 40, 9, 5 of 152); PointVS ranks the 146-count atom second and the 40-count atom first.")
a('s2.5.3.2', "Hotspots from random subsets of 10-80 structures (40 draws each): fewer structures give more variable hotspots, but the full-screen top 5 stay the most frequent even at 10.")
a('s2.5.4', "Elaboration: top-5 PointVS hotspots gave higher ΔSLE20 than top-5 API hotspots on all three targets; API hotspots ranked 6-10 scored higher, but the API could not rank its hotspots whereas PointVS ranks did separate good from worse.",
  ("unable to successfully rank them amongst themselves", "61"))
a('s2.6', "Concludes PointVS is competitive when debiased, identifies PLIP-consistent interactions and gives the first ML-based extraction of target structural information useful for elaboration. Links forward: de novo design with diffusion models.",
  ("the first ML-based method of extracting structural information from a protein target", "62"), type='discussion')

# ------------------------------------------------------------------ Chapter 3
a('ch3', "Conditioning an equivariant diffusion model on conformer quality: distorted molecules are added to training data as negative examples with a distortion label; sampling at zero distortion raises validity, strongly for drug-like datasets, weakly or negatively for QM9 and for flow-matching MolFM.",
  ("exploits the well-known utility of negative data as a resource in machine learning", "68"), type='result',
  template="Preface → Introduction → Methods → Results and discussion → Conclusions (limits and future work sit inside Conclusions; no separate Contributions section)",
  pub="Published: Vost L, Chenthamarakshan V, Das P, Deane CM. Digital Discovery 2025, 4(4), 1092-1099.")
a('s3.1', "Positions Ch 3 as a first step towards diffusion-based de novo design: diffusion models struggle with bond lengths, angles and energy for drug-like sizes; negative data can teach the model where valid space ends.")
a('s3.2', "Reviews 3D generation and its plausibility problem, then states the approach: condition EDM on conformer quality using distorted molecules from QM9, GEOM and a ZINC subset; also test GCDM and MolFM.")
a('s3.3', "Methods: EDM-style generation, distortion-based conditioning, metrics and datasets.", type='method')
a('s3.3.1', "EDM (first E(3)-equivariant diffusion model) and its variants GCDM and MolFM.")
a('s3.3.2', "Distortion recipe: sample D ~ U(0, Dmax) Å, add uniform offsets in [-D, D] to every coordinate, label with D, add to the dataset; sample at D = 0. Alternative label: XTB internal energy, sampled at the dataset's lowest energy.")
a('s3.3.3', "Metrics: 1000 samples per model (100 in ablations), bonds assigned by Open Babel, RDKit sanitisation, PoseBusters, MOSES diversity and REOS filters, bootstrap 95% CIs.")
a('s3.3.4', "Datasets: QM9, GEOM (no hydrogens used for ablations) and a 660,000-molecule ZINC subset.")
a('s3.3.4.1', "QM9: ~130,000 small molecules (average 8.2 heavy atoms).")
a('s3.3.4.2', "GEOM: ~430,000 molecules with conformers (average 20.1 heavy atoms); the no-hydrogen version trains fastest of the drug-like sets.")
a('s3.3.4.3', "ZINC subset: 660,000 drug-like molecules without repeat conformers, 26.8 heavy atoms on average.")
a('s3.4', "Results and discussion: ablation, distortion-factor conditioning, energy conditioning and transfer to other models.", type='result')
a('s3.4.1', "Ablation on GEOM (no H): best setting is 1 distorted per 50 originals with Dmax = 0.25 Å (RDKit 97%, PoseBusters 81%). Too much distortion hurts; sampling at D = Dmax gives poor molecules, so the label is informative.",
  ("Distorted molecules should therefore still bear some resemblance to realistic conformers", "77"))
a('s3.4.2', "Distortion conditioning with EDM: PoseBusters all-tests pass rate rises on GEOM (62.2 to 68.8%) and ZINC (40.0 to 74.5%) but falls on QM9 (81.1 to 46.9%).")
a('s3.4.3', "XTB internal-energy labels: best on GEOM (98% RDKit, 84% PoseBusters, n = 100) but worse on QM9 and ZINC; energies are hard to compare across molecules.",
  ("challenging to compare directly between different molecules", "81"))
a('s3.4.4', "GCDM improves clearly on ZINC (PoseBusters 40.8 to 66.5%) and marginally on GEOM; flow-matching MolFM gets worse on GEOM (80.8 to 46.8%) and slightly better on ZINC.",
  ("The reason for this degradation is unclear", "83"))
a('s3.5', "Concludes quality conditioning helps diffusion models on larger drug-like molecules, helps little on QM9 and is inconsistent for flow matching. Flags why-it-works and alternative labels as future work, then hands over to a fragment-based alternative.",
  ("selectively sample from the high-quality region of learned space", "84"), type='discussion')

# ------------------------------------------------------------------ Chapter 4
a('ch4', "An attempt to make diffusion easier by generating molecules from BRICS fragment 'blocks' instead of atoms. Centroid-only placement was capped by orientation ambiguity; adding orientation vectors raised RDKit validity to 51.7% at best, below the 84.7% atomistic baseline. Ends with a review of later hierarchical methods that work.",
  ("the highest-performing fragment-based model demonstrated inferior performance compared to the original atomistic baseline", "90"), type='result',
  template="Preface → Introduction → Methods → Results → Related Work → Conclusions",
  pub="No publication stated.")
a('s4.1', "Motivates the chapter: post-processing hides rather than fixes the plausibility problem. Hypothesis: arranging individual atoms is too hard, so use pre-assembled blocks.")
a('s4.2', "Two stated benefits of blocks: lower geometric dimensionality and potential synthesisability from commercial building blocks. Plan: adapt the Ch 3 EDM to blocks; the best block model did worse than atomistic.")
a('s4.3', "Methods: adapting EDM to blocks, decomposition schemes, rotational descriptors and metrics.", type='method')
a('s4.3.1', "Atom-based EDM recap, then changes needed for blocks.")
a('s4.3.1.1', "How atomistic EDM diffuses coordinates and categorical atom types.")
a('s4.3.1.2', "Adaptations: block centroids replace atoms, one-hot grows to ≥50 block types, and reconstruction places an RDKit conformer per block before Open Babel infers bonds.")
a('s4.3.2', "Training data and decomposition.")
a('s4.3.2.1', "QM9 rarely splits into more than two blocks, so GEOM is used.")
a('s4.3.2.2', "Two decompositions: raw BRICS and a reduced library.")
a('s4.3.2.2~regular-brics-decomposition', "Raw BRICS on GEOM gives >14,000 block types; keeping those seen >100 times leaves 172 types and 56,281 molecules.")
a('s4.3.2.2~decomposition-with-standardised-fragments', "Reduced library: canonical rings plus single atoms, 23 types, 62,746 molecules; framed as step one of a possible scaffold-then-decorate pipeline.")
a('s4.3.2.3', "Orientation descriptor: three 3D vectors per block (centroid, best-fit-plane normal, in-plane axis between the two most distant atoms). Heuristic is non-unique for symmetric blocks and ignores chirality.")
a('s4.3.3', "Metrics: same as Ch 3 in principle, but pass rates were so low that most analysis switched to visual inspection.")
a('s4.4', "Results for centroid-only, plane-aligned and rotation-aware block models.", type='result')
a('s4.4.1', "Control with ground-truth blocks and centroids: only 48/100 molecules pass RDKit, so the representation caps accuracy; the full model reaches ~4%.",
  ("even with perfect block placement, the ambiguity in fragment orientation leads to chemically invalid structures more than half the time", "97"))
a('s4.4.2', "Post-hoc plane alignment gives 10.8% sanitisation; failures are mostly wrong inter-block connectivity, so orientation must be learned.")
a('s4.4.3', "With orientation vectors the reconstruction control rises to 89/100; generation reaches 27.2% (full BRICS) and 51.7% (reduced library) versus 84.7% for the atomistic model.")
a('s4.5', "Related work since: HierDiff (coarse-to-fine with an EGNN decoder, >94% validity), CMD-GEN (pharmacophore pseudo-atoms then autoregression, 97.5%), SubGDiff (substructure-aware conformer generation, not comparable).",
  ("solving the orientation problem through a learned, end-to-end process rather than a predefined geometric heuristic", "100"), type='discussion')
a('s4.6', "Concludes the bottleneck is geometric variance in BRICS fragments that blocks a consistent local frame; recommends hierarchical models with a learned equivariant decoder.",
  ("high geometric variance within the chemically-derived BRICS fragments", "101"), type='discussion')

# ------------------------------------------------------------------ Chapter 5
a('ch5', "Preliminary work on conditioning AlphaFold-family structure prediction with cryo-EM density. Gradient-based map-overlap updates inside the OpenFold structure module gave only marginal, unstable gains; the same idea in diffusion-based Boltz-2 allowed larger rearrangements; MSA subsampling added the stochasticity needed to escape local minima. All tests use simulated maps and ground-truth alignment.",
  ("an overview of our preliminary work", "104"), type='result',
  template="Preface → Introduction → Methods → Results → Conclusions (limitations stated in Preface and Conclusions)",
  pub="No publication stated; described as preliminary work.")
a('s5.1', "Frames the problem (predictors fail on large or out-of-distribution systems, exactly where cryo-EM is used) and previews the OpenFold, Boltz-2 and MSA-subsampling findings and their limits.")
a('s5.2', "Cryo-EM growth and resolution limits; 'predict then refine' versus this thesis' idea of conditioning prediction on the map from the start (as ROCKET and CryoBoltz do).")
a('s5.3', "Methods: gradient-based map-overlap optimisation, update scheduling, MSA subsampling and datasets.", type='method')
a('s5.3.1', "Align the prediction to the map, simulate a density map, take a dot-product overlap, back-propagate to a chosen representation and add a scaled update at each recycle (OpenFold) or diffusion step (Boltz-2).")
a('s5.3.1.1', "Alignment uses the ground-truth PDB structure on Cα atoms, not usable on real new maps.")
a('s5.3.1.2', "Simulated map built by placing atom-type Gaussian kernels on a 3D grid.")
a('s5.3.1.3', "Overlap by dot product; gradient w.r.t. single, frame or coordinate representation.")
a('s5.3.1.4', "Full updates distort structures, so updates are scaled by a constant <1 chosen empirically.")
a('s5.3.1.5', "Three decay schedules for the scaling factor over 3 recycles × 8 blocks.")
a('s5.3.1.5~block-scheduling', "s = 1/i over the 8 blocks of a pass, reset each recycle.")
a('s5.3.1.5~global-scheduling', "s = 1/r over recycles, constant within a recycle.")
a('s5.3.1.5~block-and-global-scheduling', "s = 1/(8(r-1)+i), decaying from 1 to 1/24 without reset.")
a('s5.3.2', "Run five parallel MSAs sampled at 8192, 4096 or 2048 sequences, prune the lowest-overlap trajectory every 20 steps. Differs from ROCKET's very shallow MSA ladder.")
a('s5.3.3', "Ten small monomer targets whose vanilla predictions have Cα-RMSD 3-20 Å; simulated ideal maps; scored by Cα-RMSD only.",
  ("we are currently testing the method using ideal, simulated density maps generated from the ground-truth structures", "111"))
a('s5.4', "Results for OpenFold and Boltz-2 conditioning.", type='result')
a('s5.4.1', "OpenFold: three variants of structure-module conditioning.")
a('s5.4.1.1', "Constant scaling (0.1 coords/frames, 0.01 single): modest gains at coordinate and single level, none at frame level; 7VPL and 8CXO always worse (trapped in local density). 8FEI drifts about halfway to the answer.")
a('s5.4.1.2', "Decay schedules allow coordinate scaling of 1.0 but give no breakthrough; no representation-schedule pair wins consistently.")
a('s5.4.1.3', "Iterative updates: mixed. Best scheme improves 9/10 targets but only marginally; adaptive updates cut 8FEI from 3.58 to 2.20 Å yet fail badly elsewhere.",
  ("all improvements were marginal", "116"))
a('s5.4.2', "Boltz-2 is chosen because a diffusion process tolerates external guidance better and can model ligands.")
a('s5.4.2.1', "Gradient-only conditioning in Boltz-2: large rearrangements OpenFold could not make (8FEI 20.0 to 2.4 Å; 8CXO 11.7 to 7.7 Å) but worse on 6LLY and 7VLR.",
  ("inducing substantial rearrangements that were unachievable with OpenFold", "118"))
a('s5.4.2.2', "Adding MSA subsampling after concluding that late intervention cannot move large-scale structure.")
a('s5.4.2.2~only-msa-subsampling', "MSA subsampling alone helps 7VLR and 7VPL but is inconsistent; no clear best sequence number; max five MSAs for cost.")
a('s5.4.2.2~combining-with-gradient-based-optimisation', "Combined, it is the best approach tested excluding 8FEI (which gets worse); 2048 sequences most reliable overall but lowest RMSD on only 6/10 targets.")
a('s5.5', "Concludes late interventions struggle without breaking learned priors, Boltz-2 tolerates more, and early stochasticity helps; lists next steps (more MSAs, repeats, real noisy maps, no ground-truth alignment).",
  ("introducing stochasticity at an early stage is an effective means of broadening the explored conformational landscape", "122"), type='discussion')

# ------------------------------------------------------------------ Chapter 6
a('ch6', "Draws conclusions per application and four lessons: interpretability is central, negative data helps generative models, block generation needs sophisticated encoding, and guiding AlphaFold-like predictions needs early intervention plus stochasticity.",
  ("interpretability is central to ensuring that models learn physics rather than artefacts", "126"), type='discussion',
  template="One section per application (6.1-6.3) → Concluding remarks", pub="Not stated (conclusion chapter).")
a('s6.1', "Interpretability should be expected of VS models; debiased models plus attribution can guide design. With current datasets entirely bias-free scoring functions are impossible, so large consistent public protein-ligand datasets are needed.",
  ("it is impossible to train scoring functions that are entirely free from bias", "124"))
a('s6.2', "Negative data helps even where positives seem plentiful; block diffusion needs learned equivariant decoders or hierarchy; question whether diffusion that needs heavy filtering is justified.",
  ("the importance of mastering foundational principles before applying new, computationally expensive architectures", "125"))
a('s6.3', "AlphaFold-conditioning results are mixed; Boltz-2 plus MSA subsampling shows promise. Next steps: more MSAs, other schedulers, fine-tuning the predictors.",
  ("perhaps more by clarifying which strategies are ineffective than by arriving at a viable one", "126"))
a('s6.4', "Four lessons and a call for better datasets, benchmarks and more interrogation of models.",
  ("interpretability is central to ensuring that models learn physics rather than artefacts", "126"))

# ------------------------------------------------------------------ Appendices
a('app', "Appendices for Chapters 2 and 3.", type='appendix')
a('appA', "Supporting material for Chapter 2: equivariance primer, Hotspots API algorithm, structure IDs and an FGFR1 case study.", type='appendix')
a('sA.1', "Defines invariance and equivariance and why EGNN layers suit pose scoring better than CNNs. Written by Jack Scantlebury.", type='appendix',
  collab="Written by Jack Scantlebury (stated in the heading, p. 129).")
a('sA.2', "Hotspots API: SuperStar propensity grids from CSD data, probe sampling, greedy 1 Å clustering, clusters <8 points removed and scored by size.", type='appendix')
a('sA.3', "Fragalysis IDs of the bound structures for Mpro, Mac1 and NSP14, and the 20 PDBBind Core PDB IDs used in the attribution test (text mislabels this as section 3.4.2).", type='appendix')
a('sA.4', "FGFR1 / erdafitinib case study: PointVS ranks both hydrogen-bonding protein atoms 3rd and 6th; the API found only one site; a STRIFE elaboration recovers the same hydrogen bond.",
  ("making it the third fragment-derived drug to reach this stage", "133"), type='appendix')
a('appB', "Supporting tables for Chapter 3.", type='appendix')
a('sB.1', "Ablation sampled at D = Dmax (Table B.1): PoseBusters pass rate at most 53%. The thesis attributes the poor results mainly to internal-energy failures, stated in the main text on p. 78 rather than here.", type='appendix')
a('sB.2', "Full PoseBusters sub-test pass rates for every model and ablation. Table is uncaptioned in the thesis.", type='appendix')
a('sB.3', "MOSES diversity and eight REOS filter pass rates for baseline and conditioned models.", type='appendix')

# ------------------------------------------------------------------ non-TOC parts
F = {}   # front matter / back matter nodes (not in the TOC), with printed page ranges
F['fm'] = dict(title="Front matter", start='i', end='xx', summary="Title page, dedication, acknowledgements, abstract, contents, list of figures and list of abbreviations. There is no list of tables.", type='front-matter')
F['fm.title'] = dict(title="Title page", start='i', end='i', summary="Machine Learning for Molecular Modelling and Drug Discovery, Lucy Vost, Green Templeton College, University of Oxford, October 2025.", type='front-matter')
F['fm.dedication'] = dict(title="Dedication", start='iii', end='iii', summary="Dedicated to the author's grandmother.", type='front-matter')
F['fm.ack'] = dict(title="Acknowledgements", start='v', end='v', summary="Thanks to supervisors (including industry supervisors), the research group, friends and family; the PhD is described as four years of research.", type='front-matter')
F['fm.abstract'] = dict(title="Abstract", start='vii', end='viii', summary="Four-part summary: debiased virtual screening with interpretability and hotspots; conditioning diffusion on molecule quality; block-based diffusion that hit implementation challenges; cryo-EM conditioning of AlphaFold models with MSA subsampling.", type='front-matter',
                        quote=("pocket-free, 3D de novo molecule generation", "vii"))
F['fm.contents'] = dict(title="Contents", start='ix', end='xii', summary="Table of contents to subsection level.", type='front-matter')
F['fm.figures'] = dict(title="List of Figures", start='xiii', end='xvii', summary="Lists 26 figures; no list of tables is provided.", type='front-matter')
F['fm.abbrev'] = dict(title="List of Abbreviations", start='xix', end='xx', summary="Abbreviations used throughout (e.g. BRICS, CASF16, EGNN, MSA, PLIP).", type='front-matter')
F['refs'] = dict(title="References", start='141', end='155', summary="Bibliography, author-year style.", type='references')
