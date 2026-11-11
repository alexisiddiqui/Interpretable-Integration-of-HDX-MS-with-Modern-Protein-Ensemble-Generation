# 06 jax-Ka

Paragraph outline for `thesis/chapters/06-jax-ka.tex`. Each bullet develops one argument; the linked experiment notes retain the detailed comparisons and protocols.

## Motivation and computational titration models

- **Backbone pKa prediction connects side-chain-dependent protonation to inverse folding.** Designing pH-dependent binding requires reconciling the side-chain environments that determine protonation with the backbone representation used by ProteinMPNN and its variants. A predictor that accepts backbone coordinates and sequence could help rank proposed mutations by predicted protonation behaviour without rebuilding side chains for every candidate (own; [[027-extremophile-vs-pka-surface]]). The shared backbone representation also supports interaction screening through contact scores between separately encoded partners. This second application requires distinguishing partner recognition from contact recovery within known complexes (own; [[jaxka-edge-binder#Representation and comparison]]).

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

- **Matched charge changes can arise through different sequence mechanisms.** Given the limited recovery of large experimental shifts, the initial design comparison assesses how protonation-guided steering changes sequence preferences. Extremophile fine-tuning and pKa-guided steering alter surface chemistry differently even at matched formal-charge changes. Acidophile fine-tuning removes glutamate, whereas pKa steering adds lysine; the alkaliphile routes enrich acidic residues through different substitutions ([[027-extremophile-vs-pka-surface]]; `jaxka-extremophile-chemistry`).

- **Extremophile adaptation may favour additional local strain when stabilising interactions compensate for it.** The pronounced proline-to-alanine and proline-to-glutamate preferences restore backbone N–H donors that can hydrogen-bond with protein acceptors as well as water. Removing proline releases its ring constraint, but newly available intramolecular hydrogen bonds could stabilise and constrain the resulting conformation. Under highly acidic or basic conditions, these internal interactions, together with hydration and electrostatics, could compensate for additional local strain. The substitutions therefore suggest reorganisation of the protein's hydrogen-bond network alongside surface charge, a balance that charge matching alone does not reproduce ([[027-extremophile-vs-pka-surface]]; `jaxka-extremophile-chemistry`; own interpretation).

- **Monomer refolding connects sequence chemistry to the binding comparison.** After interpreting the surface substitutions, briefly establish compatibility with the design backbone (494/496 predictions with scTM above 0.5), then ask whether the binding pose is also retained ([[027-extremophile-vs-pka-surface]]; `jaxka-extremophile-monomer-refolding`).

- **Target context alone does not make surface-charge steering select pH-dependent binding.** On TNF, a bound/free linkage objective increases predicted binder-site contributions to pH selectivity among designs retaining the pose, while stronger steering reduces pose retention. This trade-off motivates ranking sequence proposals under structural constraints ([[027-extremophile-vs-pka-surface]]; `jaxka-complex-linkage-selectivity`).

- **Predicted linkage and pose retention must be interpreted together.** Increasing steering strength raises the GQT linkage objective while reducing pose retention. Comparing these with PROPKA, pKAI and pKAI+ responses among retained designs distinguishes optimisation of the design score, its structural cost and corroboration by checking predictors ([[027-extremophile-vs-pka-surface]]; `jaxka-complex-linkage-selectivity`).

### Sequence-design figures and section plan

- [jaxka-extremophile-chemistry](../../figures/jaxka-extremophile-chemistry/fig.pdf) is the main-text chemistry figure. It supports the matched-charge comparison and the biochemical interpretation of residue preferences.
- [jaxka-complex-linkage-selectivity](../../figures/jaxka-complex-linkage-selectivity/fig.pdf) goes in the main text as the full figure, keeping the linkage score, pose retention and checking-predictor responses together.
- [jaxka-extremophile-monomer-refolding](../../figures/jaxka-extremophile-monomer-refolding/fig.pdf) goes in the appendix. A brief main-text reference bridges the chemistry comparison to binding; the appendix retains the detailed scTM, pLDDT and mutation-load comparison.
- [jaxka-extremophile-overlap](../../figures/jaxka-extremophile-overlap/fig.pdf) is retained in the experiment record.
- [jaxka-extremophile-complex-confidence](../../figures/jaxka-extremophile-complex-confidence/fig.pdf) is retained in the experiment record.

## Developing the free-partner edge binder

- **Backbone-compatible interaction scoring connects inverse folding to candidate screening.** As with pKa prediction, backbone-only design pipelines need a readout that accepts backbone geometry and sequence. Predicting contacts from separately embedded partners would also allow candidate interactions to be screened without first constructing a complex pose. The questions are whether these representations retain interface information and whether stronger contact supervision improves binding-shift prediction. PINDER tests this with cross-chain edges removed and each partner's bound conformation retained (own; [[jaxka-edge-binder#Representation and comparison]]).

- **Run4 establishes a contact readout from separately embedded partners.** All-residue contact and burial supervision extend the shared representation beyond titratable sites. The width-64 model has 180,000 parameters and free-edge AUROC 0.669, AP 0.029 and within-complex AUROC 0.605 on PINDER development validation. Contact AP is about twice the contact prevalence (0.0291 against 0.0138). Within-complex AUROC measures contact discrimination for supplied partners; swapped-partner accuracy tests whether the supplied partner scores above an alternative protein ([[jaxka-edge-binder#Representation and comparison]]; [[jaxka-edge-binder#Run 4, hotspot masking and dRSA]]; `jaxka-pinder-recipe-comparison`).

- **Ranking and hotspot masking improve local contact discrimination.** Low contact precision motivates within-complex ranking and asymmetric PeSTo masking towards exposed candidate interfaces. PeSTo is used during training; inference uses unmasked backbone and sequence. Comparing three-seed hmask means with the single run4 seed, within-complex AUROC increases from 0.6053 to 0.6575 and contact AP from 0.0291 to 0.0406. Hmask reaches mean same-stratum swap accuracy 0.7563 and antibody/antigen accuracy 0.6656. Ranking and masking change together, so this comparison measures their combined effect ([[jaxka-edge-binder#Run 4, hotspot masking and dRSA]]).

- **dRSA weighting favours contacts that bury exposed surface.** Distance-based ranking does not distinguish contacts by how much surface they bury. Weighting ranking targets by the smaller burial change at the two residues raises mean surface-interface AUROC from 0.6598 under hmask to 0.7004 under dRSA. This metric measures interface-residue discrimination among surface residues using each residue's highest contact score. Antibody/antigen swap accuracy rises from 0.6656 to 0.7039. Both gains occur across seeds, while distance-defined within-complex AUROC decreases slightly from 0.6575 to 0.6546 ([[jaxka-edge-binder#Run 4, hotspot masking and dRSA]]; `jaxka-pinder-recipe-comparison`).

- **Screening requires tests beyond contact recovery at bound conformations.** At checkpoints selected by state and interface binding-shift error, contact gains do not consistently improve binding-shift MAE. The hmask-to-dRSA mean changes from 0.06561 to 0.06608, with mixed changes across seeds. Because these contact gains were measured with bound conformations retained, using the scores for screening requires tests of partner discrimination under different negative constructions and transfer to independently folded inputs ([[jaxka-edge-binder#Run 4, hotspot masking and dRSA]]; own).

### Edge-binder figures and section plan

- [jaxka-pinder-recipe-comparison](../../figures/jaxka-pinder-recipe-comparison/fig.pdf) goes in the appendix. The main text discusses the run4, hmask and dRSA comparisons and refers to this figure.

## Negative construction and geometric consistency

- **Negative construction determines what improved discrimination means.** Retyped and swapped-partner decoys increase overall swap accuracy while reducing antibody/antigen accuracy and leaving same-UniProt discrimination near chance. Within-complex noncontacts test local contact ranking without changing the partner's source. The retained recipe uses within-ranking weight 0.3 and disables retyped-decoy training ([[jaxka-edge-binder#Negative construction distinguishes contacts from sequence compatibility]]).

- **Negatome exposes dependence on structure preparation even with curated negatives.** For the original Negatome-trained model, replacing cropped true partners with full-length AlphaFold monomers lowers accuracy from 0.881 to 0.550 on the same 74 complexes. A follow-up matches preparation during training and reaches 0.587 against 0.475 for the within-ranking control on the full 95-complex evaluation, but loses antibody/antigen swap accuracy and retains limited gains on the paired subset. This comparison separates preparation dependence from the sequence shortcuts tested subsequently in POISK ([[jaxka-negatome#Matching preparation changes the apparent discrimination]]; [[jaxka-negatome#Matched training gives limited and mixed gains]]).

- **ANM consistency improves perturbation tolerance with mixed recognition gains.** Consistency training reduces the pKa penalty on approximately 2 Å ANM views from 0.038–0.040 to 0.023–0.026. Antibody/antigen swap accuracy rises across seeds while overall swap accuracy falls; edge-only augmentation and its dRSA combination provide no general discrimination gain ([[jaxka-edge-binder#ANM consistency changes robustness and discrimination differently]]).

## POISK diagnoses the source of apparent improvement

- **Hmask and dRSA improve external binder/decoy discrimination over run4.** On 11,111 independently folded apo pairs, binder/decoy pairwise accuracy using the top-50 CDR edge mean rises from 0.4366 to 0.7115 and 0.7131; predicted-dRSA-weighted CDR accuracy rises from 0.4895 to 0.6671 and 0.6755. These are different reductions of the same outputs ([[028-poisk-free-monomer#Improvements depend on the readout]]; `jaxka-poisk-recipe-comparison`).

- **Most of the burial-weighted CDR discrimination survives replacing the antigen, including for dRSA.** Wrong-antigen weighted-CDR accuracies remain 0.665 and 0.666 for hmask and dRSA. In the matched learned-readout comparison, dRSA gives accuracy 0.897 with antibody-only features, 0.893 with the correct antigen and 0.896 with a wrong antigen. Sequence composition alone reaches 0.949. Binder/decoy pool membership therefore supplies a shortcut that antigen holdout does not remove ([[028-poisk-free-monomer#Wrong-antigen and sequence controls identify the shortcut]]).

- **Removing the decoy pool exposes limited antigen discrimination in the summary scores.** Holding each antibody fixed removes antibody-only pool discrimination. Learned combinations of the 18 GQT summary scores then rank the correct antigen against a stored wrong antigen at accuracies 0.501, 0.515 and 0.528 for run4, hmask and dRSA. This comparison uses one alternative antigen and a smaller evaluation support than the embedding-product analyses ([[028-poisk-free-monomer#Removing the decoy pool exposes a smaller pairing signal]]).

- **Hmask retains a modest pairing signal under the elementwise embedding readout; dRSA is close to sequence composition.** With the antibody fixed, pairwise accuracy is 0.539 for run4, 0.562 for hmask and 0.535 for dRSA, against 0.532 for sequence-composition products. Top-1-of-10 retrieval is 0.124, 0.146 and 0.128, against 0.125 for composition and 0.1 by chance. dRSA's stronger binder/decoy discrimination therefore does not translate into better antigen pairing under this trained readout ([[028-poisk-free-monomer#Removing the decoy pool exposes a smaller pairing signal]]).

- **Matched target contexts and complex prediction investigate blind-score priorities.** POISK does not establish partner specificity of the untrained screening scores or prospective enrichment. The KRAS application used blind scores as candidate priorities, then investigated the proposed interactions through matched target-context comparisons and complex prediction ([[028-poisk-free-monomer#Pose-dependent signal and screening consequence]]).

## Scaling and implications

- Scaling comparisons refer to panels D–F of [jaxka-pinder-ablations](../../figures/jaxka-pinder-ablations/fig.pdf) in the appendix.

- **Full data extends the width-128 gain to partner discrimination in one seed.** Under the 20-epoch schedule, contact AP rises from 0.0536 to 0.0619 and antibody/antigen swap accuracy from 0.6791 to 0.7147 between the 50% and 100% pools. Width 64 improves contact AP but loses antibody/antigen accuracy. The full-data protocols use complete PeSTo coverage with no masking fallbacks ([[jaxka-edge-binder#Data scaling]]; `jaxka-pinder-ablations`).

- **A longer schedule does not improve the reported objectives consistently.** At full data, the 40-epoch schedule reduces contact AP for both widths. Width 64 recovers antibody/antigen accuracy, while width 128 loses it; state-plus-interface MAE increases for both. The comparison changes learning-rate decay and stopping patience as well as the epoch budget, and retains the checkpoint selected by pKa error ([[jaxka-edge-binder#Data scaling]]).

## KRAS pMHC screening

- **The groove-facing mutation makes specificity a peptide–MHC recognition problem.** Asp6 is buried in the TCR-bound HLA-A*11:01 decamer complex. Challenge 5 of the 2026 Anthropic × Adaptyv Bio competition required G12D binding with WT and peptide-free MHC avoidance, giving the matched target contexts their purpose ([[046-atlas-kras-screen#Target rationale and competition context]]).

- **Matched target contexts guide candidate selection.** The hmask checkpoint screens 69,060 ATLAS interface representatives against G12D pMHC with WT and peptide-free controls, retaining native fragments and their residue-edge assignments. The application tests the hmask branch, preceding dRSA ([[046-atlas-kras-screen#Completed blind screen]]).

- **Top-100 prediction identifies one high-confidence lead.** Across 300 ESMFold2 predictions, three candidates pass relative confidence gates. ID_1457932 reaches G12D interface iPTM 0.875 against WT 0.761, with four residues contacting mutant peptide position P6. All three candidates retain WT iPTM above 0.7, so predicted mutant preference does not establish WT avoidance ([[046-atlas-kras-screen#Top-100 complex prediction]]).

- **Structural comparisons locate the candidate interaction at the peptide groove.** Compare the crystal TCR and screened hit in mutant and WT contexts through electrostatics and hydrophobicity, then show the hit's aligned G12D, WT and peptide-free predictions. The maps describe saved contact surfaces and the renders separate component identity from local confidence. Without a matched random-library prediction cohort, the screen does not quantify enrichment from GQT ranking ([[046-atlas-kras-screen#Mutation-centred radial comparison]]; `jaxka-kras-pmhc-radial`, `jaxka-kras-pmhc-plddt`).

## Appendix — loss functions and training recipes

[[Loss functions and training recipes (jax-Ka)]] records the equations, reductions, masks, gradient paths and recipe coefficients checked against the frozen implementations and saved run protocols.

- **State and binding-shift losses.** Define model-compound shifts, pKPDB state MSE, PINDER bound/free state MSE and binding-shift MSE, including masks and averaging within structures before batches. Distinguish training MSE from the validation MAE used for checkpoint selection (`projects/4-jax-Ka/code/src/pkatrain/gqt_multitask_replay.py`; model `protocol.objective`).

- **Auxiliary losses.** Define titratability BCE and cysteine weighting, bound/free burial BCE and burial-change regression, then contact BCE and bound-to-free distillation. Record target construction, sampled populations, coefficients and gradient paths for each term (`projects/4-jax-Ka/code/models/ogqt-allres15-siamese-50/model.json`; [[jaxka-edge-binder]]).

- **Ranking and negative losses.** Define the normalised within-complex target, distance softening, candidate sampling and dRSA weighting, including anchors with negligible target mass. Retyped and swapped-partner objectives belong to their ablation recipes (`projects/4-jax-Ka/code/models/ogqt-allres15-within-drsa-50/model.json`; [[jaxka-edge-binder#Negative construction distinguishes contacts from sequence compatibility]]).

- **Negatome supervision.** Define the listwise objective with zero-target non-partner candidates, its coefficient of 0.3 and the retyped-decoy term retained by the early recipes. Distinguish cropped-partner and matched full-length preparation, including the separate 74- and 95-complex evaluation supports ([[jaxka-negatome]]; [[Loss functions and training recipes (jax-Ka)#Negatome listwise supervision]]).

- **Masking and consistency.** Specify which passes receive hotspot masks or alternative geometries and which losses remain on the original structures. Define edge-logit and pKa consistency penalties, their coefficients and whether gradients enter both branches. A recipe table identifies the active terms for run4, hmask, dRSA and the ANM ablations ([[jaxka-edge-binder]]; staged `_submission` launch definitions).

- **Sequence-design objectives.** Define surface protonation steering and bound/free proton-linkage steering separately from model training, including pH, sign, surface/site gates, arginine treatment and how the objective enters the sampler ([[027-extremophile-vs-pka-surface]]; source experiment `guide.py` and `selectivity.py`).
