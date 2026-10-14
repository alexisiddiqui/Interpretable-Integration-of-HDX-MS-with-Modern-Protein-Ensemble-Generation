---
type: concept
aliases:
  - non-identifiability
  - non-identifiable
  - structural identifiability
  - practical identifiability
  - distinguishability
  - competing structural hypotheses
notation: []
sources:
  - "[[@berlinRecoveringRepresentativeConformational2013#^c1]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c8]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c1]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c2]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c4]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c1]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c2]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c3]]"
  - "[[@skinnerEstimatingConstraintsProtection2019#^c7]]"
  - "[[@bradshawInterpretationHDXData2020#^c8]]"
---

## Definition

A quantity is identifiable when the data, read through the [[forward model]], fix its value. In HDX-MS integration the unknowns are the conformational populations and the forward-model parameters, and the [[inverse problem]] asks which of them the uptake actually determines.

Two kinds of failure need to be kept apart, because they call for different responses (the labels are ours).
- **Structural non-identifiability** holds even with ideal data. Ensembles have far more degrees of freedom than independent observables ([[@berlinRecoveringRepresentativeConformational2013#^c1]]), so different ensembles can fit the same averaged data ([[@bonomiPrinciplesProteinStructural2017#^c8]]). The revised ValDX manuscript states that this persists with a perfect forward model (`projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L17; manuscript pointer). More or better data of the same kind cannot remove it.
- **Practical ambiguity** comes from finite coverage, measurement noise and model discrepancy. A peptide set may not hold enough information for a clear structural interpretation ([[@bradshawInterpretationHDXData2020#^c8]]). This kind can shrink with better coverage, more time points or a better forward model.

HDX-MS adds a second level. Peptide uptake is fixed by the exchange rates of its amides, but the rates generally cannot be recovered from the uptake ([[@skinnerEstimatingConstraintsProtection2019#^c1]]). How degenerate that step is depends on the number, overlap and length of peptides ([[@skinnerEstimatingConstraintsProtection2019#^c2]]); for a long peptide with few time points, infinitely many protection-factor sets fit ([[@skinnerEstimatingConstraintsProtection2019#^c3]], [[@skinnerEstimatingConstraintsProtection2019#^c7]]). Uptake to residue protection and residue protection to populations are therefore two separate inference problems, and either can be the one that fails.

## Assumptions and limits

- **Distinguishability (ours).** Two structural hypotheses can be told apart only where they predict observables that differ by more than measurement and forward-model error. A structural difference that changes no predicted uptake is invisible to the fit, however large it is. An orthogonal measurement helps when it constrains exactly the distinctions that uptake leaves open.
- **Good agreement does not identify the ensemble.** One uptake curve has many possible structural explanations ([[@siddiquiFrameworkTestingStructural2026#^c1]]). In TeaA, ensembles with similar training error recovered different populations ([[@siddiquiFrameworkTestingStructural2026#^c2]]), and plausible intermediates absent from the target prevented recovery even when uptake matched ([[@siddiquiFrameworkTestingStructural2026#^c4]]).
- **Validation answers narrower questions.** Held-out error tests prediction ([[data splitting]]). Replicate spread tests sensitivity to the data used ([[replicate uncertainty]]). Changing one suspected cause tests attribution ([[controlled perturbation]]). None of them shows that the populations are unique.
- **References differ in what they can establish.** jaxENT orders its systems by decreasing ground-truth availability (`projects/2-jaxENT/manuscript/report/results.tex` L29; manuscript pointer).
  - A synthetic benchmark has exact populations by construction (TeaA).
  - An experimentally derived reference depends on its own state assignments and thermodynamic assumptions. The MoPrP target is HDX-NMR-derived and Boltzmann-weighted (`results.tex` L97), so "recovery" there is agreement with another model, not with exact truth ([[prion protein]]).
  - With no structural reference, only prediction and stability can be assessed ([[alpha-synuclein]]).
- **Weights and parameters trade off.** Fitting frame weights and forward-model parameters together is itself an identifiability question ([[model misspecification]], [[nuisance parameter]]).
- **Bayesian model comparison ranks, it does not identify.** An evidence score orders candidate priors given the data and error model ([[Bayes' theorem#^eq-bayes-factor]], [[BICePs]]). It cannot create a distinction the observables do not carry.

## Why it matters here

Chapter 2, "Identifiability and Competing Structural Hypotheses", and research question Q1 (§1.6). Because the ensemble is not identifiable from uptake, the thesis asks which candidate hypotheses the data support relative to one another and where that support is unstable. ValDX makes this a question of predictive accuracy plus modification from the prior ([[Work Done]]); jaxENT adds uncertainty and references of decreasing certainty.

Claims that use this term: [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]], [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]], [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]], [[Two structural hypotheses can be distinguished only where their predicted observables differ by more than measurement and model error.]].
