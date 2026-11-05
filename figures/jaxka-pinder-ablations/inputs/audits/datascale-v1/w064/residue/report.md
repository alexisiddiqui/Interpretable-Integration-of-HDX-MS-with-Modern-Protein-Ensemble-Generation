# negatives-v1: same-class negatives (within-complex listwise, same-stratum swaps) vs run 4 and decoy both (w64), allres 15 A, 50%, seed 17

Selection = PINDER val state MAE + interface paired MAE (all sites / without bonded-Cys sites). Residue metrics on every PINDER validation residue with an RSA (residue-rsa-v1).

| arm | epoch | selection | no bonded Cys | state | interface | pKPDB | benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|
| w064 | 20 | 0.6114 | 0.5930 | 0.3857 | 0.2258 | 0.4649 | 0.4822 |

## Paired (binding-shift) MAE without bonded-Cys sites, by the store's partner distance (A)

| arm | all sites | <=4 | 4-6 | 6-10 | >10 |
|---|---:|---:|---:|---:|---:|
| w064 | 0.0637 | 0.4403 | 0.2038 | 0.0964 | 0.0092 |

## Burial on interface residues (37732 within 5 A of the partner): free branch vs RSA_free, bound branch vs RSA_bound, change vs dRSA

| arm | free AUROC RSA<0.25 | free Spearman | bound AUROC RSA<0.25 | bound Spearman | change: Spearman(dP, dRSA) | change: AUROC dRSA>0.05 | change: MAE(dP, dRSA) |
|---|---:|---:|---:|---:|---:|---:|---:|
| w064 | 0.9742 | 0.9336 | 0.9648 | 0.9210 | 0.8723 | 0.9179 | 0.0543 |

## Interface from the free state (residue within 5 A of the partner)

| arm | residues | score | pooled AUROC | per-chain median AUROC (chains) |
|---|---|---|---:|---:|
| w064 | all residues | predicted exposure (free) | 0.6667 | 0.6210 (1546) |
| w064 | all residues | measured free RSA | 0.6676 | 0.6218 (1546) |
| w064 | all residues | edge max (free) | 0.7508 | 0.7200 (1546) |
| w064 | surface residues | predicted exposure (free) | 0.5809 | 0.5405 (1546) |
| w064 | surface residues | measured free RSA | 0.5815 | 0.5409 (1546) |
| w064 | surface residues | edge max (free) | 0.7201 | 0.7000 (1546) |

## Edges: w064 (surface cross pairs, contact <= 10 A)

| branch | pairs | positive rate | AUROC | AP | macro AP |
|---|---:|---:|---:|---:|---:|
| free | 18956558 | 0.0138 | 0.7458 | 0.0549 | 0.1133 |
| bound | 18956558 | 0.0138 | 0.8935 | 0.1593 | 0.3109 |
