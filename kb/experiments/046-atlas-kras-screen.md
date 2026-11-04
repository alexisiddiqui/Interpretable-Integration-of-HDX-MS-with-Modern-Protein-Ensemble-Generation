---
project: jax-ka
experiment_ids: [opig-adaptyv-045, opig-adaptyv-046, opig-adaptyv-055]
source_repository: /Users/alexi/Documents/opig-adaptyv-2026
source_commit: cc143a5c51e954b0f2931f8fafa089784e694afc
modal_volume: opig-atlas-surface-clusters
modal_prefix: atlas-c5-hmask-fragments-20261031-a
figures: [jaxka-kras-pmhc-radial, jaxka-kras-pmhc-plddt]
---

# ATLAS screening prioritises a high-confidence KRAS G12D pMHC candidate

A blind hmask-GQT screen of 69,060 ATLAS hotspot-interface representatives supplied candidates for complex prediction against KRAS G12D pMHC, WT pMHC and peptide-free MHC controls. Of the first 100 source chains predicted in all three contexts, three pass the relative confidence gates and one has G12D interface iPTM above 0.85. This tests whether the representation developed in [[jaxka-edge-binder]] can prioritise a structural candidate despite the specificity limitation exposed by [[028-poisk-free-monomer]].

## Library and checkpoint

The high-confidence ATLAS population contains 171,265 exact-sequence-deduplicated source chains. Exposed residues in a native protein contact interface are intersected with isolated-chain PeSTo interface predictions. Clustering their surface fingerprints at the hotspot-80 cutoff produces 69,060 representatives. The cutoff is an exploratory fingerprint-similarity score, not 80% sequence identity or a measure of binding equivalence. Source [experiment 045](/Users/alexi/Documents/opig-adaptyv-2026/experiments/045-atlas-voronoi-clustering/interface_only/README.md:1).

Experiment 046 uses `ogqt-allres15-within-hmask-50`, model revision `b369add67830065bb3e4b9552a5217e2c49701a1`, parameter SHA-256 `fd46dd6159ddcec450213c5d2d83be8bb73dc4ff611d1e65c13d19c3ef6a17ce`. The ATLAS result belongs to the hmask branch of model development. It does not test the later dRSA checkpoint. The frozen membership is `atlas-interface-fingerprints-20261031-d/full/clusters/interface_hotspot/80/membership.parquet` on `opig-atlas-surface-clusters`. Source [experiment 046](/Users/alexi/Documents/opig-adaptyv-2026/experiments/046-atlas-fragment-hit/README.md:1).

## Completed blind screen

All 69,060 representatives scored without failure, yielding 459,946 unique native fragments and 16,855,977 residue–fragment pairings. Each of 89 target interface residues has 200 retained candidates. These 17,800 selected pairings contain 9,119 unique fragments. Every pairing preserves its source complex, native fragment coordinates and explicit source-residue/target-residue edge, with WT and empty-MHC contrasts. The blind screen proposes fragment contacts without a target docking pose. Source [completed screen](/Users/alexi/Documents/opig-adaptyv-2026/experiments/046-atlas-fragment-hit/README.md:23).

The screen compares G12D pMHC with matched WT, experimental WT and matched peptide-free HLA controls. Peptide position C:6 is the mutation site. Missing peptide edges in an empty-MHC context remain absent, while shared-groove contrasts compare the common target chains. These controls define directional candidate scores; their presence does not certify selectivity before structural testing.

## Top-100 complex prediction

The first 100 intact source chains by frozen `exposure_rank` were selected from a 1,026-patch exposure-weighted ranking. Some selected candidates failed the blind directional gates, so the prediction cohort is not a set of 100 blind positives. ESMFold2 completed all 300 predictions, one per source and context, using one sample and seed 102. The contexts were G12D pMHC, matched WT pMHC and peptide-free HLA-A*11:01/β2m. Target MSAs were supplied for HLA and β2m; candidate and peptide chains had no MSA. Source [experiment 055](/Users/alexi/Documents/opig-adaptyv-2026/experiments/055-kras-top100-pilot/README.md:19).

For each binder–target chain pair, the report uses the better directional iPTM and then averages over target chains. Target–target interfaces are excluded. A G12D pose passes when its full binder–target iPTM exceeds 0.7 and its WT counterpart, and its binder–HLA/β2m common-chain iPTM exceeds the empty-MHC counterpart. All positive metrics must come from the same G12D pose. Geometry was examined for the three passing candidates, using a 4.5 Å heavy-atom contact threshold.

| Source | Blind rank | G12D full iPTM | WT full iPTM | G12D common-chain iPTM | Empty common-chain iPTM | Source residues contacting mutant position P6 |
|---|---:|---:|---:|---:|---:|---:|
| ID_1457932 | 54 | 0.875 | 0.761 | 0.854 | 0.192 | 4 |
| ID_1233690 | 24 | 0.753 | 0.739 | 0.787 | 0.169 | 0 |
| ID_1230782 | 27 | 0.737 | 0.720 | 0.693 | 0.149 | 1 |

