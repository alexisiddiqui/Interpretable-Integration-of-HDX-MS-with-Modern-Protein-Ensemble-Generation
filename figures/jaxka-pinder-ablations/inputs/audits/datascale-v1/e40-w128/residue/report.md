# negatives-v1: same-class negatives (within-complex listwise, same-stratum swaps) vs run 4 and decoy both (w64), allres 15 A, 50%, seed 17

Selection = PINDER val state MAE + interface paired MAE (all sites / without bonded-Cys sites). Residue metrics on every PINDER validation residue with an RSA (residue-rsa-v1).

| arm | epoch | selection | no bonded Cys | state | interface | pKPDB | benchmark |
|---|---:|---:|---:|---:|---:|---:|---:|
| e40-w128 | 34 | 0.6128 | 0.5931 | 0.3877 | 0.2251 | 0.4582 | 0.4800 |

## Paired (binding-shift) MAE without bonded-Cys sites, by the store's partner distance (A)

| arm | all sites | <=4 | 4-6 | 6-10 | >10 |
|---|---:|---:|---:|---:|---:|
| e40-w128 | 0.0637 | 0.4462 | 0.2035 | 0.0946 | 0.0089 |

## Burial on interface residues (37732 within 5 A of the partner): free branch vs RSA_free, bound branch vs RSA_bound, change vs dRSA

| arm | free AUROC RSA<0.25 | free Spearman | bound AUROC RSA<0.25 | bound Spearman | change: Spearman(dP, dRSA) | change: AUROC dRSA>0.05 | change: MAE(dP, dRSA) |
|---|---:|---:|---:|---:|---:|---:|---:|
| e40-w128 | 0.9760 | 0.9392 | 0.9685 | 0.9283 | 0.8802 | 0.9209 | 0.0521 |

## Interface from the free state (residue within 5 A of the partner)

| arm | residues | score | pooled AUROC | per-chain median AUROC (chains) |
|---|---|---|---:|---:|
| e40-w128 | all residues | predicted exposure (free) | 0.6684 | 0.6218 (1546) |
| e40-w128 | all residues | measured free RSA | 0.6676 | 0.6218 (1546) |
| e40-w128 | all residues | edge max (free) | 0.7494 | 0.7272 (1546) |
| e40-w128 | surface residues | predicted exposure (free) | 0.5836 | 0.5450 (1546) |
| e40-w128 | surface residues | measured free RSA | 0.5815 | 0.5409 (1546) |
| e40-w128 | surface residues | edge max (free) | 0.7176 | 0.6961 (1546) |

## Edges: e40-w128 (surface cross pairs, contact <= 10 A)

| branch | pairs | positive rate | AUROC | AP | macro AP |
|---|---:|---:|---:|---:|---:|
| free | 18956558 | 0.0138 | 0.7564 | 0.0598 | 0.1325 |
| bound | 18956558 | 0.0138 | 0.9133 | 0.1562 | 0.3666 |
