# Asymmetric hotspot-masked scoring of the residue edge head (hotspot-mask-v2, PINDER validation, free branch)

{'complexes': 800, 'more_than_two_chains': 0, 'with_contacts': 800, 'surface_pairs_true': 18956558}; strata {'hetero': 466, 'homo': 205, 'Ab/Ag': 129}; Ab/Ag with role 117 (antibody = chain 1 in 60); oracle pesto; masks {}. Pairwise accuracy, ties 1/2, chance 0.5. varying = only the chain that differs between true and decoy is masked (within / edge: chain 1 masked); both = v1 symmetric mask. Definitions in report.json.

| arm | mode | epoch | re-typed | swap all | swap hetero | swap homo | swap Ab/Ag | Ab/Ag varying antibody | Ab/Ag varying antigen | surface all | surface Ab/Ag | edge AUROC | edge AP | pKa clean |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| w064 | unmasked | 20 | 0.8310 | 0.8175 | 0.8099 | 0.9200 | 0.6822 | 0.6967 (n 300) | 0.6491 (n 285) | 0.6600 | 0.5814 | 0.7458 | 0.0549 | 0.5930 |

## Wrong-partner controls and within-complex ranking

| arm | mode | different protein | same UniProt other complex | Ab/Ag wrong antibody | within AUROC | within top-1 | hetero | homo | Ab/Ag |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| w064 | unmasked | 0.6060 (n 2330) | 0.5210 (n 333) | 0.5795 (n 585) | 0.6664 | 0.3039 | 0.6560 | 0.6857 | 0.6464 |

## Within ranking vs the dRSA-weighted target (drsa-within-v1; same anchors / candidates as within AUROC)

| arm | mode | anchors | NDCG dRSA (n) | Spearman dRSA (n) | NDCG distance | NDCG dRSA hetero | homo | Ab/Ag |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| w064 | unmasked | 69825 | 0.5440 (37146) | 0.2255 (37146) | 0.5257 | 0.5537 | 0.5164 | 0.6107 |

## Chain-1-masked vs chain-0-masked (within AUROC, edge AUROC / AP; the other chain full)

| arm | keep | within AUROC c1-masked | within AUROC c0-masked | edge AUROC c1-masked | edge AUROC c0-masked | edge AP c1-masked | edge AP c0-masked | isolation max abs diff (c1 rows, c0 rows) |
|---|---:|---:|---:|---:|---:|---:|---:|---|

## Hotspot-only score (both mode)

| arm | mode | complexes | swap all | swap Ab/Ag | different protein | Ab/Ag wrong antibody |
|---|---|---:|---:|---:|---:|---:|

## GATES (control = w064; unmasked and varying at each run's keep, control beside)

| arm | mode | Ab/Ag-vs-Ab/Ag swapped | swapped partner all | wrong-partner different protein | within AUROC | edge AUROC | edge AP | pKa clean |
|---|---|---:|---:|---:|---:|---:|---:|---:|
