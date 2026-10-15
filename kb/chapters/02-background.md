# 02 Background and Literature Review

Chapter hub: concepts and their equations in the order of `thesis/chapters/02-background.tex`. Equation links point at single displayed equations (`#^eq-…`). Every symbol follows [[2026-10-13 canonical HDX and ensemble notation]]; `notation.md` lists them.

Markers:
- **gap**: something the chapter needs that has no verified source or manuscript form yet.
- **decision**: a choice to make before writing.

## 2.1 HDX-MS: Measurement, Exchange Kinetics, and Structural Interpretation

Introductory equations: [[protection factor#^eq-pf]] and [[deuterium uptake#^eq-uptake-residue]].

### Experimental Workflow and Measurement Limitations
- [[deuterium uptake]]: peptide averaging [[deuterium uptake#^eq-uptake-peptide]] and back-exchange correction [[deuterium uptake#^eq-uptake-corr]].
- **decision**: present back-exchange as an equation or in prose. It is commented out in the current jaxENT methods.
- [[HDX-MS reports deuterium uptake at the peptide level, not the residue level.]]

### Intrinsic Exchange Rates
- [[intrinsic exchange rate]]: [[intrinsic exchange rate#^eq-kint]], [[intrinsic exchange rate#^eq-kint-sequence]], [[intrinsic exchange rate#^eq-kint-temperature]].
- **gap**: no manuscript applies Bai's temperature correction. Bai's Eqs. (2a) and (3) are images and need checking against the PDF.

### Linderstrøm–Lang Exchange Kinetics and EX1/EX2 Regimes
- [[Linderstrøm–Lang model]]: scheme [[Linderstrøm–Lang model#^eq-ll-scheme]], steady state [[Linderstrøm–Lang model#^eq-ll-kobs]], limits [[Linderstrøm–Lang model#^eq-ex2]] and [[Linderstrøm–Lang model#^eq-ex1]], with the derivation in the note.
- Distinguish exchange kinetics from conformational timescales: [[protein dynamics]].
- **gap**: no PDF for Hvidt and Nielsen 1966 or Smith 1997. Skinner 2012 and Englander 1997 carry the sources for now.

### Protection Factors and Peptide Uptake
- [[protection factor]]: [[protection factor#^eq-pf]] and [[protection factor#^eq-dgop]] (EX2 free energy, with derivation).
- [[deuterium uptake]]: [[deuterium uptake#^eq-uptake-residue]] → [[deuterium uptake#^eq-uptake-peptide]].
- [[Predicted protection factors are transformed into theoretical deuterium uptake for direct comparison with HDX-MS data.]]

### Structural Forward Models for HDX
- [[Best–Vendruscolo model]]: [[Best–Vendruscolo model#^eq-bv-feature]] and [[Best–Vendruscolo model#^eq-bv-ensemble]].
- [[The Best-Vendruscolo model predicts protection factors from coordinates by counting structural features that impede exchange.]]
- [[Structure-to-uptake models rely on hydrogen bonding and solvent exposure but add systematic errors that accumulate at peptide level.]]
- [[HDX protection-factor model]] gives the alternatives and their shared assumptions (EX2, independent residues, calibration to conditions). It has no equation of its own, because BV carries the displayed form.
- Order the subsection from what structure predicts to what data can determine. Structure-based models predict a protection factor per residue. Peptide data generally cannot recover those values, which is why the thesis compares at the uptake level.
  - [[Residue protection factors are generally underdetermined by peptide-level uptake.]] (supported)
  - [[A single protection factor per residue cannot describe a residue whose environment differs between populated conformers.]] (supported)
  - [[Residue protection factors test structural models more stringently than peptide uptake alone.]] (supported)
- **gap**. The switch-function variant needs Radou et al. 2014 (Biophys J 107, 983–990), which could not be downloaded. Park 2015's PDF is unreadable.
- **decision**. ValDX `6_methods_omc.tex` L624 cites Skinner 2019 for the switch-function BV model. Skinner 2019 describes no such model and cites Radou 2014, so the manuscript citation should change.

## 2.2 Protein Conformational Ensembles and Their Generation

### Molecular Dynamics and Empirical Force Fields
- [[molecular dynamics]]: [[molecular dynamics#^eq-newton]] (very light).
- [[Boltzmann distribution]]: [[Boltzmann distribution#^eq-boltzmann]].
- **gap**: a displayed-equation source for Newton's or Langevin's equation.
- [[force field]] potential energy $U(x)$ as a score for one conformation. A low energy flags a plausible structure under the model, not a populated state, because population depends on the free energy of the whole basin.

### Enhanced Sampling
- [[Markov chain Monte Carlo]]: detailed balance [[Markov chain Monte Carlo#^eq-detailed-balance]] and Metropolis–Hastings [[Markov chain Monte Carlo#^eq-metropolis-hastings]], if the chapter needs them. Extended ensembles and reweighting back to the target are in the note's limits.
- Claims: [[Metadynamics enhances sampling by adding a history-dependent biasing potential to the system's energy landscape.]]

### Learned Structure Predictors and Ensemble Generators
- Very light equation. [[statistical potential#^eq-statistical-potential]] writes any model density as an energy. This answers the `.tex` stub "Discuss statistical potentials" (L41).
- [[statistical potential]] is the general idea, and [[knowledge-based potential]] is its database-count case ([[knowledge-based potential#^eq-inverse-boltzmann]]). Such an energy is a statistical quantity unless its density is the physical equilibrium one. AF2 exposes no normalised density, so ValDX's "AF2 generates structures according to a statistical potential" is an analogy.
- [[protein structure predictor]] is trained for one PDB-like structure and reports accuracy, not population.
  - [[Structure predictors are trained to return the single structure most likely to appear in the PDB.]] (supported)
  - [[A structure predictor's confidence score measures expected accuracy, not the free energy or population of a conformation.]] (supported)
  - [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]] (supported)
- [[MSA subsampling]] turns a predictor into a source of candidates. Present the population evidence as qualitative and the mechanism as contested.
  - [[Subsampled AlphaFold2 can predict the direction of population shifts qualitatively, but quantitative Boltzmann ratios have not been shown.]] (supported)
  - [[Frequencies of states in MSA-clustered AlphaFold2 predictions reflect family abundance, not Boltzmann weights.]] (supported)
  - [[Whether MSA clustering recovers alternative states through evolutionary couplings is contested.]] (supported)
  - Do not reuse [[MSA-subsampling has been shown to broadly follow a physical energy landscape.]] (partial) as worded.

### Diffusion Models for Protein Structure Generation
- [[diffusion model]]: [[diffusion model#^eq-diffusion-forward]] and [[diffusion model#^eq-diffusion-reverse]]. The link back to MD (Boltzmann score = force / $k_BT$) is in the note's derivation.
- [[Diffusion models trained on PDB structures learn a distribution concentrated on folded, low-energy states rather than the equilibrium distribution.]] (supported)

### Sampling Coverage and Ensemble Populations
- [[conformational free-energy landscape]], [[population shift]], [[structural ensemble]].
- [[importance sampling]]: [[importance sampling#^eq-importance-sampling]]; effective sample size (**gap**: no source for the Kish formula).
- [[reference ratio method]]: [[reference ratio method#^eq-reference-ratio]] and its KL optimality [[reference ratio method#^eq-reference-ratio-kl]].
- [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]]
- [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

## 2.3 Integrating Biophysical Data with Structural Ensembles

### The Inverse Problem and Forward Modelling
- [[Bayes' theorem]]: [[Bayes' theorem#^eq-bayes]].
- [[inverse problem]]: the posterior over structure and nuisance parameters, [[inverse problem#^eq-isd-posterior]], with the derivation in the note.
- [[forward model]]: likelihood [[forward model#^eq-likelihood]], Gaussian error model [[forward model#^eq-gaussian-error]], ensemble-averaged prediction [[forward model#^eq-ensemble-prediction]].
- [[nuisance parameter]]: marginalisation [[nuisance parameter#^eq-marginal]], hybrid energy as negative log posterior [[nuisance parameter#^eq-hybrid-energy]], data weight [[nuisance parameter#^eq-data-weight]].
- [[Many ensembles can explain the same data, given complex conformational landscapes and simple structure-experiment models.]]

### Maximum-Entropy and Bayesian Ensemble Refinement
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
- Open from the tilted landscape ([[maximum entropy principle#^eq-maxent-potential]]). Reweighting applies the tilt to fixed frames, and a restrained simulation applies it while sampling, so it can reach states the prior lacked.
- [[restrained simulation]] gives the replica restraint [[restrained simulation#^eq-replica-restraint]] and the derivation of its maximum-entropy limit.
  - [[Restraining replica-averaged observables in MD reproduces the maximum-entropy ensemble in the limit of many replicas.]] (supported)
  - [[Several groups have restrained simulations or pruned ensembles post hoc with HDX-MS data, mainly for simpler systems.]] (supported)
- [[metainference]] gives the energy [[metainference#^eq-metainference-energy]], with a per-datum uncertainty sampled as a [[nuisance parameter]].
  - [[Metainference infers an uncertainty for each datum alongside the structures, so the restraint weakens where data or forward model are unreliable.]] (supported)
  - [[Without errors in data or forward model, metainference reduces to replica-averaged maximum-entropy restraints.]] (supported)
- End on what HDX lacks. Every restraint needs a forward model with forces, and no HDX collective variable is published (ValDX `8_future_work.tex` L36–40). The project's differentiable formulation stays in its research chapter.

### Experimental Guidance of Diffusion Models
- [[guided diffusion]] gives the guided score [[guided diffusion#^eq-guided-score]], ExEnDiff's restraint approximation [[guided diffusion#^eq-guidance-restraint]] and ConfDiff's energy tilt [[guided diffusion#^eq-energy-tilt]].
  - [[Experimental guidance adds the gradient of a data likelihood to a pretrained diffusion score at sampling time.]] (supported)
  - [[Too strong an experimental guidance term makes diffusion sampling noisy and produces unphysical structures.]] (supported)
  - [[Guided diffusion samples are not equilibrium-weighted unless a correction such as reweighting is applied.]] (draft, inferred)
- Set guidance beside the restraint, since both add a bias to a prior. ExEnDiff restrains single structures, while HDX data are ensemble averages. That mismatch motivates the project's approach without describing it here.
- **gap**. Both papers test small proteins, and ExEnDiff guides only with synthetic observables taken from the MD it is scored against.

## 2.4 Validation, Uncertainty, and Interpretability

Grounding concepts (from BMSB): [[posterior uncertainty]]; [[regularisation]], with $\chi^2$ [[regularisation#^eq-chi2]], the regularised objective [[regularisation#^eq-regularised-objective]] and good parameters [[regularisation#^eq-good-parameters]]; model comparison with [[Bayes' theorem#^eq-bayes-factor]].

### Experimental Uncertainty and Forward-Model Discrepancy
- Three layers run through this subsection and the next: the statistical principle, what integrative practice does with it, and what ValDX and jaxENT add ([[2026-10-14 layered presentation of validation and uncertainty]]). The citation shows the layer. One general source carries a principle, primary papers carry practice, and a manuscript line or figure carries ours.
- Open on the taxonomy in [[experimental uncertainty]]. Six quantities are called uncertainty; the table says what moves each, what reduces it and what does not.
  - [[HDX-MS precision differs between repeat measurements in one laboratory and measurements across laboratories.]] (supported)
  - [[Replicate precision bounds only the random part of measurement error, so a precision threshold does not bound systematic bias.]] (draft, inferred)
  - [[Experimental error estimates are usually lower bounds because they miss systematic errors.]] (supported)
  - [[Noise in the data and structural heterogeneity are difficult to tell apart.]] (supported)
- Systematic bias and processing. Back-exchange correction with a fully deuterated control ([[deuterium uptake#^eq-uptake-corr]]). Scaling to the last time point leaves the bias in place, the control has its own precision, and residue-level references are derived through the intrinsic rate and EX2 ([[deuterium uptake]]). These stay as concept bullets; promote one to a claim only if a chapter paragraph cites it.
- Forward-model discrepancy, in three failures that are easily conflated ([[model misspecification]]): parameter uncertainty, miscalibration and an inadequate functional form. The failure that is operating decides the advice.
  - [[Best–Vendruscolo coefficients are empirical, and their optimal values depend on the protein and experimental conditions.]] (supported)
  - [[Recalibrating forward-model coefficients can correct a miscalibration but not an inadequate functional form.]] (draft, inferred; the kinetic benchmark is revised ValDX only)
  - [[Averaging log protection factors, exchange rates or uptake over frames are different forward models, and held-out uptake error and population recovery can favour different choices.]] (jaxENT, draft)
- What inferring the error scale resolves and what it does not ([[metainference]], [[nuisance parameter]]).
  - [[Metainference folds experimental, systematic, forward-model and finite-replica errors into one effective uncertainty per datum, so the inferred value does not say which source dominates.]] (draft, inferred)
- Posterior uncertainty against partition sensitivity ([[posterior uncertainty]], [[replicate uncertainty]]).
  - [[Split replicates measure sensitivity to peptide partitioning, not independent replication of the measurement.]] (revised ValDX only)
- Hand off to [[error covariance]]. The product likelihood assumes independent errors, overlap breaks the assumption at the prediction level, and the correction is inverse-covariance weighting.
  - [[Weighting residuals by the inverse error covariance corrects least squares for unequal variances and correlated errors.]] (supported; stated by Theobald for superposition)
  - [[Correlations between overlapping peptides are recognised in HDX-MS statistics but left unmodelled.]] (supported)
  - [[A covariance built from candidate-ensemble coordinates describes how peptides are expected to co-vary structurally, so weighting residuals by it assumes their errors co-vary in the same way.]] (jaxENT, draft, inferred)
- **decision**. jaxENT's Σ is presented as the current policy, the geometric selection-time weighting in [[Observation weighting and selection (jaxENT)]], and the manuscript's fitted covariance-weighted MSE as history. The ISO closed-label circularity and the validation block used are stated with any number quoted.
- Wording to avoid. "Accounts for experimental uncertainty and correlations between fragments" (jaxENT `methods/analysis.tex` L31) until Σ does; "robust success metrics" and "guards against overfitting" (`results.tex` L13); the Fig. 5 caption on sampling against force-field limitations (`results.tex` L203); "systematic errors accumulate at the peptide level" (confirmation, unsupported).

### Cross-Validation with Overlapping Measurements
- The principle first ([[data splitting]]). Held-out error is informative only when the withheld unit is not predictable from the retained data, so the partition has to follow the dependence.
  - [[When observations are dependent, a random partition gives optimistic validation error, so the partition should follow the dependence.]] (draft until the general source is seeded)
  - [[Repeating a random split reduces dependence on one partition but not the leakage within each partition.]] (draft, inferred)
- HDX dependence has two routes, one direct and one physical.
  - [[Overlapping peptides share residue information, so random splits leak information between training and validation sets.]] (supported)
  - [[Native proteins contain cooperative unfolding units smaller than the whole protein, which hydrogen exchange can identify.]] (supported; [[cooperative unfolding unit]])
  - [[Cooperative unfolding couples exchange at residues that share no peptide, so removing peptide overlap does not make training and validation peptides independent.]] (draft, inferred)
  - [[Structured splits reduce dependence between training and validation peptides but do not guarantee independence.]] (revised ValDX only)
- The unit withheld decides the question asked (table in [[data splitting]]). [[BPTI]] is the contrast case: residue-level data without peptide overlap, still correlated through shared openings.
  - [[Withholding a time point, a peptide, a sequence region or a structural region asks different predictive questions.]] (draft, inferred)
- Field practice, credited then bounded ([[model selection]] for the free R value; [[data splitting]], "In integrative practice"). Skinner et al. 2019 show from the data side why splits interact with information content; coverage, overlap and peptide length decide how far residue protection factors are determined ([[HDX protection-factor model]]).
  - [[A large change in the inferred ensemble when part of the data is removed signals poor accuracy.]] (supported)
  - [[In the HDX ensemble-integration studies examined, robustness is assessed by removing selected peptides, refitting forward-model parameters or comparing with orthogonal data, not by partitions designed around peptide dependence.]] (draft, inferred)
- Our partitions, replicates, consensus and selection ([[Peptide splitting and consensus (ValDX)]]).
  - [[Random and sequential splits gave no discrimination between candidate ensembles beyond training error.]] (supported)
  - [[Fitting outcomes depend on which peptides and time points are used, and replicate fits quantify this dependence.]] (supported)
  - [[Averaging models fitted to different subsets of the data reduces variance due to data selection, most for unstable fitting procedures.]] (draft until the general source is seeded; [[model averaging]])
  - [[Averaging fitted models reduces their variance but retains any error they share.]] (draft, inferred)
  - [[Averaging frame weights across fits averages their predicted log protection factors only while forward-model coefficients are held fixed.]] (draft, step ours)
  - [[Averaging reweighting fits across split replicates stabilises the consensus and reduces overfitting to particular peptide subsets.]] (revised ValDX only; needs a figure)
  - [[A consensus over split replicates does not by itself make the candidate ensemble representative.]] (revised ValDX only)
  - [[Selecting a model by its validation error makes that error optimistic, so performance must be estimated on data unused in selection.]] (draft until the general source is seeded)
- jaxENT's complement: selection on HDX-MS validation with evaluation against the reference ([[Evaluation design (jaxENT)]]), and weighting instead of partitioning for the dependence that structured splits leave behind.
  - [[Weighting validation residuals by the conditional precision given the training peptides discounts held-out peptides whose information is redundant with the training set.]] (jaxENT, draft, inferred; holds for the conditional selector only)
- **decision**. The HDX-NMR layer is described as "selection on HDX-MS validation and evaluation against HDX-NMR, nested in structure with a single outer evaluation". "Nested cross-validation" is kept for a resampled outer loop.
- **decision**. The jaxENT splitter's overlap behaviour is flagged in [[Evaluation design (jaxENT)]] and not changed in this pass.
- Close on the limit. Validation tests prediction of uptake and stability under partitioning; it does not show that the populations are unique, which is the next subsection ([[identifiability]]).
- Wording to avoid. "Ensure" and "genuinely withheld" (posted v1); "powerful diagnostic tool" (`7_results_omc.tex` L55); "statistically rigorous framework" (`1_introduction_omc.tex` L33); "selected by test error minimisation" (jaxENT `protocols.tex` L325, legacy); "integrative biophysics never splits data".

### Identifiability and Competing Structural Hypotheses
- Open with [[identifiability]]. Structural non-identifiability holds even with ideal data and a perfect forward model. Practical ambiguity comes from coverage, noise and model discrepancy, and better data can reduce it. [[inverse problem]] holds the general frame, with Berlin et al. 2013 for the count argument and Bonomi et al. 2017 for ensembles that fit the same averages.
  - [[One uptake curve can arise from many different conformational populations, so a good fit does not identify the ensemble.]] (supported)
  - [[Similar uptake agreement can coexist with different population recovery, so training error cannot verify populations.]] (supported)
- Two levels of ambiguity. Uptake may not fix residue protection factors (Skinner et al. 2019, depending on peptide number, overlap and length), and protection factors may not fix populations. Say which level a result addresses.
- Distinguishability. Hypotheses can be told apart only where their predicted observables differ by more than measurement and model error. An orthogonal measurement earns its place by constraining what uptake leaves open.
  - [[Two structural hypotheses can be distinguished only where their predicted observables differ by more than measurement and model error.]] (draft, inferred)
- References of decreasing certainty. A synthetic benchmark has exact populations (TeaA). An experimental reference such as the HDX-NMR-derived MoPrP target depends on its own state assignments and thermodynamic assumptions. A system with no structural reference allows only prediction and stability to be assessed (α-synuclein).
- Validation answers narrower questions. Held-out error tests prediction, replicate spread tests sensitivity, and [[controlled perturbation]] tests attribution. None of them shows that the populations are unique.
- Ranking rather than identifying. [[BICePs]] ranks candidate priors by an evidence ratio while inferring the error scale. ValDX instead asks whether a fit generalises and how much it changed the prior.
  - [[A fitting metric can rank candidate ensembles against data or reveal them as inadequate, so integration becomes structural hypothesis testing.]] (supported)
  - [[BICePs ranks candidate priors by an evidence ratio while inferring the experimental uncertainty as a nuisance parameter.]] (supported)
- Close on the hand-off to the next subsection. Once the data cannot pick one ensemble, the comparison between candidates has to be made in representations the reader can inspect.

### Ensemble Comparison and Interpretable Representations
- [[ensemble comparison]] gives the Jensen–Shannon divergence [[ensemble comparison#^eq-jsd]], built from [[Kullback–Leibler divergence#^eq-kl]].
  - [[Comparing ensembles requires comparing probability distributions over conformations, not single-structure RMSD.]] (supported)
  - [[The Jensen–Shannon divergence is a symmetric, bounded measure of ensemble similarity that stays defined where one ensemble has no density.]] (supported)
  - [[Dimensionality reduction by PCA or MDS assumes a linear conformational space.]] (supported)
  - [[Ensemble similarity scores compare equilibrium distributions and do not capture changes in dynamics or transition rates.]] (supported)
- Structural distributions. [[positional covariance]] gives RMSF and dynamic cross-correlation, and [[Wasserstein distance]] compares whole distributions in the units of the variable. ValDX's residue-averaged pair-distance $W_1$ and neighbourhood LCC are its own constructions ([[Structural comparison metrics (ValDX)]]).
  - [[Superposition can introduce artefactual correlations into atomic covariance estimates.]] (supported)
  - [[Linear displacement correlation misses non-linear and perpendicular coupled motions.]] (supported)
  - [[Agreement of per-residue pair-distance distributions does not establish that two ensembles share the same joint conformational distribution.]] (draft, inferred)
- Populations. JSD between state populations, with the log base stated. jaxENT's recovery score needs base 2 ([[Ground-truth recovery (jaxENT)]]).
- Change induced by fitting. [[Work Done]] measures how far fitting moved the protection profile from the prior, and apparent work measures how far it moved the weights ([[Kullback–Leibler divergence]]). High Work Done shows substantial modification with several possible causes, not overfitting by itself. Full equations stay in Chapter 3 ([[Work Done (ValDX)]]).
  - [[Distinct protection profiles can give zero Work Done, so Work Done is not a distance between profiles.]] (draft, inferred)
- Compact representations. [[clustering]] covers representatives and resolution. Rule-based states (jaxENT MoPrP) and shape-space GMM clusters (jaxENT α-synuclein) are also chosen resolutions, so conclusions should be checked across them.
  - [[Clustering sets the resolution of an ensemble comparison and ignores differences within clusters and similarities across them.]] (supported)
  - [[Clustering into representative structures gives compact, interpretable ensembles with little loss of accuracy.]] (supported)
  - [[Conclusions drawn from representative structures should be checked for stability across cluster sizes.]] (revised ValDX only)
- Close on the boundary. [[conformational kinetics]] marks how far a weighted ensemble reaches towards mechanism. Under EX2 the data report the fraction of time open, not the opening rate.
  - [[Weighted conformational ensembles describe which states are occupied, not the order, rates or causal pathways of transitions between them.]] (draft, inferred)
- **gap**. No citable source yet for the general $W_1$ definition (SciPy documentation only). jaxENT's ternary shape space and GMM clustering are manuscript-only.

## 2.5 Protein Protonation and pH-Dependent Properties

Short section, two to three pages. [[prion protein|MoPrP]] carries it. The jaxENT HDX-MS data for its partially unfolded forms were taken at pD 4 ([[@moulickPartiallyUnfoldedForms2015]]), and Chapter 5 simulates MoPrP at pH 4 and pH 7. Both depend on which groups are protonated, which is what this section supplies. The computational titration models (PROPKA, PypKa, constant-pH MD, pKAI, KaML) are introduced in the Chapter 6 preface ([[06-jax-ka]]), not here.

### Acid–Base Equilibria and Protein Charge
- Open on [[pKa]]: the Henderson–Hasselbalch protonated fraction [[pKa#^eq-hh]] and net charge [[pKa#^eq-net-charge]], with model-compound values from alanine pentapeptides.
- MoPrP framing. Lowering the pH from 7 to 4 crosses the model pKa of His and approaches those of Asp and Glu.
  - [[Between pH 7 and pH 4, His side chains become protonated and Asp and Glu partly protonated, so a protein's net charge becomes more positive.]] (supported, inferred)
- Linkage, which is why charge changes alter stability and binding.
  - [[A group whose pKa differs between two states makes the equilibrium between those states pH-dependent.]] (supported)
- The prion protein at acidic pH, one paragraph. Use mouse numbering (H186 = human H187).
  - [[Mouse PrP(121–231) populates a β-rich intermediate only at acidic pH, and urea is needed to populate it substantially.]] (supported)
  - [[Protonation of H186 or D201 drives MoPrP misfolding, and HDX-MS shows helix 1 and the α1–β2 loop become more dynamic.]] (supported)
  - Optional: MoPrP folds and unfolds by one pathway at pH 7 and by distinct pathways at pH 4 ([[@moulickRuggednessFreeEnergy2019#^c1]]); Malevanets et al. 2017 for a buried His pKa near 5 ([[@malevanetsInterplayBuriedHistidine2017]]).
- HDX link, pointing back to §2.1 rather than repeating it ([[intrinsic exchange rate#^eq-pd]] for pD; ionisable neighbours in the same note).
  - [[His, Asp and Glu neighbours change intrinsic exchange rates with pH through their own ionisation.]] (supported)
- **decision** (recommended, applied in the KB): the pD correction and the ionisable-neighbour factors are stated in §2.1 Intrinsic Exchange Rates, and §2.5 points back.

### Structural Influences on pKa
- [[pKa shift]], with PROPKA's decomposition as the one light equation [[pKa shift#^eq-propka]]. The equation is vocabulary for the determinants; PROPKA as a method is in the ch. 6 preface.
  - [[Most measured pKa values in folded proteins lie close to model-compound values, and large shifts occur for buried or interacting groups.]] (draft)
- Consequence for simulation.
  - [[Standard molecular dynamics fixes one protonation state per titratable residue for the whole run, while constant-pH MD lets protonation states change.]] (supported)
  - [[Constant-pH MD of human PrP at low pH populates a β-rich form in which His187 protonation separates the subdomains.]] (draft, optional; the β-rich form was at pH 2)
- Close on the hand-off to Chapter 6.
  - [[Our candidate ensembles were protonated once at pH 7 or 7.4, so a pH 4 ensemble depends on protonation states that were not assigned for pH 4.]] (draft, inferred)
- Optional, cut first if space is short: coupled sites and titration that does not follow Henderson–Hasselbalch (Onufriev, Case & Ullmann 2001; Ullmann 2003; not seeded).

## Gaps (Chapter 2 literature)
- §2.5 and ch. 6 papers all have PDFs and blocks. Yang & Honig 1993 and Hvidt 1954 are OCR text, so check their quotes against the page.
- ValDX `2_hdx_theory_omc.tex` L7 cites Kim, Fuchs & Woodward 1993 for "the protection factor reports on the free energy of local unfolding"; Kim does not say this (no protection factors, no EX2). Cite Vendruscolo et al. 2003 (^c2) instead.
- `vendruscoloRareFluctuationsNative2003` has two Zotero duplicates (`…2003a`, `…2003b`); merge them.
- `baiPrimaryStructureEffects1993` is duplicated in Zotero (two items, one key); merge them.
- ValDX `2_hdx_theory_omc.tex` L5 cites Nguyen 2018 as the webpage snapshot `ReferenceParametersProtein`; re-key to `nguyenReferenceParametersProtein2018` when adapting into ch. 3 and retire `kb/papers/@ReferenceParametersProtein.md`.
- The jaxENT SI (`si_figures.tex` L225) cites `wuConformationalHeterogeneitySavinase2020` for "Nguyen et al." reference parameters; the correct paper is Nguyen, Mayne, Phillips & Englander 2018 (JASMS 29:1936).
- No published pH 4 against pH 7 simulation of mouse PrP was found (human and bovine only), so the Chapter 5 MoPrP runs would be the first mouse-specific comparison. Check again before claiming it.
- Two general sources for layer 1b of §2.4: a statistical-learning text (Hastie, Tibshirani and Friedman, ch. 7 for selection and §8.7 for bagging) and Roberts et al. 2017 on validation with dependent observations. Four draft claims wait on them. Optional: Breiman 1996, Cawley and Talbot 2010, Maity 2005 for the foldon term, MDRefine and DynaXL as held-out-restraint comparators.
- A figure or notebook ID comparing the ValDX consensus with single-replicate fits; without it the consensus claim stays draft.
- jaxENT: record which validation block the reported selections used, the provenance of `moprp.weights`, and the splitter's overlap behaviour; update the manuscript's covariance and selection wording to the current policy ([[Observation weighting and selection (jaxENT)]], [[Evaluation design (jaxENT)]]).
- The pinned ValDX package lacks the Non-Redundant and Spatial split code and the consensus mean that the benchmarks used ([[Peptide splitting and consensus (ValDX)]]).
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
