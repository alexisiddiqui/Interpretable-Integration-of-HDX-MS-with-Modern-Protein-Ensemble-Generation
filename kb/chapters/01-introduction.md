# 01 Introduction

Chapter hub: the argument in order, one claim per line. Sections follow `thesis/chapters/01-introduction.tex`.

Markers:
- **supported**: lint-verified evidence.
- **partial**: flagged for review because support is partial or indirect.
- **gap**: the cited paper does not support the claim, so it needs a new source or rewording.
- Unmarked claims are drafts that have not been flagged.

## 1.1 Proteins as Dynamic Ensembles

Why [[population shift|conformational populations]] matter for function and disease. The order follows the confirmation intro (`biological_dynamics.tex`). The ValDX opener ("understanding protein dynamics is crucial to understanding biological function, and therefore disease") and the jaxENT synthesis map onto groups 1 and 9.

**1. Static structures are not enough.** Function, disease and drug response depend on [[protein dynamics]], and the tools have mostly frozen proteins in time.
- [[Static structures alone cannot explain many biological phenomena; dynamics underlie disease mechanisms and drug response.]]
- [[Mounting evidence suggests that understanding dynamics is the key to novel therapeutic strategies.]]
- [[There is a persistent, critical gap in our ability to predict and understand protein dynamics.]]
- [[Tools have been dominated by methods that freeze proteins in time, hiding links between structure, dynamics, function and disease.]]

**2. The gap is one of scale.** Dynamic structural data are scarce next to static structures.
- [[Only about 12,000 experimental structural ensembles exist, covering 21% of CATH superfamilies, so dynamic data are scarce.]]
- [[Tools to estimate protein dynamics are decades old, but public datasets hold only thousands to tens of thousands of entries.]] (supported)

**3. Mutations shift populations, not structures.** Disease mutations can leave the crystal structure unchanged while reshaping the [[conformational free-energy landscape]].
- [[Cancer-causing p53 mutants have crystal structures nearly identical to wild type but very different DNA binding and pathologies.]] (gap)
- [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]]
- [[Mutations create neither steric clashes nor new folds but shift conformational ensembles, which needs sampling of many distributions.]] (partial)

**4. Static methods and their limits.** [[X-ray crystallography]], [[cryo-EM]] and [[NMR]] have transformed structural biology, but they restrict understanding to what they can measure.
- [[Structural biology has made tremendous strides in solving static protein structures by X-ray crystallography, cryo-EM and NMR.]]
- [[The fundamental limitations of these methods restrict our understanding to what can be measured experimentally.]]
- [[Across disease categories, high-resolution structures exist but mechanisms remain unclear.]] (gap)

**5. Kinases: drug sites preserved, equilibria shifted.** An example of [[allostery]] and [[population shift]].
- [[Kinases and their inhibitor resistance mutations often preserve drug-binding sites while shifting conformational equilibria.]]
- [[Shifted conformational equilibria are a major reason why most kinases are still undruggable.]] (gap)
- [[EGFR L858R and T790M mutations rigidify sub-domains and shift equilibria toward active states, preserving active-site geometry.]]

**6. Misfolding diseases share a dynamic mechanism.** [[protein misfolding and aggregation|Misfolding]] runs through transient [[high-energy intermediate|intermediates]].
- [[Diseases involving protein misfolding are prime case studies that highlight the limitations of structural biology.]]
- [[Alzheimer's, Parkinson's and prion diseases share dynamic conformational transitions that start pathological aggregation.]]
- [[The conformational dynamics underlying pathogenic aggregation are central to understanding these diseases.]] (partial)
- [[These neurodegenerative diseases involve transient oligomeric intermediates that never crystallize.]] (partial)
- [[High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.]] (partial)