Source [top-100 results](/Users/alexi/Documents/opig-adaptyv-2026/data/designs/055-kras-top100-pilot/esmfold2-results/RESULTS.md:1) and [candidate table](/Users/alexi/Documents/opig-adaptyv-2026/data/designs/055-kras-top100-pilot/esmfold2-results/candidate-results.csv). The maximum G12D full-interface iPTM is 0.874608. ID_1457932 also has two original patch residues contacting P6, binder–peptide iPTM 0.917 and bound source-interface pLDDT 88.1. The other candidates' WT confidence margins are only 0.013 and 0.017.

The outcome is one lead above 0.85 iPTM among 100 predicted candidates, with relative predicted mutant preference and contact support at the mutated residue. All three passing candidates retain WT iPTM above 0.7. WT avoidance and experimental binding selectivity remain unresolved. Because no matched random-library prediction cohort was evaluated here, this result alone does not quantify enrichment caused by GQT ranking.

## Mutation-centred radial comparison

Figure `jaxka-kras-pmhc-radial` compares the enhanced JDIa41b1 TCR in experimental G12D and WT pMHC complexes (7OW6 and 7OW5) with the screened lead ID_1457932 in its predicted G12D and WT complexes. Both crystal structures contain the bound TCR and an observed mutation site. The comparison uses the dashboard's saved radial data and original renderer, with a common 25 Å radius and fixed property scales. The [combined electrostatic and hydrophobicity comparison](../../figures/jaxka-kras-pmhc-radial/fig.pdf) is accompanied by [surface height](../../figures/jaxka-kras-pmhc-radial/shape.pdf), [hydrophobicity](../../figures/jaxka-kras-pmhc-radial/hydrophobicity.pdf) and [side-chain size](../../figures/jaxka-kras-pmhc-radial/size.pdf) comparisons.

The maps project partner contact surfaces onto a frame defined by sequence-matched HLA groove Cα positions aligned to 7OW6. The observed peptide P6 Cα defines the origin, the peptide N-to-C direction defines the horizontal axis, and height follows the outward groove normal. Contacts use a 4.5 Å heavy-atom cutoff against the complete target. Footprints enclose projected buried solvent-accessible samples calculated using a 1.4 Å probe and 256 points per atom. Their projected area is not buried SASA. The TCR has one and two P6-contacting residues in G12D and WT, respectively; the predicted lead has four and one. These counts describe separate saved poses, not binding affinities.

Electrostatics represents the isolated complete partner in its saved bound conformation. PDB2PQR 3.7.1 with AMBER/PROPKA assigns pH 7 protonation, and APBS 3.4.1 solves linearised Poisson–Boltzmann at 298.15 K, 150 mM monovalent salt and protein/water dielectrics of 2/78.54. The fine grid contains 129³ points spanning 96 Å, and potentials are sampled on the original buried surface. Target charges are excluded. Hydrophobicity uses the Kyte–Doolittle scale; side-chain size is the union volume of modelled side-chain heavy-atom van der Waals spheres on a 0.4 Å lattice. Source [dashboard methods](/Users/alexi/Documents/opig-adaptyv-2026/docs/challenge-5/structures/README.md).

The [figure folder](../../figures/jaxka-kras-pmhc-radial/README.md) retains all four exact coordinate files for the separate structural views, complete radial records, source hashes, a reproducible builder and a [caption](../../figures/jaxka-kras-pmhc-radial/caption.md). Every coordinate hash matches its radial record. Crystal chains A/B/C are HLA/β2m/peptide and D/E are TCR; predicted chains A/B/C have the same target roles and D is the screened candidate.

The [pLDDT structural figure](../../figures/jaxka-kras-pmhc-plddt/fig.pdf) shows the lead in G12D, WT and peptide-free contexts using PyMOL cartoons, a common HLA alignment and a shared orthographic camera. The [regeneration script and instructions](../../figures/jaxka-kras-pmhc-plddt/README.md) retain all three CIFs, the editable session, camera and alignment checks. WT and peptide-free HLA align to the mutant with Cα RMSD of 0.106 and 0.285 Å over residues 1–180, respectively. The hit retains its different predicted position in the peptide-free context. These poses are ESMFold2 predictions. Refold verification with other models is in flight.

## Sources and artifacts

The source repository provides the [Challenge 5 dashboard](/Users/alexi/Documents/opig-adaptyv-2026/docs/challenge-5/index.html), [top-100 dashboard](/Users/alexi/Documents/opig-adaptyv-2026/data/designs/055-kras-top100-pilot/esmfold2-results/index.html), candidate table and complete report JSON. Local copies include all 300 prediction CIFs. Per-residue confidence arrays and original run artifacts remain on Modal.

Remote report and prediction roots below `opig-atlas-surface-clusters:/atlas-c5-hmask-fragments-20261031-a/` are `top100-method-pilot/20261101-a/` and `esmfold2-target-msa/20261101-a/cases/`. The [source receipt](../../.experiments/jaxka-binder-isambard-2026-11-04/opig-source-receipt.json) records report and table hashes. Experiment 055 ended after ESMFold2; no top-100 Boltz comparison was launched.
