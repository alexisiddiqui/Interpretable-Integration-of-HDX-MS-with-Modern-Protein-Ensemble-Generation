---
project: jax-ka
experiment_id: opig-adaptyv-027
started: 2026-10-27
local_root: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface
source_repository: /Users/alexi/Documents/opig-adaptyv-2026
source_commit: f54c6d0505da5217b35c307a9a2edf3101b8e5dd
modal_volume: opig-design-runs
modal_prefix: 027-extremophile-vs-pka-surface
staged_inputs: .experiments/opig-adaptyv-027/inputs
access_audit: .experiments/opig-adaptyv-027/access-audit.json
figures: [jaxka-extremophile-overlap, jaxka-extremophile-chemistry, jaxka-extremophile-complex-confidence, jaxka-complex-linkage-selectivity, jaxka-extremophile-monomer-refolding]
---

# Extremophile fine tuning and pKa guided sequence design

Matching a change in formal surface charge revealed different sequence mechanisms in extremophile fine-tuning and pKa-guided design. The acidophile weights removed glutamate, whereas the pKa loss added lysine. Both alkaliphile routes enriched acidic residues, with different substitution preferences. When the target was included during design, the alkaliphile fine-tune lost the TNF binding pose despite retaining the binder fold. A subsequent loss comparing bound and free protonation produced predicted pH-selective binding, but increasing steering strength reduced pose retention. These results motivate using GQT to rank proposed mutations online, with structural compatibility constraining which proposals are retained.

The chemistry comparison uses binder-only designs. The complex-confidence and binding arguments use designs generated with the target present. Monomer refolding supports the chemistry comparison but does not establish binding competence. The original methods, results and corrections are in the [027 report][report].

## Access and available figure inputs

Experiment 027 belongs to `/Users/alexi/Documents/opig-adaptyv-2026`, rather than the thesis's `projects/4-jax-Ka/code` checkout. Its code, report and reduced results are in `experiments/027-extremophile-vs-pka-surface/` within that repository. The experiment directory had no uncommitted changes at source commit `f54c6d0505da5217b35c307a9a2edf3101b8e5dd` when checked on 2 November 2026.

The original sequence records and refold structures are on the Modal volume `opig-design-runs`, beneath `027-extremophile-vs-pka-surface/`. Inside run containers, this volume is mounted at `/runs`. Access requires an authenticated profile for the shared Modal workspace that owns this volume. The local CLI is `/Users/alexi/Documents/opig-adaptyv-2026/.venv/bin/modal`. Live listing of the experiment prefix and its 48 yield design records succeeded on 2 November 2026; the listings are staged in `.experiments/opig-adaptyv-027/modal-root-listing.json` and `modal-yield-designs-listing.json` under the thesis root. This is a storage read, without launching design or folding jobs.

| Contents | Location below the Modal experiment prefix |
|---|---|
| Baseline binder-only sequence records | `anchors-all-2026-10-28/designs/` |
| Target-context baseline sequence records | `anchors-target-2026-10-28/designs/` |
| Target-context surface-steered sequence records | `search-target-2026-10-28/designs/` |
| Target-context complex refolds | `complexcheck-target-2026-10-28/refolds/` |
| Linkage sweep sequence records | `select-2026-10-29/designs/` |
| Linkage yield sequence records | `select-yield-2026-10-29/designs/` |
| Linkage sweep and yield refolds | `selectcheck-2026-10-29/refolds/`, `selectcheck-yield-2026-10-30/refolds/` |

Individual structure paths are recorded in the local fold-check JSON rows as `pdb`; these paths are relative to the volume root, not to the experiment prefix. For binder-only matched steering records, `analysis.json` records each selected search tag in `inputs.steered_designs_loaded`; use those tags rather than loading every search trial.

To inspect the stored runs from the source repository, use the existing CLI environment.

```sh
cd /Users/alexi/Documents/opig-adaptyv-2026
.venv/bin/modal volume ls opig-design-runs 027-extremophile-vs-pka-surface --json
```

