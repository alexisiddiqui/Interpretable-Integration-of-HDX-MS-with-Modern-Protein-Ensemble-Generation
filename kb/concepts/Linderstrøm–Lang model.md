---
type: concept
aliases:
  - Linderstrøm-Lang model
  - Linderstrom-Lang model
  - Linderstrøm–Lang kinetics
  - EX2
  - EX1
  - EX2 regime
  - EX1 regime
notation:
  - {symbol: 'k_\text{op}', meaning: 'opening rate constant of an amide', units: 's^-1'}
  - {symbol: 'k_\text{cl}', meaning: 'closing rate constant of an amide', units: 's^-1'}
  - {symbol: 'K_\text{op}', meaning: 'opening equilibrium constant, k_op / k_cl', units: null}
  - {symbol: 'k_{\text{obs},i}', meaning: 'observed exchange rate of residue i', units: 's^-1'}
sources:
  - "[[@skinnerProteinHydrogenExchange2012#^c1]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c2]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c3]]"
  - "[[@skinnerProteinHydrogenExchange2012#^c5]]"
  - "[[@englanderHydrogenExchangeModern1997#^c1]]"
  - "[[@englanderHydrogenExchangeModern1997#^c2]]"
  - "[[@jamesAdvancesHydrogenDeuterium2022#^c7]]"
  - "[[@vinciauskaiteFundamentalsHDXMS2023#^c4]]"
---

## Definition

The Linderstrøm–Lang model treats each backbone amide as switching between a closed state, which cannot exchange, and a transiently open state, which exchanges at the [[intrinsic exchange rate]]. Exchange is a competition between chemical exchange and reclosing. Their relative rates define two limits:
- **EX2:** stable structure and fast reclosing. The observed rate is the intrinsic rate scaled by the fraction of time open, which gives the [[protection factor]].
- **EX1:** reclosing slower than chemical exchange. The observed rate is the opening rate itself.

## Equations

$$ \text{NH}_\text{cl} \underset{k_\text{cl}}{\overset{k_\text{op}}{\rightleftharpoons}} \text{NH}_\text{op} \xrightarrow{k_{\text{int},i}} \text{ND} $$
^eq-ll-scheme

Source: [[@skinnerProteinHydrogenExchange2012#^c1]] (Scheme 1, p. 8); [[@englanderHydrogenExchangeModern1997#^c1]] (p. 1).
Manuscript form: milestones/2025-11-confirmation-of-status/jaxENT_paper1/report/methods/HDX.tex#L13. ValDX writes $C_i \rightleftharpoons O_i \rightarrow D_i$ with $k_{\text{open},i}$, $k_{\text{close},i}$ (projects/1-ValDX/manuscript/report/6_methods_omc.tex#L136).

$$ k_{\text{obs},i} = \frac{k_\text{op}\, k_{\text{int},i}}{k_\text{cl} + k_\text{op} + k_{\text{int},i}} $$
^eq-ll-kobs

Source: steady state of the scheme above (step ours). See the derivation below.
Manuscript form: jaxENT_paper1/report/methods/HDX.tex#L21 drops $k_\text{op}$ from the denominator, which assumes $k_\text{op} \ll k_\text{cl} + k_{\text{int},i}$.

$$ \text{EX2 } (k_\text{cl} \gg k_{\text{int},i},\ k_\text{cl} \gg k_\text{op}):\quad k_{\text{obs},i} \approx K_\text{op}\, k_{\text{int},i}, \qquad K_\text{op} = \frac{k_\text{op}}{k_\text{cl}} $$
^eq-ex2

Source: [[@skinnerProteinHydrogenExchange2012#^c3]], Eq. (2), p. 8; [[@englanderHydrogenExchangeModern1997#^c2]], p. 2. In words, an EX2 amide opens many times before it exchanges ([[@jamesAdvancesHydrogenDeuterium2022#^c7]], p. 2), and each opening is only a chance to exchange ([[@vinciauskaiteFundamentalsHDXMS2023#^c4]], p. 3).
Manuscript form: jaxENT_paper1/report/methods/HDX.tex#L31.

$$ \text{EX1 } (k_{\text{int},i} \gg k_\text{cl}):\quad k_{\text{obs},i} \approx k_\text{op} $$
^eq-ex1

Source: [[@skinnerProteinHydrogenExchange2012#^c5]], p. 8.
Manuscript form: jaxENT_paper1/report/methods/HDX.tex (EX1 paragraph after L37).

## Derivation

1. Write the closed and open populations as $C$ and $O$. With exchange irreversible in excess D₂O, $\dot C = -k_\text{op} C + k_\text{cl} O$ and $\dot O = k_\text{op} C - (k_\text{cl} + k_{\text{int},i}) O$ (step ours, from the scheme in [[@skinnerProteinHydrogenExchange2012#^c1]]).
2. Under a quasi-steady state for the open form, $\dot O \approx 0$ gives $O = k_\text{op} C / (k_\text{cl} + k_{\text{int},i})$ (step ours).
3. The observed rate is the exchange flux per unexchanged amide, $k_{\text{obs},i} = k_{\text{int},i}\, O/(C + O)$. Substituting step 2 gives the equation above (step ours).
4. EX2: if $k_\text{cl} \gg k_{\text{int},i}$ and $k_\text{cl} \gg k_\text{op}$, then $k_{\text{obs},i} \to (k_\text{op}/k_\text{cl})\, k_{\text{int},i} = K_\text{op}\, k_{\text{int},i}$. This is Skinner Eq. (2) ([[@skinnerProteinHydrogenExchange2012#^c3]]).
5. EX1: if $k_{\text{int},i} \gg k_\text{cl}, k_\text{op}$, then $k_{\text{obs},i} \to k_\text{op}$ ([[@skinnerProteinHydrogenExchange2012#^c5]]).

## Assumptions and limits

- There are two states per amide, opening is independent of exchange, and labelling is irreversible (excess D₂O).
- EX2 is the usual regime under native conditions, and only EX2 yields an equilibrium [[protection factor]]. EX1, or mixed kinetics, at high pH or for slow-reclosing units reports the opening rate instead.
- The model says nothing about which structural motions cause opening. That is the job of a forward model such as the [[Best–Vendruscolo model]].

## Why it matters here

Every structure-to-uptake model in the thesis assumes EX2. This note is where that assumption and its limits are stated, before [[protection factor|protection factors]] and [[deuterium uptake]] build on it.

Claims that use this term: [[Under EX2 an amide opens and closes many times before it exchanges, so the observed rate combines intrinsic chemistry with the opening equilibrium.]], [[Labelling time measures accumulated exchange, not the duration of a conformational motion.]].
