---
type: concept
aliases:
  - atomic covariance
  - RMSF
  - root-mean-square fluctuation
  - dynamic cross-correlation
  - dynamic cross correlation
  - DCC
  - DCCM
  - correlated motion
  - displacement correlation
notation:
  - {symbol: '\mathbf{r}_i(x)', meaning: 'position of atom or residue i in conformation x', units: 'Å'}
  - {symbol: '\Delta\mathbf{r}_i(x)', meaning: 'displacement of atom or residue i from its ensemble-mean position', units: 'Å'}
  - {symbol: '\text{RMSF}_i', meaning: 'root-mean-square fluctuation of atom or residue i about its mean position', units: 'Å'}
  - {symbol: 'C_{ij}', meaning: 'dynamic cross-correlation of the displacements of i and j', units: null}
sources:
  - "[[@bmsb2012ch8#^c2]]"
  - "[[@bmsb2012ch8#^c3]]"
  - "[[@bmsb2012ch8#^c5]]"
  - "[[@bmsb2012ch8#^c7]]"
  - "[[@bmsb2012ch8#^c1]]"
  - "[[@bmsb2012ch8#^c4]]"
  - "[[@kasaharaNovelApproachDynamic2014#^c1]]"
  - "[[@kasaharaNovelApproachDynamic2014#^c2]]"
  - "[[@kasaharaNovelApproachDynamic2014#^c3]]"
  - "[[@kasaharaNovelApproachDynamic2014#^c4]]"
  - "[[@meloGeneralizedCorrelationbasedDynamical2020#^c2]]"
  - "[[@meloGeneralizedCorrelationbasedDynamical2020#^c3]]"
  - "[[@appaduraiDynamicalNetworkHIV12016#^c2]]"
  - "[[@appaduraiDynamicalNetworkHIV12016#^c4]]"
  - "[[@bunzelEvolutionDynamicalNetworks2021#^c1]]"
  - "[[@gowersMDAnalysisPythonPackage2019a#^c1]]"
---

## Definition

Positional covariance describes how atoms move about their mean positions across an ensemble. Its diagonal gives each atom's variance, and its off-diagonal terms give how pairs of atoms move together. A likelihood treatment of structure superposition estimates exactly this object, a covariance matrix giving the variance and correlations of each atom ([[@bmsb2012ch8#^c5]]).