To retrieve an individual record or refold, use `.venv/bin/modal volume get opig-design-runs <volume-relative-path> <local-destination>`. Select `--profile` or `--env` if the active CLI configuration points at a different workspace or environment. Repository access alone does not grant volume access. The source repository's `docs/running/README.md`, lines 35–49, records the shared-workspace requirement.

Eleven reduced result files, totalling approximately 3.5 MB, are staged under `.experiments/opig-adaptyv-027/inputs/` in the thesis workspace. `access-audit.json` records their absolute source paths, sizes, SHA-256 hashes, source commit and coverage checks. These inputs support all three proposed main figures, plus the monomer-refolding supplement, without further remote computation.

| Figure input | Verified coverage | Additional retrieval needed |
|---|---|---|
| Surface chemistry and overlap | All 23 matched pairs; 20 finite amino-acid frequency changes for each matched backbone and arm | None for heatmaps, backbone points or null comparisons |
| Target-context complex confidence | 128 designs and two native sequences, eight refolds each, 1,040 rows; ipTM, scTM, pLDDT and recovery fields finite | None for the proposed confidence and pose panels |
| Linkage strength response | Median linkage and histidine count at each sampled strength | Individual-design linkage and histidine distributions require the Modal sequence records |
| Linkage pose yield | Eight designs per original sweep condition and 24 at each yield setting; eight repeated designs identified at strength 0.20 | None for yield curves and binomial intervals |
| Predicted binding response | All 12 and four passing yield designs at strengths 0.15 and 0.20 join to binding rows with finite pH-6 binder scores under all three predictors; target-context surface controls are present separately | None for per-design selectivity points or stored pH-grid profiles |
| Monomer refolding | 496 local design/native rows | None for existing scTM and pLDDT plots |
| Structural renderings and binder-specific pLDDT | Local rows identify the saved remote refolds | Retrieve selected structures |
| Matched GQT/pKAI inference speed | The local 027 file provides GQT timing only | Locate the separate matched benchmark |

The residue-level revision additionally uses 376 matched binder-only design records retrieved from the same Modal volume. They are staged in `.experiments/opig-adaptyv-027/replacement-records/`; `replacement-records-manifest.json` records each exact volume path and SHA-256 hash. The retrieval script is `figures/fetch_opig027_replacements.py` and reads only the designs selected by the monomer fold-check table, without launching compute jobs. Reconstructed matrices reproduce all 46 saved class matrices and the composition changes for all 35 arm–backbone comparisons to their reported precision. The check receipt is `.experiments/opig-adaptyv-027/qa/replacement-checks.json`.

## Experimental comparison

To distinguish mutation preferences from the magnitude of the charge change, we compared fine-tuned and steered designs at matched signed effects on formal surface charge. AcidSecMPNN and AlkSecMPNN used autoregressive decoding and were compared with vanilla ProteinMPNN. Four steered arms used Gibbs sampling on vanilla ProteinMPNN, combining either GQT or pKAI with a charge objective at pH 3 or 10. Their reference was an unsteered Gibbs arm, `gibbs0`. Each effect was measured against its own sampler's control.

| Arms | Model | Sampling | Objective | Reference |
|---|---|---|---|---|
| `vanilla`, `acid`, `alk` | ProteinMPNN, AcidSecMPNN, AlkSecMPNN, respectively | Autoregressive | Sequence likelihood | `vanilla` |
| `gibbs0` | ProteinMPNN | Gibbs | Sequence likelihood | `gibbs0` |
| `pka_gqt_acid`, `pka_pkai_acid` | ProteinMPNN | Gibbs | More positive free-binder surface charge at pH 3 | `gibbs0` |
| `pka_gqt_alk`, `pka_pkai_alk` | ProteinMPNN | Gibbs | More negative free-binder surface charge at pH 10 | `gibbs0` |

