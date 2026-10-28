---
type: concept
aliases:
  - M7
  - Persson-Halle model
  - fractional-population HDX model
notation:
  - {symbol: '\kappa_i', meaning: 'closed-to-open population ratio of amide i', units: null}
  - {symbol: 'p_{C,i}', meaning: 'equilibrium closed-state population of amide i', units: null}
  - {symbol: 'p_{O,i}', meaning: 'equilibrium open-state population of amide i', units: null}
  - {symbol: '\tau_{C,i}', meaning: 'mean residence time in the closed state of amide i', units: 's'}
  - {symbol: '\tau_{O,i}', meaning: 'mean residence time in the open state of amide i', units: 's'}
sources:
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c3]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c5]]"
  - "[[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c6]]"
---

## Definition

The Persson–Halle model estimates residue protection by classifying each amide as open or closed in successive [[molecular dynamics]] frames, then calculating the relative populations of the two states. It is M7 in Mohammadiarani et al.'s comparison of [[HDX protection-factor model|protection-factor models]], which attributes it to Persson and Halle (2015, ref. 30). An amide is open when its hydrogen has at least two water oxygens within 2.6 Å and no protein polar atom within 2.6 Å, subject to the neighbouring-residue exclusions specified by the model. These criteria represent solvent access and disruption of intramolecular hydrogen bonding ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Model definitions in supporting information]], p. S7).

The population ratio connects the sampled conformations to the opening equilibrium in the [[Linderstrøm–Lang model]]. It therefore depends on both the structural definition of opening and how frequently the trajectory samples conformations satisfying it.

## Equations

$$ \kappa_i = \frac{p_{C,i}}{p_{O,i}} = \frac{\tau_{C,i}}{\tau_{O,i}} $$
^eq-population-ratio

Source: [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c3]], p. 3; [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c5]], pp. 8–9; Table 1, p. 21 (writes the ratio as PF). The residence-time equality is an equilibrium relation; finite-trajectory estimates can differ because the first and last visits are incomplete. Notation: [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Notation]].

$$ P_{f,i} = \frac{k_{\text{int},i}}{k_{\text{obs},i}} = 1 + \kappa_i = \frac{1}{p_{O,i}} \approx \kappa_i \qquad (p_{O,i} \ll 1) $$
^eq-population-pf

Source: [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c3]] and [[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Model definitions in supporting information]], p. S7 (unnumbered EX2 rate equation); [[protection factor#^eq-pf]] for the canonical rate-based definition. The final approximation requires predominantly closed amides.

## Derivation

1. The model's EX2 rate equation gives the observed rate as the intrinsic rate divided by one plus the closed-to-open population ratio ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#Model definitions in supporting information]], p. S7).
2. Taking the intrinsic-to-observed rate ratio gives the rate-based protection factor in [[#^eq-population-pf]] (step ours).
3. The closed and open populations sum to one, so one plus their ratio is the inverse open population (step ours).

## Assumptions and limits

- Exchange from the open state is assigned the [[intrinsic exchange rate]], and the population-to-rate relation assumes EX2. Mohammadiarani et al. call the closed-to-open ratio PF, whereas the KB defines protection as the intrinsic-to-observed rate ratio. They agree to the predominantly closed approximation above.
- Classical MD supplies candidate exchange-competent conformations; it does not simulate the chemical exchange reaction. Changing the water or polar-atom cutoffs changes the population being measured.
- A finite trajectory must sample enough openings to estimate their population. Highly protected amides can require millisecond or longer trajectories ([[@mohammadiaraniInterpretingHydrogenDeuteriumExchange2018#^c6]]). If no openings are observed, the sampled ratio diverges; this does not establish infinite physical protection.

## Why it matters here

M7 gives Chapter 2 a population-based comparison with the empirical [[Best–Vendruscolo model]] and [[Mohammadiarani SASA–distance model]]. The contrast distinguishes estimating how often an exchange-competent state occurs from calibrating structural features against protection.