Two standard summaries come from it.
- The **root-mean-square fluctuation** (RMSF) of atom or residue $i$ is the square root of its mean squared displacement from the mean position. High RMSF marks flexible regions, and low RMSF marks rigid ones.
- The **dynamic cross-correlation** (DCC) of $i$ and $j$ is their displacement covariance normalised by both fluctuations ([[@kasaharaNovelApproachDynamic2014#^c2]], Eq. 1, p. 2). It lies between $-1$ and $1$, positive for motion in the same direction and negative for opposite motion. DCC is widely used to quantify correlated motion between atoms in MD ([[@kasaharaNovelApproachDynamic2014#^c1]]), and a DCC map (DCCM) shows it for every pair ([[@appaduraiDynamicalNetworkHIV12016#^c2]]).

## Equations

$$ \text{RMSF}_i = \sqrt{\left\langle \lVert \Delta\mathbf{r}_i(x) \rVert^2 \right\rangle}, \qquad \Delta\mathbf{r}_i(x) = \mathbf{r}_i(x) - \langle \mathbf{r}_i \rangle $$
^eq-rmsf

Source: the definition in the MDAnalysis documentation, `MDAnalysis.analysis.rms.RMSF` (https://docs.mdanalysis.org/2.6.1/documentation_pages/analysis/rms.html; doc pointer, not a quoted block). MDAnalysis itself is cited as [[@gowersMDAnalysisPythonPackage2019a#^c1]]. Averages are over frames, or weighted by population in a reweighted ensemble.
Manuscript form: projects/1-ValDX/manuscript/report/6_methods_omc.tex#L330 (unweighted notation); weighted form in projects/1-ValDX/manuscript/report/9_Supplementary_information.tex#L304.

$$ C_{ij} = \frac{\left\langle \Delta\mathbf{r}_i(x) \cdot \Delta\mathbf{r}_j(x) \right\rangle}{\sqrt{\left\langle \lVert\Delta\mathbf{r}_i(x)\rVert^2 \right\rangle \left\langle \lVert\Delta\mathbf{r}_j(x)\rVert^2 \right\rangle}} $$
^eq-dcc

Source: [[@kasaharaNovelApproachDynamic2014#^c2]], Eq. (1), p. 2. Kasahara et al. write time averages $\langle\cdot\rangle_t$ over a trajectory and $\Delta r_i(t)$. The numerator is the off-diagonal element of the positional covariance, and the denominator is the product of the two RMSF values.
Manuscript form: projects/1-ValDX/manuscript/report/Extended_SI.tex#L580 ($\delta\mathbf r_i(t)$; unweighted frame averages).

## Assumptions and limits

- **A reference frame must be chosen first.** Fluctuations are measured after rigid-body motion is removed by superposition, and the MDAnalysis RMSF routine performs none itself, so the trajectory must already be aligned and molecules made whole (documentation pointer). Least-squares superposition assumes that every atom has the same variance and that atoms move independently ([[@bmsb2012ch8#^c1]]). Neither holds. Regions of a simulated protein can undergo large changes ([[@bmsb2012ch8#^c2]]), and adjacent main-chain atoms covary through covalent bonds ([[@bmsb2012ch8#^c3]]).
- **Superposition can create correlation.** Covariance estimated after least-squares superposition was biased and showed a strong artefactual pattern of correlation ([[@bmsb2012ch8#^c7]]). Which regions are excluded from the fit also changes the result ([[@bmsb2012ch8#^c4]]). A DCC map therefore depends on the alignment as well as the motion.
- **One mean per atom.** DCC uses displacements from a single average position, so it can miss correlations in multi-modal motion and is well defined only for a unimodal coordinate ([[@kasaharaNovelApproachDynamic2014#^c3]], [[@kasaharaNovelApproachDynamic2014#^c4]]). An ensemble with two distinct states can show strong apparent correlation that only reflects switching between them (ours).
- **Linear only.** Pearson-type correlation misses non-linear contributions and correlated motion in perpendicular directions. Generalised correlation based on mutual information addresses this ([[@meloGeneralizedCorrelationbasedDynamical2020#^c2]], [[@meloGeneralizedCorrelationbasedDynamical2020#^c3]]).
- **Correlation is not a pathway.** Correlation maps are read as communication between regions ([[@appaduraiDynamicalNetworkHIV12016#^c4]]; [[@bunzelEvolutionDynamicalNetworks2021#^c1]] compares them between ground- and transition-state ensembles). These are equilibrium second moments. They do not give the order or rate of transitions ([[conformational kinetics]], [[allostery]]).
- **Within one ensemble.** RMSF and DCC describe one ensemble. Comparing two ensembles means comparing these profiles, which is a choice of representation like any other ([[ensemble comparison]]).

## Why it matters here

Chapter 2, "Ensemble Comparison and Interpretable Representations". ValDX compares generator ensembles by weighted RMSF and by a dynamical local cross-correlation, which averages $C_{ij}$ over each residue's neighbours within 8 Å of mean Cα distance. That neighbourhood summary is ValDX's construction and is defined in [[Structural comparison metrics (ValDX)]]. It must not be confused with the structural local-distance correlation used to clean AF2 ensembles, which compares distance patterns between two structures, not motion over frames.

Claims that use this term: [[Superposition can introduce artefactual correlations into atomic covariance estimates.]], [[Linear displacement correlation misses non-linear and perpendicular coupled motions.]].
