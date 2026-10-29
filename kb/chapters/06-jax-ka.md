# 06 jax-Ka

Chapter hub for `thesis/chapters/06-jax-ka.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. Its place in the thesis is the pH thread ([[01-introduction]] §1.1 B (prions), §1.2 group 2, §1.3 group 2), and [[prion protein|MoPrP]] carries it. A pKa model that differentiates through backbone coordinates is a second forward model of the kind ch. 5 builds. The titration models (PROPKA, PypKa, constant-pH MD, pKAI, KaML) are introduced in the chapter preface, not in [[02-background]] §2.2.

Status sentence: in progress (frozen relational default, interface experiments open). **decision**: full research chapter, short chapter, or appendix. `DEADLINES.md` has no entry for it.

Markers:
- **gap**: something the chapter needs that has no verified source or manuscript form yet.
- **decision**: a choice to make before writing.

## Preface: computational titration models

Argument: the methods form a ladder of cost against physical detail, and jax-Ka sits at the fast end while being trained on a slower method. The preface ends on what that means for how jax-Ka can be assessed.

- **Empirical.** PROPKA estimates the [[pKa shift]] as a sum of desolvation, hydrogen-bond and charge–charge terms from one structure, in seconds ([[@liVeryFastEmpirical2005#^c1]]; PROPKA3, [[@olssonPROPKA3ConsistentTreatment2011#^c1]]; ligands and coupled residues in PROPKA 3.1, [[@sondergaardImprovedTreatmentLigands2011#^c1]], [[@sondergaardImprovedTreatmentLigands2011#^c2]]). The earlier jaxpropka surrogate in the jax-Ka repository is a PROPKA-parameterised mean-field model (`docs/MODEL.md`); one sentence at most.
- **Poisson–Boltzmann with Monte Carlo.** Continuum electrostatics for the state energies, sampled over protonation states.
  - [[PypKa computes protein pKa values with Poisson–Boltzmann electrostatics and Monte Carlo sampling of protonation states.]]
  - The PypKa server precomputes values for over 200,000 PDB and AlphaFold DB structures ([[@reisPypKaServerOnline2024#^c2]]) and falls back to pKAI above 1,500 residues ([[@reisPypKaServerOnline2024#^c4]]). Historical anchors if wanted: Bashford & Karplus 1990, Yang et al. 1993, MCCE (not seeded).
- **Constant-pH MD.** Protonation and conformation sampled together; the reference that fixed-protonation MD approximates ([[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]). Cost limits it to single proteins.
- **Machine-learned predictors.** pKAI is a three-layer network on the N, O and S atoms within 15 Å, trained on PypKa shifts ([[@reisFastInterpretableDeep2022#^c1]], [[@reisFastInterpretableDeep2022#^c2]]); pKAI+ adds a penalty on large shifts and uses the same theoretical data ([[@reisFastInterpretableDeep2022#^c3]]). KaML uses a CatBoost tree model and the first graph attention network for protein pKa, with trees ahead ([[@shenKaMLsPredictingProtein2025#^c1]], [[@shenKaMLsPredictingProtein2025#^c3]]), and introduces PKAD-3: 1,167 pKas in 247 proteins ([[@shenKaMLsPredictingProtein2025#^c2]]).
- **Data.** Training labels are computed; experiment enters at validation.
  - [[pKPDB holds PypKa pKa estimates for structures across the PDB, so a model trained on it learns PypKa's pKas, not experimental ones.]]
  - PINDER supplies about 2.3 million dimers with holo, apo and predicted structures and interface-clustered splits ([[@kovtunPINDERProteinInteraction2024#^c1]], [[@kovtunPINDERProteinInteraction2024#^c2]], [[@kovtunPINDERProteinInteraction2024#^c3]]). jax-Ka's free state is partner removal at the bound conformation, not PINDER's apo structures. Experimental sets: PKAD, 1,350 wild-type and 232 mutant residues ([[@pahariPKADDatabaseExperimentally2019#^c2]]); PKAD-R, its curated successor ([[@chenPKADRCuratedRedesigned2025#^c1]], [[@chenPKADRCuratedRedesigned2025#^c3]]); PKAD-3 (in KaML).
- **Assessment.** Overall error rewards predicting no shift.
  - [[A null model that assigns model-compound pKa values is hard to beat on experimental protein pKas.]]
- **Architecture.** Attention over a protein graph, in local frames, with relation types.
  - Query–key–value attention ([[@vaswaniAttentionAllYou2017#^c1]], [[@vaswaniAttentionAllYou2017#^c2]]).
  - Residue graphs with local-frame direction, relative orientation and sequence-offset edge features ([[@ingrahamGenerativeModelsGraphbased2019#^c2]], [[@ingrahamGenerativeModelsGraphbased2019#^c3]]); backbone frames from N, Cα and C as in AlphaFold2 ([[@jumperHighlyAccurateProtein2021#^c9]]).
  - [[A relational graph network gives each relation type its own weight matrix for messages between neighbours.]]
  - Shared-weight bound and free branches ([[@bromleySignatureVerificationUsing1993#^c1]]); ANM perturbations for augmentation ([[@atilganAnisotropyFluctuationDynamics2001#^c1]]).
- Close on the hand-off to the research sections: jax-Ka is a fast, differentiable student of PypKa and pKAI, so its accuracy is bounded by theirs on the training distribution and is measured against experiment only on PKAD-R and PKAD-3.


## Methods: data preparation

Argument: every label comes from a prepared structure, and every site's label is only trusted away from the material that was removed or never modelled. The section fixes the states, the teachers, the masks that remove untrusted sites, and the splits that keep the held-out sets clean. One pipeline serves the benchmark and the training pools. Record: what was run, not the original build specification ([[2026-10-29 jax-Ka data pipeline record and teacher]]).

- **States.** Each complex gives AB, and each partner alone (A, B) in the bound conformation, without relaxation. ΔpKa is pKa(AB) minus the pKa of the free state that contains the site. Partners are run in their own box (`experiments/00_shared.md`, Glossary and States).
- **Sources.**
  - pKPDB, 121,283 entries screened, 63,814 structures and 1.79M clean sites kept; labels are PypKa (`experiments/4_backbone/05_pinder_dataset.md`).
  - PINDER 2024-02, 2.32M dimers prefiltered to 93,293 accepted, labelled by pKAI in the bound and free states.
  - A benchmark set of PDB assemblies and SAbDab antibody–antigen complexes (two partners, at most 1,500 residues, at least 500 Å² buried per side), labelled by PypKa 2.10.0.
- **Preparation.** First positive-occupancy altloc, waters and hydrogens removed, missing atoms rebuilt with PDB2PQR, disulfides kept within a partner and rejected across partners (`experiments/00_shared.md`, Prep policy). Rebuilt residues lose their own site labels.
- **Teachers.** PypKa 2.10.0 is the benchmark reference (dielectric 15, 0.1 M, GROMOS 54a7, Ser/Thr off). pKAI labels PINDER and is the training teacher, because it agrees more closely with PypKa. pKAI+ is scored in the benchmark and compared on PKAD, never used as a teacher. pKPDB labels come from PypKa versions whose API changed, so they are not equivalent to the 2.10.0 configuration; across the dataset that matters less than a preparation error (`experiments/1_benchmark/18_historical_pkpdb_settings.md`).
- **pKAI termini.** Released pKAI ignores termini. Converting real chain termini to NTR and CTR residues reduced the N-terminal MAE against PypKa from 0.90 to 0.50 (`05_pinder_dataset.md`, terminus labels). No teacher labels arginine.

## Methods: data cleaning and filtering

Argument: a site keeps its label only if its error from removed or missing material is below a noise target, so each kind of material gets a radius measured against that target. The tight targets are available only where the measurement tool allows them.

- **Noise target.** 0.1 pKa is the practical target and anything well under 0.5 is acceptable. Components use 0.01 (training) and 0.001 (evaluation) because their error was measured with PROPKA, whose finite cutoffs reach zero by about 22.5 Å ([[2026-10-29 jax-Ka masking noise targets]]).
- **Components are stripped, not rejected.** Ligands 15/25 Å, buffers 15/20 Å, glycans 20/25 Å, exposed ions 25/25 Å and buried metals 30/30 Å (training/evaluation), measured to the nearest removed heavy atom (`experiments/1_benchmark/07_stripped_reference_policy.md`, `15_buffer_mask_revision.md`). The glycan radii are deliberately conservative, about 5 Å beyond where their curve meets the targets. Error-against-distance figures exist for buffers (`audits/buffer-propka-v2`) and glycans (`audits/glycan-propka-ccd-v1`).
- **Gaps.** Radii come from deleting residues from fully modelled references and measuring the pKAI and PypKa error against distance to the nearest visible anchor, to the 0.1 pKa criterion. Terminal deletions of 10 to 50 residues and internal deletions of 5 to 20 give radii from 20 to 45 Å (`audits/radial-error-v2-nearcomplete`, 23 complexes with PypKa; `audits/pinder-longgap-v1`, 516 references with pKAI). Adopting them raised usable PINDER training sites from 1.8M to 2.66M.
- **Sequence leakage.** Training structures with a chain at least 70% identical over at least 80% of both sequences to a held-out chain are removed, with an experimental 30% rule and a 90% fragment rule for PKAD references. Antibody chains are screened by CDR (`05_pinder_dataset.md`, held-out exclusions v3).
- **Splits.** Benchmark split by sequence group at 30% identity and 80% coverage, with experimental reference chains reserved in test. Frozen usable interface pairs are 778 train, 151 validation and 523 test (`experiments/1_benchmark/16_structural_split_freeze.md`).
- **Training pools.** Pool-v4 holds 800 pKPDB groups and 800 PINDER clusters for validation, leaving 27,933 PINDER complexes and 56,191 pKPDB structures for training. Nested 10%, 50%, 75% and 100% subsets keep sequence groups whole.
- **Experimental labels.** PKAD-3 (1,804 records) and PKAD-R (317 retained records) are evaluation-only (`experiments/1_benchmark/10_experimental_inventory.md`, `26_experimental_expansion.md`).

## Detail moved from §1.7

- A backbone-only pKa predictor, the orientation Graph Query Transformer (oGQT) with relational edges: a spatial residue graph plus explicit ±1 and ±2 sequence edges, a separate key and value projection per relation, and titratable-site query tokens. Trained on pKPDB (PypKa labels) and PINDER complexes labelled by pKAI in the bound and free states, with a binding-shift loss and a burial auxiliary. Its readout differentiates through backbone coordinates. Stub (`projects/4-jax-Ka/code` `models/ogqt-relational-50-frozen`).
- What the current results test: that relational edges improve backbone-only pKa prediction (selection error 0.649 to 0.632 over three seeds at 50% of the pool, `experiments/4_backbone/08_frozen_relational.md`); that an experimental-pH auxiliary adds nothing (the head learns crystal against EM, not pH; `07_handoff.md`).
- The earlier Kd-ratio numbers (under 9% all-atom, 30% backbone, under 20% transformer) are not in the current records and are dropped.
- Application to test: which MoPrP sites change protonation between pH 4 and pH 7, and whether they sit in the regions that unfold.

## Drafting sources

- `projects/4-jax-Ka/code` experiment records (`experiments/4_backbone/`); chapter tex comments (`06-jax-ka.tex`).
- Preface papers are seeded in `kb/papers/` (see the Preface section below); seven still lack PDFs.
