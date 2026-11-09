# jaxka-relational-edges

Rendered on Coulson by `pkabench.relation_plots` (jax-Ka repo, `src/pkabench/relation_plots.py`, `render` mode) in the `radial-plots` environment, on the login node, 2026-11-02.

- Data: `runs.csv`, one row per training run, exported on Isambard with `python3 relation_plots.py export $R/training/gqt-production-v2/runs runs.csv` from each run's `selection.json` (sha256 per row). Isambard copy: `/scratch/u6xq/hussain.u6xq/_runtime/jax-Ka/pkabench/audits/relation-figures-v1/runs.csv`.
- Cluster output: `/u/oc/lina4225/_runtime/jax-Ka/pkabench/audits/relation-figures-v1/plots/relation_width.{pdf,png,svg,json}`, copied here as `fig.*` unchanged. `fig.json` holds per-arm means, SDs and per-seed values.
- Runs: 50% pool, seeds 17, 29 and 43. The 4/4, 6/4 and 4/1 full-attention arms ran on seed 17 only. Summaries of the same runs are in Isambard `audits/relations-v1-50`, `shared-projection-v1-50`, `relation-maps-v1-50` and `full-attention-v1-50`.
- Regenerate: on Coulson, `PYTHONPATH=/u/oc/lina4225/jax-Ka/src envs/radial-plots/bin/python -m pkabench.relation_plots render audits/relation-figures-v1/runs.csv audits/relation-figures-v1`, then copy the four files here.

## Thesis presentation

The SVG artwork is the editable source for the thesis. `figures/style_jaxka_artwork.py` removes the small methods notes beneath the axes, trims the unused margins and exports `fig.pdf` and `fig.png`. The notes are carried by `figure.tex` and the appendix protocol. The relation-map legend now reads “Width controls, no relation maps”. Plotted axes, observations and numerical summaries are unchanged; `fig.json` retains the original analysis provenance. Run this presentation script again after regenerating the original cluster artwork.
