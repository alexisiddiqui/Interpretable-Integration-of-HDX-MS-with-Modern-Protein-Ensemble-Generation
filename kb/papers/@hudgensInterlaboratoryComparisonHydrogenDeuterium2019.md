---
type: paper
citekey: hudgensInterlaboratoryComparisonHydrogenDeuterium2019
year: 2019
read: false
pdf: kb/_pdf/@hudgensInterlaboratoryComparisonHydrogenDeuterium2019.pdf
extraction: auto
needs_review: false
review_reason:
---

# Interlaboratory Comparison of Hydrogen-Deuterium Exchange Mass Spectrometry Measurements of the Fab Fragment of NISTmAb (2019)

## Main point

A NIST-led comparison in which fifteen laboratories measured bottom-up HDX-MS on the same antibody Fab fragment under a shared protocol. The paper separates precision into repeatability, intermediate measurement precision and reproducibility. Most laboratories repeated centroid masses to within 0.15 Da. For back-exchange corrected uptake, the reproducibility across the fifteen laboratories was (9.0 ± 0.9) % of uptake, and (6.5 ± 0.6) % within the cohort that labelled at 25 °C (pp. 3, 10). The paper offers the Fab as a reference material for checking system fitness.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Precision has three components: repeatability, intermediate measurement precision and reproducibility. ^c1
  - page: 4
  - quote: "Precision is characterized by the components of repeatability, intermediate measurement precision"
  - quote_check: pass
  - reviewed: false
- Reproducibility allows instruments, reagents, locations and operators to vary, whereas repeatability holds them fixed. ^c2
  - page: 4
  - quote: "Determinations of reproducibility allow for variations of instruments, reagents, locations, and operators"
  - quote_check: pass
  - reviewed: false
- The reproducibility of bottom-up HDX-MS was determined from 244 peptide sequences shared across laboratories; the value is (9.0 ± 0.9) % of corrected uptake (p. 10). ^c3
  - page: 10
  - quote: "measurements on 244 shared sequences determined that the reproducibility of HDX-MS"
  - quote_check: pass
  - reviewed: false
- Reproducibility is computed as the sample standard deviation of corrected peptide uptake across laboratories measuring at the same temperature. ^c4
  - page: 9
  - quote: "Reproducibility of HDX-MS is derived using sample standard deviations"
  - quote_check: pass
  - reviewed: false
- The reproducibility figures refer to uptake corrected for the D2O fraction and for back-exchange. ^c5
  - page: 10
  - quote: "This analysis used the correction for D2O fraction and for back-exchange"
  - quote_check: pass
  - reviewed: false

## What I use from it

- The precision vocabulary for [[experimental uncertainty]] (^c1, ^c2): repeatability within a laboratory is not reproducibility across laboratories, and neither bounds systematic bias.
- The 9.0 % reproducibility as the scale of experimental variability against which ValDX reads its weaker between-ensemble differences (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L606) and its 5 % RSD time-point filter (L61). Both refer to corrected uptake (^c5).
- The distinction between measurement replication and split replication in [[replicate uncertainty]].

## Disagreements / limitations

- One protein, one shared protocol. The numbers describe a reference measurement under controlled conditions, not the spread of published datasets.
- Precision is reported for centroid masses and peptide uptake, not for any quantity inferred from them. Propagation to protection factors or populations is not addressed.
- Systematic error is treated only through the back-exchange and D2O-fraction corrections (^c5). The paper does not estimate bias that survives those corrections.