**7. α-Synuclein: dynamics hidden in plain sight.** In [[alpha-synuclein]], the fibril is solved but the protective solution state is an ensemble.
- [[Alpha-synuclein is an unfolded monomer, yet cryo-EM has solved its Lewy body fibril structures at atomic resolution.]] (partial)
- [[Cryo-EM fibrils are helical but the solution state is disordered, so aggregation-prone states can escape standard methods.]] (partial)
- [[Soluble alpha-synuclein stays compact through transient long-range contacts between its charged C-terminus and hydrophobic centre.]] (gap)
- [[Conformational heterogeneity from pathogenic mutations fundamentally alters alpha-synuclein's protective intramolecular interactions.]] (gap)
- [[NMR showed protective picosecond intramolecular interactions in soluble alpha-synuclein, whose disruption starts aggregation.]] (partial)
- [[Linking fast molecular motions to slow pathological processes requires conformational dynamics that static structures cannot capture.]]

**8. IDPs: heterogeneity is the function.** For an [[intrinsically disordered protein]], the ensemble is the description.
- [[For intrinsically disordered proteins, the failure of static structural biology becomes apparent.]]
- [[Intrinsically disordered proteins lack stable structures and exist as heterogeneous conformational ensembles.]] (supported)
- [[The conformational heterogeneity of IDPs is not a limitation but the functional mechanism by which they carry out their roles.]]

**9. Prion protein: the full ensemble is needed.** The [[prion protein]] case study links to the MoPrP test system used in jaxENT.
- [[Atomic structures of PrP-C and PrP-Sc show an alpha-to-beta transition, yet how monomeric PrP-C traverses it is unclear.]] (partial)
- [[Rate-limiting conformational changes take microseconds to milliseconds, beyond the reach of traditional structural methods.]] (partial)
- [[High-energy intermediates with enhanced conformational heterogeneity precede aggregation but resist crystallization.]] (partial)
- [[Sparsely populated intermediates act as critical gateway states that control the kinetics of pathological conversion.]]
- [[Combining MD simulations with NMR chemical shifts has revealed misfolding intermediates invisible to crystallography.]] (supported)
- [[Understanding prion conversion requires the complete conformational ensemble, not just the ground and fully misfolded states.]] (partial)

**10. Bridge to 1.2: ensembles need populations, and populations need measurements.** A [[structural ensemble]] is only useful once its weights are known.
- [[Integrating over time turns individual structures into structural ensembles, a quantitative route to mechanisms.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]
- [[Without experimental measurements of protein dynamics, the biological mechanism of misfunction can remain unclear.]]
- [[Quantifying state populations requires experimental measurements of protein dynamics.]]
- [[Bridging the gap requires a shift toward integrative approaches combining measurements of dynamics with advanced simulations.]]

### Gaps
- **No claim yet** for the jaxENT synthesis: "Protein conformational dynamics govern biological function and modulate disease-associated conformational states, necessitating their representation as diverse structural ensembles rather than single static models" (`projects/2-jaxENT/manuscript/report/introduction.tex` ¶1). Two of its citations are not yet in `thesis/references.bib` or `kb/papers/`: `moulickPartiallyUnfoldedForms2015` and `bonomiPrinciplesProteinStructural2017`.
- **gap** claims above need a source that supports them, or rewording to what the checked source says:
  - p53: neither cited paper covers it.
  - Kinase druggability: Lisi and Loria's remark concerns phosphatases.
  - α-synuclein contacts and mutations: Mukherjee describes an N- to C-terminal contact protecting NAC.
  - "Across disease categories": Lee et al. does not address it.

## 1.2 Measuring Protein Dynamics

Not yet assembled.

## 1.3 Estimating Protein Dynamics

Not yet assembled.

## 1.4 Integrating Experiment and Ensembles

Not yet assembled.

## 1.5 Trusting Integrative Ensemble Models

Not yet assembled.

## 1.6 Research Questions and Objectives

Not yet assembled.

## 1.7 Thesis Outline and Contributions

Not yet assembled.
