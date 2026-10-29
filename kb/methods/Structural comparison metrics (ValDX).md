---
type: method
project: 1-ValDX
status: draft
needs_review: false
review_reason:
code:
  - projects/1-ValDX/analyses@1d78b96:notebooks/SI-Fig-1_AF_MD_PCA_Space/SI-Fig1-T-FES.py#L1887-L1985
  - projects/1-ValDX/analyses@1d78b96:notebooks/SI-Fig-1_AF_MD_PCA_Space/SI-Fig1-T-FES.py#L1647-L1730
sources:
  - "[[@kasaharaNovelApproachDynamic2014#^c2]]"
  - "[[@bmsb2012ch8#^c7]]"
  - "[[@lindorff-larsenSimilarityMeasuresProtein2009#^c10]]"
---

<!-- Note name: Structural comparison metrics (ValDX). Concepts: [[ensemble comparison]], [[Wasserstein distance]], [[positional covariance]]. -->

## What it does

ValDX compares candidate ensembles at several structural scales, each restricted to residues covered by HDX-MS peptides (revised `projects/1-ValDX/manuscript/report/6_methods_omc.tex` L294–360).
- **PCA of pairwise Cα distances** shows the coverage of each ensemble in one projected space (L299). PCA assumes a linear space, so it can hide differences ([[@lindorff-larsenSimilarityMeasuresProtein2009#^c10]]).
- **Local mean pair-distance RMS difference** compares the ensemble-mean Cα–Cα distances within residue-centred neighbourhoods, defined from the first ensemble's mean coordinates (L305). It compares mean geometry only.
- **Residue-averaged pair-distance $W_1$** compares, for each residue, the full distribution of its Cα distances to all other Cα atoms between two ensembles, then averages over residues (L309). This construction is ValDX's own. The general distance is [[Wasserstein distance]].
- **RMSF**, weighted by structure probabilities, gives per-residue flexibility (L330; weighted form in `9_Supplementary_information.tex` L304). See [[positional covariance#^eq-rmsf]].
- **Dynamical local cross-correlation (LCC)** averages the standard displacement correlation $C_{ij}$ ([[positional covariance#^eq-dcc]]; [[@kasaharaNovelApproachDynamic2014#^c2]]) over each residue's neighbours within 8 Å of mean Cα distance (L349; `Extended_SI.tex` L580). The pair coefficient is standard DCC, and the neighbourhood mean is ValDX's summary.

A different quantity shares the "local correlation" name. The **structural local-distance correlation** used to clean AF2 ensembles is a Pearson correlation between corresponding local Cα distances of two individual structures (`Extended_SI.tex` L557). It compares distance patterns between structures, not motion over frames, and must not be read as LCC.

## Equations

$$ \langle W_1(X_1, X_2) \rangle = \frac{1}{N}\sum_{i=1}^{N} W_1\!\left(\Omega_{i,1}, \Omega_{i,2}\right) $$
^eq-residue-w1

Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L309 (Eq. `wasserstein_simple`). $\Omega_{i}$ is the distribution of pairwise Cα distances of residue $i$; $W_1$ is [[Wasserstein distance#^eq-w1]].

$$ \text{LCC}_i(X) = \frac{1}{|\mathcal V_i|}\sum_{j \in \mathcal V_i} C_{ij}(X), \qquad \mathcal V_i = \left\{ j \neq i : \langle \lVert \mathbf r_i - \mathbf r_j \rVert \rangle \le 8\,\text{Å},\ C_{ij} \text{ defined} \right\} $$
^eq-lcc

Manuscript form: projects/1-ValDX/manuscript/report/Extended_SI.tex#L580 (Eqs. `dynamical_pair_correlation`, `intra_ensemble_residue_lcc`). A mean near zero can mean weak correlation or cancellation between positive and negative pairs.

## Implementation notes

- **W1 code versus SI equation.** The code pools, for residue $i$, all Cα distances to every Cα over all frames, smooths each ensemble's pool with `scipy.stats.gaussian_kde` (Scott's rule), evaluates both densities on a common 1,000-point grid, and passes the grid and densities to `scipy.stats.wasserstein_distance` (pinned lines L1887–1985). That is a standard 1-D $W_1$ between smoothed marginals. The SI equation (`Extended_SI.tex` L469–483) instead writes an infimum over couplings named $\gamma_\text{HDXer}$, sets $\gamma \equiv 1$, and adds a harmonic-mean factor $\alpha(x_1,x_2)$ that the code does not use. The thesis writes the code's form (`thesis/appendices/a-valdx-protocols.tex`, `eq:valdx-w1`).
- In the code each residue's pool includes its zero distance to itself in every frame, and frames are unweighted. LCC averages are unweighted over frames in the SI (`Extended_SI.tex` L593). For W1 the methods defer weighting to the SI (`6_methods_omc.tex` L327), whose only weighting term is the α factor the code does not use. The W1 and LCC figures compare unweighted ensembles (author).
- **Alignment.** `calculate_local_correlations` computes fluctuations from raw positions and does not superpose frames itself (pinned lines L1647–1730). Unless trajectories were aligned upstream, rigid-body motion enters $C_{ij}$, and least-squares alignment can itself add artefactual correlation ([[@bmsb2012ch8#^c7]]). Record the alignment used. Neither the revised methods nor the SI state an alignment. Only LCC is affected; PCA, the pair-distance RMS difference and $W_1$ use pairwise Cα distances, which do not depend on superposition. The AF2 cleaning notebook aligns in memory for its own metrics but writes `_all_filtered.xtc` from a freshly loaded, unaligned Universe (`projects/1-ValDX/analyses@1d78b96:notebooks/AF_Ensemble_Cleaning/AF10K_traj_cleaning_Final_json_corrected.ipynb`, cell 41), so the AF2 frames LCC reads are as written before cleaning. The MD inputs (`*_concatenated_stripped.xtc`, `*_combined.xtc`) are prepared outside the repository. Trajectories were aligned on Cα before analysis (author).
- **Boundary for interpretation.** Per-residue $W_1$ agreement is agreement of marginals, not of the joint distribution ([[Agreement of per-residue pair-distance distributions does not establish that two ensembles share the same joint conformational distribution.]]).
- These scripts live in an SI figure notebook. Its last change (analyses 371db20, 2025-09-19) predates the SI figures (`SI_LCC_all_proteins.png` and the `*_pairwise_RMSD_W1.png` set, added 2025-12-16), so the pinned version is the one behind them.
