# negatives-v1: same-class negatives (within-complex listwise, same-stratum swaps) vs run 4 and decoy both (w64), allres 15 A, 50%, seed 17

Selection = PINDER val state MAE + interface paired MAE (all sites / without bonded-Cys sites). Residue metrics on every PINDER validation residue with an RSA (residue-rsa-v1).

| arm | epoch | selection | no bonded Cys | state | interface | pKPDB | benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|
| w128 | 20 | 0.6079 | 0.5895 | 0.3820 | 0.2258 | 0.4576 | 0.4852 |

## Paired (binding-shift) MAE without bonded-Cys sites, by the store's partner distance (A)

| arm | all sites | <=4 | 4-6 | 6-10 | >10 |
|---|---:|---:|---:|---:|---:|
| w128 | 0.0638 | 0.4433 | 0.1969 | 0.0964 | 0.0094 |

## Burial on interface residues (37732 within 5 A of the partner): free branch vs RSA_free, bound branch vs RSA_bound, change vs dRSA

| arm | free AUROC RSA<0.25 | free Spearman | bound AUROC RSA<0.25 | bound Spearman | change: Spearman(dP, dRSA) | change: AUROC dRSA>0.05 | change: MAE(dP, dRSA) |
|---|---:|---:|---:|---:|---:|---:|---:|
| w128 | 0.9751 | 0.9368 | 0.9676 | 0.9249 | 0.8767 | 0.9187 | 0.0528 |

## Interface from the free state (residue within 5 A of the partner)

| arm | residues | score | pooled AUROC | per-chain median AUROC (chains) |
|---|---|---|---:|---:|
| w128 | all residues | predicted exposure (free) | 0.6679 | 0.6216 (1546) |
| w128 | all residues | measured free RSA | 0.6676 | 0.6218 (1546) |
| w128 | all residues | edge max (free) | 0.7566 | 0.7319 (1546) |
| w128 | surface residues | predicted exposure (free) | 0.5827 | 0.5408 (1546) |
| w128 | surface residues | measured free RSA | 0.5815 | 0.5409 (1546) |
| w128 | surface residues | edge max (free) | 0.7297 | 0.7057 (1546) |

## Edges: w128 (surface cross pairs, contact <= 10 A)

| branch | pairs | positive rate | AUROC | AP | macro AP |
|---|---:|---:|---:|---:|---:|
| free | 18956558 | 0.0138 | 0.7522 | 0.0619 | 0.1303 |
| bound | 18956558 | 0.0138 | 0.9148 | 0.1884 | 0.3757 |
