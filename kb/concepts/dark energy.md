---
type: concept
aliases:
  - dark energy in proteins
  - functional dark energy
  - dark energy of the functional protein universe
notation:
  - {symbol: 'E_\text{dark}', meaning: 'dark energy of a sequence, the evolutionary energy rescaled by the folding selection temperature minus the folding energy', units: 'kcal mol^-1'}
  - {symbol: 'E_\text{fold}', meaning: 'folding energy gap of a sequence, the energy difference between its native state and the unfolded ensemble', units: 'kcal mol^-1'}
  - {symbol: '\Psi_\text{evo}', meaning: 'evolutionary free energy of a sequence inferred from sequence data (a Massieu function)', units: null}
  - {symbol: 'T_\text{sel}^\text{fold}', meaning: 'folding selection temperature relating the evolutionary and folding energy scales', units: 'K'}
sources:
  - "[[@galpernProbingDarkEnergy2026#^c1]]"
  - "[[@galpernProbingDarkEnergy2026#^c2]]"
  - "[[@galpernProbingDarkEnergy2026#^c3]]"
  - "[[@galpernProbingDarkEnergy2026#^c5]]"
  - "[[@galpernProbingDarkEnergy2026#^c14]]"
  - "[[@galpernProbingDarkEnergy2026#^c15]]"
  - "[[@galpernProbingDarkEnergy2026#^c16]]"
  - "[[@galpernProbingDarkEnergy2026#^c17]]"
---

## Definition

Dark energy is the difference between the physical folding free energies and the evolutionary free energies inferred from sequences ([[@galpernProbingDarkEnergy2026#^c1]]). It is the part of the evolutionary constraint on a sequence that folding does not explain. A variant that affects folding alone shifts both energies together and leaves the dark energy unchanged ([[@galpernProbingDarkEnergy2026#^c14]]), while a variant that affects a function beyond folding is expected to change it significantly ([[@galpernProbingDarkEnergy2026#^c16]]). The dark energy is largely localised at functional sites, which are also often energetically frustrated from the point of view of folding ([[@galpernProbingDarkEnergy2026#^c2]]; [[local frustration]]), and about a quarter of the positions of folded globular proteins display some significant dark energy ([[@galpernProbingDarkEnergy2026#^c3]]).

## Equations

$$ E_\text{dark} = k_B T_\text{sel}^\text{fold}\,\Psi_\text{evo} - E_\text{fold} $$
^eq-dark-energy

Source: [[@galpernProbingDarkEnergy2026#^c17]], Eq. (5), p. 3. Galpern et al. write the dark energy of a sequence $\sigma$ as $E^{dark}(\sigma)$, with $\Psi^{evo}$ and $E^{fold}$. The talk figure (panel D of `fig:intro-evolutionary-funnel`) labels the same difference $E^{dynamics}$.

## Why it matters here

The score of a sequence-evolutionary model reflects folding and function together, so a deleterious variant can be flagged without showing which of the two it affects. The dark energy separates them (`fig:intro-evolutionary-funnel`). Variants on the stability trend are destabilising, and the outliers are functionally deleterious without a proportional loss of stability ([[@galpernProbingDarkEnergy2026#^c15]]), which is the content of `fig:intro-destabilising-mutations`. A two-component mixture puts about a quarter of single-site variants in the mainly function-related group ([[@galpernProbingDarkEnergy2026#^c5]]). See [[dynamic disease mechanism]].

## Assumptions and limits

- The folding energy is a global $\Delta\Delta G$ or an AWSEM energy computed on one fixed native structure, so a shift in populations within the native basin appears as dark energy. Whether dark energy at sites far from the active site reflects enzyme dynamics and allostery is proposed in the paper and not tested ([[@galpernProbingDarkEnergy2026#^c10]]).
- The quarter depends on a Gaussian-mixture threshold and on the folding-energy method (25 to 35%).

Claims that use this term: [[Sequence-evolutionary scores combine folding and function, so their excess over folding energy, the dark energy, marks function-related change.]], [[Deleterious variants are not only destabilising ones, because about a quarter of single-site variants act mainly on function.]], [[Function conflicts with folding, so sequences encode function locally at sites that sacrifice stability.]].
