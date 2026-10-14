---
type: concept
aliases:
  - cross-validation
  - held-out validation
  - validation split
  - training and validation split
  - structured split
  - validation leakage
  - peptide overlap
  - dependence-aware partitioning
notation: []
sources:
  - "[[@siddiquiFrameworkTestingStructural2026#^c8]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c12]]"
  - "[[@siddiquiFrameworkTestingStructural2026#^c16]]"
  - "[[@bonomiPrinciplesProteinStructural2017#^c10]]"
  - "[[@englanderHydrogenExchangeModern1997#^c6]]"
  - "[[@bradshawInterpretationHDXData2020#^c20]]"
  - "[[@jiaIntegratingHydrogenDeuterium2023#^c4]]"
  - "[[@jiaIntegratingHydrogenDeuterium2023#^c5]]"
  - "[[@burnleyModellingDynamicsProtein2012#^c1]]"
  - "[[@crookEmpiricalBayesFunctional2022#^c1]]"
---

## Definition

Data splitting fits a model to part of the data (training) and tests it on the rest (validation), to measure how well it generalises ([[overfitting]]). The test is informative only when the withheld observations carry information the retained ones do not. When observations are dependent, a random partition leaves the validation set partly predictable from the training set, so its error is optimistic, and the partition should follow the structure of the dependence so that it withholds the kind of information the model is meant to predict. The general source for this principle, validation with dependent observations, is not yet in the vault (see Gaps in [[02-background]]). Repeating a random split many times averages over the choice of partition. It does not remove the leakage inside each partition.

HDX-MS observations are dependent through two routes. The first is direct. Peptides overlap, so the same residues appear in several peptides, and a random split puts peptides in the validation set whose uptake is predictable from training peptides covering similar regions ([[@siddiquiFrameworkTestingStructural2026#^c8]]). The second is physical. Residues open in [[cooperative unfolding unit|cooperative units]] smaller than the whole protein ([[@englanderHydrogenExchangeModern1997#^c6]]), so exchange at residues that share no peptide can still report the same opening reaction.

ValDX responds with structured partitions. Non-Redundant splits cluster peptides by sequence position and withhold whole regions. Spatial splits withhold peptides whose residues are close in the structure. Both drop peptides that still overlap across the boundary. Random and Sequential splits are kept as baselines, and on experimental datasets they added no discrimination beyond training error ([[@siddiquiFrameworkTestingStructural2026#^c16]]). Repeated splits of each kind test how much the result depends on which peptides and time points were used ([[@siddiquiFrameworkTestingStructural2026#^c12]]; [[replicate uncertainty]]). The algorithms are in [[Peptide splitting and consensus (ValDX)]].

## Unit withheld

Each partition withholds a different unit and so asks a different predictive question. State the unit whenever a validation result is reported.

| Unit withheld | Question asked | Where |
|---|---|---|
| Time point | Does the kinetic model extrapolate in time for peptides it has seen? ([[@bradshawInterpretationHDXData2020#^c20]]) | Proposed for HDXer |
| Peptide, at random | Does the fit reproduce a peptide whose residues it has mostly seen? Leakage makes this close to training error | ValDX baselines |
| Residue | Does the fit predict unseen residues? No peptide overlap, but [[cooperative unfolding unit|cooperative]] dependence remains | BPTI (NMR), HDX-NMR references |
| Sequence region | Does the fit predict a region of the chain it has not seen? | Non-Redundant |
| Structural region | Does the fit predict a region of the fold it has not seen? | Spatial |
| Experimental condition | Does an ensemble fitted to one condition explain another? | α-synuclein buffers (jaxENT, as negative controls) |

## Assumptions and limits

- Structured splits reduce dependence between the sets but do not guarantee independence (revised ValDX, `projects/1-ValDX/manuscript/report/1_introduction_omc.tex` L37; `6_methods_omc.tex` L52). Posted v1 says they "ensure" that validation error reflects true predictive performance; do not reuse that wording.
- Overlap also correlates the errors of neighbouring peptides, which most likelihoods treat as independent ([[forward model]], [[error covariance]]). jaxENT addresses this residual dependence by weighting rather than partitioning.
- Removing data is also a test of accuracy. A large change in the ensemble when a fraction of the data is removed is a typical sign of poor accuracy ([[@bonomiPrinciplesProteinStructural2017#^c10]]). This is the data-side case of a [[controlled perturbation]].
- Overlap removal has a cost. Dropping cross-boundary peptides changes the realised training fraction, and ValDX adjusts the redundancy dropout or removes long peptides when a split fails (`6_methods_omc.tex` L81, L482). With few peptides left the validation error itself is noisy.
- Selection and evaluation must use different data. If the fitting strength is chosen on validation error, that error is optimistic ([[model selection]]).
- Validation tests prediction of uptake. It does not show that the populations are unique ([[identifiability]]), and it does not test them directly, which is why ValDX adds [[Work Done]] and reference benchmarks.

## In integrative practice

- Crystallographic ensemble refinement selects its parameters on held-out reflections through Rfree ([[@burnleyModellingDynamicsProtein2012#^c1]]). Reflections do not share residues, so the leakage problem does not arise there.
- HDXer's authors propose splitting time points into training and validation sets ([[@bradshawInterpretationHDXData2020#^c20]]). The XylE study assessed robustness by re-optimising the Best–Vendruscolo coefficients and reweighting again, and concluded the interpretation was relatively robust to small forward-model uncertainties ([[@jiaIntegratingHydrogenDeuterium2023#^c4]], [[@jiaIntegratingHydrogenDeuterium2023#^c5]]). Neither check withholds peptides around their dependence.
- HDX-MS statistics recognise overlap correlation and leave it unmodelled ([[@crookEmpiricalBayesFunctional2022#^c1]]).
- Credit what each check achieves, then name what it leaves open. The defensible statement is that none of the HDX ensemble-integration studies examined partitions the data around peptide dependence; "integrative biophysics never splits data" is not defensible.

## Why it matters here

Introduction §1.5, paragraph 4, and the ValDX chapter's splitting protocol. Bayesian model comparison by evidence is the alternative for choosing a regularisation weight ([[Bayes' theorem#^eq-bayes-factor]], [[regularisation]]). The spread across split replicates and the consensus formed from them are in [[replicate uncertainty]] and [[model averaging]]. jaxENT's splitter differs from ValDX's in cluster number and dropout ([[Evaluation design (jaxENT)]]).

Claims that use this term: [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]], [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]], [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]], [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]], [[When observations are dependent, a random partition gives optimistic validation error, so the partition should follow the dependence.]], [[Repeating a random split reduces dependence on one partition but not the leakage within each partition.]], [[Cooperative unfolding couples exchange at residues that share no peptide, so removing peptide overlap does not make training and validation peptides independent.]], [[Withholding a time point, a peptide, a sequence region or a structural region asks different predictive questions.]], [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]], [[In the HDX ensemble-integration studies examined, robustness is assessed by removing selected peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions designed around peptide dependence.]].
