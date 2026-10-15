---
type: concept
aliases:
  - intrinsic rate
  - intrinsic exchange rates
  - chemical exchange rate
  - random coil exchange rate
  - k_int
notation:
  - {symbol: 'k_{\text{int},i}', meaning: 'intrinsic (random-coil) exchange rate of residue i', units: 's^-1'}
  - {symbol: 'k_\text{acid}', meaning: 'second-order rate constant for acid-catalysed exchange', units: 'M^-1 s^-1'}
  - {symbol: 'k_\text{base}', meaning: 'second-order rate constant for base-catalysed exchange', units: 'M^-1 s^-1'}
  - {symbol: 'k_\text{water}', meaning: 'rate constant for water-catalysed exchange', units: 's^-1'}
  - {symbol: 'E_a', meaning: 'activation energy of a catalysed exchange rate constant', units: 'kcal mol^-1'}
  - {symbol: '\text{pD}', meaning: 'acidity of a D2O solution, -log10 of the deuterium-ion activity', units: null}
  - {symbol: '\text{pH}_\text{read}', meaning: 'reading of a glass electrode calibrated in H2O and placed in a D2O solution', units: null}
sources:
  - "[[@baiPrimaryStructureEffects1993#^c2]]"
  - "[[@baiPrimaryStructureEffects1993#^c3]]"
  - "[[@baiPrimaryStructureEffects1993#^c4]]"
  - "[[@baiPrimaryStructureEffects1993#^c5]]"
  - "[[@glasoeUseGlassElectrodes1960#^c1]]"
  - "[[@connellyIsotopeEffectsPeptide1993#^c1]]"
  - "[[@connellyIsotopeEffectsPeptide1993#^c2]]"
  - "[[@nguyenReferenceParametersProtein2018#^c1]]"
  - "[[@nguyenReferenceParametersProtein2018#^c2]]"
---

## Definition

The intrinsic exchange rate $k_{\text{int},i}$ is the rate at which the amide hydrogen of residue $i$ would exchange in an unstructured, fully solvent-exposed peptide. It is the sum of acid-, base- and water-catalysed terms. It depends on pH, on temperature, and on the two neighbouring side chains through blocking and inductive effects. Bai et al. give side-chain factors and an additivity rule to predict it from sequence.

## Equations

$$ k_{\text{int},i} = k_\text{acid}[\text{H}^+] + k_\text{base}[\text{OH}^-] + k_\text{water} $$
^eq-kint

Source: [[@baiPrimaryStructureEffects1993#^c2]], Eq. (1), p. 3. Bai writes $k_A$, $k_B$ and $k_W$. They are renamed here because $k_B$ is the Boltzmann constant (notation: [[@baiPrimaryStructureEffects1993#Notation]]).
Manuscript form: milestones/2025-11-confirmation-of-status/jaxENT_paper1/report/methods/HDX.tex#L51.

$$ \log_{10} k_{\text{int},i} = \log_{10} k_{\text{base},\text{ref}} + \log_{10} B_L + \log_{10} B_R + \text{pH} - \text{p}K_W \quad (\text{base-catalysed term}) $$
^eq-kint-sequence

Source: [[@baiPrimaryStructureEffects1993#^c3]], Eq. (2a), p. 8, which writes the base term as the alanine reference constant times the side-chain factors $B_L B_R$ and the hydroxide concentration. Eq. (2a) is an image in the PDF; check it against the page. $B_L$ and $B_R$ are the side-chain factors of the left and right neighbours. The log form, with $[\text{OH}^-] = 10^{\text{pH} - \text{p}K_W}$, is step ours. The acid term is analogous, with $A_L$ and $A_R$.
Manuscript form: jaxENT_paper1/report/methods/HDX.tex#L57 writes the base term with "sequence corrections".

$$ k(T) = k(293\,\text{K}) \exp\!\left[-\frac{E_a}{R}\left(\frac{1}{T} - \frac{1}{293\,\text{K}}\right)\right] $$
^eq-kint-temperature

Source: [[@baiPrimaryStructureEffects1993#^c4]], Eq. (3), p. 8. Eq. (3) is an image in the PDF, so this is the standard Arrhenius form; check it against the page. Bai recommends $E_a$ = 14, 17 and 19 kcal mol⁻¹ for $k_\text{acid}$, $k_\text{base}$ and $k_\text{water}$ (below Table III). The reference temperature of 20 °C is from the same page.
Manuscript form: none. **Gap:** no manuscript applies a temperature correction.

$$ \text{pD} = \text{pH}_\text{read} + 0.40 $$
^eq-pd

Source: [[@glasoeUseGlassElectrodes1960#^c1]]; used for HX by Connelly et al. ([[@connellyIsotopeEffectsPeptide1993#^c2]]). Nguyen et al. give +0.36 instead of +0.40 for 90% D₂O ([[@nguyenReferenceParametersProtein2018#^c2]]), so the offset depends on the D₂O fraction of the labelling buffer. HDX labelling is done in D₂O, so the "pD 4" of the MoPrP data (jaxENT) is a corrected glass-electrode reading. Whether the reported value is $\text{pH}_\text{read}$ or pD changes the intrinsic rates by a factor of about 2.5 in the base-catalysed regime (step ours, from Eq. ^eq-kint-sequence).
Manuscript form: none. jaxENT computes intrinsic rates "at pD 4" (`protocols.tex` L185) without saying whether the correction was applied.

### Ionisable neighbours

His, Asp and Glu neighbours need separate rate constants for their protonated and unprotonated forms, so their side-chain factors themselves depend on pH around the side-chain pKa ([[@baiPrimaryStructureEffects1993#^c5]]; pKa,read in D₂O at 5 °C: His 7.02, Glu 4.53, Asp 4.08). Between pD 7 and pD 4 every His neighbour and part of the Asp and Glu neighbours change form, so a single factor per residue type is wrong across that range. Exchange rate constants also differ between H₂O and D₂O ([[@connellyIsotopeEffectsPeptide1993#^c1]]).

## Assumptions and limits

- The reference rates are for unstructured peptides in low salt. Real disordered regions may deviate.
- Side-chain effects are assumed additive between nearest neighbours.
- D₂O/H₂O isotope effects are treated by Connelly et al. ([[@connellyIsotopeEffectsPeptide1993]]), the companion paper. Nguyen et al. 2018 raise the Ala–Ala reference rate by a factor of 1.35 relative to Bai and Connelly ([[@nguyenReferenceParametersProtein2018#^c1]]).

## Why it matters here

$k_{\text{int},i}$ is the reference against which every [[protection factor]] is measured, and it enters every [[deuterium uptake]] prediction. An error here propagates to every residue regardless of the structural ensemble. This is one reason forward-model error and ensemble error are hard to separate.

The pH dependence links this concept to [[pKa]]: §2.5 points back here for the pD correction and the ionisable neighbours, rather than repeating them.

Claims that use this term: [[Amide exchange rates depend on intrinsic chemistry and on local protection from hydrogen bonding, burial and transient opening.]], [[His, Asp and Glu neighbours change intrinsic exchange rates with pH through their own ionisation.]].
