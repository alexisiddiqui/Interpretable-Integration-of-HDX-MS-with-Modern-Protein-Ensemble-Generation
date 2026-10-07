# -*- coding: utf-8 -*-
"""Hand-curated journey stages, contributions and negative results.
Every page reference is a PRINTED page label (roman numerals for front matter)."""

JOURNEY_ARC = (
    "The thesis starts from a limitation of mass-spectrometry spatial proteomics: proteins are assigned to organelles "
    "by supervised classifiers that output a single label, although up to half the proteome cannot be robustly assigned to one location (p. 11). "
    "Crook reformulates the problem as Bayesian generative modelling (TAGM, ch. 2), packages it as Bioconductor software (ch. 3) and tests it on a poorly "
    "annotated parasite, Toxoplasma gondii (ch. 4). That application exposes the dependence on marker proteins, so the model is extended to discover "
    "unannotated niches (Novelty TAGM, ch. 5) and then recast with Gaussian-process regression to match the data-generating process (ch. 6), "
    "which gives only modest gains. The direction then changes from static allocation to the dynamic question of which proteins change location after a "
    "perturbation (differential localisation); BANDLE (ch. 7) answers it and is applied to EGF stimulation, an AP-4 knockout and cytomegalovirus infection. "
    "The conclusion (ch. 8) lists what is still missing, including missing values, hierarchical models, PTM-level localisation and multi-condition designs."
)
JOURNEY_CAVEAT = (
    "The stage order follows the thesis's own chapter-to-chapter motivations (e.g. pp. 7-8, 97, 123, 157, 187), which are a retrospective narrative. "
    "The thesis does not say in what order the work was actually done, so the stages show the logical story, not a lab-book chronology. "
    "Outcome labels (worked / partial / failed / pivot) are my reading of the author's own results and wording; each stage says whether the label is stated or inferred. "
    "The author reports no approach as having failed outright, so no stage is labelled 'failed'; the negative and limiting results are listed explicitly instead."
)

