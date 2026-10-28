---
type: concept
aliases:
  - protection-factor model
  - protection-factor models
  - protection-factor predictor
  - HDX forward model
  - structure-based protection-factor model
  - switch-function BV
notation: []
sources:
  - "[[@bestStructuralInterpretationHydrogen2006#^c2]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c3]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c4]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c5]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c2]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c3]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c4]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c7]]"
  - "[[@wanReconcilingSimulatedEnsembles2020#^c2]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c1]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c7]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c8]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c9]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c10]]"
  - "[[@bradshawInterpretationHDXData2020#^c13]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c7]]"
---

## Definition

An HDX protection-factor model is the [[forward model]] for HDX: it predicts each residue's [[protection factor]] from structure. Uptake then follows from the protection factors ([[deuterium uptake]]). Models differ in what structural features they count and how.
- **Phenomenological counting.** The [[Best–Vendruscolo model]] approximates local exchange ([[@bestStructuralInterpretationHydrogen2006#^c2]]). Protection comes from burial and hydrogen bonding ([[@bestStructuralInterpretationHydrogen2006#^c3]]), so ln P is a weighted sum of heavy-atom contacts and amide hydrogen bonds ([[@bestStructuralInterpretationHydrogen2006#^c4]]), averaged over the ensemble ([[@bestStructuralInterpretationHydrogen2006#^c5]]). A switch-function variant replaces the hard contact cutoff with a smooth one (Radou et al. 2014; not yet in the KB).
- **Exchange events in MD.** Atomistic simulation can resolve protection residue by residue ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c2]]). Park et al. 2015 estimate protection from hydrogen-bond analysis of MD (PDF unreadable, so not yet in the KB).
- **Opening populations.** The [[Persson–Halle population model]] (M7) classifies amides as open or closed using nearby waters and protein polar atoms, then estimates protection from their relative populations ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c3]]). Its opening criterion and sampling of rare events determine the prediction.
- **Empirical SASA and distance.** The [[Mohammadiarani SASA–distance model]] (M8) predicts log protection from amide-hydrogen solvent exposure and distance to the nearest eligible protein polar atom ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c4]]). Its four fitted parameters map these features to protection directly. The paper's M9 instead uses the same features to define open states ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c7]]).
- **Inside an inference.** Wan et al. use a protection-factor predictor within BICePs to choose between ensembles and estimate state populations ([[@wanReconcilingSimulatedEnsembles2020#^c2]]).

The data-side alternative is to estimate protection factors from uptake without a structure. Peptide uptake is fixed by the amide rates, but the rates generally cannot be recovered from it ([[@skinnerEstimatingConstraintsProtection2019#^c1]]). Fitting each peptide alone leaves residue protection factors severely underdetermined ([[@skinnerEstimatingConstraintsProtection2019#^c7]]). Where they can be estimated, they can be converted into structural information ([[@skinnerEstimatingConstraintsProtection2019#^c9]]), and they test structural models more stringently than uptake alone ([[@skinnerEstimatingConstraintsProtection2019#^c10]]). Skinner's method is a random search and least-squares fit, not Bayesian inference.

## Assumptions and limits

- **Exchange regime and calibration.** Under EX2, protection relates to the opening equilibrium and its free energy ([[Linderstrøm–Lang model]]). The models predict exchange residue by residue. Empirical coefficients require calibration to the protein and conditions. Optimal BV values depend on both ([[@bradshawInterpretationHDXData2020#^c13]]), and they mainly compensate for differences from the calibration conditions ([[@siddiquiFrameworkTestingStructural2026#^c7]]). Fitted coefficients can therefore absorb error ([[model misspecification]]). M7 instead requires a structural opening criterion and sufficient sampling of that state.
- **One protection factor per residue fails for mixtures.** The assumption of a single value per residue is false when several conformers are populated ([[@skinnerEstimatingConstraintsProtection2019#^c8]]). Ensemble models avoid this by averaging over conformers.
- **Differentiability.** A hard cutoff gives a piecewise-constant count with no useful gradient. A smooth (switch-function) count is needed for [[restrained simulation]] or [[guided diffusion]] (ours).
- **Model mismatch is a test design.** ValDX generated synthetic protection factors with the switch-function variant but fitted with the hard-cutoff BV model, a deliberate forward-model mismatch (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L624). The manuscript cites Skinner 2019 for the switch function. Skinner 2019 describes no such model; it cites Radou et al. 2014 (its ref. 42), which should be cited instead.

## Why it matters here

Chapter 2, "Structural Forward Models for HDX", which introduces BV "and alternatives, with their assumptions and limits". Every method in the thesis passes through this model, so its assumptions bound what any fit can show.

Claims that use this term: [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]], [[Residue protection factors are generally underdetermined by peptide-level uptake.]], [[A single protection factor per residue cannot describe a residue whose environment differs between populated conformers.]], [[Residue protection factors test structural models more stringently than peptide uptake alone.]].

## Wording history

Historical formulation from this note before M7 and M8 were added (also condensed in [[02-background]]): "Shared assumptions. EX2 exchange, so that ln P is a free energy. Residues treated independently. Coefficients calibrated to the protein and conditions" (links and subsequent BV-specific explanation omitted here). Calibration applies to empirical predictors such as BV and M8; M7 estimates an opening population from a structural criterion. The revised wording separates those requirements as the model comparison expands.
