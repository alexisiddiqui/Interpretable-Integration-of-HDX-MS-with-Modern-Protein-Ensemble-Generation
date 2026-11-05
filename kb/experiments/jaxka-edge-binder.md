---
project: jax-ka
experiment_ids: [residue-siamese-v1, negatives-v1, hotspot-mask-v2, drsa-within-v1, anm-aug-v1, anm-edge-v1, drsa-anm-v1, drsa-cap-v1, drsa-rel-v1, datascale-v1]
authoritative_location: isambard
runtime_root: /scratch/u6xq/hussain.u6xq/_runtime/jax-Ka/pkabench
submission_root: /scratch/u6xq/hussain.u6xq/_submission
staged_inputs: .experiments/jaxka-binder-isambard-2026-11-04
figures: [jaxka-pinder-recipe-comparison, jaxka-pinder-ablations]
---

# From backbone pKa prediction to a free-partner edge binder

The second half of [[06-jax-ka]] develops a residue-pair edge binder from the shared bound/free representation used for pKa and binding-shift prediction. Run 4 establishes the all-residue model. Within-complex ranking, PeSTo hotspot augmentation and dRSA weighting then direct its free-state embeddings towards interface recognition. Negative construction and ANM consistency test which improvements survive more discriminating comparisons. [[028-poisk-free-monomer]] tests transfer to antibody binder/decoy discrimination, and [[046-atlas-kras-screen]] records the structural screen.

## Representation and comparison

All-residue prediction was introduced to make pKa-based sequence optimisation accommodate changes in titratable-site identity. The earlier site representation restricted mutations to existing titratable sites. Giving every residue a token retains a prediction site as residue identities change, with a titratability gate determining its contribution. This design motivation precedes the use of the representation for contact prediction (own).

Run 4 is `control-v2-50-relations-4-1-allres-cut15-cysmask-gate01-ressiamese-redge01-s17`, epoch 17. The model has 180,000 parameters and width 64. It uses backbone coordinates and sequence, orientation edges and backbone dihedrals, relation maps 4/1 in the two residue layers, and an all-residue token graph with a 15 Å cutoff. The heads predict pKa, titratability, burial and residue-pair contacts. Shared bound/free supervision includes binding-induced pKa shifts, burial changes and distillation of bound contact predictions into the free branch. The [run-4 model card](../../projects/4-jax-Ka/code/models/ogqt-allres15-siamese-50/README.md) records the architecture, targets and checkpoint.

In PINDER, free means partner removal at the bound conformation. Cross-chain edges are masked while each partner is embedded; a subsequent pair head compares the separately embedded residues. These evaluations test free-branch prediction at a supplied conformation. POISK additionally supplies independently folded free partners.

Unless stated otherwise, the following results reuse the 800-complex pool-v4 development validation cohort. Checkpoints are selected by PINDER state MAE plus interface binding-shift MAE. “Clean pKa selection” excludes bonded-Cys sites. Interface ranking does not select a checkpoint. AUROC, AP, ranking accuracy and pKa MAE measure different quantities.

[[Loss functions and training recipes (jax-Ka)]] gives the complete retained objective and ablation coefficients, with the reductions, sampled populations and gradient paths checked against the frozen training implementations. Contact distillation detaches its bound target, while the executed ANM consistency recipes differentiate through both views. The titratability gate has its own BCE and does not multiply the pKa training loss.

## Run 4, hotspot masking and dRSA

Within-complex listwise ranking asks an interface anchor to distinguish its contacting residues from non-contacting interface residues on the same partner. Contact targets decrease with distance, noncontacts receive zero, and targets are normalised per anchor. The retained coefficient is 0.3. Because candidates come from one partner in one complex, they share its sequence and structural source.

Hotspot masking (`hmask-v2-50-within03-asym50-w064-s17`, epoch 18) adds an asymmetric augmentation. On half the training visits, one chain's residue identities are retained only on the top half of its surface ranked by PeSTo interface probability. Buried identities are masked. The free contact and within-ranking losses read this masked pass; pKa, gate and Siamese burial supervision retain their original passes. Inference is unmasked and requires no PeSTo calculation. The [hmask model card](../../projects/4-jax-Ka/code/models/ogqt-allres15-within-hmask-50/README.md) records the recipe and three seeds.

