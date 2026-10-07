# -*- coding: utf-8 -*-
"""Claims tied to a section, supporting figure(s)/table(s), page(s) and a journey stage.
check = tokens that must occur on the cited printed pages (verified by the build script)."""

def C(id,stage,node,text,pages,figs=(),check=(),basis="stated",conf="high"):
    return dict(id=id,stage=stage,node=node,text=text,source_pages=list(pages),figures=list(figs),check=list(check),basis=basis,confidence=conf)

CLAIMS = [
 # ---- chapter 2
 C("c01","s1","s2.2","Up to half of proteins cannot be robustly assigned to one sub-cellular location, so assignment is uncertain.",["9","11"],check=["half"]),
 C("c02","s2","s2.3.2","TAGM models each known niche as a multivariate Gaussian and adds a multivariate-t outlier component (kappa = 4; M = global mean; V = half the global variance).",["27","28"],figs=["fig:2.1"],check=["κ = 4","outlier"]),
 C("c03","s2","s2.3.4","Inference is by EM (MAP) or by MCMC with a collapsed Gibbs sampler; MCMC gives Monte-Carlo averages and 95% equi-tailed intervals of localisation probabilities.",["29","31"],check=["collapsed Gibbs","equi-tailed"]),
 C("c04","s2","s2.4","On macro-F1, no single classifier (SVM, KNN, TAGM-MAP, TAGM-MCMC) consistently outperforms the others across datasets.",["33"],figs=["fig:2.2"],check=["no single classifier"]),
 C("c05","s2","s2.4","TAGM-MCMC achieves the lowest quadratic loss versus SVM and KNN in 16 of 19 datasets (all except the three HeLa Hirst datasets).",["36"],figs=["fig:2.3"],check=["16 out of 19"]),
 C("c06","s2","s2.4","When TAGM-MCMC is wrong it is usually less confident than the other classifiers, and when it is right it is more confident.",["36"],figs=["fig:2.3"],check=["lower confidence","greater confidence"]),
 C("c07","s2","s2.4","On unlabelled mESC proteins TAGM-MCMC and the SVM agree strongly, with some disagreement for lysosome vs plasma membrane, cytosol vs proteasome and 40S vs 60S ribosome.",["38"],figs=["fig:2.4"],check=["lysosome and plasma membrane"]),
 C("c08","s2","s2.5","For TRIP12 (G5E870) the SVM assigned no location; TAGM-MCMC places it most probably in nucleus non-chromatin with some 40S ribosome probability.",["42"],figs=["fig:2.8"],check=["TRIP12","40S"]),
 C("c09","s2","s2.5","The 1,111 proteins allocated to known components with probability below 0.95 are enriched for cytoskeleton and cell-division terms, supporting the outlier component.",["45"],figs=["fig:A.3"],check=["1111","cytoskeletal"]),
 C("c10","s2","s2.5","Posterior uncertainty is highest where organelle assignments overlap (secretory pathway, cytosol/proteasome boundary); mitochondria are well resolved.",["51","52"],figs=["fig:2.12"],check=["mitochondria"]),
 C("c11","s2","s2.6","From about 1,000 markers and 4,000 unknowns, the SVM and TAGM-MCMC give rigorous localisation for roughly 2,000 proteins, and uncertainty-aware TAGM adds about 1,000 more.",["54","55"],figs=["fig:2.13"],check=["1000 proteins"]),
 C("c12","s2","s2.6","The robustness (breakdown) properties of the TAGM model are not characterised, and the model relies on marker annotation.",["56"],check=["breakdown robustness"],basis="stated"),
 # ---- chapter 3
 C("c13","s3","s3.5","TAGM-MCMC is computationally intensive; running overnight on a desktop is usually enough but a few hours should not be expected.",["69"],figs=["fig:3.5"],check=["overnight"]),
 C("c14","s3","s3.6","In the worked example 6 chains were run for 20,000 iterations (10,000 burn-in, thin 20); after convergence checks 3 chains were discarded and the rest pooled.",["72","81","82"],figs=["fig:3.6","fig:3.7"],check=["6 chains","discard chains 1, 2 and 4"]),
 C("c15","s3","s3.6.3","Default priors are empirical-Bayes: prior mean = data mean, lambda0 = 0.01, nu0 = number of fractions + 2.",["84"],figs=["fig:3.8","fig:3.9"],check=["0.01"]),
 C("c16","s3","s3.7","Uptake of Bayesian analysis among cell biologists is low because of computational and practical barriers.",["96"],check=["uptake"]),
 # ---- chapter 4
 C("c17","s4","s4.3.1","hyperLOPIT was adapted to T. gondii tachyzoites using nitrogen cavitation because the cell pellicle resists hypotonic lysis.",["103"],figs=["fig:4.6"],check=["nitrogen cavitation"]),
 C("c18","s4","s4.4.1","Three experiments quantified about 4,100 proteins each; 3,832 proteins were common to all three, giving 30-fraction profiles.",["105"],figs=["fig:4.7"],check=["3, 832"]),
 C("c19","s4","s4.4.1","656 literature markers resolve 23 compartments; 62 proteins tagged by gene editing all showed localisation concordant with hyperLOPIT, and were added to give 718 markers.",["105","106","111"],figs=["fig:4.8","fig:4.9","fig:4.10","fig:4.11","fig:4.12"],check=["656","718"]),
 C("c20","s4","s4.4.1","TAGM-MAP (probability above 0.99) allocated 1,916 previously unlocalised proteins to 26 niches; roughly 30% of proteins were not assigned to any single location.",["111"],figs=["fig:4.13"],check=["1, 916","30%"]),
 C("c21","s4","s4.4.1","Plasma membrane, Golgi and endomembrane vesicles share probability while rhoptries, micronemes and dense granules have well-defined single localisations.",["111"],figs=["fig:4.13","fig:4.15"],check=["rhoptries"]),
 C("c22","s4","s4.4.3","Of the 1,916 newly allocated proteins, 795 were annotated only as hypothetical before.",["117"],check=["795"]),
 C("c23","s4","s4.4.3","CRISPR-screen data show plasma membrane, dense granules, micronemes, rhoptries and IMC biased toward dispensable proteins, while the apicoplast is depleted of dispensable proteins (p < 0.01).",["118"],figs=["fig:4.17"],check=["apicoplast"]),
 C("c24","s4","s4.4.3","dN/dS is positively skewed in the plasma membrane, rhoptries (soluble) and dense granules, which the author reads as pressure to outpace the host.",["118"],figs=["fig:4.17"],check=["dN /dS"],conf="medium"),
 C("c25","s4","s4.5","TAGM cannot model niches without annotation or with too few proteins to supply markers.",["121"],check=["unable to"]),
 # ---- chapter 5
 C("c26","s5","s5.3.2","Novelty TAGM uses an overfitted mixture with K_novelty = 10 extra components and beta_j = 0.5; unsupported components stay empty.",["133"],figs=["fig:5.1"],check=["Knovelty = 10","0.5"]),
 C("c27","s5","s5.3.2","Label switching among new phenotypes is handled with posterior similarity matrices summarised by PEAR; discovery probability gives the chance a protein belongs to a new phenotype.",["133","134"],figs=["fig:5.1"],check=["PEAR","label switching"]),
 C("c28","s5","s5.4.1","With chromatin, nuclear and ribosomal annotations removed, Novelty TAGM recovers chromatin-associated phenotypes: 9 putative phenotypes in U-2 OS and 8 in mESC.",["137","138","140"],figs=["fig:5.2","fig:5.3"],check=["9 putative","8 new putative"]),
 C("c29","s5","s5.4.2","In yeast hyperLOPIT a 20-protein group with COPII/COPI roles suggests a novel ER-to-early-Golgi trafficking niche (11 of 20 are COPII components).",["143"],figs=["fig:5.4"],check=["11 out of the total 20"]),
 C("c30","s5","s5.4.2","In HCMV-infected fibroblasts (24 hpi) Novelty TAGM separates the large and small ribosomal subunits, which the original analysis overlooked.",["143"],figs=["fig:5.5"],check=["ribosomal subunits"]),
 C("c31","s5","s5.4.3","In mouse primary neurons 10 phenotypes were found but 8 have no enriched GO annotation, attributed to technical variability.",["147"],figs=["fig:5.7"],check=["8 of these phenotypes"]),
 C("c32","s5","s5.5","On HEK-293 data phenoDisco and Novelty TAGM both find 8 phenotypes; 4 (phenoDisco) vs 5 (Novelty TAGM) have significant GO terms.",["150"],figs=["fig:5.8"],check=["four of the phenotypes","five of the Novelty TAGM"]),
 C("c33","s5","s5.6","All 7 proteins with uncertain assignment to the new U-2 OS endosome class are known endosome-related proteins; for KIF16B the HPA gives mitochondrion, which the author says contradicts the results and the literature (suspecting antibody specificity).",["152","153"],figs=["fig:5.9"],check=["KIF16B","Rab5"],conf="medium"),
 C("c34","s5","s5.7","Novelty TAGM reveals additional annotation in all 10 spatial proteomics datasets analysed.",["155"],check=["every single dataset"]),
 # ---- chapter 6
 C("c35","s6","s6.3.4","The GP covariance has tensor structure so extended Trench and Durbin algorithms reduce inversion cost; the code is released as an R package.",["158","185"],check=["Trench","toeplitz"]),
 C("c36","s6","s6.4.1","Using unlabelled as well as labelled data shifts and shrinks the posterior of the noise parameters in the Drosophila data.",["175"],figs=["fig:6.2"],check=["shrinkage"]),
 C("c37","s6","s6.4.1","Predictive performance shows only minor sensitivity to the choice of hyper-prior (KS test, threshold 0.01).",["179"],figs=["fig:6.6"],check=["minor sensitivity"]),
 C("c38","s6","s6.4.3","GP models beat TAGM on quadratic loss in 4 of 5 datasets, by roughly 16 to 80 points (8 to 40 proteins), with TAGM better on HeLa (Itzhak).",["182","183"],figs=["fig:6.11"],check=["four out of five","8 to 40"]),
 C("c39","s6","s6.4.3","Empirical Bayes matches or beats the fully Bayesian GP in three datasets by at most 6 points (about 3 proteins).",["182","183"],figs=["fig:6.11"],check=["at most a 6 point"]),
 C("c40","s6","s6.5","HMC hyperparameter updates can be up to an order of magnitude more efficient than Metropolis-Hastings.",["185","318"],figs=["tab:B.7"],check=["order of magnitude"]),
 # ---- chapter 7
 C("c41","s7","s7.2","The MR method relies on a multivariate outlier test and reproducibility score, whose thresholds are hard to interpret, and can allow false discovery rates up to 23%.",["188","189"],check=["23%"]),
 C("c42","s7","s7.4.2","For the MR statistic a gamma fit beats the chi-squared fit and p-value histograms deviate from uniform; cubing p-values makes Benjamini-Hochberg meaningless.",["205","206"],figs=["fig:7.3"],check=["Gamma","cube"]),
 C("c43","s8","s7.4.2","BANDLE has higher AUC than MR in all five simulated scenarios (t-test p < 0.01), including batch effects and fraction permutation.",["203"],figs=["fig:7.2"],check=["all scenarios"]),
 C("c44","s8","s7.4.2","With the Dirichlet prior BANDLE discovers around twice as many true re-localising proteins as MR.",["203"],figs=["fig:7.2"],check=["twice as many"]),
 C("c45","s9","s7.4.3","In the EGF data MR flags 7 proteins (including SHC1, GRB2, EGFR); BANDLE ranks proteins by differential localisation probability and shows those three shifting.",["210"],figs=["fig:7.4"],check=["SHC1","7 proteins"]),
 C("c46","s9","s7.4.3","BANDLE ranks correlate more with phospho-proteomic change than MR ranks (Spearman 0.68 vs 0.40, top 10), but the BANDLE interval (0.02, 0.98) is wide.",["211"],figs=["fig:7.4"],check=["0.68","0.40"],conf="medium"),
 C("c47","s9","s7.4.3","In the AP-4 knockout data SERINC1 and SERINC3 have differential localisation probability above 0.95, and TMEM199 is implicated as AP-4-dependent.",["214","215"],figs=["fig:7.5"],check=["SERINC","TMEM"]),
 C("c48","s9","s7.4.4","In HCMV-infected cells at 24 hpi hundreds of proteins differentially localise; enriched terms reflect early infection (translation, transport, viral and immune processes).",["219"],figs=["fig:7.6"],check=["hundreds of proteins","early phase"]),
 C("c49","s9","s7.4.4","Differentially localised proteins are not more likely to be degraded or more abundant, and are not enriched for acetylation increases (Skp1 aside).",["222","223"],figs=["fig:7.6","fig:7.7"],check=["no more likely","acetylation"]),
 C("c50","s9","s7.4.4","Most host interactors of a viral bait share its localisation: UL8 interactors in plasma membrane/cytosol, UL70 interactors in cytosol.",["226"],figs=["fig:7.7"],check=["UL8","UL70"],conf="medium"),
 # ---- chapter 8
 C("c51","s10","s8.1","The author concludes Bayesian modelling will form a key part of the process as spatial proteomics grows more complex.",["229"],check=["key part of the process"]),
 C("c52","s10","s8.2","Listed limitations include missing values, hierarchical models, PTM-level localisation, multiple/temporal perturbations and covariates.",["231","232","233","234"],check=["missing values","covariates"]),
]