STAGES = [
 dict(id="s1", title="Reframing the problem: from labels to uncertainty",
  question="How should mass-spectrometry spatial proteomics data be analysed when up to half of proteins cannot be robustly assigned to a single compartment?",
  approach="Chapter 1 surveys proteomics and the three families of spatial proteomics (microscopy, proximity labelling, fractionation + MS) and argues that a Bayesian treatment suits many latent variables and uncertainty. Chapter 2's introduction reviews the supervised classifiers in use (PLS-DA, kNN, random forest, naive Bayes, neural nets, SVM), which output discrete assignments.",
  outcome="pivot", outcome_basis="inferred",
  outcome_note="The author says the framework is reformulated (p. 9) but does not call it a pivot; I label it one because the analysis target changes from a point classifier to a probability model.",
  why_next="Quantifying uncertainty needs a probabilistic generative model of the profiles, which becomes TAGM.",
  chapters=["ch1","ch2"], sections=["s1.5.3","s1.6","s1.7","s2.1","s2.2"],
  evidence=["vi","5","7","9","11"],
  quote=dict(text="half the proteome cannot be robustly assigned to a single sub-cellular location", page="11"),
  negative_results=[], confidence="high", basis="stated"),

 dict(id="s2", title="TAGM: a Bayesian mixture with an outlier component",
  question="Can a Bayesian generative classifier match state-of-the-art classifiers and also quantify uncertainty in protein-organelle assignment?",
  approach="One multivariate Gaussian per annotated niche plus a heavy-tailed multivariate-t outlier component (the T-augmented Gaussian mixture, TAGM). Inference by EM (MAP) and by a collapsed Gibbs sampler (MCMC). Benchmarked against SVM and kNN with 100 stratified 80/20 splits on 19 datasets, scored by macro-F1 and quadratic (Brier) loss, then applied to a mouse embryonic stem cell hyperLOPIT map.",
  outcome="worked", outcome_basis="stated",
  outcome_note="Macro-F1 shows no consistent winner; TAGM-MCMC has the lowest quadratic loss in 16 of 19 datasets. The three HeLa (Hirst et al.) datasets are the exception on quadratic loss, and the HeLa (Itzhak) 'Large Protein Complex' class does not fit the Gaussian assumption.",
  why_next="Limits named at the end of ch. 2: reliance on marker annotations, no explicit multi-localisation, outlier component hints at unannotated niches, and robustness theory not worked out (p. 56). Next the method is packaged for users.",
  chapters=["ch2","appA"], sections=["s2.3.2","s2.3.3","s2.3.4","s2.4","s2.5","s2.6"],
  evidence=["10","27","33","36","45","51","55","56"],
  quote=dict(text="To our knowledge this is the first Bayesian model of MS-based spatial proteomics data.", page="10"),
  negative_results=["n1","n2"], confidence="high", basis="stated"),

 dict(id="s3", title="Making it usable: a Bioconductor workflow",
  question="How can biologists who are not versed in Bayesian analysis run, check and interpret TAGM?",
  approach="Implemented in pRoloc/MSnbase/pRolocdata (S4 classes). Step-by-step workflow for TAGM-MAP and TAGM-MCMC: running chains, convergence diagnostics (Gelman-Rubin, Geweke), discarding and pooling chains, default prior choices, and uncertainty visualisations, with a primer on Bayesian ideas.",
  outcome="worked", outcome_basis="stated",
  outcome_note="Software and guidance delivered. The author notes that uptake among cell biologists is still low (p. 96).",
  why_next="A hard real application is needed to test it: a poorly characterised, non-model organism (p. 97).",
  chapters=["ch3"], sections=["s3.3","s3.4","s3.5","s3.6","s3.7"],
  evidence=["57","59","72","81","84","96"],
  quote=dict(text="the uptake amongst cell biologists is still low", page="96"),
  negative_results=[], confidence="high", basis="stated"),

 dict(id="s4", title="Stress test: a subcellular atlas of Toxoplasma gondii",
  question="Can hyperLOPIT plus TAGM map the proteome of a non-model apicomplexan parasite where few ground truths exist?",
  approach="hyperLOPIT adapted to T. gondii tachyzoites (nitrogen-cavitation lysis), three experiments; 656 literature markers plus 62 gene-edited, epitope-tagged validation proteins (718 markers); TAGM-MAP then TAGM-MCMC. Spatial classes are then cross-tested against a genome-wide CRISPR-Cas9 screen, dN/dS and SNP density with permutation tests.",
  outcome="worked", outcome_basis="stated",
  outcome_note="1,916 proteins allocated to 26 niches at probability above 0.99, all 62 tested proteins concordant by microscopy. About 30% of proteins were not assigned to a single location, and TAGM cannot model niches that lack markers.",
  why_next="Poor annotation in non-model organisms makes marker lists hard to build, which motivates detecting niches without markers (p. 121-122, 123).",
  chapters=["ch4"], sections=["s4.3.1","s4.4.1","s4.4.2","s4.4.3","s4.5"],
  evidence=["105","106","111","117","118","121"],
  quote=dict(text="This is the first comprehensive and detailed spatial proteome of an apicomplexan cell.", page="121"),
  negative_results=["n3"], confidence="high", basis="stated"),

 dict(id="s5", title="Novelty TAGM: discovering niches without markers",
  question="Can the model discover unannotated sub-cellular niches and quantify the uncertainty in how many exist and which proteins belong to them?",
  approach="Overfitted mixture: allow up to 10 extra components and leave unsupported ones empty; modified collapsed Gibbs sampler; posterior similarity matrices summarised by posterior expected adjusted Rand index (PEAR); discovery probability per protein. Validated by masking known annotations (chromatin, nuclear, ribosomal), Human Protein Atlas and GO enrichment, on 10 datasets and against phenoDisco.",
  outcome="worked", outcome_basis="stated",
  outcome_note="The author reports additional annotation in every dataset. Many putative phenotypes have no GO enrichment (e.g. 8 of 10 in mouse neurons), so several remain putative.",
  why_next="Posterior similarity matrices hint at sub-clusters, and a multivariate Gaussian ignores the ordering of gradient fractions, which suggests Gaussian processes (p. 155-156).",
  chapters=["ch5"], sections=["s5.3.2","s5.4.1","s5.4.2","s5.4.3","s5.5","s5.6","s5.7"],
  evidence=["123","133","137","143","147","150","155"],
  quote=dict(text="revealed additional annotation in every single dataset", page="155"),
  negative_results=["n4"], confidence="high", basis="stated"),

 dict(id="s6", title="Non-parametric Bayes: Gaussian-process mixtures",
  question="Can the model better reflect how the data are generated, with smooth niche profiles along the density gradient?",
  approach="A mixture of Gaussian-process regression models, one per niche, with an outlier component. Hamiltonian-within-Gibbs updates for hyperparameters and a tensor/Toeplitz decomposition of the covariance (Trench and Durbin algorithms) for fast inversion. Empirical Bayes versus fully Bayesian hyperparameters; case studies on Drosophila and mouse stem cells; 5-dataset comparison with TAGM.",
  outcome="partial", outcome_basis="inferred",
  outcome_note="GP models beat TAGM in 4 of 5 datasets on quadratic loss, but by 8-40 proteins' worth; TAGM wins on HeLa (Itzhak). Empirical Bayes ties or beats fully Bayesian. The author calls the remaining GP extensions 'incremental improvements'.",
  why_next="'More interesting questions' remain, including which proteins change localisation upon external stimulus and the role of post-translational modifications (p. 185).",
  chapters=["ch6","appB"], sections=["s6.3.4","s6.3.6","s6.4.1","s6.4.2","s6.4.3","s6.5"],
  evidence=["157","158","175","179","182","183","185"],
  quote=dict(text="can we develop a model that better reflects the data generating process of the data?", page="157"),
  negative_results=["n5","n6"], confidence="medium", basis="stated"),

 dict(id="s7", title="Pivot: from allocation to differential localisation",
  question="Which proteins change their resident organelle upon subcellular perturbation?",
  approach="Define differential localisation precisely, review how current methods answer it (the movement-reproducibility, MR, score of Itzhak et al., and a classification pipeline by Kennedy et al.), and test their assumptions on simulated data.",
  outcome="pivot", outcome_basis="stated",
  outcome_note="The change from the 'allocation problem' to the 'dynamic question' is stated on pp. 8 and 187. Critique of MR: chi-squared fit is poor (gamma fits better), and cubing p-values is invalid.",
  why_next="MR has restrictive assumptions, needs replicates and gives no uncertainty, so a Bayesian model of the pair of conditions is developed.",
  chapters=["ch7"], sections=["s7.1","s7.2","s7.3.1","s7.4.2"],
  evidence=["8","187","189","205","206"],
  quote=dict(text="which proteins change their resident organelle upon subcellular perturbation?", page="187"),
  negative_results=[], confidence="high", basis="stated"),

 dict(id="s8", title="BANDLE: model and simulation study",
  question="Can an integrative semi-supervised functional mixture give a calibrated probability that each protein differentially localises?",
  approach="Gaussian random field mixtures for each niche, replicate and condition; a joint prior on the pair of allocations (matrix Dirichlet, or Pólya-Gamma-augmented for correlation); penalised-complexity priors; prior predictive calibration; MCMC. Five simulation scenarios from a Drosophila map (noise, random and systematic batch effects, fraction permutation), 10 repeats each, versus MR.",
  outcome="worked", outcome_basis="stated",
  outcome_note="Higher AUC than MR in every scenario (p < 0.01) and about twice as many correct re-localisations with the Dirichlet prior. The Pólya-Gamma prior gave no significant AUC gain. Simulations start from a single real dataset.",
  why_next="Apply to real dynamic experiments, including single-replicate designs where MR cannot be used.",
  chapters=["ch7","appC"], sections=["s7.3","s7.4.1","s7.4.2"],
  evidence=["189","194","198","203","204"],
  quote=dict(text="Extensive simulation studies demonstrate that BANDLE reduces the number of both type I and type II errors", page="188"),
  negative_results=["n7"], confidence="high", basis="stated"),

 dict(id="s9", title="BANDLE on real data: EGF, AP-4 knockout, cytomegalovirus",
  question="Does BANDLE recover known re-localisations and give new biological insight?",
  approach="Re-analysis of three published experiments: EGF stimulation of HeLa cells, an AP-4 knockout, and HCMV-infected fibroblasts (24 hpi, single replicate). Results are linked to phosphoproteomics, STRING functional categories, degradation assays, abundance, acetylation and a viral interactome.",
  outcome="partial", outcome_basis="inferred",
  outcome_note="Known biology recovered (SHC1, GRB2, EGFR; SERINC1 and SERINC3 above 0.95) and TMEM199 implicated in AP-4-dependent localisation, but not tested experimentally. Several integrative hypotheses were negative. The phospho-correlation interval is wide.",
  why_next="Remaining limits: PTM-level localisation, multiple or temporal perturbations and joint (not stepwise) integration of other data (pp. 228, 233-234).",
  chapters=["ch7","appC"], sections=["s7.4.3","s7.4.4","s7.5"],
  evidence=["188","210","211","214","215","219","222","223","227"],
  quote=dict(text="we implicate TMEM199 as potentially overlooked AP-4 cargo", page="227"),
  negative_results=["n8"], confidence="medium", basis="stated"),

 dict(id="s10", title="Synthesis and open problems",
  question="What do the contributions add up to, and what is still missing?",
  approach="Chapter 8 summarises findings chapter by chapter and lists 12 limitations or future directions, from the theory of mixed mixtures and missing values to hierarchical models, PTM localisation and differential localisation with several perturbations, time or covariates.",
  outcome="partial", outcome_basis="inferred",
  outcome_note="The author frames the list as limitations and directions for future work; no item is claimed to be resolved.",
  why_next="End of thesis; future work (pp. 231-234).",
  chapters=["ch8"], sections=["s8.1","s8.2"],
  evidence=["229","230","231","234"],
  quote=dict(text="we believe the use of Bayesian modelling will form a key part of the process", page="229"),
  negative_results=[], confidence="high", basis="stated"),
]