All arms used eight design seeds and temperature 0.1; Gibbs sampling used ten sweeps. Disulfide cysteines were fixed, additional cysteines were excluded, and every other position was designable. Surface positions had relative SASA at least 0.25. The loss acted on the surface, although ProteinMPNN could change buried residues. GQT used `ogqt-allres15-siamese-50`, epoch 17, approximately 180,000 parameters, checkpoint SHA-256 prefix `395beb5c`. This differs from experiment 015's `ogqt-relational-50-frozen` estimator. [Setup and checkpoint provenance][setup].

The matching statistic was `(K + R − D − E) / N_surface`. Histidine contributed to the denominator but not the numerator. Steering strength was fitted independently for each backbone and arm until the change from `gibbs0` matched the corresponding fine-tune's change from `vanilla`, within the backbone's replicate noise floor. Equal changes therefore did not imply equal absolute charges, and agreement in the fitted statistic was imposed by design.

Baseline designs covered 34 backbones; steering searches covered eight. Of 32 backbone–arm searches, 23 matched, six were weakly determined, two had no resolvable target and one exhausted the search. The main chemistry comparison uses six matched backbones across challenges 1, 2, 3 and 5. The pKAI alkaliphile arm has five because one comparison could not be matched. Weakly determined challenge-4 results are kept separate. Summaries weight each challenge equally. [Comparison population][population].

## Different surface chemistry at matched charge changes

The acidophile fine-tune raised formal surface charge mainly by removing glutamate, while pKa steering raised it mainly by adding lysine. AcidSecMPNN increased glutamine and alanine and slightly increased lysine; both pKa backends increased lysine much more strongly and also increased glutamate. The distinction is depletion of acidic groups versus enrichment of basic groups.

| Direction and arm | Surface frequency increases, percentage points | Surface frequency decreases, percentage points |
|---|---|---|
| AcidSecMPNN | Q +6.1, A +5.5, K +1.8 | E −5.0, P −4.8, N −2.8 |
| GQT acid steering | K +12.0, E +2.8, R +1.5 | S −5.1, A −5.0, T −3.2 |
| pKAI acid steering | K +12.8, E +3.3, R +0.9 | S −5.6, A −5.5, T −3.2 |
| AlkSecMPNN | E +18.2, D +4.5, K +1.8 | P −10.6, A −5.2, Q −3.6 |
| GQT alk steering | E +10.6, D +6.9 | S −6.5, A −2.6, K −2.4 |
| pKAI alk steering | E +9.1, D +7.2 | S −6.2, A −2.6, K −2.1 |

Values are changes against each arm's own reference on the matched set. Both alkaliphile routes enriched acidic residues, but the fine-tune favoured glutamate more strongly and depleted proline. Steering distributed the enrichment across aspartate and glutamate, depleted serine and reduced lysine. [Surface chemistry results][chemistry].

Residue-level replacement preferences resolve which control identities contribute to these changes. For each surface position, we multiply the control frequency of residue a by the design frequency of residue b, subtract the reverse exchange and average over surface positions. Results are expressed per 100 surface positions, with equal weight per challenge. This comparison uses all independent control–design draw pairs and does not pair designs by seed. Its signed column sums recover the composition changes.

AcidSecMPNN favours E→Q (+1.91 net replacements per 100 surface positions), while GQT and pKAI show small preferences in the reverse direction (−0.23 and −0.22). D→N is negative for all three acid arms. The scaffold-preserving interpretation therefore applies to the E/Q preference rather than to a general conversion of carboxylates to amides. The inference concerns corresponding sequence positions; side-chain geometry was not measured.

Proline and alanine provide a larger distinction among the non-polar residues. AcidSecMPNN favours P→A (+3.43), whereas acid steering favours A→K (+2.55 for GQT and +2.68 for pKAI). AlkSecMPNN favours P→E (+6.96), compared with +0.83 and +0.68 under GQT and pKAI. These preferences explain why matching a charge change leaves large differences in the residues removed from the surface.

Proline depletion also changes the hydrogen-bonding capacity of the backbone. An internal proline lacks a backbone N–H donor because its side chain closes onto the backbone nitrogen. Both P→A and P→E restore this donor, allowing hydrogen bonding with water where it is exposed or with a protein acceptor where the geometry permits. The P→A preference therefore offers a route to altered backbone hydration without introducing an ionisable side chain. Restoration of the donor is a chemical consequence of the replacement; increased hydration at these positions remains an interpretation. [Proline stereochemistry and stability][proline-stereochemistry].

