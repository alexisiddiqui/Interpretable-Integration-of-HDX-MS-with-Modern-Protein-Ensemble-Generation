---
type: concept
aliases:
  - protection factors
  - PF
  - P_f
  - free energy of opening
notation:
  - {symbol: 'P_{f,i}', meaning: 'protection factor of residue i', units: null}
  - {symbol: '\Delta G_\text{op}', meaning: 'free energy of the opening reaction', units: 'kJ mol^-1'}
sources:
  - "[[@skinnerProteinHydrogenExchange2012#^c4]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c6]]"
  - "[[@baiPrimaryStructureEffects1993#^c1]]"
  - "[[@bestStructuralInterpretationHydrogen2006#^c1]]"
---

## Definition

A protection factor is the ratio of the [[intrinsic exchange rate]] of an amide to its observed exchange rate in the protein. It measures how much structure slows exchange: unprotected amides have $P_f = 1$, and buried, hydrogen-bonded amides have $P_f \gg 1$. Under EX2 ([[Linderstrøm–Lang model]]), $P_f$ is the inverse of the opening equilibrium constant, so $RT \ln P_f$ is the free energy of the opening reaction. This is why protection factors are a source of structural and thermodynamic information.

## Equations

$$ P_{f,i} = \frac{k_{\text{int},i}}{k_{\text{obs},i}} $$
^eq-pf

Source: [[@skinnerProteinHydrogenExchange2012#^c4]], Eq. (3), p. 8; [[@baiPrimaryStructureEffects1993#^c1]], p. 1 (as $P = k_\text{rc}/k_\text{prot}$).
Manuscript form: projects/1-ValDX/manuscript/report/2_hdx_theory_omc.tex#L5; jaxENT_paper1/report/methods/HDX.tex#L37 (writes $P_f$); projects/2-jaxENT/manuscript/report/methods/HDX.tex#L19 (writes $\text{PF}_i$).

$$ \text{EX2:}\quad P_{f,i} = \frac{1}{K_\text{op}} \qquad \Delta G_\text{op} = -RT \ln K_\text{op} = RT \ln P_{f,i} $$
^eq-dgop

Source: [[@skinnerProteinHydrogenExchange2012#^c4]] ($P_f = (K_\text{op}+1)/K_\text{op}$, Eq. 3, p. 8, which reduces to $1/K_\text{op}$ when $K_\text{op} \ll 1$); [[@skinnerProteinHydrogenExchange2012#^c6]] ($\Delta G_\text{op}$, p. 3).
Manuscript form: 2_hdx_theory_omc.tex#L11 (writes $\Delta G_\text{open} \approx RT\ln P_f$, with 5.7 kJ mol⁻¹ per tenfold at 300 K); jaxENT_paper1/report/methods/HDX.tex#L37 (writes $k_BT\log P_f$, per molecule). Canonical: $RT \ln$, per mole ([[2026-10-13 canonical HDX and ensemble notation]]).

## Derivation

1. In EX2, $k_{\text{obs},i} = K_\text{op} k_{\text{int},i}$ ([[Linderstrøm–Lang model#^eq-ex2]]).
2. Substituting into the definition gives $P_{f,i} = 1/K_\text{op}$ (step ours). Skinner's exact form, $(K_\text{op}+1)/K_\text{op}$, keeps the closed-plus-open normalisation.
3. $\Delta G_\text{op} = -RT \ln K_\text{op} = RT \ln P_{f,i}$ (Skinner p. 3, [[@skinnerProteinHydrogenExchange2012#^c6]]).

## Assumptions and limits

- The free-energy reading holds only in EX2, and only for the opening that limits exchange of that amide. It is not a barrier height.
- Protection factors are residue-level, but HDX-MS measures peptides. Going back from peptide uptake to residue $P_f$ is underdetermined (see [[deuterium uptake]]).

## Why it matters here

$P_f$ is the quantity a structural forward model predicts ([[Best–Vendruscolo model]]) and the hinge between structure and [[deuterium uptake]]. It is also the level at which ValDX's Work Done metrics are computed. Those metrics are ValDX method notes, not this concept.

Claims that use this term: [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]], [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]].
