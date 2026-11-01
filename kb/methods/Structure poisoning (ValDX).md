---
type: method
project: 1-ValDX
status: draft
needs_review: false
review_reason:
code:
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L657-L695
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L697-L731
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L779-L835
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L863-L905
sources: []
---

<!-- Note name: Structure poisoning (ValDX). Concepts: [[negative control]], [[decoy conformations]]. -->

## What it does

Structure poisoning adds artificially corrupted structures to a clustered candidate ensemble and refits it, as a negative control on whether optimisation separates plausible from corrupted conformations (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L256–282, L707–717). Two operations are artefacts, Gaussian coordinate noise and coordinate mixing. The third, backbone proton shuffling, is a no-op and is reported as an unmodified control that adds copies of existing structures (`Extended_SI.tex` L364–444; see below). The thesis places the descriptions in `sec:valdx-decoys`, the algorithms in `app:valdx-poison-algorithms` and the BRD4 results in `sec:valdx-brd4-perturbations`.

## Implementation notes

- **Proton shuffling is a no-op (unmodified control).** `shuffle_backbone_protons` (L657–665) shuffles `universe.select_atoms("backbone and name H")`. In MDAnalysis the `backbone` keyword selects N, CA, C and O, so the intersection with `name H` is empty and every frame is written out unchanged. The author confirmed this, and the thesis reports the operation as an unmodified control.
  - Test: `python3 -I -c "import MDAnalysis as mda; u=mda.Universe('BRD4_cv_bfactors.pdb'); print(len(u.select_atoms('backbone and name H')))"`, run with MDAnalysis 2.9.0 on `projects/1-ValDX/code/figure_scripts/fig5/BRD4_cv_bfactors.pdb` (480 residues). Result: 0 atoms, against 405 for `name H`; `backbone` covers N, CA, C and O.
  - Representatives (inferred from the code, not compared on the files): the unchanged coordinates go through the same `KMeans(n_clusters=1000, random_state=42)` as the base ensemble, so the "poisoned" representatives are the base representatives. Each dose adds copies of 1, 10, 100 or 500 of them in `np.argsort(msd)` order. That order mixes two separately fitted projections, so it is not a most-central-first order, and for AF2-MSAss the copies can be implausible structures.
- **Z-score and dose statistics.** `BRD4_Compare_Poisons.ipynb` cell 44 (Work opt) and cell 45 (ΔMSE opt) print every SD and R value in `9_Supplementary_information.tex` L240–274.
  - Z-score: centred on the mean over split replicates at 0%. Scaled by the sample SD (ddof=1) over the split replicates at all doses, 0–50%, for that ensemble and perturbation type. Non-Redundant split (`'R3'`) only.
  - The scale is specific to each ensemble and perturbation type, so SD compares spread in each ensemble's own normalised units, not absolute sensitivity. For the two artefacts the 50% shift dominates the scale (every ensemble lands near |Z|≈1.8–2.5 at 50%), while for the control no dose dominates. Z magnitudes are therefore not comparable across perturbation types.
  - SD and R: `stats_poison_levels = ["p0","p1","p10","p100"]`. SD is the population SD (`np.std`) of the four mean Z-scores, and R is the Pearson correlation with 0, 1, 10 and 100 added structures. The 50% dose is excluded from both but contributes to the Z-score scale. The manuscript's "first three doses" (S230) is corrected in the thesis.
  - Error bars: standard error of the mean over three replicates.
- **Gaussian noise.** The variance is per atom and per Cartesian axis within each residue, over frames (`np.var(positions, axis=0)`), not one value per residue. The SI algorithm transcribes this literally.
- **Dose construction.** The code's form is in the thesis (`app:valdx-poison-construction`):
  - each poison acts on every frame of the parent ensemble;
  - poisoned and unmodified ensembles are each clustered by k-means ($k=1000$, `random_state=42`) on a 50-component PCA of all-atom Cartesian coordinates, and the first frame of each cluster is the representative;
  - poisoned representatives are ordered by squared distance from the mean of a separate 50-component PCA of coverage-filtered Cα pair distances of the unmodified ensemble;
  - doses add the first 1, 10, 100 or 500 ordered representatives to the 1000 unmodified ones. Sets of 20 and 50 were also generated but are not reported.

  The manuscript sentence ("ordered by Euclidean distance (RMSD in PCA space) to the uncorrupted ensemble-average", L717) does not match this, because the two projections are fitted separately.
- **Base clustering.** The poisoning base ensemble uses this Cartesian clustering, not the k-means on 10 pair-distance principal components used for the other clustered ensembles (`6_methods_omc.tex` L301, L705).
- **Prior weights.** Clustered representatives start with uniform prior weights (author), so a copied representative has its prior weight raised.
