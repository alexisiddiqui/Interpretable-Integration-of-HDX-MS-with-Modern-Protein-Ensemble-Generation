---
type: paper
citekey: bonomiPrinciplesProteinStructural2017
year: 2017
read: false
pdf: kb/_pdf/@bonomiPrinciplesProteinStructural2017.pdf
extraction: auto
needs_review: false
review_reason:
---

# Principles of Protein Structural Ensemble Determination (2017)

## Main point

A review arguing that the principles of structure determination should be extended to structural ensembles. Experiments give sparse, ensemble-averaged data with random and systematic errors, and simulations are limited by force fields and sampling. Combining both is the proposed route. The authors classify methods by maximum entropy against maximum parsimony, Bayesian or not, and restraint against reweighting. They favour Bayesian methods that infer the error level and use the data as restraints during simulation, such as metainference. The review closes with community goals for comparison, validation and deposition of ensembles.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Noise in the data and structural heterogeneity are difficult to tell apart. ^c1
  - page: 2
  - quote: "noise and structural heterogeneity are difficult to disentangle"
  - quote_check: pass
  - reviewed: false
- An error estimate taken from the experiment is usually only a lower bound on the real uncertainty, because it misses systematic errors. ^c2
  - page: 5
  - quote: "in most situations this estimate only provides a lower bound on the real data uncertainty because it does not fully account for systematic errors"
  - quote_check: pass
  - reviewed: false
- The forward model that predicts an observable from a structural ensemble is often inaccurate. ^c3
  - page: 5
  - quote: "the theoretical model to calculate an experimental observable from a structural ensemble, commonly referred to as predictor or forward model, is often inaccurate"
  - quote_check: pass
  - reviewed: false
- The review reports that replica-averaged simulations have been shown equivalent to the maximum-entropy Lagrange-multiplier solution. ^c4
  - page: 4
  - quote: "The equivalence between replica-averaged simulations and the maximum entropy Lagrange-multipliers solution was demonstrated recently"
  - quote_check: pass
  - reviewed: false
- In Bayesian ensemble refinement and metainference, the restraint on the replica average depends on the unknown noise level and scales linearly with N when noise is present. ^c5
  - page: 5
  - quote: "intensity of this restraint on the structural ensemble is variable, depends on the unknown level of noise in the data, and scales linearly with N"
  - quote_check: pass
  - reviewed: false
- In metainference without data noise, the data energy term scales more than linearly with N, as the maximum entropy principle requires. ^c6
  - page: 5
  - quote: "the data energy term explicitly scales more than linearly with N in absence of data noise, as requested by the maximum entropy principle"
  - quote_check: pass
  - reviewed: false
- Poor prior information, including a coarse-grained model, can be compensated by a large amount of experimental data. ^c7
  - page: 5
  - quote: "a coarse-grained representation of the system, and in general poor prior information, can be compensated by the use of a large amount of experimental data"
  - quote_check: pass
  - reviewed: false
- Determining ensemble members from ensemble-averaged data is ill-defined, because different ensembles can fit the same averages. ^c8
  - page: 6
  - quote: "is an ill-defined problem, in the sense that it allows multiple solutions, as different structural ensembles can fit the same averaged data"
  - quote_check: pass
  - reviewed: false
- Reweighting is inaccurate when the prior used to generate the ensemble differs strongly from the reweighted distribution. ^c9
  - page: 7
  - quote: "Reweighting schemes are inaccurate whenever the prior distribution used to generate the initial ensemble differs significantly from the final, reweighted distribution"
  - quote_check: pass
  - reviewed: false
- If removing a fraction of the input data changes the ensemble a lot, that is a typical sign of poor accuracy. ^c10
  - page: 8
  - quote: "Upon removing a fraction of the input data, a large modulation in the resulting structural ensemble is a typical sign of poor accuracy"
  - quote_check: pass
  - reviewed: false

## What I use from it

For "Experimentally Restrained Simulations and Metainference" and "Maximum-Entropy and Bayesian Ensemble Refinement" in Chapter 2:
- the error sources that motivate a [[nuisance parameter]] per datum (^c1–^c3), with [[forward model]] error as one of them (^c3);
- the replica-average link to the [[maximum entropy principle]] (^c4) and the scaling of the restraint with N (^c5, ^c6);
- prior against data in [[metainference]] (^c7);
- underdetermination of the [[inverse problem]] (^c8);
- why restraints may be preferred over [[ensemble reweighting]] (^c9);
- validation by data removal (^c10), which leads into data splitting and replicate fits in §1.5.

The review also argues that the problem is well-defined from the point of view of measurement. Ensembles that give the same predicted observables can be treated as equivalent (p. 6, Fig. 3). This is a useful counterpoint to ^c8.

## Disagreements / limitations

- **It is a review with a stake.** Three authors developed metainference and M&M, and the review recommends both. The case for restraints over reweighting (p. 7) is stated as the authors' belief, not shown.
- **The MaxEnt equivalence is cited, not shown.** ^c4 points to refs. 32 and 38. Cesari et al. (2018) say the equivalence holds in the limit of many replicas, which the review does not mention.
- **Validation advice is brief.** Data removal (^c10) is one sentence. The review gives no threshold for a "large modulation" and does not ask whether the removed data overlap with the rest.
- **Well-defined only if the observables are the right ones.** The well-defined view rests on ensembles being indistinguishable by measurement. Whether independent observables will agree is assumed, not tested.
- **No HDX-MS.** The methods table and examples cover NMR, SAXS, FRET, XL-MS and cryo-EM.
