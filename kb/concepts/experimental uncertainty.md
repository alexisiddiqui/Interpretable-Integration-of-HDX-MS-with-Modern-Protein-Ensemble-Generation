---
type: concept
aliases:
  - measurement uncertainty
  - measurement error
  - measurement precision
  - repeatability
  - reproducibility
  - intermediate precision
  - systematic error
  - random error
  - error bars
  - uncertainty taxonomy
notation: []
sources:
  - "[[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c1]]"
  - "[[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c2]]"
  - "[[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c3]]"
  - "[[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c4]]"
  - "[[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c5]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c2]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c3]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c4]]"
  - "[[@massonRecommendationsPerformingInterpreting2019#^c2]]"
---

## Definition

Experimental uncertainty is the spread of a measurement about the value it would take if the experiment were repeated without error. Metrology separates precision into repeatability, intermediate precision and reproducibility, according to what is allowed to vary between repeats ([[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c1]]). Repeatability holds instrument, operator and reagents fixed. Reproducibility lets them vary ([[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c2]]). Repetition narrows random error and leaves systematic bias where it is, so an error estimate taken from repeats is usually a lower bound on the real uncertainty ([[@bonomiPrinciplesProteinStructural2017#^c2]]).

For bottom-up HDX-MS the reference numbers come from the NIST interlaboratory study. Reproducibility of back-exchange corrected uptake across fifteen laboratories was (9.0 ± 0.9) % of uptake, and (6.5 ± 0.6) % within the cohort labelling at 25 °C, computed as the sample standard deviation across laboratories for the same peptide and temperature ([[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c3]], [[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c4]], [[@hudgensInterlaboratoryComparisonHydrogenDeuterium2019#^c5]]).

## The sources of uncertainty in an integrated model

Several quantities are called uncertainty in an ensemble fit, and they answer different questions. The table keeps them apart. Each row names what moves the quantity, what reduces it, what does not, and the note that owns it.

| Source | What it moves | Reduced by | Not reduced by | Owner |
|---|---|---|---|---|
| Repeatability of the measurement | Uptake values between technical replicates | More replicates, the RSD filter | Anything done to the model | this note |
| Systematic experimental bias | The scale and shape of uptake, through back-exchange, D₂O fraction and normalisation ([[deuterium uptake#^eq-uptake-corr]]) | A fully deuterated control ([[@massonRecommendationsPerformingInterpreting2019#^c2]]) | Replicates; scaling to the last time point | [[deuterium uptake]] |
| Forward-model discrepancy | Predicted uptake for a given structure ([[@bonomiPrinciplesProteinStructural2017#^c3]]) | Recalibration, when the form is adequate | Better data of the same kind | [[model misspecification]] |
| Finite conformational sampling | Which states the candidate ensemble can represent | More or different sampling | Reweighting | [[sampling coverage]] |
| Posterior uncertainty | What the data leave undetermined under one model | More informative data | Repeating the same fit | [[posterior uncertainty]] |
| Partition sensitivity | Fitted weights and parameters between data splits | Averaging fits, larger training sets | Measurement replicates | [[replicate uncertainty]] |

Metainference folds the first three rows and the finite number of replicas into one effective uncertainty per datum ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c4]]). That makes the restraint honest about the total, and it also means the inferred value does not say which row is responsible ([[metainference]], [[nuisance parameter]]).

## In integrative practice

- Most reweighting fixes the error scale by hand. HDXer and ValDX use a fixed uptake uncertainty of one in the error term (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L458), which makes the fit a fixed-error maximum a posteriori estimate ([[nuisance parameter#^eq-data-weight]]).
- Metainference and [[BICePs]] infer the error scale with the structures ([[@bonomiMetadynamicMetainferenceEnhanced2016#^c4]]).
- Measured replicate standard deviations rarely enter the loss. When they do, they enter as weights, not as a calibrated likelihood.

## Why it matters here

- ValDX uses the measurement precision twice and keeps it apart from split sensitivity. Time points with replicate RSD above 5 % are removed before fitting (L61), and between-ensemble differences weaker than the 9 % reproducibility are marked for context rather than discarded (L606). The split replicates measure sensitivity to peptide partitioning, which is a different quantity ([[replicate uncertainty]]).
- jaxENT's current MoPrP policy uses the measured dispersion only in selection, as a weight proportional to one over the standard deviation ([[Observation weighting and selection (jaxENT)]]).
- Chapter 2 §2.4 opens on this table. The question the subsection has to answer is which row a given diagnostic can move, and which rows it leaves where they were.

Claims that use this term: [[Replicate precision bounds only the random part of measurement error, so a precision threshold does not bound systematic bias.]], [[HDX-MS precision differs between repeat measurements in one laboratory and measurements across laboratories.]], [[Metainference folds experimental, systematic, forward-model and finite-replica errors into one effective uncertainty per datum, so the inferred value does not say which source dominates.]], [[Experimental error estimates are usually lower bounds because they miss systematic errors.]].