dRSA weighting retains that recipe and changes the within-ranking target to `soft(distance_ac) * min(dRSA_a, dRSA_c)`, where `dRSA = clip(RSA_free - RSA_bound, 0, 1)`. This gives greater target mass to contacts that bury exposed surface. About 48% of sampled anchors have negligible total target and are omitted. Native RSA supplies training targets only. The [dRSA model card](../../projects/4-jax-Ka/code/models/ogqt-allres15-within-drsa-50/README.md) and its [numerical summary](../../projects/4-jax-Ka/code/models/ogqt-allres15-within-drsa-50/validation-summary.json) record all three seeds.

| PINDER validation metric | Run 4, seed 17 | Hmask, mean of 3 seeds | dRSA, mean of 3 seeds |
|---|---:|---:|---:|
| Same-stratum swapped-partner accuracy | 0.7310 | 0.7563 | 0.7986 |
| Antibody/antigen swapped-partner accuracy | 0.6341 | 0.6656 | 0.7039 |
| Wrong-partner accuracy, different protein | 0.5571 | 0.5804 | 0.5901 |
| Contact-edge AP | 0.0291 | 0.0406 | 0.0458 |
| Within-complex contact AUROC | 0.6053 | 0.6575 | 0.6546 |
| Clean pKa selection | 0.6047 | 0.6127 | 0.6157 |

The matched hmask-to-dRSA comparison improves surface-interface AUROC from 0.6598 to 0.7004 and dRSA-weighted NDCG from 0.5195 to 0.5338. Surface-interface and swapped-partner improvements occur in each seed. The distance-defined within-complex AUROC decreases slightly. Binding-shift MAE over the fixed 29,305 clean sites changes from 0.06561 to 0.06608, with inconsistent large-shift gains across seeds. The edge-binder improvement therefore does not establish improved pKa prediction.

The [PINDER recipe figure](../../figures/jaxka-pinder-recipe-comparison/fig.pdf) shows contact AP, antibody/antigen swap accuracy and clean binding-shift MAE across run4, hmask and dRSA. Individual seeds and arithmetic means remain visible. The [supporting ablation figure](../../figures/jaxka-pinder-ablations/fig.pdf) separates negative construction, ANM consistency and scaling. Both have regeneration scripts, frozen source reports, point-level data and captions in their figure directories.

## Negative construction distinguishes contacts from sequence compatibility

The negative experiments compare retyped interface residues, cross-complex partner swaps, same-stratum swaps, curvature-matched swaps and within-complex noncontacts. Retyping constructs a synthetic sequence contrast; a swapped partner is an assumed negative, without a measured nonbinding label. Within-complex noncontacts have a structural noncontact label in the supplied pose. These constructions ask different questions.

The `negatives-v1` report evaluates true contacts against five same-stratum swapped partners per complex, with separate heteromer, homomer and antibody/antigen strata. Additional surface-only controls compare different proteins, the same UniProt partner in another complex and wrong antibodies. Exact score definitions, training protocols and run IDs are in `audits/negatives-v1/decoy-ranking/report.json`; the weight sweep is in `audits/negatives-v1/sweep/decoy-ranking/report.json`. Both are staged with [verified source checksums](../../.experiments/jaxka-binder-isambard-2026-11-04/source-receipt.json).

| Seed-17 training recipe | Same-stratum swap accuracy | Antibody/antigen swap accuracy | Same-UniProt wrong-partner accuracy | Within-complex AUROC | Clean pKa selection |
|---|---:|---:|---:|---:|---:|
| Run 4 | 0.7310 | 0.6341 | 0.5300 | 0.6053 | 0.6047 |
| Retyped and batch-swapped decoys (`decoy both`) | 0.8255 | 0.5659 | 0.5240 | 0.5933 | 0.6121 |
| Within-ranking coefficient 0.3 | 0.7460 | 0.6403 | 0.5120 | 0.6637 | 0.6121 |
| Within-ranking coefficient 1.0 | 0.7965 | 0.6558 | 0.4820 | 0.6870 | 0.6209 |

Cross-complex decoys increase overall swapped-partner accuracy while reducing antibody/antigen accuracy and leaving same-UniProt discrimination near chance. The hmask model record identifies the withdrawn decoy recipe's gain as a family-similarity shortcut. Within-complex ranking improves local contact discrimination with a pKa trade-off as its coefficient rises. The retained recipe uses coefficient 0.3 and turns off retyped-decoy training. These are comparisons of the recorded recipes, not isolated estimates of every loss term's contribution.