Removing proline can relieve local conformational strain, but only where the original geometry is unfavourable. Opening the ring broadens the accessible backbone conformations and may allow local relaxation. Conversely, proline can preorganise a favourable turn and restrict the unfolded ensemble, so its removal can sacrifice stabilising rigidity. The net effect depends on the site and on both folded and unfolded states. Proline depletion alone does not establish strain relief or increased stability. [Proline stereochemistry and stability][proline-stereochemistry].

The replacement residue determines how these backbone changes couple to surface chemistry. P→A reduces side-chain bulk, but does not by itself establish a reduction in hydrophobicity. P→E adds a carboxylate that would generally be deprotonated at alkaline pH, providing an additional route to favourable hydration and electrostatic interactions. We therefore interpret the fine-tune preferences as potentially changing backbone hydration and conformational constraints alongside surface charge. The surface-charge loss does not directly reward a restored backbone donor or relieved strain, although sequence-dependent pKa predictions can respond indirectly to changes in the local environment. This distinction provides a biochemical hypothesis for the stronger proline depletion under fine-tuning.

For the thesis, the matched comparison supports this hypothesis on the sampled backbones, without establishing why the fine-tunes learned it. A broader paper would benefit from additional independent backbones and design draws, together with position-resolved analysis of backbone geometry, solvent exposure and hydrogen-bond partners. More samples would assess generality; structural and experimental evidence would be needed to distinguish hydration or strain relief from shared training-set preferences and to establish a benefit at extreme pH. The present analysis compares sequence ensembles and does not measure water organisation, strain energies or stability changes.

Both fine-tunes enrich methionine mainly at positions occupied by serine, glycine and proline in their controls. The corresponding preferences are small under either steering backend, and the fine-tunes show no net I→M or L→M preference. Backbone-level points show that these effects vary across systems. Their similar direction in both fine-tunes is compatible with a shared training-set preference, but this experiment does not distinguish that explanation from adaptation to extreme environments. Full signed matrices and challenge-weighted means are exported with the [revised chemistry figure](../../figures/jaxka-extremophile-chemistry/fig.pdf).

The methods acted at overlapping surface positions without reproducing the same residue preferences. Surface-position Jaccard scores were 0.559–0.577 against chance expectations of 0.366–0.400. Surface residue-frequency delta correlations were only 0.193–0.202 in the alk direction and 0.008–0.039 in the acid direction. Off-diagonal class-substitution profiles agreed beyond both wrong-direction and permutation nulls in all 11 matched alk comparisons. Acid-direction profiles exceeded the permutation null in only one of six backbones per backend. The class statistic describes substitution chemistry across the surface; it does not localise that agreement to shared positions. [Position and chemistry comparison][overlap].

These substitutions suggest that extremophile sequence preferences encode more than a target net charge. Removing a carboxylate and adding a basic side chain change the groups available for protonation, hydration and local interactions, even when the formal charge change agrees. The fine-tunes reflect sequences selected in different chemical environments, whereas GQT supplies a pKa-based score on the supplied backbone. This is the biophysical interpretation to develop from the comparison. Composition alone does not establish adaptation, stability or activity at extreme pH.

The training-environment context is that GQT was not trained on an extremophile adaptation task. Alexi's interpretation is that its structural training examples represent approximately room-temperature, near-neutral conditions. A claim that it has *only* seen such conditions needs the checkpoint's training-coordinate provenance; pKa labels themselves are not restricted to pH 7. This distinction matters when attributing the chemistry difference to the training environment rather than to the objective.

Binder-only ESMFold2 refolding supports structural compatibility of these chemistry changes. Across 496 analysed designs, 494 exceeded scTM 0.5, and arm-level family-weighted scTM values were 0.92–0.96 on the matched tier. The fine-tunes reduced predicted confidence, but also changed more residues and more buried positions. This monomer result establishes compatibility with the design backbone under the refolder, without testing a binding pose. [Monomer refolding][monomer].

