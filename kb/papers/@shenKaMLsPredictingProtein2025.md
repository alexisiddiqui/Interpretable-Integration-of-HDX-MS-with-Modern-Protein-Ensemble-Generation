---
type: paper
citekey: shenKaMLsPredictingProtein2025
year: 2025
read: false
pdf: kb/_pdf/@shenKaMLsPredictingProtein2025.pdf
extraction: auto
needs_review: false
review_reason:
---

# KaMLs for Predicting Protein pKa Values and Ionization States: Are Trees All You Need? (2025)

## Main point

KaML models, a CatBoost decision tree (KaML-CBtree) and a graph attention network (KaML-GAT), are trained on PKAD-3, an expanded experimental pKa database of 1167 pKa values in 247 proteins. Both outperform PROPKA3, and the lightweight tree model gives the more accurate pKa values and protonation states across all six titratable amino acids.

## Claims

- The KaML models are a CatBoost decision tree (CBtree) and what the authors describe as the first graph attention network (GAT) for protein pKa prediction. ^c1
  - page: 3
  - quote: "using the CatBoost decision tree (CBtree) model and to our best knowledge the first graph attention network (GAT)"
  - quote_check: pass
  - reviewed: false
- The new experimental database PKAD-3 contains 1167 pKa values of 992 unique residues in 247 wild-type or mutant proteins, increases of 53, 61 and 119% over the cleaned PKAD-2 (763 pKa values, 615 residues, 113 proteins). ^c2
  - page: 3
  - quote: "992 unique residues in 247 proteins (WT or mutant), representing increases of 53, 61, and 119%"
  - quote_check: pass
  - reviewed: false
- Both KaML-CBtree and KaML-GAT outperform PROPKA3, but the CBtree gives the more accurate pKa and protonation-state predictions for all six titratable amino acids. ^c3
  - page: 10
  - quote: "While both KaML-CBtree and KaML-GAT outperform PROPKA3, KaML-CBtree offers more accurate pKa and protonation state predictions for all six titratable amino acids."
  - quote_check: pass
  - reviewed: false
- Predicted pKa values are discretised at pH 7 into protonated (pKa < 6.52), deprotonated (pKa > 7.48) and titrating classes, which turns the regression into a classification scored by precision and recall; the titrating class is left out of the analysis. ^c4
  - page: 4
  - quote: "This discretization step effectively transforms the regression problem into a classification task"
  - quote_check: pass
  - reviewed: false
- On the held-out tests the CBtree gives RMSEs of 0.76 (acid) and 0.79 (base), against 1.28 and 0.95 for PROPKA3. ^c5
  - page: 6
  - quote: "compared to PROPKA3 PCCs of 0.74/0.90, RMSEs of 1.28/0.95"
  - quote_check: pass
  - reviewed: false
- The CBtree also outperforms PypKa, pKAI, pKAI+ and DeepKa on their reported overall metrics, although the authors note that the comparison uses different test sets. ^c6
  - page: 9
  - quote: "However, this comparison is not optimal due to the different test sets used."
  - quote_check: pass
  - reviewed: false
- Part of the gain is attributed to separate acid and base models, data augmentation with AlphaFold structures and pretraining on a theoretical pKa database. ^c7
  - page: 1
  - quote: "including the separate treatment of acid and base, data augmentation using AlphaFold structures, and model pretraining on a theoretical pKa database"
  - quote_check: pass
  - reviewed: false

## What I use from it

KaML-CBtree as the current experimentally trained, structure-based pKa predictor, PKAD-3 as its training set, and the pH-7 protonation-state classification as an evaluation that matters more than pKa RMSE when the aim is assigning charge states.

## Disagreements / limitations

The models see a single structure and do not capture conformational change. Cys and Tyr test sets are very small, and the titrating class near pH 7 is excluded from the classification metrics.
