# 02 Background and Literature Review

Chapter hub: concepts and their equations in the order of `thesis/chapters/02-background.tex`. Equation links point at single displayed equations (`#^eq-…`). Every symbol follows [[2026-10-13 canonical HDX and ensemble notation]]; `notation.md` lists them.

Markers:
- **gap**: something the chapter needs that has no verified source or manuscript form yet.
- **decision**: a choice to make before writing.

## 2.1 HDX-MS: Measurement, Exchange Kinetics, and Structural Interpretation

**Argument.** Structural interpretation of HDX-MS requires a model of how conformational opening and chemical exchange produce the measured peptide uptake. Intrinsic exchange rates provide the chemical reference, while the exchange regime determines whether observed rates report on opening equilibria or opening kinetics. Protection factors connect these rates to structural models under the EX2 assumption. Predicting peptide uptake from those models permits direct comparison with experiment, although agreement does not uniquely determine the underlying residue protection or conformational populations.

Introductory equations: [[protection factor#^eq-pf]] and [[deuterium uptake#^eq-uptake-residue]].

### Experimental Workflow and Measurement Limitations

HDX-MS records exchange by measuring peptide mass increases after defined labelling intervals. Each peptide combines contributions from several amides, and back-exchange during sample handling changes the amount of deuterium retained. Peptide averaging and back-exchange correction therefore determine how a predicted exchange profile should be compared with the measurement.

- [[deuterium uptake]]: peptide averaging [[deuterium uptake#^eq-uptake-peptide]] and back-exchange correction [[deuterium uptake#^eq-uptake-corr]].
- **decision**: present back-exchange as an equation or in prose. It is commented out in the current jaxENT methods.
- [[Conventional peptide-level HDX-MS reports uptake averaged over the exchangeable amides within each fragment.]]

### Intrinsic Exchange Rates

The measured uptake combines contributions from amides with different chemical exchange rates. Structural interpretation therefore begins with the rate expected for each amide in an unstructured, solvent-exposed peptide. The intrinsic rate depends on neighbouring residues, temperature and solution acidity through acid-, base- and water-catalysed exchange. These chemical contributions must be specified before a difference in observed exchange can be attributed to structural protection.

- [[intrinsic exchange rate]]: [[intrinsic exchange rate#^eq-kint]], [[intrinsic exchange rate#^eq-kint-sequence]], [[intrinsic exchange rate#^eq-kint-temperature]].
- **gap**: no manuscript applies Bai's temperature correction. Bai's Eqs. (2a) and (3) are images and need checking against the PDF.

### Linderstrøm–Lang Exchange Kinetics and EX1/EX2 Regimes

Intrinsic rates describe exchange in an exposed amide, but exchange in a folded protein also depends on access to that state. The Linderstrøm–Lang model connects the chemical rate to conformational opening and closing. Under EX2 conditions, repeated opening and closing precede exchange, so the observed rate combines the opening equilibrium with intrinsic chemistry. In the EX1 limit, exchange occurs before reclosing and the observed rate approaches the opening rate. The exchange regime therefore determines which aspect of conformational behaviour the measurement reports.

- [[Linderstrøm–Lang model]]: scheme [[Linderstrøm–Lang model#^eq-ll-scheme]], steady state [[Linderstrøm–Lang model#^eq-ll-kobs]], limits [[Linderstrøm–Lang model#^eq-ex2]] and [[Linderstrøm–Lang model#^eq-ex1]], with the derivation in the note.
- Distinguish exchange kinetics from conformational timescales: [[protein dynamics]].
- **gap**: no PDF for Hvidt and Nielsen 1966 or Smith 1997. Skinner 2012 and Englander 1997 carry the sources for now.

### Protection Factors and Peptide Uptake

The EX2 limit provides the basis for interpreting exchange protection thermodynamically. The protection factor, defined as the ratio of an amide's intrinsic exchange rate to its observed exchange rate, relates exchange to the opening equilibrium under these conditions. For predominantly closed amides under EX2, its logarithm relates protection to the equilibrium free energy of opening. Residue-level exchange predictions are combined over each peptide to calculate uptake, but the reverse inference is generally underdetermined. Several residue protection profiles can produce the same peptide uptake.

- [[protection factor]]: [[protection factor#^eq-pf]] and [[protection factor#^eq-dgop]] (EX2 free energy, with derivation).
- [[deuterium uptake]]: [[deuterium uptake#^eq-uptake-residue]] → [[deuterium uptake#^eq-uptake-peptide]].
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]]

### Structural Forward Models for HDX

Protection factors provide a route to calculating uptake, but do not specify the conformations responsible for protection. Structural forward models supply that connection by estimating protection from features of candidate conformations. The Best–Vendruscolo model estimates residue protection from hydrogen bonding and burial, with empirical coefficients that calibrate these features against exchange. The choice of features, calibration and ensemble averaging determines the prediction. Comparison at the peptide level retains the experimental readout, while residue protection factors, where available, provide a more stringent test.

- [[Best–Vendruscolo model]]: [[Best–Vendruscolo model#^eq-bv-feature]] and [[Best–Vendruscolo model#^eq-bv-ensemble]].
- [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]]
- [[HDX protection-factor model]] gives the alternatives and their shared assumptions (EX2, independent residues, calibration to conditions). It has no equation of its own, because BV carries the displayed form.
- Structure-based models predict a protection factor per residue. Peptide data generally cannot determine those values uniquely, which is why the thesis compares predictions with measured uptake.
  - [[Residue protection factors are generally underdetermined by peptide-level uptake.]]
  - [[A single protection factor per residue cannot describe a residue whose environment differs between populated conformers.]]
  - [[Residue protection factors test structural models more stringently than peptide uptake alone.]]
- **gap**. The switch-function variant needs Radou et al. 2014 (Biophys J 107, 983–990), which could not be downloaded. Park 2015's PDF is unreadable.
- **decision**. ValDX `6_methods_omc.tex` L624 cites Skinner 2019 for the switch-function BV model. Skinner 2019 describes no such model and cites Radou 2014, so the manuscript citation should change.

A structural forward model provides a route from candidate conformations to predicted uptake. It does not determine which conformations should be included or how much each should contribute. Those choices depend first on how the candidate ensemble is generated.

## 2.2 Protein Conformational Ensembles and Their Generation

**Argument.** The conformations supplied to an HDX forward model depend on the sampling method used to generate them. Molecular dynamics, enhanced sampling and learned generators differ in both the states they reach and the distributions from which those states are sampled. Their outputs must therefore be assessed separately for conformational coverage, equilibrium populations and transition kinetics. These distinctions determine how a generated ensemble can be used to interpret experiment.

### Molecular Dynamics and Empirical Force Fields

Molecular dynamics generates trajectories by integrating equations of motion under a force field. When equilibrium sampling has converged, conformational populations reflect the Boltzmann distribution of that approximate potential. A low potential energy for one structure does not establish a high population for its conformational state, because state populations depend on the free energy of the entire basin.

- [[molecular dynamics]]: [[molecular dynamics#^eq-newton]] (very light).
- [[Boltzmann distribution]]: [[Boltzmann distribution#^eq-boltzmann]].
- **gap**: a displayed-equation source for Newton's or Langevin's equation.
- The [[force field]] defines the potential energy $U(x)$ of a conformation. The distinction between this energy and the free energy of a basin governs how individual structures and state populations are assessed.

### Enhanced Sampling

The equilibrium distribution of a force field is useful only to the extent that the simulation explores it. When conventional molecular dynamics rarely crosses between relevant states, enhanced sampling changes the sampling procedure to improve their exploration. Bias potentials or extended ensembles change the sampling distribution, so equilibrium estimates require a correction to the intended target distribution. Recovering equilibrium populations does not generally recover the kinetics of the unbiased system.

- [[Markov chain Monte Carlo]]: detailed balance [[Markov chain Monte Carlo#^eq-detailed-balance]] and Metropolis–Hastings [[Markov chain Monte Carlo#^eq-metropolis-hastings]], if the chapter needs them. Extended ensembles and reweighting back to the target are in the note's limits.
- Claims: [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]]

### Learned Structure Predictors and Ensemble Generators

Enhanced sampling broadens exploration through modified simulation protocols. Learned predictors and generators provide another source of candidate conformations, whose interpretation depends on the training objective and the distribution represented by their outputs. A predictor supplies structural candidates and estimates of prediction accuracy, whereas a probabilistic generator samples a learned distribution. Neither prediction confidence nor the frequency of a generated conformation can be interpreted as its physical population without establishing the relationship between the model and the equilibrium distribution.

- Very light equation. [[statistical potential#^eq-statistical-potential]] writes any model density as an energy. This answers the `.tex` stub "Discuss statistical potentials" (L41).
- [[statistical potential]] is the general idea, and [[knowledge-based potential]] is its database-count case ([[knowledge-based potential#^eq-inverse-boltzmann]]). Such an energy is a statistical quantity unless its density is the physical equilibrium one. AF2 exposes no normalised density, so ValDX's "AF2 generates structures according to a statistical potential" is an analogy.
- [[protein structure predictor]] is trained for one PDB-like structure and reports accuracy, not population.
  - [[AlphaFold2 is trained on PDB structures to predict the structure most likely to appear in the PDB.]]
  - [[A structure predictor's confidence score measures expected accuracy, not the free energy or population of a conformation.]]
  - [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]]
- [[MSA subsampling]] turns a predictor into a source of candidates. Present the population evidence as qualitative and the mechanism as contested.
  - [[Subsampled AlphaFold2 can predict the direction of population shifts qualitatively, but quantitative Boltzmann ratios have not been shown.]]
  - [[Frequencies of states in MSA-clustered AlphaFold2 predictions reflect family abundance, not Boltzmann weights.]]
  - [[Whether MSA clustering recovers alternative states through evolutionary couplings is contested.]]
  - Do not reuse [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]] as worded.

### Diffusion Models for Protein Structure Generation

Sampling a learned structural distribution requires a procedure for generating new conformations from it. Diffusion models construct that procedure by learning to reverse the progressive corruption of training structures with noise. The reverse process samples a learned structural distribution; its steps are not increments of physical simulation time. For models trained on deposited protein structures, the resulting distribution reflects the training data and does not by itself specify equilibrium populations in solution.

- [[diffusion model]]: [[diffusion model#^eq-diffusion-forward]] and [[diffusion model#^eq-diffusion-reverse]]. The link back to MD (Boltzmann score = force / $k_BT$) is in the note's derivation.
- [[PDB-trained diffusion models learn conformations represented in a structural database rather than equilibrium populations under specified solution conditions.]]

### Sampling Coverage and Ensemble Populations

Structural diversity from a generator establishes neither equilibrium populations nor physical transition kinetics. Assessing the resulting ensemble therefore requires distinguishing which states have been sampled from what their sampling frequencies mean. Importance sampling corrects contributions for differences between the sampling and target distributions, provided the sampled ensemble adequately covers the target. It cannot recover states absent from the candidates. The reference distribution must therefore be specified before a statistical correction can be interpreted physically.

- [[conformational free-energy landscape]], [[population shift]], [[structural ensemble]].
- [[importance sampling]]: [[importance sampling#^eq-importance-sampling]]; effective sample size (**gap**: no source for the Kish formula).
- [[reference ratio method]]: [[reference ratio method#^eq-reference-ratio]] and its KL optimality [[reference ratio method#^eq-reference-ratio-kl]].
- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

The sampling procedure establishes the reference distribution from which experimental refinement begins. Where the candidates cover the relevant states, measurements can constrain their relative contributions. Where states are absent, adjusting their weights cannot repair the omission.

## 2.3 Integrating Biophysical Data with Structural Ensembles

**Argument.** Experimental integration uses the candidate ensembles described above to formulate structural explanations of the measured uptake. A forward model predicts the observable, while prior information and an error model determine how disagreement with the data changes the inferred ensemble. The constraints can act on the weights of existing conformations or during the generation of new ones. These approaches differ in whether the candidate structures remain fixed during inference.

### The Inverse Problem and Forward Modelling

Forward modelling predicts a measurement from a proposed structure or ensemble. The inverse problem uses that measurement to infer which structural explanations remain plausible. A Bayesian formulation combines the likelihood with prior information and includes uncertain model parameters in the inference, so structural conclusions depend on both the forward model and its treatment of error.

- [[Bayes' theorem]]: [[Bayes' theorem#^eq-bayes]].
- [[inverse problem]]: the posterior over structure and nuisance parameters, [[inverse problem#^eq-isd-posterior]], with the derivation in the note.
- [[forward model]]: likelihood [[forward model#^eq-likelihood]], Gaussian error model [[forward model#^eq-gaussian-error]], ensemble-averaged prediction [[forward model#^eq-ensemble-prediction]].
- [[nuisance parameter]]: marginalisation [[nuisance parameter#^eq-marginal]], hybrid energy as negative log posterior [[nuisance parameter#^eq-hybrid-energy]], data weight [[nuisance parameter#^eq-data-weight]].
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]

### Maximum-Entropy and Bayesian Ensemble Refinement

Because the measurements do not determine a unique population distribution, refinement requires a rule for balancing experimental agreement against prior information. Relative maximum-entropy refinement supplies such a rule by minimising changes from a specified reference ensemble. The change is measured by the Kullback–Leibler divergence, whose direction fixes which distribution is compared with which reference. When observations are uncertain, their error model determines how closely they should be fitted. Minimal modification preserves prior information; it does not establish that the prior is accurate.

- [[maximum entropy principle]]:
  - problem: [[maximum entropy principle#^eq-maxent-problem]];
  - posterior: [[maximum entropy principle#^eq-maxent-posterior]];
  - discrete weights: [[maximum entropy principle#^eq-maxent-weights]];
  - biased potential: [[maximum entropy principle#^eq-maxent-potential]];
  - apparent work: [[maximum entropy principle#^eq-apparent-work]].
- The KL divergence derived from the Lagrangian is steps 1–7 of the MaxEnt derivation.
- [[Kullback–Leibler divergence]]: [[Kullback–Leibler divergence#^eq-kl]] and [[Kullback–Leibler divergence#^eq-kl-weights]]. State the KL direction wherever it is used.
- Reweighting as importance sampling: [[importance sampling]], derivation step 4.
- The SAXS MaxEnt regulariser is the same prior: [[regularisation#^eq-maxent-regulariser]].
- Bayesian equivalence: [[Bayes' theorem]] (derivation steps 1–2).
- [[The MaxEnt reweighting optimisation problem is solved with the method of Lagrange multipliers.]]
- [[Minimising apparent work and KL divergence gives a reweighted ensemble that satisfies the constraints with minimal deviation.]]

### Experimentally Restrained Simulations and Metainference

Reweighting can change the contributions of sampled conformations, but cannot assign population to states absent from the candidates. Applying experimental constraints during simulation allows those constraints to influence the exploration of additional conformations. Replica-averaged restraints act on ensemble predictions, and metainference also infers an effective uncertainty for each datum. The inferred uncertainty controls restraint strength without identifying which source of error dominates.

- The maximum-entropy bias can be applied to fixed frames through reweighting or during simulation through a modified potential ([[maximum entropy principle#^eq-maxent-potential]]). Applying it during sampling allows the simulation to explore additional states.
- [[restrained simulation]] gives the replica restraint [[restrained simulation#^eq-replica-restraint]] and the derivation of its maximum-entropy limit.
  - [[Restraining replica-averaged observables in MD reproduces the maximum-entropy ensemble in the limit of many replicas.]]
  - [[Several groups have restrained simulations or pruned ensembles post hoc with HDX-MS data, mainly for simpler systems.]]
- [[metainference]] gives the energy [[metainference#^eq-metainference-energy]], with a per-datum uncertainty sampled as a [[nuisance parameter]].
  - [[Metainference infers an uncertainty for each datum alongside the structures, so the restraint weakens where data or forward model are unreliable.]]
  - [[Without errors in data or forward model, metainference reduces to replica-averaged maximum-entropy restraints.]]
- Applying an HDX restraint during molecular dynamics requires derivatives of the forward model with respect to atomic coordinates. ValDX identifies the absence of a published HDX collective variable with forces (`8_future_work.tex` L36–40). The project's differentiable formulation belongs in its research chapter.

### Experimental Guidance of Diffusion Models

The structural derivatives needed to calculate restraint forces can also be used to guide a learned generator. In diffusion models, experimental guidance acts during denoising, so the constraints modify the generation of candidate structures. This requires a differentiable forward model and a choice of guidance strength. For ensemble-average measurements such as HDX-MS uptake, the prediction must account for contributions from multiple conformations. Restraining each generated structure to the same measured average imposes a different constraint.

- [[guided diffusion]] gives the guided score [[guided diffusion#^eq-guided-score]], ExEnDiff's restraint approximation [[guided diffusion#^eq-guidance-restraint]] and ConfDiff's energy tilt [[guided diffusion#^eq-energy-tilt]].
  - [[Experimental guidance adds the gradient of a data likelihood to a pretrained diffusion score at sampling time.]]
  - [[Too strong an experimental guidance term makes diffusion sampling noisy and produces unphysical structures.]]
  - [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]] (own)
- Guidance modifies a learned sampling distribution, while experimental restraints modify simulation through a bias potential. ExEnDiff applies its restraint to single structures, whereas HDX-MS data describe ensemble averages. This difference motivates the ensemble treatment developed in the research chapter.
- **gap**. Both papers test small proteins, and ExEnDiff guides only with synthetic observables taken from the MD it is scored against.

Experimental constraints can improve agreement by changing populations, forward-model parameters or the conformations sampled. Agreement alone does not establish which change was warranted. Assessment must therefore examine whether the resulting model predicts withheld measurements and whether its structural conclusions remain supported when the data and modelling assumptions are varied.

## 2.4 Validation, Uncertainty, and Interpretability

**Argument.** Assessing an integrated ensemble requires separating the prediction of experimental observables from the accuracy of the structural interpretation. Measurement uncertainty and forward-model discrepancy determine how agreement should be judged, while dependence between observations determines what a validation partition can test. Even accurate prediction may leave several population distributions consistent with the data. Comparing those alternatives requires representations that make their structural differences explicit.

Grounding concepts (from BMSB): [[posterior uncertainty]]; [[regularisation]], with $\chi^2$ [[regularisation#^eq-chi2]], the regularised objective [[regularisation#^eq-regularised-objective]] and good parameters [[regularisation#^eq-good-parameters]]; model comparison with [[Bayes' theorem#^eq-bayes-factor]].

### Experimental Uncertainty and Forward-Model Discrepancy

Uncertainty in an inferred ensemble can arise from measurement error, an approximate forward model or sensitivity to the data used in fitting. These sources require different assessments. Repeat measurements estimate precision, recalibration tests parameter mismatch, and changes to the forward model test assumptions that coefficient fitting cannot repair. Correlated measurement or prediction errors also determine how residuals should contribute to the fitting objective.

- Three layers run through this subsection and the next: the statistical principle, what integrative practice does with it, and what ValDX and jaxENT add ([[2026-10-14 layered presentation of validation and uncertainty]]). The citation shows the layer. One general source carries a principle, primary papers carry practice, and a manuscript line or figure carries ours.
- The taxonomy in [[experimental uncertainty]] distinguishes six uncertainty quantities by their origin, the changes that affect them and the evidence needed to assess them.
  - [[HDX-MS precision differs between repeat measurements in one laboratory and measurements across laboratories.]]
  - [[Replicate precision bounds only the random part of measurement error, so a precision threshold does not bound systematic bias.]] (own)
  - [[Experimental error estimates are usually lower bounds because they miss systematic errors.]]
  - [[Noise in the data and structural heterogeneity are difficult to tell apart.]]
- Systematic bias and processing. Back-exchange correction with a fully deuterated control ([[deuterium uptake#^eq-uptake-corr]]). Scaling to the last time point leaves the bias in place, the control has its own precision, and residue-level references are derived through the intrinsic rate and EX2 ([[deuterium uptake]]). These stay as concept bullets; promote one to a claim only if a chapter paragraph cites it.
- Parameter uncertainty, miscalibration and an inadequate functional form have different consequences for inference ([[model misspecification]]). Estimating parameter uncertainty describes the range of compatible values, recalibration addresses incorrect coefficients, and an inadequate functional form requires revising the model.
  - [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]]
  - [[Recalibrating forward-model coefficients can correct a miscalibration but not an inadequate functional form.]] (own; the kinetic benchmark is revised ValDX only)
  - [[Averaging log protection factors, exchange rates or uptake over frames are different forward models, and held-out uptake error and population recovery can favour different choices.]] (jaxENT, draft)
- What inferring the error scale resolves and what it does not ([[metainference]], [[nuisance parameter]]).
  - [[Metainference folds experimental, systematic, forward-model and finite-replica errors into one effective uncertainty per datum, so the inferred value does not say which source dominates.]] (own)
- Posterior uncertainty against partition sensitivity ([[posterior uncertainty]], [[replicate uncertainty]]).
  - [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]]
- A product likelihood assumes independent errors. Peptide overlap can correlate prediction errors, so an appropriate [[error covariance]] is needed to weight their residuals jointly.
  - [[Weighting residuals by the inverse error covariance corrects least squares for unequal variances and correlated errors.]] (stated by Theobald for superposition)
  - [[Correlations between overlapping peptides are recognised in HDX-MS statistics but left unmodelled.]]
  - [[A covariance built from candidate-ensemble coordinates describes how peptides are expected to co-vary structurally, so weighting residuals by it assumes their errors co-vary in the same way.]] (jaxENT, draft, inferred)
- **decision**. jaxENT's Σ is presented as the current policy, the geometric selection-time weighting in [[Observation weighting and selection (jaxENT)]], and the manuscript's fitted covariance-weighted MSE as history. The ISO closed-label circularity and the validation block used are stated with any number quoted.
- Wording to avoid. "Accounts for experimental uncertainty and correlations between fragments" (jaxENT `methods/analysis.tex` L31) until Σ does; "robust success metrics" and "guards against overfitting" (`results.tex` L13); the Fig. 5 caption on sampling against force-field limitations (`results.tex` L203); "systematic errors accumulate at the peptide level" (confirmation, unsupported).

### Cross-Validation with Overlapping Measurements

An error model determines how discrepancies contribute to fitting, but does not establish prediction beyond the fitted data. Cross-validation tests that prediction, provided the partition accounts for information shared between observations. Overlapping HDX-MS peptides share residue information, while cooperative opening can couple exchange even between non-overlapping peptides. Structured partitions reduce dependence without guaranteeing independence. The withheld unit determines the predictive question, and data used to select a model cannot also provide an unbiased assessment of that selection.

- The partition should reflect dependence between observations ([[data splitting]]). Otherwise, information shared with the training data can make held-out error optimistic.
  - [[When observations are dependent, a random partition gives optimistic validation error, so the partition should follow the dependence.]]
  - [[Repeating a random split reduces dependence on one partition but not the leakage within each partition.]] (own)
- HDX dependence has two routes, one direct and one physical.
  - [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]]
  - [[Native proteins contain cooperative unfolding units smaller than the whole protein, which hydrogen exchange can identify.]] ([[cooperative unfolding unit]])
  - [[Cooperative unfolding couples exchange at residues that share no peptide, so removing peptide overlap does not make training and validation peptides independent.]] (own)
  - [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]]
- The unit withheld decides the question asked (table in [[data splitting]]). [[BPTI]] is the contrast case: residue-level data without peptide overlap, still correlated through shared openings.
  - [[Withholding a time point, a peptide, a sequence region or a structural region asks different predictive questions.]] (own)
- Field practice, credited then bounded ([[model selection]] for the free R value; [[data splitting]], "In integrative practice"). Skinner et al. 2019 show from the data side why splits interact with information content; coverage, overlap and peptide length decide how far residue protection factors are determined ([[HDX protection-factor model]]).
  - [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]]
  - [[In the HDX ensemble-integration studies examined, robustness is assessed by removing selected peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions designed around peptide dependence.]] (own)
- Our partitions, replicates, consensus and selection ([[Peptide splitting and consensus (ValDX)]]).
  - [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]]
  - [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]]
  - [[Averaging models fitted to different subsets of the data reduces variance due to data selection, most for unstable fitting procedures.]] ([[model averaging]])
  - [[Averaging fitted models reduces their variance but retains any error they share.]] (own)
  - [[Averaging frame weights across fits averages their predicted log protection factors only while forward-model coefficients are held fixed.]] (step ours)
  - [[Averaging reweighting fits across split replicates stabilises the consensus and reduces overfitting to particular peptide subsets.]] (needs a figure)
  - [[A consensus over split replicates does not by itself make the candidate ensemble representative.]]
  - [[Selecting a model by its validation error makes that error optimistic, so performance must be estimated on data unused in selection.]]
- jaxENT's complement: selection on HDX-MS validation with evaluation against the reference ([[Evaluation design (jaxENT)]]), and weighting instead of partitioning for the dependence that structured splits leave behind.
  - [[Weighting validation residuals by the conditional precision given the training peptides discounts held-out peptides whose information is redundant with the training set.]] (jaxENT, draft, inferred; holds for the conditional selector only)
- **decision**. The HDX-NMR layer is described as "selection on HDX-MS validation and evaluation against HDX-NMR, nested in structure with a single outer evaluation". "Nested cross-validation" is kept for a resampled outer loop.
- **decision**. The jaxENT splitter's overlap behaviour is flagged in [[Evaluation design (jaxENT)]] and not changed in this pass.
- Validation tests prediction of uptake and stability under partitioning. Establishing whether the populations are unique is a separate question of [[identifiability]].
- Wording to avoid. "Ensure" and "genuinely withheld" (posted v1); "powerful diagnostic tool" (`7_results_omc.tex` L55); "statistically rigorous framework" (`1_introduction_omc.tex` L33); "selected by test error minimisation" (jaxENT `protocols.tex` L325, legacy); "integrative biophysics never splits data".

### Identifiability and Competing Structural Hypotheses

Accurate prediction of withheld uptake does not establish that only one population distribution could have produced it. Identifiability concerns whether the observations distinguish that distribution from competing structural explanations. For HDX-MS, ambiguity can arise both when inferring residue protection from peptide uptake and when inferring populations from protection. Better coverage and lower noise can reduce practical ambiguity, but structurally non-identifiable populations remain indistinguishable even with ideal data and a perfect forward model. Validation can support a comparison between hypotheses without establishing a unique population distribution.

- [[identifiability]] distinguishes structural non-identifiability from practical ambiguity due to coverage, noise and model discrepancy. The [[inverse problem]] note gives the general formulation, with Berlin et al. 2013 for the count argument and Bonomi et al. 2017 for ensembles that fit the same averages.
  - [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]]
  - [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]]
- Two levels of ambiguity. Uptake may not fix residue protection factors (Skinner et al. 2019, depending on peptide number, overlap and length), and protection factors may not fix populations. Say which level a result addresses.
- Distinguishability. Hypotheses can be told apart only where their predicted observables differ by more than measurement and model error. An orthogonal measurement earns its place by constraining what uptake leaves open.
  - [[Two structural hypotheses can be distinguished only where their predicted observables differ by more than measurement and model error.]] (own)
- References of decreasing certainty. A synthetic benchmark has exact populations (TeaA). An experimental reference such as the HDX-NMR-derived MoPrP target depends on its own state assignments and thermodynamic assumptions. A system with no structural reference allows only prediction and stability to be assessed (α-synuclein).
- Validation answers narrower questions. Held-out error tests prediction, replicate spread tests sensitivity, and [[controlled perturbation]] tests attribution. None of them shows that the populations are unique.
- Ranking rather than identifying. [[BICePs]] ranks candidate priors by an evidence ratio while inferring the error scale. ValDX instead asks whether a fit generalises and how much it changed the prior.
  - [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]]
  - [[BICePs ranks candidate priors by an evidence ratio while inferring the experimental uncertainty as a nuisance parameter.]]
- When several ensembles remain consistent with the data, structural representations make their differences explicit and allow the competing interpretations to be inspected.

### Ensemble Comparison and Interpretable Representations

When several ensembles remain consistent with the observations, their structural differences must be examined directly. Distributional comparisons and representative structures make those differences explicit, while defining the resolution at which the alternatives are assessed. Coordinate fluctuations, pair-distance distributions and populations of structural clusters each describe a different aspect of that comparison. A representation determines which differences are retained and which are averaged away, so conclusions should be checked across appropriate resolutions. Equilibrium similarity does not establish similarity of transition rates or pathways.

- [[ensemble comparison]] gives the Jensen–Shannon divergence [[ensemble comparison#^eq-jsd]], built from [[Kullback–Leibler divergence#^eq-kl]].
  - [[Comparing ensembles requires comparing probability distributions over conformations, not single-structure RMSD.]]
  - [[The Jensen–Shannon divergence is a symmetric, bounded measure of ensemble similarity that stays defined where one ensemble has no density.]]
  - [[Dimensionality reduction by PCA or MDS assumes a linear conformational space.]]
  - [[Ensemble similarity scores compare equilibrium distributions and do not capture changes in dynamics or transition rates.]]
- Structural distributions. [[positional covariance]] gives RMSF and dynamic cross-correlation, and [[Wasserstein distance]] compares whole distributions in the units of the variable. ValDX's residue-averaged pair-distance $W_1$ and neighbourhood LCC are its own constructions ([[Structural comparison metrics (ValDX)]]).
  - [[Superposition can introduce artefactual correlations into atomic covariance estimates.]]
  - [[Linear displacement correlation misses non-linear and perpendicular coupled motions.]]
  - [[Agreement of per-residue pair-distance distributions does not establish that two ensembles share the same joint conformational distribution.]] (own)
- Populations. JSD between state populations, with the log base stated. jaxENT's recovery score needs base 2 ([[Ground-truth recovery (jaxENT)]]).
- [[Work Done]] quantifies changes in the predicted protection profile during fitting, while apparent work quantifies changes in the ensemble weights through the [[Kullback–Leibler divergence]]. High Work Done indicates substantial modification but does not by itself identify overfitting. Full equations belong in Chapter 3 ([[Work Done (ValDX)]]).
  - [[Distinct protection profiles can give zero Work Done, so Work Done is not a distance between profiles.]] (own)
- Compact representations. [[clustering]] covers representatives and resolution. Rule-based states (jaxENT MoPrP) and shape-space GMM clusters (jaxENT α-synuclein) are also chosen resolutions, so conclusions should be checked across them.
  - [[Clustering sets the resolution of an ensemble comparison and ignores differences within clusters and similarities across them.]]
  - [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]]
  - [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]]
- Weighted ensembles describe state populations, while transition rates and pathways require evidence about [[conformational kinetics]]. Under EX2, exchange reports on the fraction of time an amide is open through the intrinsic exchange rate; it does not determine the opening rate.
  - [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]] (own)
- **gap**. No citable source yet for the general $W_1$ definition (SciPy documentation only). jaxENT's ternary shape space and GMM clustering are manuscript-only.

These assessments remain conditional on the physical and chemical conditions represented by the model. In pH-dependent applications, those conditions affect both intrinsic exchange chemistry and the protonation states that govern structural interactions. Interpreting a difference in uptake therefore requires considering changes in the exchange rates as well as changes in the conformational ensemble.

## 2.5 Protein Protonation and pH-Dependent Properties

**Argument.** The intrinsic-rate model in §2.1 accounts for the chemical effect of solution acidity on amide exchange. Changes in protonation can also alter the conformational populations being measured, because they change the interactions that stabilise each state. This distinction matters for [[prion protein|MoPrP]], whose HDX-MS data for partially unfolded forms were measured at pD 4 ([[@moulickPartiallyUnfoldedForms2015]]) and whose simulations in Chapter 5 are compared at pH 4 and pH 7. Interpreting these conditions requires both an appropriate exchange model and protonation assignments that reflect the structural environment.

**Section structure.** Two to three pages, using MoPrP as the example. The computational titration models (PROPKA, PypKa, constant-pH MD, pKAI, KaML) are introduced in the Chapter 6 preface ([[06-jax-ka]]).

### Acid–Base Equilibria and Protein Charge

The pKa of a titratable group determines how its protonated fraction changes with solution pH. Changes in protonation alter protein charge, and differences in pKa between conformational or binding states make their equilibrium pH-dependent. These relationships connect acid–base chemistry to stability and binding, while the intrinsic exchange rates in §2.1 account for the separate effect of pH on HDX chemistry.

- [[pKa]] defines the Henderson–Hasselbalch protonated fraction [[pKa#^eq-hh]] and net charge [[pKa#^eq-net-charge]], with model-compound values from alanine pentapeptides.
- MoPrP framing. Lowering the pH from 7 to 4 crosses the model pKa of His and approaches those of Asp and Glu.
  - [[Between pH 7 and pH 4, His side chains become protonated and Asp and Glu partly protonated, so a protein's net charge becomes more positive.]] (own)
- Linkage, which is why charge changes alter stability and binding.
  - [[A group whose pKa differs between two states makes the equilibrium between those states pH-dependent.]]
- The prion protein at acidic pH, one paragraph. Use mouse numbering (H186 = human H187).
  - [[Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH, and urea is needed to populate it substantially.]]
  - [[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]]
  - Optional: MoPrP folds and unfolds by one pathway at pH 7 and by distinct pathways at pH 4 ([[@moulickRuggednessFreeEnergy2019#^c1]]); Malevanets et al. 2017 for a buried His pKa near 5 ([[@malevanetsInterplayBuriedHistidine2017]]).
- HDX link, pointing back to §2.1 rather than repeating it ([[intrinsic exchange rate#^eq-pd]] for pD; ionisable neighbours in the same note).
  - [[His, Asp and Glu neighbours change intrinsic exchange rates with pH through their own ionisation.]]
- **decision** (recommended, applied in the KB): the pD correction and the ionisable-neighbour factors are stated in §2.1 Intrinsic Exchange Rates, and §2.5 points back.

### Structural Influences on pKa

Applying these acid–base relationships requires pKa values appropriate to the protein environment. Model-compound values provide a reference, but burial, hydrogen bonding and neighbouring charges can change the relative stability of protonation states. Most measured protein pKa values remain close to those reference values, but buried or interacting groups can differ substantially. Protonation assignments for a simulation must therefore consider both solution pH and the structural environment of each titratable site.

- [[pKa shift]], with PROPKA's decomposition as the one light equation [[pKa shift#^eq-propka]]. The equation is vocabulary for the determinants; PROPKA as a method is in the ch. 6 preface.
  - [[Most measured pKa values in folded proteins lie close to model-compound values, and large shifts occur for buried or interacting groups.]]
- Consequence for simulation.
  - [[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]]
  - [[Constant-pH MD of human PrP at low pH populates a β-rich form in which His187 protonation separates the subdomains.]] (optional; the β-rich form was at pH 2)
- Chapter 6 addresses the protonation assignments required for the pH-dependent applications.
  - [[Our candidate ensembles were protonated once at pH 7 or 7.4, so a pH 4 ensemble depends on protonation states that were not assigned for pH 4.]] (own)
- Optional, cut first if space is short: coupled sites and titration that does not follow Henderson–Hasselbalch (Onufriev, Case & Ullmann 2001; Ullmann 2003; not seeded).

## Gaps (Chapter 2 literature)
- Removed (2026-10-15): the claim that structure-to-uptake models rely on hydrogen bonding and solvent exposure but add systematic errors that accumulate at peptide level. No checked passage evaluated those models or their errors. A source is needed if §2.1 keeps the point.
- §2.5 and ch. 6 papers all have PDFs and blocks. Yang & Honig 1993 and Hvidt 1954 are OCR text, so check their quotes against the page.
- ValDX `2_hdx_theory_omc.tex` L7 cites Kim, Fuchs & Woodward 1993 for "the protection factor reports on the free energy of local unfolding"; Kim does not say this (no protection factors, no EX2). Cite Vendruscolo et al. 2003 (^c2) instead.
- `vendruscoloRareFluctuationsNative2003` has two Zotero duplicates (`…2003a`, `…2003b`); merge them.
- `baiPrimaryStructureEffects1993` is duplicated in Zotero (two items, one key); merge them.
- ValDX `2_hdx_theory_omc.tex` L5 cites Nguyen 2018 as the webpage snapshot `ReferenceParametersProtein`; re-key to `nguyenReferenceParametersProtein2018` when adapting into ch. 3 and retire `kb/papers/@ReferenceParametersProtein.md`.
- The jaxENT SI (`si_figures.tex` L225) cites `wuConformationalHeterogeneitySavinase2020` for "Nguyen et al." reference parameters; the correct paper is Nguyen, Mayne, Phillips & Englander 2018 (JASMS 29:1936).
- No published pH 4 against pH 7 simulation of mouse PrP was found (human and bovine only), so the Chapter 5 MoPrP runs would be the first mouse-specific comparison. Check again before claiming it.
- A statistical-learning source for bagging (Hastie, Tibshirani and Friedman §8.7, or Breiman 1996); two draft claims on [[model averaging]] wait on it. Optional: Maity 2005 for the foldon term, MDRefine and DynaXL as held-out-restraint comparators.
- A figure or notebook ID comparing the ValDX consensus with single-replicate fits; without it the consensus claim stays draft.
- jaxENT: record which validation block the reported selections used, the provenance of `moprp.weights`, and the splitter's overlap behaviour; update the manuscript's covariance and selection wording to the current policy ([[Observation weighting and selection (jaxENT)]], [[Evaluation design (jaxENT)]]).
- The ValDX submodule is pinned to `origin/GSD-stats-HPC` at 0b79aad, which has the Non-Redundant and Spatial split code and the consensus mean. Settle the median against mean for the BV constants and the peptide dropout wording before Chapter 3 cites the note ([[Peptide splitting and consensus (ValDX)]]).
- Hudgens 2019, Crook 2022, Moulick 2015 and Burnley 2012 are seeded with PDFs; all `read: false`, all quotes `reviewed: false`.
- Add to Zotero the two hand-added bib entries, `lindorff-larsenSimilarityMeasuresProtein2009` and `tibertiENCORESoftwareQuantitative2015`. Otherwise the next Better BibTeX export drops them.
- Radou et al. 2014 is needed for the switch-function BV model. Add it to Zotero or `kb/_pdf/`.
- The original metainference paper (Bonomi et al. 2016, Sci Adv) is not in the library. Bonomi 2016 Sci Rep and the 2017 review carry the definition for now.
- All new paper notes are `read: false`, and all quotes are `reviewed: false`.
- BICePs v2.0 (Raddi, Ge & Voelz 2023) is in Zotero as `raddiBICePsV20Software2023c`, because trashed copies hold the base key. Empty the trash and refresh the key, then seed it. Raddi et al. 2025 (forward-model learning) is seeded.
- A citable source for the Wasserstein-1 definition, if the chapter needs more than the SciPy documentation.
- jaxENT `methods/analysis.tex` L10 should state that JSD is in base 2. Its MoPrP caption (`results.tex` L82) says "ground-truth MoPrP populations" for an HDX-NMR-derived reference.
- ValDX structural metrics. The SI $W_1$ equation does not match the implementation, and the correlation code does not align frames itself ([[Structural comparison metrics (ValDX)]]).
- Chapter 3 must define the Work metrics, HDXer apparent work and the BICePs score side by side (`thesis/chapters/03-valdx.tex` L9).
