---
type: concept
aliases:
  - hydrogen-deuterium exchange mass spectrometry
  - hydrogen/deuterium exchange mass spectrometry
  - HDX
  - HDX/MS
notation: []
sources:
  - "[[@massonRecommendationsPerformingInterpreting2019#^c4]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c3]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c4]]"
  - "[[@massonOverviewHydrogenDeuterium2017#^c5]]"
  - "[[@vinciauskaiteFundamentalsHDXMS2023#^c2]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c2]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c7]]"
  - "[[@vinciauskaiteFundamentalsHDXMS2023#^c4]]"
  - "[[@vinciauskaiteFundamentalsHDXMS2023#^c5]]"
  - "[[@bradshawInterpretationHDXData2020#^c5]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c5]]"
  - "[[@massonOverviewHydrogenDeuterium2017#^c6]]"
  - "[[@massonRecommendationsPerformingInterpreting2019#^c5]]"
  - "[[@englanderHydrogenExchangeModern1997#^c3]]"
  - "[[@bradshawInterpretationHDXData2020#^c8]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c2]]"
  - "[[@narangHDXMSAnalyticalTool2020#^c5]]"
  - "[[@bradshawInterpretationHDXData2020#^c4]]"
---

## Definition

HDX-MS measures the exchange of backbone amide hydrogens with deuterium in the solvent. It reports on protein structure and conformational dynamics in solution, but only indirectly.

**What is recorded.** The protein is diluted into D₂O for a series of labelling times, then quenched and digested. Mass spectrometry measures the mass increase of each peptide, because each deuterium adds about one dalton ([[@massonRecommendationsPerformingInterpreting2019#^c4]], [[@jamesAdvancesHydrogenDeuterium2022#^c3]]). Under EX2 this gives a gradual mass shift over labelling time, the [[deuterium uptake]] curve ([[@jamesAdvancesHydrogenDeuterium2022#^c4]]).

**What sets the rate.** Two things set how fast an amide exchanges:
- **Intrinsic chemistry:** neighbouring residues, pH and temperature, giving the [[intrinsic exchange rate]] ([[@massonOverviewHydrogenDeuterium2017#^c5]]).
- **Local protection:** hydrogen bonding and burial keep an amide closed, and it exchanges only when a transient opening makes it exchange-competent ([[@vinciauskaiteFundamentalsHDXMS2023#^c2]], [[@skinnerProteinHydrogenExchange2012#^c2]]).

Under the usual EX2 regime, an amide opens many times before it exchanges, and each opening is only a chance to exchange ([[@jamesAdvancesHydrogenDeuterium2022#^c7]], [[@vinciauskaiteFundamentalsHDXMS2023#^c4]]). The observed rate is therefore the intrinsic rate divided by the [[protection factor]]. The kinetics are in [[Linderstrøm–Lang model]].

**What is resolved.** Digestion gives overlapping peptides of about 5–30 residues ([[@vinciauskaiteFundamentalsHDXMS2023#^c5]]). Each uptake curve averages over the exchangeable amides in its peptide ([[@bradshawInterpretationHDXData2020#^c5]]; [[deuterium uptake#^eq-uptake-peptide]]). HDX-MS does not give atomic positions ([[@jamesAdvancesHydrogenDeuterium2022#^c5]]).

## Assumptions and limits

- **Averaging is many-to-one.** Different residue-level patterns, and different conformational populations, can give the same peptide curve ([[deuterium uptake]]).
- **Uptake reports protection, not "flexibility" directly.** The molecular reasons an amide exchanges at a given rate are still not settled ([[@massonOverviewHydrogenDeuterium2017#^c6]]). A simple experiment is not simple to interpret ([[@massonRecommendationsPerformingInterpreting2019#^c5]]).
- **Labelling time is accumulated exchange, not the duration of a motion.** Under EX2, slow exchange can mean that exchange-competent states are rarely populated, not that the motion is slow (ours, from the EX2 kinetics above).
- **A change in uptake is a change in protection, not a mechanism.** Even residue-resolved exchange does not directly distinguish between alternative structural interpretations ([[@englanderHydrogenExchangeModern1997#^c3]]). A peptide set may not hold enough information for a clear structural interpretation ([[@bradshawInterpretationHDXData2020#^c8]]).
- **Scope.** HDX-MS suits many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools ([[@jamesAdvancesHydrogenDeuterium2022#^c2]], [[@narangHDXMSAnalyticalTool2020#^c5]]). It still has practical limits, such as resolving every peptide in a large system. Do not write "without size limitations".
- Back-exchange, coverage and EX1 kinetics are Chapter 2 material ([[deuterium uptake#^eq-uptake-corr]], [[Linderstrøm–Lang model#^eq-ex1]]).

## Why it matters here

HDX-MS is the measurement this thesis integrates with ensemble generation, in ValDX and jaxENT. The measurement ends at peptide uptake. Structure enters only through a [[forward model]] that predicts exchange from candidate structures ([[@bradshawInterpretationHDXData2020#^c4]]), so interpreting HDX-MS structurally is an [[inverse problem]]. That boundary is the subject of introduction §1.2.

Claims that use this term: [[HDX-MS measures protein conformational dynamics in solution.]], [[HDX-MS measures the exchange of backbone amide hydrogens with deuterium in the solvent.]], [[Measuring the mass increase of peptides over time lets HDX-MS report on protein dynamics and conformational changes.]], [[Amide exchange rates depend on intrinsic chemistry and on local protection from hydrogen bonding, burial and transient opening.]], [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]], [[HDX-MS reports deuterium uptake at the peptide level, not the residue level.]], [[HDX-MS data alone do not give the atomic positions that NMR, crystallography and cryo-EM provide.]], [[Labelling time measures accumulated exchange, not the duration of a conformational motion.]], [[Greater deuterium uptake indicates less protection from exchange, not directly greater flexibility.]], [[A change in HDX-MS uptake shows a change in protection but does not on its own identify the structural mechanism.]], [[Interpreting dynamics measurements in structural terms is a grand challenge, as they can be indirect or ensemble-averaged.]], [[HDX-MS can study many systems that are too large, flexible, heterogeneous or sample-limited for other structural tools.]], [[The primary benefits of HDX-MS are sensitivity, flexibility and low sample needs compared with other biophysical techniques.]], [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]], [[Connecting uptake to a structural explanation requires a forward model that predicts exchange from candidate structures or ensembles.]], [[To address this ambiguity, researchers increasingly turn to molecular simulations for structural hypotheses.]], [[To quantitatively connect measurements of dynamics to biological mechanisms, they must be interpreted in structural terms.]].
