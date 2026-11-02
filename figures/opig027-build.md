# Experiment 027 figure builds

The main and monomer figure directories are `jaxka-extremophile-chemistry`, `jaxka-extremophile-complex-confidence`, `jaxka-complex-linkage-selectivity` and `jaxka-extremophile-monomer-refolding`. The last is a supporting figure. `jaxka-extremophile-overlap` separately contains the original position-overlap and class-chemistry panels. Each directory contains `make.py`, PDF, SVG and PNG exports, the plotted data as CSV, a caption and a provenance receipt. Shared plotting code is in `figures/opig027.py`; the residue-level chemistry and overlap figures use `figures/opig027_replacements.py`.

From the thesis repository root, with the packages in `figures/requirements-opig027.txt` installed, run the corresponding entrypoint.

```sh
python figures/jaxka-extremophile-chemistry/make.py
python figures/jaxka-extremophile-complex-confidence/make.py
python figures/jaxka-complex-linkage-selectivity/make.py
python figures/jaxka-extremophile-monomer-refolding/make.py
```

The builders read `.experiments/opig-adaptyv-027/inputs/` and verify each input against `.experiments/opig-adaptyv-027/access-audit.json` before plotting. Input snapshots are deliberately kept outside git. The [experiment access record](../kb/experiments/027-extremophile-vs-pka-surface.md#access-and-available-figure-inputs) identifies the original source repository and Modal volume. The initial build used `/private/tmp/opig027-figures/bin/python`; the scripts do not depend on that temporary environment's path.

`provenance.json` records the source commit, absolute source files, input hashes, dependency versions, shared plotting-code hash and output hashes. CSV exports preserve the plotted backbone or design values. Rebuilding requires the original input JSONs, rather than only the exported CSVs.

The chemistry panels use each arm's own sampler control and keep weakly determined backbones separate. Points in the complex comparison average the eight refolds of each design before comparison. Linkage pose yield uses exact binomial intervals, replaces the overlapping eight-design strength-0.20 sweep with the 24-design yield run and shows scores only for pose-passing designs. The figure captions identify the different folding protocols and the restriction to binder-site linkage contributions. The monomer supplement uses the six matched backbones, with five for pKAI alk, and weights each challenge equally.

The efficiency benchmark and structural renderings are not part of these builds. The former needs the separate matched benchmark; the latter needs selected remote structure files.

The revised chemistry builder also verifies 376 raw records under `.experiments/opig-adaptyv-027/replacement-records/` against `replacement-records-manifest.json`. To restore these inputs, use the authenticated Modal environment to run `python figures/fetch_opig027_replacements.py`. This reads existing selected design files and launches no jobs. The remote volume paths and record hashes are also copied into the chemistry figure's provenance receipt. The ordinary plotting environment needs no Modal dependency.

The chemistry entrypoint builds both the main residue-level figure and the overlap supplement. The supplement can also be rebuilt alone with `python figures/jaxka-extremophile-overlap/make.py`. Each signed replacement matrix uses independent control–design draw pairs and subtracts the reverse exchange. Checks reproduce the original class matrices and composition changes before plotting. The main heatmaps show positive preferences on a shared logarithmic scale; both signed directions and unthresholded values remain in the CSV exports. `surface_deltas.csv` and `overlap_and_chemistry.csv` in the chemistry directory are retained from the original composition figure for comparison.
