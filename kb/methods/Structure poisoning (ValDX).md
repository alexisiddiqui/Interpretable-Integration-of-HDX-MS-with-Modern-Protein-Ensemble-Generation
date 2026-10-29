---
type: method
project: 1-ValDX
status: draft
needs_review: true
review_reason: "Proton shuffling selects atoms with MDAnalysis `select_atoms(\"backbone and name H\")`. MDAnalysis `backbone` is N, CA, C and O only (checked on 2.9), so the selection is empty, and if this script made the ensembles the proton-shuffled frames are unmodified. Check before porting the BRD4 results."
code:
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L657-L695
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L697-L731
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L779-L835
  - projects/1-ValDX/analyses@1d78b96:notebooks/Figure_5_Poisoned_Ensemble/Ensemble_Poison.py#L863-L905
sources: []
---

<!-- Note name: Structure poisoning (ValDX). Concepts: [[negative control]], [[decoy conformations]]. -->

## What it does

Structure poisoning adds artificially corrupted structures to a clustered candidate ensemble and refits it, as a negative control on whether optimisation separates plausible from corrupted conformations (`projects/1-ValDX/manuscript/report/6_methods_omc.tex` L256–282, L707–717). There are three operations: Gaussian coordinate noise, coordinate mixing and backbone proton shuffling (`Extended_SI.tex` L364–444). The thesis places the descriptions in `sec:valdx-decoys` and the algorithms in `app:valdx-poison-algorithms`.

## Implementation notes

- **Proton shuffling selection.** `shuffle_backbone_protons` (L657–665) shuffles `universe.select_atoms("backbone and name H")`. In MDAnalysis the `backbone` keyword selects N, CA, C and O, so the intersection with `name H` is empty and `np.random.shuffle` acts on an empty array. Unless the ensembles came from other code, the "proton-shuffled" representatives are unmodified frames chosen by the poisoned-ensemble clustering. The thesis ports the manuscript's description unchanged.
- **Gaussian noise.** The variance is per atom and per Cartesian axis within each residue, over frames (`np.var(positions, axis=0)`), not one value per residue. The SI algorithm transcribes this literally.
- **Dose construction.** The code's form is in the thesis (`app:valdx-poison-construction`):
  - each poison acts on every frame of the parent ensemble;
  - poisoned and unmodified ensembles are each clustered by k-means ($k=1000$, `random_state=42`) on a 50-component PCA of all-atom Cartesian coordinates, and the first frame of each cluster is the representative;
  - poisoned representatives are ordered by squared distance from the mean of a separate 50-component PCA of coverage-filtered Cα pair distances of the unmodified ensemble;
  - doses add the first 1, 10, 100 or 500 ordered representatives to the 1000 unmodified ones. Sets of 20 and 50 were also generated but are not reported.

  The manuscript sentence ("ordered by Euclidean distance (RMSD in PCA space) to the uncorrupted ensemble-average", L717) does not match this, because the two projections are fitted separately.
- **Base clustering.** The poisoning base ensemble uses this Cartesian clustering, not the k-means on 10 pair-distance principal components used for the other clustered ensembles (`6_methods_omc.tex` L301, L705).
- **Prior weights.** Clustered representatives start with uniform prior weights (author).