## Fine tuning reduces confidence in complexes

To assess the fine-tunes in a binding context, the relevant comparison uses designs generated with the target chains present as fixed ProteinMPNN context. The surface mask, charge loss and pKa predictions still used the isolated binder, and fresh searches matched all eight target-context backbone–arm comparisons. Complex refolding used four ESMFold2 critics and two fold seeds per design. A pose passed when binder Cα RMSD after target alignment was at most 5 Å and binder ipTM was at least 0.5. [Target-context experiment][target].

Only TNF and TCR/pMHC passed the native-sequence pose-recovery control among the eight tested backbones, so the complex comparison is restricted to these two systems. Each arm has eight independent designs and eight refolds per design. Refolds measure consistency of recovery and must not be treated as 64 independent sequences.

| System | Arm | Whole-complex pLDDT | Binder ipTM | Binder scTM in complex | Pose-passing refolds |
|---|---|---:|---:|---:|---:|
| TNF | Native | 0.875 | 0.729 | 0.994 | 5/8 |
| TNF | Vanilla | 0.872 | 0.601 | 0.984 | 26/64 |
| TNF | AcidSecMPNN | 0.863 | 0.528 | 0.978 | 23/64 |
| TNF | AlkSecMPNN | 0.846 | 0.227 | 0.963 | 0/64 |
| TCR/pMHC | Native | 0.897 | 0.742 | 0.967 | 5/8 |
| TCR/pMHC | Vanilla | 0.849 | 0.393 | 0.931 | 1/64 |
| TCR/pMHC | AcidSecMPNN | 0.805 | 0.404 | 0.868 | 0/64 |
| TCR/pMHC | AlkSecMPNN | 0.802 | 0.350 | 0.872 | 0/64 |

Confidence and scTM values are means calculated from `fold-check-complexcheck-target-2026-10-28.json`, grouping `rows` by backbone and arm. The saved `plddt` averages the whole complex. Binder-specific pLDDT would require extracting residue-level values from the saved refolds.

AlkSecMPNN's TNF defect was primarily loss of interface confidence and pose recovery. Its binder still folded close to the design backbone, with mean scTM 0.963, but mean binder ipTM fell to 0.227 and no refold retained the pose. AcidSecMPNN retained the pose at a frequency similar to vanilla. The pKa-steered arms retained it in 19–31/64 refolds, compared with 23/64 for `gibbs0`; none differed detectably from that control at eight designs per arm. Interface mutation fraction alone did not explain the alk defect, because it rewrote 58% against vanilla's 52%. [Complex results][target].

Both fine-tunes reduced whole-complex pLDDT and binder scTM for TCR/pMHC. Pose recovery was poor across the redesigned arms, however, so this system supports a structural-confidence comparison rather than a selective claim about fine-tuning destroying binding. The larger mutation load and buried substitutions remain possible explanations for the fine-tune confidence penalty.

## Complex aware steering produces predicted pH selective binding

Target context preserved a usable TNF pose but did not make the surface-charge objective select pH-dependent binding. For pose-passing target-context designs, restrained OpenMM minimisation was followed by PROPKA, pKAI and pKAI+ predictions on the bound complex and separated partners. Protonation linkage gave predicted `log10[KD(pH)/KD(7.4)]`. Binder-site contributions were compared across arms because a target glutamate dominated some whole-complex PROPKA scores. Each design contributed its mean over passing refolds. [Binding readout][binding].

At pH 6, surface-charge steering gave approximately zero release under pKAI and pKAI+. AcidSecMPNN alone retained a modest response through interface histidines, with median binder-site scores of +0.44, +0.28 and +0.18 under PROPKA, pKAI and pKAI+, respectively. A free-binder charge objective at pH 3 or 10 does not reward a difference between bound and free protonation or between pH 7.4 and 6.0. Disagreement between predictors prevents a consistent binding interpretation at pH 3 and 10.

