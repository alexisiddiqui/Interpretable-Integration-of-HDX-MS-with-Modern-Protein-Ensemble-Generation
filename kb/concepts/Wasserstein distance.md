---
type: concept
aliases:
  - Wasserstein-1 distance
  - Wasserstein-1
  - earth mover's distance
  - EMD
  - optimal transport distance
notation:
  - {symbol: 'W_1', meaning: 'Wasserstein-1 (earth mover''s) distance between two distributions', units: 'units of the compared variable'}
  - {symbol: 'F_A(t)', meaning: 'cumulative distribution function of distribution A at value t', units: null}
sources: []
---

## Definition

The Wasserstein-1 distance between two distributions is the least total "work" needed to move the probability mass of one onto the other, where moving mass costs its amount times the distance moved. It is also called the earth mover's distance. Unlike a divergence such as [[Kullback–Leibler divergence|KL]] or [[ensemble comparison#^eq-jsd|JSD]], it uses the geometry of the variable. Two narrow distributions 1 Å apart are closer than two 5 Å apart, even when neither pair overlaps, and the distance is in the units of the variable.

For one-dimensional distributions it reduces to the area between their cumulative distribution functions.

## Equations

$$ W_1(A, B) = \int_{-\infty}^{\infty} \left| F_A(t) - F_B(t) \right| dt $$
^eq-w1

Source: SciPy documentation, `scipy.stats.wasserstein_distance` (https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wasserstein_distance.html; doc pointer, not a quoted block). It accepts weighted samples, so reweighted ensembles can be compared directly.

## Assumptions and limits

- **gap.** No quotable source in the KB yet. The SciPy documentation gives the definition, and the software citation is Virtanen et al. 2020 (`virtanenSciPy10Fundamental2020`, in both project bibliographies, no local PDF). A textbook or primary optimal-transport source would make this a sourced definition.
- **Marginals are not the joint distribution (ours).** ValDX applies $W_1$ to each residue's distribution of pairwise Cα distances and averages over residues. Agreement there means the per-residue marginals agree. It does not establish that two ensembles share the same joint conformational distribution, because different couplings between residues can give the same marginals.
- **Smoothing is a choice.** With finite frames the distributions are estimated, for example by kernel density estimation, and the bandwidth changes the distance (ours).
- **Distance without direction.** A large $W_1$ says how far the distributions are apart, not which ensemble is closer to experiment. That needs a reference ([[sampling coverage]]).

## Why it matters here

Chapter 2, "Ensemble Comparison and Interpretable Representations". ValDX uses a residue-averaged $W_1$ between pair-distance distributions to say where two generator ensembles differ in their full distribution, not only in mean geometry. The pair-distance construction and its weighting are ValDX's own and are defined in [[Structural comparison metrics (ValDX)]].

Claims that use this term: [[Agreement of per-residue pair-distance distributions does not establish that two ensembles share the same joint conformational distribution.]].
