# negatives-v1: same-class negatives (within-complex listwise, same-stratum swaps) vs run 4 and decoy both (w64), allres 15 A, 50%, seed 17

Selection = PINDER val state MAE + interface paired MAE (all sites / without bonded-Cys sites). Residue metrics on every PINDER validation residue with an RSA (residue-rsa-v1).

| arm | epoch | selection | no bonded Cys | state | interface | pKPDB | benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|
| e40-w064 | 15 | 0.6188 | 0.6023 | 0.3925 | 0.2264 | 0.4796 | 0.4977 |

## Paired (binding-shift) MAE without bonded-Cys sites, by the store's partner distance (A)

| arm | all sites | <=4 | 4-6 | 6-10 | >10 |
|---|---:|---:|---:|---:|---:|
| e40-w064 | 0.0634 | 0.4510 | 0.2000 | 0.0931 | 0.0085 |

## Burial on interface residues (37732 within 5 A of the partner): free branch vs RSA_free, bound branch vs RSA_bound, change vs dRSA

| arm | free AUROC RSA<0.25 | free Spearman | bound AUROC RSA<0.25 | bound Spearman | change: Spearman(dP, dRSA) | change: AUROC dRSA>0.05 | change: MAE(dP, dRSA) |
|---|---:|---:|---:|---:|---:|---:|---:|
| e40-w064 | 0.9721 | 0.9300 | 0.9633 | 0.9166 | 0.8685 | 0.9141 | 0.0545 |

## Interface from the free state (residue within 5 A of the partner)

| arm | residues | score | pooled AUROC | per-chain median AUROC (chains) |
|---|---|---|---:|---:|
| e40-w064 | all residues | predicted exposure (free) | 0.6649 | 0.6193 (1546) |
| e40-w064 | all residues | measured free RSA | 0.6676 | 0.6218 (1546) |
| e40-w064 | all residues | edge max (free) | 0.7429 | 0.7128 (1546) |
| e40-w064 | surface residues | predicted exposure (free) | 0.5780 | 0.5373 (1546) |
| e40-w064 | surface residues | measured free RSA | 0.5815 | 0.5409 (1546) |
| e40-w064 | surface residues | edge max (free) | 0.7070 | 0.6850 (1546) |

## Edges: e40-w064 (surface cross pairs, contact <= 10 A)

| branch | pairs | positive rate | AUROC | AP | macro AP |
|---|---:|---:|---:|---:|---:|
| free | 18956558 | 0.0138 | 0.7267 | 0.0465 | 0.1075 |
| bound | 18956558 | 0.0138 | 0.8605 | 0.1031 | 0.2253 |
