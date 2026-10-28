---
type: concept
aliases:
  - M8
  - Mohammadiarani SASA-distance model
notation:
  - {symbol: '\mathrm{SASA}_i', meaning: 'solvent-accessible surface area of the amide hydrogen of residue i', units: 'Å^2'}
  - {symbol: 'd_{\mathrm{pol},i}', meaning: 'distance from amide hydrogen i to the nearest eligible protein polar atom', units: 'Å'}
  - {symbol: '\beta_s', meaning: 'M8 coefficient for the SASA term', units: 'Å^(2 gamma_s)'}
  - {symbol: '\beta_p', meaning: 'M8 coefficient for the polar-atom distance term', units: 'Å^(gamma_p)'}
  - {symbol: '\gamma_s', meaning: 'M8 exponent for the SASA term', units: null}
  - {symbol: '\gamma_p', meaning: 'M8 exponent for the polar-atom distance term', units: null}
sources:
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c4]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c7]]"
---

## Definition

The Mohammadiarani SASA–distance model predicts residue [[protection factor|protection factors]] from the solvent-accessible surface area of the amide hydrogen and its distance to the nearest eligible protein polar atom. It is the empirical model M8 in Mohammadiarani et al. (2018). Two power-law terms map these features to log protection, with four fitted parameters. The polar-atom distance excludes neighbouring residues, so solvent exposure can be considered alongside protection by protein polar atoms ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c4]]; [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Model definitions in supporting information]], pp. S9–S10).

## Equations

$$ \ln P_{f,i} = \beta_s\,\mathrm{SASA}_i^{-\gamma_s} + \beta_p\,d_{\mathrm{pol},i}^{-\gamma_p} $$
^eq-sasa-distance-pf

Source: [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c7]], Table 1, p. 21; supporting information Table S2, p. S10. The feature definitions are described in [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c4]], p. 5, and supporting information pp. S9–S10. Notation: [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Notation]]; the source's distance $D_i$ is written as $d_{\mathrm{pol},i}$ to distinguish it from [[deuterium uptake]].

## Assumptions and limits

- SASA refers to the amide hydrogen, not the whole residue. The distance refers to the nearest eligible protein polar atom, not the nearest water oxygen. These feature definitions and their units are part of the calibrated model.
- The coefficients and exponents were fitted against peptide-level uptake across RGS4, RGS8 and RGS19, separately for each force field ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Model definitions in supporting information]], pp. S8–S10; parameter values in Table S3, p. S13). They are empirical parameters whose transfer to other systems requires assessment.
- The formula predicts log protection directly. It does not classify frames as open or closed or calculate opening populations. The same paper's M9 uses the same features with thresholds to define open states; M9 is a separate model.
- The displayed feature-to-protection relationship does not prescribe an ensemble-averaging rule. Applying it to averaged features, averaging predicted log protection and averaging uptake are different operations ([[forward model]]).

## Why it matters here

M8 gives Chapter 2 an empirical alternative to the contact and hydrogen-bond counts in the [[Best–Vendruscolo model]]. Comparing it with the [[Persson–Halle population model]] separates two choices in an HDX forward model, which structural features represent protection and how those features are converted into an exchange prediction.
