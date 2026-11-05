# 06 jax-Ka

Paragraph outline for `thesis/chapters/06-jax-ka.tex`. Each bullet develops one argument; the linked experiment notes retain the detailed comparisons and protocols.

## Motivation and computational titration models

- **Backbone pKa prediction connects side-chain-dependent protonation to inverse folding.** Designing pH-dependent binding requires reconciling the side-chain environments that determine protonation with the backbone representation used by ProteinMPNN and its variants. A predictor that accepts backbone coordinates and sequence could help rank proposed mutations by predicted protonation behaviour without rebuilding side chains for every candidate (own; [[027-extremophile-vs-pka-surface]]).

- **Titration methods trade computational cost against physical detail.** Introduce empirical PROPKA, Poisson–Boltzmann/Monte Carlo PypKa, constant-pH MD and learned pKAI/KaML predictors. Their assumptions define the reference against which a fast backbone model is assessed ([[@olssonPROPKA3ConsistentTreatment2011#^c1]]; [[PypKa computes protein pKa values with Poisson–Boltzmann electrostatics and Monte Carlo sampling of protonation states.]]; [[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]; [[@reisFastInterpretableDeep2022#^c1]]; [[@shenKaMLsPredictingProtein2025#^c1]]).

- **Computed labels and experimental pKas test different claims.** pKPDB and PINDER provide computational supervision, while PKAD-R and PKAD-3 assess agreement with experiment. Overall accuracy must be compared with the model-compound null and separated from performance on large shifts ([[pKPDB holds PypKa pKa estimates for structures across the PDB, so a model trained on it learns PypKa's pKas, not experimental ones.]]; [[A null model that assigns model-compound pKa values is hard to beat on experimental protein pKas.]]).

## Methods

- **The bound/free comparison isolates the predicted effect of the partner.** Each complex supplies AB and the isolated partners at their bound conformations, without relaxation. Binding-induced ΔpKa is the bound prediction minus the corresponding free prediction. pKPDB supplies PypKa state labels, PINDER supplies pKAI state and binding-shift labels, and the structural benchmark uses PypKa 2.10.0 ([[2026-10-29 jax-Ka data pipeline record and teacher]]; `projects/4-jax-Ka/code/experiments/00_shared.md`).

- **Preparation and masking define which labels remain usable.** Rebuilding atoms, stripping components and masking missing regions prevent incomplete environments from being treated as reliable supervision. Component and gap radii follow measured error against distance; their different noise targets reflect the tools used for calibration. Termini require explicit pKAI labels, and arginine has no teacher labels ([[2026-10-29 jax-Ka masking noise targets]]; [[2026-10-29 jax-Ka data pipeline record and teacher]]; `jaxka-component-cutoffs`, `jaxka-gap-cutoffs`).

- **Sequence separation fixes the evaluation question.** Training exclusions cover sequence overlap with held-out chains and experimental references, with CDR screening for antibodies. Pool-v4 holds out 800 PINDER clusters and 800 pKPDB groups; nested training fractions preserve groups. Development validation, the frozen structural benchmark and experimental pKas retain separate roles (`projects/4-jax-Ka/code/experiments/4_backbone/05_pinder_dataset.md`; [[jax-ka]]).

- **Shared graph features support state and binding-shift prediction.** Residues exchange information through spatial and sequence-relation edges carrying local-frame geometry; query tokens predict shifts from model-compound pKas. Shared bound/free weights train against state and binding-shift targets, with burial supervision. The appendix defines each loss, mask and reduction ([[A relational graph network gives each relation type its own weight matrix for messages between neighbours.]]; `projects/4-jax-Ka/code/models/ogqt-relational-50-frozen/model.json`).

- **All-residue prediction permits changes in titratable-site identity.** We introduced a prediction token at every residue so that pKa-based sequence optimisation could change which positions were titratable. The earlier site representation restricted mutations to existing titratable sites. All-residue prediction retains a readout as residue identities change, with the titratability gate determining its contribution (own; [[jaxka-edge-binder#Representation and comparison]]).

## Backbone pKa and binding-shift prediction

- **Joint pKAI training improves all-atom prediction more than backbone prediction.** At full data, joint training lowers all-atom pKPDB MSE from 0.319 to 0.287 and interface paired MSE from 0.059 to 0.034; backbone pKPDB MSE changes from 1.045 to 1.043. This comparison motivates testing a representation built around backbone geometry. It combines PINDER state and paired losses and uses one seed (`jaxka-pkai-siamese`; `projects/4-jax-Ka/code/experiments/4_backbone/09_backbone_baseline_results.md`).

- **Orientation and dihedrals improve backbone GQT prediction.** At full data, mean selection MAE falls from 0.6503 to 0.6212, comprising state MAE 0.4143 to 0.3923 and interface binding-shift MAE 0.2360 to 0.2289. Side-chain dropout during training gives a further gain under backbone-only evaluation. Greater width, depth and experimental-pH supervision do not improve this comparison (`projects/4-jax-Ka/code/experiments/4_backbone/07_handoff.md`).

- **Relation maps improve the smaller-data model at modest computational cost.** At 50% data, typed relations lower selection MAE from 0.6494 to 0.6324 and outperform a similarly sized width control; the advantage disappears at full data. Relation maps add no attended pairs and cost 3–8% more training memory and 15–24% more step time at 1,536 residues (`jaxka-relational-edges`, `jaxka-relational-memory`).

- **Full attention adds cost without a consistent accuracy gain.** A full-attention second layer changes selection error from 0.6349 to 0.6344 in the seed-17 comparison, while adding 28% GPU memory and 29% step time. Coordinate gradients remain available across configurations, costing 1.5–1.6 GiB and 84–87 ms for the graph models at 1,500 residues; these timings include a dense candidate-pair feature rebuild (`jaxka-relational-memory`, `jaxka-coordinate-gradients`).

- **Experimental accuracy remains limited by large pKa errors.** On 1,421 common PKAD-3 entries, run4 has RMSE 1.42 and MAE 0.82, against 1.31 and 0.84 for the model-compound null. The full comparison separates common-support performance, residue types and shift magnitudes, so agreement with computational teachers does not become a claim of experimental superiority (`.experiments/jaxka-pkad/default-allres-report.md`; [[A null model that assigns model-compound pKa values is hard to beat on experimental protein pKas.]]).

## pKa-guided sequence design

- **Matched charge changes can arise through different sequence mechanisms.** Extremophile fine-tuning and pKa-guided steering alter surface chemistry differently even at matched formal-charge changes. Acidophile fine-tuning removes glutamate, whereas pKa steering adds lysine; the alkaliphile routes enrich acidic residues through different substitutions ([[027-extremophile-vs-pka-surface]]; `jaxka-extremophile-chemistry`, `jaxka-extremophile-overlap`).

- **A binding objective must account for target context.** Surface steering alone does not target pH-dependent binding. A bound/free linkage objective produces predicted pH selectivity on the TNF example, while stronger steering reduces pose retention. This trade-off motivates ranking sequence proposals under structural constraints ([[027-extremophile-vs-pka-surface]]; `jaxka-extremophile-complex-confidence`, `jaxka-complex-linkage-selectivity`).

## Developing the free-partner edge binder

- **Run4 establishes a contact readout from separately embedded partners.** All-residue contact and burial supervision extend the shared representation beyond titratable sites. The width-64 model has 180,000 parameters and free-edge AUROC 0.669, AP 0.029 and within-complex AUROC 0.605 on PINDER development validation ([[jaxka-edge-binder#Representation and comparison]]).

- **Hotspot augmentation improves local contact discrimination.** Within-complex ranking and asymmetric PeSTo masking direct training towards exposed candidate interfaces. PeSTo is used during training; inference uses unmasked backbone and sequence. Hmask reaches mean same-stratum swap accuracy 0.7563 and antibody/antigen accuracy 0.6656 across three seeds ([[jaxka-edge-binder#Run 4, hotspot masking and dRSA]]).

- **dRSA weighting favours contacts that bury exposed surface.** Weighting ranking targets by the smaller burial change at the two residues raises mean surface-interface AUROC from 0.6598 to 0.7004 and antibody/antigen swap accuracy from 0.6656 to 0.7039. The gains occur across seeds, while distance-defined within-complex AUROC and binding-shift MAE do not improve consistently ([[jaxka-edge-binder#Run 4, hotspot masking and dRSA]]; `jaxka-pinder-recipe-comparison`).

## Negative construction and geometric consistency

- **Negative construction determines what improved discrimination means.** Retyped and swapped-partner decoys increase overall swap accuracy while reducing antibody/antigen accuracy and leaving same-UniProt discrimination near chance. Within-complex noncontacts test local contact ranking without changing the partner's source. The retained recipe uses within-ranking weight 0.3 and disables retyped-decoy training ([[jaxka-edge-binder#Negative construction distinguishes contacts from sequence compatibility]]).

- **ANM consistency improves perturbation tolerance with mixed recognition gains.** Consistency training reduces the pKa penalty on approximately 2 Å ANM views from 0.038–0.040 to 0.023–0.026. Antibody/antigen swap accuracy rises across seeds while overall swap accuracy falls; edge-only augmentation and its dRSA combination provide no general discrimination gain ([[jaxka-edge-binder#ANM consistency changes robustness and discrimination differently]]).

## POISK diagnoses the source of apparent improvement

- **Run4, hmask and dRSA improve external binder/decoy discrimination.** On 11,111 apo pairs, top-50 CDR edge accuracy rises from 0.4366 to 0.7115 and 0.7131; predicted-dRSA-weighted CDR accuracy rises from 0.4895 to 0.6671 and 0.6755. These are different reductions of the same outputs ([[028-poisk-free-monomer#Improvements depend on the readout]]; `jaxka-poisk-recipe-comparison`).

- **Most of the gain survives replacing the antigen.** Wrong-antigen weighted-CDR accuracies remain 0.665 and 0.666 for hmask and dRSA. Antibody-only learned readouts and sequence-composition controls expose binder/decoy pool membership as a shortcut that antigen holdout does not remove ([[028-poisk-free-monomer#Wrong-antigen and sequence controls identify the shortcut]]).

- **Removing the decoy pool reveals a smaller pairing signal.** With the antibody fixed, the learned hmask readout ranks its own antigen against wrong antigens at accuracy 0.566 and top-1-of-10 retrieval 0.147. Sequence-composition products give 0.532 and 0.124. This supports using blind scores to prioritise candidates for structural testing ([[028-poisk-free-monomer#Removing the decoy pool exposes a smaller pairing signal]]).

## KRAS pMHC screening

- **Matched target contexts guide candidate selection.** The hmask checkpoint screens 69,060 ATLAS interface representatives against G12D pMHC with WT and peptide-free controls, retaining native fragments and their residue-edge assignments. The application tests the hmask branch, preceding dRSA ([[046-atlas-kras-screen#Completed blind screen]]).

- **Top-100 prediction identifies one high-confidence lead.** Across 300 ESMFold2 predictions, three candidates pass relative confidence gates. ID_1457932 reaches G12D interface iPTM 0.875 against WT 0.761, with four residues contacting mutant peptide position P6. All three candidates retain WT iPTM above 0.7, so predicted mutant preference does not establish WT avoidance ([[046-atlas-kras-screen#Top-100 complex prediction]]).

- **Structural comparisons locate the candidate interaction at the peptide groove.** Compare the crystal TCR and screened hit in mutant and WT contexts through electrostatics and hydrophobicity, then show the hit's aligned G12D, WT and peptide-free predictions. The maps describe saved contact surfaces and the renders separate component identity from local confidence. Without a matched random-library prediction cohort, the screen does not quantify enrichment from GQT ranking ([[046-atlas-kras-screen#Mutation-centred radial comparison]]; `jaxka-kras-pmhc-radial`, `jaxka-kras-pmhc-plddt`).

## Scaling and implications

- **Full data extends the width-128 gain to partner discrimination in one seed.** Under the 20-epoch schedule, contact AP rises from 0.0536 to 0.0619 and antibody/antigen swap accuracy from 0.6791 to 0.7147 between the 50% and 100% pools. Width 64 improves contact AP but loses antibody/antigen accuracy. The full-data protocols use complete PeSTo coverage with no masking fallbacks ([[jaxka-edge-binder#Data scaling]]; `jaxka-pinder-ablations`).

- **A longer schedule does not improve the reported objectives consistently.** At full data, the 40-epoch schedule reduces contact AP for both widths. Width 64 recovers antibody/antigen accuracy, while width 128 loses it; state-plus-interface MAE increases for both. The comparison changes learning-rate decay and stopping patience as well as the epoch budget, and retains the checkpoint selected by pKa error ([[jaxka-edge-binder#Data scaling]]).

## Appendix — loss functions and training recipes

[[Loss functions and training recipes (jax-Ka)]] records the equations, reductions, masks, gradient paths and recipe coefficients checked against the frozen implementations and saved run protocols.

- **State and binding-shift losses.** Define model-compound shifts, pKPDB state MSE, PINDER bound/free state MSE and binding-shift MSE, including masks and averaging within structures before batches. Distinguish training MSE from the validation MAE used for checkpoint selection (`projects/4-jax-Ka/code/src/pkatrain/gqt_multitask_replay.py`; model `protocol.objective`).

- **Auxiliary losses.** Define titratability BCE and cysteine weighting, bound/free burial BCE and burial-change regression, then contact BCE and bound-to-free distillation. Record target construction, sampled populations, coefficients and gradient paths for each term (`projects/4-jax-Ka/code/models/ogqt-allres15-siamese-50/model.json`; [[jaxka-edge-binder]]).

- **Ranking and negative losses.** Define the normalised within-complex target, distance softening, candidate sampling and dRSA weighting, including anchors with negligible target mass. Retyped and swapped-partner objectives belong to their ablation recipes (`projects/4-jax-Ka/code/models/ogqt-allres15-within-drsa-50/model.json`; [[jaxka-edge-binder#Negative construction distinguishes contacts from sequence compatibility]]).

- **Masking and consistency.** Specify which passes receive hotspot masks or alternative geometries and which losses remain on the original structures. Define edge-logit and pKa consistency penalties, their coefficients and whether gradients enter both branches. A recipe table identifies the active terms for run4, hmask, dRSA and the ANM ablations ([[jaxka-edge-binder]]; staged `_submission` launch definitions).

- **Sequence-design objectives.** Define surface protonation steering and bound/free proton-linkage steering separately from model training, including pH, sign, surface/site gates, arginine treatment and how the objective enters the sampler ([[027-extremophile-vs-pka-surface]]; source experiment `guide.py` and `selectivity.py`).
