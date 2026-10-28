---
type: paper
citekey: mohammadiaraniInterpretingHydrogenDeuteriumExchange2018
year: 2018
read: false
pdf: kb/_pdf/@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018.pdf
extraction: auto
needs_review: false
review_reason:
---

# Interpreting Hydrogen-Deuterium Exchange Events in Proteins Using Atomistic Simulations: Case Studies on Regulators of G-protein Signaling Proteins (2018)

## Main point

The study compares seven existing protection-factor models against HDX-MS data for RGS4, RGS8 and RGS19 using two force fields, and introduces an empirical SASA–distance model (M8) and a population-based model using the same features (M9). M7 is the earlier Persson–Halle population model. M7 and M8 provide the population-based and empirical alternatives developed in the Chapter 2 model comparison.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- HDX-MS results only provide fragment-level resolution. ^c1
  - page: 8
  - quote: "since HDX-MS results only provide fragment-level resolution"
  - quote_check: pass
  - reviewed: false
- Atomistic MD simulations complement fragment-resolution HDX-MS data by giving single-residue detail on amide-hydrogen protection. ^c2
  - page: 7
  - quote: "atomistic MD simulations complement these data by providing additional details on the protections of amide hydrogens at a single-residue resolution"
  - quote_check: pass
  - reviewed: false
- M7 estimates protection from the closed-to-open population ratio of each amide. ^c3
  - page: 3
  - quote: "the PF is defined as a fractional population of the closed state to the open state for each amide-hydrogen"
  - quote_check: pass
  - reviewed: false
- M8 and M9 use amide-hydrogen SASA and distance to the nearest protein polar atom as structural features. ^c4
  - page: 5
  - quote: "based on the SASA of each amide hydrogen and its distance from the first polar atom"
  - quote_check: pass
  - reviewed: false
- Fractional-population models classify amides as open or closed in individual MD frames before calculating protection. ^c5
  - page: 8
  - quote: "Two specific criteria (see Table S3) were evaluated to classify amides as being in the open or closed states for each frame"
  - quote_check: pass
  - reviewed: false
- Observing openings of highly protected amides can require millisecond or longer trajectories. ^c6
  - page: 9
  - quote: "would require trajectories on time-scales of millisecond or higher for observing open states"
  - quote_check: pass
  - reviewed: false
- Table 1 distinguishes the empirical M8 model from the fractional-population M9 model and gives their equations. ^c7
  - page: 21
  - quote: "M8 is an empirical model and M9 is a fractional population model"
  - quote_check: pass
  - reviewed: false

## Model definitions in supporting information

The [supporting information](../_pdf/@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018-SI.pdf) is available from [ACS Figshare](https://doi.org/10.1021/acs.jpcb.8b07494.s001). Its printed S-page numbers match the PDF page indices.

- **M7, p. S7.** Open amides have at least two water oxygens within 2.6 Å of the amide hydrogen and no protein polar atom within 2.6 Å, with neighbouring-residue exclusions. The review attributes this definition to Persson and Halle, *How amide hydrogens exchange in native proteins* (2015), main-text ref. 30 / SI ref. 9, DOI [10.1073/pnas.1506079112](https://doi.org/10.1073/pnas.1506079112).
- **M7 normalisation, p. S7.** The source calls the closed-to-open population ratio PF and writes the EX2 exchange rate with a denominator of PF plus one. The KB's rate-based protection factor is therefore one plus this population ratio. For predominantly closed amides the distinction is negligible; [[Persson–Halle population model]] retains it explicitly.
- **M8, pp. S9–S10 and Table S2.** The empirical model predicts log protection as the sum of inverse-power SASA and polar-atom distance terms. The distance excludes neighbouring residues. Four parameters are fitted by minimising the peptide-uptake objective, separately for each force field (protocol, pp. S8–S9; values, Table S3, p. S13).
- **M9, p. S10.** The same SASA and distance features classify frames using fitted thresholds, after which protection is estimated from the closed/open ratio. It is not the empirical model M8.

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $\mathrm{PF}_i$ (M8) | Intrinsic-to-observed exchange-rate ratio | $P_{f,i}$ | Same rate-based definition as the KB. |
| $\mathrm{PF}_i$ (M7) | Closed-to-open population ratio | $\kappa_i$ | Canonical rate-based protection is one plus this ratio under EX2. |
| $\tau_C$, $\tau_O$ | Mean residence times in closed and open states | — | Written $\tau_{C,i}$ and $\tau_{O,i}$ for residue-specific quantities. |
| $\mathrm{SASA}_i$ | Solvent-accessible surface area of the amide hydrogen | $\mathrm{SASA}_i$ | Not the SASA of the whole residue. |
| $D_i$ (M8) | Distance to the nearest eligible protein polar atom | $d_{\mathrm{pol},i}$ | Renamed to distinguish it from fractional deuterium uptake. |
| $\beta_s$ | Coefficient for the M8 SASA term | $\beta_s$ | Units depend on the SASA exponent. |
| $\beta_p$ | Coefficient for the M8 polar-atom distance term | $\beta_p$ | Units depend on the distance exponent. |
| $\gamma_s$ | Exponent for the M8 SASA term | $\gamma_s$ | Dimensionless. |
| $\gamma_p$ | Exponent for the M8 polar-atom distance term | $\gamma_p$ | Dimensionless. |

## What I use from it

The [[Persson–Halle population model]] and [[Mohammadiarani SASA–distance model]] distinguish sampled opening populations from empirical structural predictors in [[HDX protection-factor model]] and [[02-background]].

## Disagreements / limitations