The subsequent `pka_gqt_select` arm directly rewarded linkage between bound and free states at pH 7.4 and 6.0. It used vanilla ProteinMPNN with Gibbs sampling and target context on TNF. This objective included target sites as well as binder sites. Steering strength was swept rather than matched to formal surface charge, because linkage is a different physical quantity. Native-sequence GQT predicted a binder-site score of +0.42, within the three checking predictors' +0.19 to +0.58 range. [Linkage experiment][linkage].

Increasing steering strength increased GQT linkage and histidine content but reduced pose retention. At strengths 0.025 and 0.05, the binder-site objective remained near zero and 6/8 or 7/8 designs retained the pose. At 0.4 and 0.8, the objective rose to +5.09 and +7.25 while no design retained the pose. A subsequent 24-seed experiment resolved the useful intermediate region.

| Steering strength | Designs | Median binder-site GQT linkage | Median His count | Designs retaining pose | 95% interval for pose retention |
|---|---:|---:|---:|---:|---|
| 0.15 | 24 | +1.32 | 6 | 12/24 | 29–71% |
| 0.20 | 24 | +2.25 | 8 | 4/24 | 5–37% |

The retained designs at strength 0.15 showed predicted release under all three checking predictors. Nine of twelve exceeded the native binder-site response under all three.

| Pose-passing population | n | PROPKA median | pKAI median | pKAI+ median |
|---|---:|---:|---:|---:|
| Source complex, rescored in yield run | 1 | +0.53 | +0.28 | +0.24 |
| Linkage steering, 0.15 | 12 | +1.50 | +0.96 | +0.65 |
| Linkage steering, 0.20 | 4 | +1.87 | +0.54 | +0.53 |

These scores are binder-site contributions to predicted log10 KD ratios. They provide a computational proof of concept on one backbone; they are not measured affinities or complete experimental binding free energies. GQT's increasing objective alone is not validation. The three checking predictors provide the corroborating calculation, and none supports a 100-fold switch for any design under all three predictors. [Yield and selectivity results][yield].

## Online mutation ranking as the next use of GQT

The steering response has an inactive region followed by a region where larger predicted selectivity costs the pose. Strength 0.15 shows that a useful compromise exists on TNF, but it does not establish a generally transferable strength or precise control over the resulting selectivity. The practical consequence is to rank mutations proposed by a structurally informed generator using GQT's change in linkage, while allowing structural compatibility to constrain acceptance. Ranking is the next methodological choice; this experiment did not compare its yield with continuous steering.

GQT makes online ranking practical by sharing the protein representation across predicted sites. pKAI constructs site-centred inputs and applies its predictor separately to each site, even when those inputs are batched. GQT predicts the sites together, so its opportunity for computational reuse is distinct from parameter count. The 027 checkpoint has approximately 180,000 parameters, compared with 3,608,001 for the native pKAI architecture, about twenty-fold fewer. A measured speedup at equal parameter count would isolate the architectural contribution. The [backbone-pKAI experiments][bbpkai] supply the prediction baselines, and the [joint pKAI record][jointpkai] documents the native architecture and expanded feature encodings.

Candidate scoring with GQT requires backbone coordinates and sequence, without side-chain reconstruction or minimisation. The backbone-pKAI comparator also avoids side-chain coordinates, but retains site-centred prediction. PROPKA checking of candidate sequences requires atomistic preparation in this workflow. The 027 timing probe measured 175 ms per batch of 20 candidates on the 595-residue complex, supporting online use; this is not itself a matched GQT-versus-pKAI timing benchmark (`results/selectivity-cost.json`).

## Data for the three figures