The early within-ranking arms in this table retain a retyped-decoy coefficient of 0.1, including the 0.3 and 1.0 ranking variants. Hmask removes that term. The [saved run protocols](../../.experiments/jaxka-loss-audit/source/protocols/) and [[Loss functions and training recipes (jax-Ka)#Complete retained objective and recipe coefficients|loss table]] identify the active terms explicitly.

The [weight-sweep report](../../.experiments/jaxka-binder-isambard-2026-11-04/negatives-v1/sweep/decoy-ranking/report.md) also reports a curvature proxy. It predicts interface membership among surface residues at AUROC 0.519, while correlating with surface RSA at Spearman 0.698. Curvature matching alone therefore supplies little interface-specific information.

## ANM consistency changes robustness and discrimination differently

`anm-aug-v1` draws minimised, approximately 1 Å ANM or approximately 2 Å ANM free-state views on half the visits. `anmtie` treats the alternative views as interchangeable training inputs. `anmcons` additionally penalises differences between alternative and crystal free-state edge logits and pKas, with weights 0.3 and 1.0 and gradients through both passes. Definitions are in the frozen `_submission/anm-aug-v1/train.sbatch`, retained in the [source snapshot](../../.experiments/jaxka-binder-isambard-2026-11-04/source/_submission/anm-aug-v1/train.sbatch).

| Seed | Hmask antibody/antigen swap accuracy | ANM-consistency accuracy | Hmask pKa penalty on 2 Å view | ANM-consistency pKa penalty |
|---|---:|---:|---:|---:|
| 17 | 0.6713 | 0.6915 | +0.0404 | +0.0237 |
| 29 | 0.6667 | 0.6713 | +0.0391 | +0.0255 |
| 43 | 0.6589 | 0.6667 | +0.0378 | +0.0233 |

The pKa penalty is alternative-view minus crystal clean selection on the same 793 complexes. Crystal-mode antibody/antigen swap accuracy increases in each seed, but overall swap accuracy decreases in each seed. This supports reduced sensitivity to these coordinate perturbations, with a mixed discrimination outcome. Carrying labels between nearby views is a training assumption; this comparison does not measure experimental pKa changes between conformations. Source `audits/anm-aug-v1/seeds/gates/gates.md`, [local copy](../../.experiments/jaxka-binder-isambard-2026-11-04/anm-aug-v1/seeds/gates/gates.md).

`anm-edge-v1` restricts alternative geometry to the edge losses and preserves the crystal free pass for pKa, burial and gate targets. Neither edge-only augmentation nor edge-only consistency improves the seed-17 crystal antibody/antigen swap result over hmask (0.6620 and 0.6698 against 0.6713). Source `audits/anm-edge-v1/gates/gates.md`, [local copy](../../.experiments/jaxka-binder-isambard-2026-11-04/anm-edge-v1/gates/gates.md).

`drsa-anm-v1` combines dRSA targets with edge-only alternative views. The dRSA weights remain defined by crystal RSA on those visits. At seed 17, antibody/antigen swap accuracy falls from 0.7023 to 0.6682 and dRSA NDCG changes from 0.5349 to 0.5334. On the 2 Å view, overall swap accuracy changes from 0.7874 to 0.7899. The augmented model raises scores on alternative geometries without a general improvement in discrimination. Source `audits/drsa-anm-v1/gates.md`, [local copy](../../.experiments/jaxka-binder-isambard-2026-11-04/drsa-anm-v1/gates.md).

## Width and relational-edge scaling

The final 50% comparisons retain the dRSA recipe and vary width or relation maps. The base uses width 64 and relation maps 4/1. Width 96 has one seed; width 128 and relation maps 6/1 and 6/6 have seeds 17, 29 and 43. The table reports unmasked development validation; three-seed rows are descriptive arithmetic means of the gate reports, with no new uncertainty test.

| Model | Parameters | Seeds | Clean pKa selection | Edge AP | Within AUROC | Antibody/antigen swap accuracy | All same-class swap accuracy | dRSA NDCG |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| dRSA, width 64, maps 4/1 | 180,000 | 3 | 0.6157 | 0.0458 | 0.6546 | 0.7039 | 0.7986 | 0.5338 |
| Width 96, maps 4/1 | 394,944 | 1 | 0.6179 | 0.0491 | 0.6607 | 0.7054 | 0.8063 | 0.5375 |
| Width 128, maps 4/1 | 693,856 | 3 | 0.6156 | 0.0505 | 0.6622 | 0.6806 | 0.8120 | 0.5383 |
| Width 64, maps 6/1 | 188,320 | 3 | 0.6140 | 0.0458 | 0.6541 | 0.6842 | 0.7858 | 0.5324 |
| Width 64, maps 6/6 | 209,120 | 3 | 0.6147 | 0.0453 | 0.6552 | 0.6925 | 0.7969 | 0.5340 |

Width 128 improves aggregate contact AP, within-complex ranking and overall swapped-partner accuracy, while reducing antibody/antigen swap accuracy. Additional relation maps do not supply a consistent improvement over 4/1. These axes do not produce a better model across the reported objectives. A blanket statement that scaling changes no metric would miss the contact gains.

Sources are `audits/drsa-cap-v1/{w096,w128}/s*/gates.md` and `audits/drsa-rel-v1/{rel61,rel66}/s*/gates.md`; the [download receipt](../../.experiments/jaxka-binder-isambard-2026-11-04/receipt.json) records every source path and verified SHA-256. Exact launch definitions are in `_submission/drsa-cap-v1/train.sbatch` and `_submission/drsa-rel-v1/train.sbatch`, retained in the staged source snapshot. These frozen snapshots identify the experiment code; a later checkout commit does not identify code used by an earlier run.

## Data scaling

At 100% data, the width-128 seed-17 model improves both contact AP and antibody/antigen swap accuracy relative to its 50% counterpart (0.0536 to 0.0619 and 0.6791 to 0.7147). Width 64 improves contact AP but reduces antibody/antigen accuracy (0.0463 to 0.0549 and 0.7023 to 0.6822). The width-128 result therefore extends the contact gain to partner discrimination under the full-data, 20-epoch schedule. This comparison uses one seed.

| Width | Epoch budget | Selected epoch | Edge AP | Antibody/antigen swap accuracy | All-strata swap accuracy | Clean state + interface MAE | Clean binding-shift MAE |
|---|---:|---:|---:|---:|---:|---:|---:|
| 64 | 20 | 20 | 0.0549 | 0.6822 | 0.8175 | 0.5930 | 0.06370 |
| 128 | 20 | 20 | 0.0619 | 0.7147 | 0.8430 | 0.5895 | 0.06380 |
| 64 | 40 | 15 | 0.0465 | 0.7054 | 0.8265 | 0.6023 | 0.06338 |
| 128 | 40 | 34 | 0.0598 | 0.7054 | 0.8523 | 0.5931 | 0.06371 |

The 40-epoch schedule gives mixed gains. Width 64 improves antibody/antigen swap accuracy while contact AP falls; width 128 improves overall swap accuracy while both contact AP and antibody/antigen accuracy fall. Clean state-plus-interface MAE increases for both widths. Width 64 stopped after 31 epochs and selected epoch 15, while width 128 ran 40 epochs and selected epoch 34. The longer schedule holds the base learning rate at $10^{-3}$ through epoch 20 before cosine decay to $10^{-5}$ at epoch 40, with the same $\sqrt{2}$ multiplier and patience increased from 8 to 16. It changes the optimisation trajectory as well as the epoch budget.

All four runs completed with exit code zero. Their executed protocols use `store-hotspot-v2`, covering 28,733 records, and every training epoch records zero masking fallbacks. They share the exported 50% dRSA model's pool-manifest hashes and the same 800-complex validation support, with 4,000 all-strata and 645 antibody/antigen swap comparisons. The actual masking coverage therefore resolves the uncertainty left by the earlier launch definition. Checkpoints remain selected by state-plus-interface MAE, with no selection on contact or partner-ranking performance.

Sources are `audits/datascale-v1/{w064,w128,e40-w064,e40-w128}/{masked2,residue}/report.json` and their saved training protocols, histories, selections and resource records. The [download receipt](../../.experiments/jaxka-pinder-2026-11-05/receipt.json) records remote checksums. The [figure source map](../../figures/jaxka-pinder-ablations/source.json), [scaling audit](../../figures/jaxka-pinder-ablations/scaling-audit.json) and [extracted values](../../figures/jaxka-pinder-ablations/plotted-data.csv) retain the source paths and numerical results. The incorporated full-data comparison covers widths 64 and 128 at seed 17.