CONTRIBUTIONS = [
 dict(id="k1", text="TAGM, a semi-supervised Bayesian mixture model with a heavy-tailed outlier component for MS-based spatial proteomics, with EM and MCMC inference, uncertainty summaries (Shannon entropy) and visualisations.", chapters=["ch2"], stage="s2", source_pages=["10","54","229","230"], basis="stated"),
 dict(id="k2", text="An open pRoloc/Bioconductor implementation and a reproducible workflow including convergence assessment and a Bayesian primer.", chapters=["ch3"], stage="s3", source_pages=["57","96","230"], basis="stated"),
 dict(id="k3", text="The first comprehensive spatial proteome of an apicomplexan cell: 1,916 T. gondii proteins allocated to 26 niches, linked to CRISPR-screen essentiality and evolutionary-pressure data.", chapters=["ch4"], stage="s4", source_pages=["111","117","118","121","230"], basis="stated"),
 dict(id="k4", text="Novelty TAGM: semi-supervised novelty detection via overfitted mixtures with uncertainty in the number of new niches, applied to 10 datasets.", chapters=["ch5"], stage="s5", source_pages=["155","230"], basis="stated"),
 dict(id="k5", text="A mixture of Gaussian-process regression models for spatial proteomics, with fast Toeplitz-structure matrix algorithms (also released as an R package) and HMC hyperparameter updates.", chapters=["ch6"], stage="s6", source_pages=["158","184","185","230"], basis="stated"),
 dict(id="k6", text="A definition of differential localisation and BANDLE, a Bayesian model giving the probability that a protein re-localises, shown by simulation to reduce type I and II errors versus the MR method.", chapters=["ch7"], stage="s8", source_pages=["188","203","230","231"], basis="stated"),
 dict(id="k7", text="Case studies: EGF stimulation, AP-4 knockout (TMEM199 implicated) and HCMV infection, including integration with degradation, abundance, acetylation and interactome data.", chapters=["ch7"], stage="s9", source_pages=["214","219","227","231"], basis="stated"),
]