The figure drafts are [jaxka-extremophile-chemistry](../../figures/jaxka-extremophile-chemistry/fig.pdf), [jaxka-extremophile-complex-confidence](../../figures/jaxka-extremophile-complex-confidence/fig.pdf) and [jaxka-complex-linkage-selectivity](../../figures/jaxka-complex-linkage-selectivity/fig.pdf). The position-overlap and class-chemistry panels are now in [jaxka-extremophile-overlap](../../figures/jaxka-extremophile-overlap/fig.pdf). The supporting monomer figure is [jaxka-extremophile-monomer-refolding](../../figures/jaxka-extremophile-monomer-refolding/fig.pdf). Each folder also contains a PNG preview, SVG, plotted data, caption and provenance receipt. [Build instructions](../../figures/opig027-build.md) describe the input snapshot and shared code.

All filenames below are relative to the experiment's local root. The local JSON files contain analysis and refold metrics; sequence records and structure paths may refer to the Modal `opig-design-runs` volume. Rendering a structural example or extracting new residue-level measurements therefore requires retrieving the corresponding saved refold.

| Story and proposed panels | Data files and fields | Population and aggregation |
|---|---|---|
| Surface chemistry heatmap and substitution preferences | `results/analysis.json`, `readouts.2_position_frequencies.per_arm`, surface frequency deltas and per-backbone rows | Matched tier only, own-reference deltas, challenge-weighted summaries with backbone points |
| Surface overlap and class-chemistry agreement | Same file, `readouts.3_position_agreement.pairs`, `jaccard_surface`, `jaccard_chance_surface`, off-diagonal profiles and permutation-null summaries | Separate acid and alk directions; report location and chemistry separately |
| Supporting monomer refolding | `results/fold-check-foldcheck-2026-10-28.json` | Binder-only designs, matched backbones, own controls |
| Complex confidence and pose recovery | `results/fold-check-complexcheck-target-2026-10-28.json`, `rows[].binder_iptm`, `reproduced`, `binder_sctm_in_complex`, `plddt` | Target-context TNF and TCR separately; average eight refolds within each design before comparing arms |
| Interface mutation context | `results/interface-mutations-target-visible.json` | Target-context arms only; descriptive context rather than a causal explanation |
| Linkage and pose yield versus steering strength | `results/selectivity-sweep-select-2026-10-29.json`, `results/selectivity-sweep-select-yield-2026-10-29.json`, `results/fold-check-selectcheck-2026-10-29.json`, `results/fold-check-selectcheck-yield-2026-10-30.json` | One point per design where available; binomial intervals for design-level pose yield |
| Predicted pH release by arm and predictor | `results/binding-ph-bindingph-select-2026-10-29.json`, `results/binding-ph-bindingph-yield-2026-10-30.json`, `rows[].profile` | Pose-passing designs; separate PROPKA, pKAI and pKAI+; distinguish binder-site from total scores |

The complex-aware sweep used one critic and one fold seed per design, whereas the target-context surface comparison used eight refolds per design. Their pose yields must retain those different protocols. The 0.20 yield run repeats the sweep's first eight design seeds, so the 24-design yield population replaces the eight-design sweep population at that strength. Binding distributions must display the pose-retention denominator alongside them.

The charge analysis must use per-design pKas. An earlier implementation applied native-sequence pKas to designed identities; the corrected report withdraws its pH 7.4 and pH 10 charge interpretations. The current substitution and overlap results provide the primary chemistry evidence. [Charge correction][correction].

## Gaps

- Locate the completed matched inference benchmark before assigning a numerical GQT-versus-pKAI speedup, including any comparison at equal parameter count.
- Locate checkpoint-specific training-coordinate provenance for the room-temperature, near-neutral training-environment interpretation.

[report]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:1
[setup]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:29
[population]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:239
[chemistry]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:266
[overlap]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:360
[monomer]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:539
[target]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:647
[binding]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:718
[linkage]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:778
[yield]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:848
[correction]: /Users/alexi/Documents/opig-adaptyv-2026/experiments/027-extremophile-vs-pka-surface/README.md:922
[bbpkai]: ../../projects/4-jax-Ka/code/experiments/4_backbone/09_backbone_baseline_results.md
[jointpkai]: ../../projects/4-jax-Ka/code/experiments/3_paired_complex/48_pkai_joint_scale.md:3
[proline-stereochemistry]: https://doi.org/10.1371/journal.pcbi.0030241
