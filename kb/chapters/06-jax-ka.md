# 06 jax-Ka

Chapter hub for `thesis/chapters/06-jax-ka.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. Its place in the thesis is the pH thread ([[01-introduction]] §1.1 D3, §1.2 group 2, §1.3 group 2), and [[prion protein|MoPrP]] carries it. A pKa model that differentiates through backbone coordinates is a second forward model of the kind ch. 5 builds. The titration models (PROPKA, PypKa, constant-pH MD, pKAI, KaML) are introduced in the chapter preface, not in [[02-background]] §2.5.

Status sentence: in progress (frozen relational default, interface experiments open). **decision**: full research chapter, short chapter, or appendix. `DEADLINES.md` has no entry for it.

Markers:
- **gap**: something the chapter needs that has no verified source or manuscript form yet.
- **decision**: a choice to make before writing.

## Preface: computational titration models

Argument: the methods form a ladder of cost against physical detail, and jax-Ka sits at the fast end while being trained on a slower method. The preface ends on what that means for how jax-Ka can be assessed.

- **Empirical.** PROPKA estimates the [[pKa shift]] as a sum of desolvation, hydrogen-bond and charge–charge terms from one structure, in seconds ([[@liVeryFastEmpirical2005#^c1]]; PROPKA3, [[@olssonPROPKA3ConsistentTreatment2011#^c1]]; ligands and coupling, Søndergaard et al. 2011, [[@sondergaardImprovedTreatmentLigands2011]], no PDF). The earlier jaxpropka surrogate in the jax-Ka repository is a PROPKA-parameterised mean-field model (`docs/MODEL.md`); one sentence at most.
- **Poisson–Boltzmann with Monte Carlo.** Continuum electrostatics for the state energies, sampled over protonation states.
  - [[PypKa computes protein pKa values with Poisson–Boltzmann electrostatics and Monte Carlo sampling of protonation states.]]
  - The PypKa server and its precomputed PDB and AlphaFold DB values ([[@reisPypKaServerOnline2024]], no PDF). Historical anchors if wanted: Bashford & Karplus 1990, Yang et al. 1993, MCCE (not seeded).
- **Constant-pH MD.** Protonation and conformation sampled together; the reference that fixed-protonation MD approximates ([[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]). Cost limits it to single proteins.
- **Machine-learned predictors.** pKAI and pKAI+ predict pKas from the residue environment with a small network ([[@reisFastInterpretableDeep2022]], no PDF; check their training data before writing); KaML uses tree models and a graph attention network and introduces PKAD-3 ([[@shenKaMLsPredictingProtein2025]], no PDF).
- **Data.** Training labels are computed; experiment enters at validation.
  - [[pKPDB holds PypKa pKa estimates for structures across the PDB, so a model trained on it learns PypKa's pKas, not experimental ones.]]
  - PINDER supplies bound and unbound complexes ([[@kovtunPINDERProteinInteraction2024]], no PDF). Experimental sets: PKAD ([[@pahariPKADDatabaseExperimentally2019]]), PKAD-R ([[@chenPKADRCuratedRedesigned2025]]) and PKAD-3 (in KaML); none has a PDF yet.
- **Assessment.** Overall error rewards predicting no shift.
  - [[A null model that assigns model-compound pKa values is hard to beat on experimental protein pKas.]]
- **Architecture.** Attention over a protein graph, in local frames, with relation types.
  - Query–key–value attention ([[@vaswaniAttentionAllYou2017#^c1]], [[@vaswaniAttentionAllYou2017#^c2]]).
  - Residue graphs with local-frame direction, relative orientation and sequence-offset edge features ([[@ingrahamGenerativeModelsGraphbased2019#^c2]], [[@ingrahamGenerativeModelsGraphbased2019#^c3]]); backbone frames from N, Cα and C as in AlphaFold2 ([[@jumperHighlyAccurateProtein2021#^c9]]).
  - [[A relational graph network gives each relation type its own weight matrix for messages between neighbours.]]
  - Shared-weight bound and free branches ([[@bromleySignatureVerificationUsing1993#^c1]]); ANM perturbations for augmentation ([[@atilganAnisotropyFluctuationDynamics2001#^c1]]).
- Close on the hand-off to the research sections: jax-Ka is a fast, differentiable student of PypKa and pKAI, so its accuracy is bounded by theirs on the training distribution and is measured against experiment only on PKAD-R and PKAD-3.

- **gap**: PDFs for Søndergaard 2011, PypKa server 2024, pKAI 2022, KaML 2025, PKAD, PKAD-R and PINDER, so their blocks can be added.

## Detail moved from §1.7

- A backbone-only pKa predictor, the orientation Graph Query Transformer (oGQT) with relational edges: a spatial residue graph plus explicit ±1 and ±2 sequence edges, a separate key and value projection per relation, and titratable-site query tokens. Trained on pKPDB (PypKa labels) and PINDER complexes labelled by pKAI in the bound and free states, with a binding-shift loss and a burial auxiliary. Its readout differentiates through backbone coordinates. Stub (`projects/4-jax-Ka/code` `models/ogqt-relational-50-frozen`).
- What the current results test: that relational edges improve backbone-only pKa prediction (selection error 0.649 to 0.632 over three seeds at 50% of the pool, `experiments/4_backbone/08_frozen_relational.md`); that an experimental-pH auxiliary adds nothing (the head learns crystal against EM, not pH; `07_handoff.md`).
- The earlier Kd-ratio numbers (under 9% all-atom, 30% backbone, under 20% transformer) are not in the current records and are dropped.
- Application to test: which MoPrP sites change protonation between pH 4 and pH 7, and whether they sit in the regions that unfold.

## Drafting sources

- `projects/4-jax-Ka/code` experiment records (`experiments/4_backbone/`); chapter tex comments (`06-jax-ka.tex`).
- Preface papers are seeded in `kb/papers/` (see the Preface section below); seven still lack PDFs.
