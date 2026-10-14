---
type: concept
aliases:
  - uptake
  - deuterium uptake curve
  - deuterated fraction
  - fractional uptake
  - back-exchange
notation:
  - {symbol: 'D_i(t)', meaning: 'fractional deuterium uptake of residue i at labelling time t', units: null}
  - {symbol: 'D_p(t)', meaning: 'fractional deuterium uptake of peptide p at labelling time t', units: null}
  - {symbol: 'D_\text{corr}', meaning: 'back-exchange corrected fractional deuterium level', units: null}
  - {symbol: 't', meaning: 'labelling time', units: 's'}
sources:
  - "[[@bradshawInterpretationHDXData2020#^c14]]"
  - "[[@bradshawInterpretationHDXData2020#^c15]]"
  - "[[@bradshawInterpretationHDXData2020#^c16]]"
  - "[[@bradshawInterpretationHDXData2020#^c5]]"
  - "[[@massonRecommendationsPerformingInterpreting2019#^c2]]"
  - "[[@massonRecommendationsPerformingInterpreting2019#^c3]]"
  - "[[@vinciauskaiteFundamentalsHDXMS2023#^c5]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c7]]"
  - "[[@vinciauskaiteFundamentalsHDXMS2023#^c4]]"
---

## Definition

Deuterium uptake is the fraction of exchangeable amide hydrogens replaced by deuterium after a labelling time $t$. For one residue under EX2, uptake follows first-order kinetics at the observed rate $k_{\text{int},i}/P_{f,i}$. HDX-MS measures peptides, typically overlapping fragments of 5–30 residues ([[@vinciauskaiteFundamentalsHDXMS2023#^c5]]), so the observable is an average over the peptide's exchangeable residues. Prolines are excluded, and so is the first residue, whose N-terminal hydrogens are lost after digestion. Measured uptake is normalised to non-deuterated and maximally deuterated controls, to correct for the D₂O fraction and for back-exchange during analysis.

## Equations

$$ D_i(t) = 1 - \exp\!\left(-\frac{k_{\text{int},i}}{P_{f,i}}\, t\right) $$
^eq-uptake-residue

Source: first-order kinetics at $k_{\text{obs},i}$ ([[protection factor#^eq-pf]]); [[@bradshawInterpretationHDXData2020#^c14]], p. 7.
Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L48; projects/2-jaxENT/manuscript/report/methods/HDX.tex#L43.

$$ D_p(t) = \frac{1}{|p|} \sum_{i \in p} D_i(t), \qquad p = \{m_p + 1, \dots, n_p\} \setminus \{\text{Pro}\} $$
^eq-uptake-peptide

Source: [[@bradshawInterpretationHDXData2020#^c14]], Eq. (2), p. 7; [[@bradshawInterpretationHDXData2020#^c15]] (first residue omitted).
Manuscript form: projects/2-jaxENT/manuscript/report/methods/HDX.tex#L53 writes the unnormalised sum $D_\text{peptide}(t) = \sum_i [\dots]$ (absolute deuterium). Canonical: the fractional average, which matches Bradshaw and ValDX.

$$ D_\text{corr} = \frac{m - m_{0\%}}{m_{100\%} - m_{0\%}} $$
^eq-uptake-corr

Source: [[@massonRecommendationsPerformingInterpreting2019#^c2]], p. 5. $m$, $m_{0\%}$ and $m_{100\%}$ are the observed, non-deuterated and maximally labelled peptide centroid masses. The back-exchange of a model system has its own equation, [[@massonRecommendationsPerformingInterpreting2019#^c3]].
Manuscript form: jaxENT_paper1/report/methods/HDX.tex#L117 and #L123 ($f_\text{back}$, $D_\text{corrected}$). These lines are commented out in the current projects/2-jaxENT/manuscript/report/methods/HDX.tex#L61. **Needs decision:** whether Chapter 2 presents back-exchange correction as an equation or only in prose.

## Assumptions and limits

- EX2 is assumed for every residue (see [[Linderstrøm–Lang model]]).
- Residues are independent within a peptide.
- Labelling time $t$ measures accumulated exchange, not the duration of a conformational motion. Under EX2 an amide opens many times before it exchanges, and each opening is only a chance to exchange ([[@jamesAdvancesHydrogenDeuterium2022#^c7]], [[@vinciauskaiteFundamentalsHDXMS2023#^c4]]). Slow uptake can therefore mean rarely populated exchange-competent states rather than a slow motion (ours). The data constrain $k_{\text{obs},i}$ most where $k_{\text{obs},i}\, t \sim 1$.
- Averaging over residues is many-to-one: different residue-level patterns give the same peptide curve. This is the resolution limit behind the reweighting ambiguity ([[@bradshawInterpretationHDXData2020#^c5]]).
- Comparing predictions with uptake that is not corrected for back-exchange biases the fitted scale. Scaling to the last measured time point does not correct back-exchange. ValDX's MBP data lack a fully deuterated control and were scaled this way, so their absolute uptake may be underestimated and peptide-specific deuterium loss may distort relative uptake as well (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L39, L58). A global scale term cannot repair a peptide-specific loss.
- The correction itself carries uncertainty. The fully deuterated control is a peptide-level measurement with its own precision, so corrected uptake inherits it ([[experimental uncertainty]]).
- Residue-level references are derived, not measured. ValDX converts BPTI's NMR protection factors into residue uptake curves through the intrinsic rate and the EX2 kinetics of [[#^eq-uptake-residue]] (`6_methods_omc.tex` L47). The reference therefore carries the intrinsic-rate and EX2 assumptions, and peptide-overlap leakage does not arise for it ([[data splitting]]).

## Why it matters here

This is the forward model's last step, from predicted [[protection factor|protection factors]] to the numbers HDX-MS reports. Its averaging is why overlapping peptides leak information between training and validation splits in ValDX.

Claims that use this term: [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]], [[HDX-MS reports deuterium uptake at the peptide level, not the residue level.]], [[Measuring the mass increase of peptides over time lets HDX-MS report on protein dynamics and conformational changes.]], [[Labelling time measures accumulated exchange, not the duration of a conformational motion.]], [[Greater deuterium uptake indicates less protection from exchange, not directly greater flexibility.]].