NEGATIVE = [
 dict(id="n1", stage="s2", node="s2.4", kind="limiting", text="On the three HeLa (Hirst et al.) datasets TAGM-MCMC did not have the lowest quadratic loss (the SVM did, with MAP not significantly different in two). For HeLa (Itzhak) the author attributes the classifier differences to a 'Large Protein Complex' class that probably mixes several structures, and leaves it unmodelled in ch. 2.", source_pages=["33","34","36"], figures=["fig:2.2","fig:2.3"], basis="stated"),
 dict(id="n2", stage="s2", node="s2.4", kind="limiting", text="TAGM-MCMC and the SVM disagree for some proteins (lysosome vs plasma membrane, cytosol vs proteasome, 40S vs 60S ribosome).", source_pages=["38"], figures=["fig:2.4"], basis="stated"),
 dict(id="n3", stage="s4", node="s4.5", kind="limiting", text="About 30% of Toxoplasma proteins were not assigned to any single location, and TAGM cannot model niches without markers or with too few proteins to supply markers.", source_pages=["111","121"], figures=["fig:4.13"], basis="stated"),
 dict(id="n4", stage="s5", node="s5.4.3", kind="negative", text="Many Novelty TAGM phenotypes have no enriched GO annotation: 8 of 10 in mouse primary neurons (attributed to technical noise), 3 of 7 in HeLa (Hirst) are singletons, and several in the fibroblast and yeast data are unenriched.", source_pages=["142","143","145","147"], figures=["fig:5.5","fig:5.7"], basis="stated"),
 dict(id="n5", stage="s6", node="s6.4.3", kind="negative", text="Empirical Bayes performs as well as or better than fully Bayesian GP inference, with at most a 6-point loss difference (about 3 proteins), which the author calls hardly worth the loss of uncertainty quantification.", source_pages=["182","183"], figures=["fig:6.11"], basis="stated"),
 dict(id="n6", stage="s6", node="s6.4.3", kind="negative", text="TAGM outperforms the GP models on the HeLa (Itzhak) dataset, where the 'large protein complex' class violates modelling assumptions.", source_pages=["183"], figures=["fig:6.11"], basis="stated"),
 dict(id="n7", stage="s8", node="s7.4.2", kind="negative", text="Adding prior correlation with the Pólya-Gamma prior gave no significant AUC improvement over the Dirichlet prior in simulations.", source_pages=["203"], figures=["fig:7.2"], basis="stated"),
 dict(id="n8", stage="s9", node="s7.4.4", kind="negative", text="In the HCMV integration, differentially localised proteins were no more likely to be targeted for degradation or to be more abundant, and acetylation was not increased among them (apart from a Skp1 effect).", source_pages=["222","223"], figures=["fig:7.6","fig:7.7"], basis="stated"),
]
