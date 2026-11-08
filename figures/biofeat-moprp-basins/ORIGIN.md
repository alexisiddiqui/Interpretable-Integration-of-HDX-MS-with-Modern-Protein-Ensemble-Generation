# biofeat-moprp-basins

Reference figure for the MoPrP basins from which the basin-seeded unbiased runs start. Reading in `kb/experiments/bf-moprp.md`.

- `moprp_basins_101`: MI and MI+PB frames on the Cartesian PCA of the 101 HDX residues at pH 4 and pH 7, with the three MI+PB basin circles per pH, and 12 representative frames of each circle rendered as putty coloured by per-residue backbone RMSD from the minimised AF3 start (PrP 127–223 shown). The seed groups pH 4 #1–3 and pH 7 #1–3 come from the same circles (`seeded_apo/basins_seed.json` has the same centres and radius).
- Panel titles use the structural names: Folded (old "native"), β1-detached arm, near ("arm, midway"), β1-detached arm, far ("arm, far end"), core-distorted lobe ("bottom lobe") and detached β1–α1 set ("right shoulder").
- Made on 2026-10-17 in the local mirror `~/Coulson-Chemistry/moprp_basins/` (PyMOL renders by `render_basins.py`, composed by `compose.py`). Redrawn there on 2026-11-08 with the same renders and arguments, through `../biofeat-moprp-puf-rules/source/relabel_run.py` with `source/relabel_map.json`, which changes the panel titles only. Command, from `moprp_basins/`: `relabel_run.py compose.py frames101_trim renders101_trim pca101_scores.npz 0.5 8 <out> "MoPrP Cartesian-PCA basins on the 101 HDX residues (PrP 123-223), mi-v2: representative frames, PrP 127-223 shown" "PrP 127-223"`.
- SHA-256 prefix: `357599b5` moprp_basins_101.
- Code: `source/compose.py`, `source/render_basins.py` and `source/basins.json` (circle definitions with the old names), copied from the mirror.
