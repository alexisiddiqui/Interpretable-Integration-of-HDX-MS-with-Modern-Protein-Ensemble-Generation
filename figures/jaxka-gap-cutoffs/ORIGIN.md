# jaxka-gap-cutoffs

Rendered on Coulson by `pkabench.cutoff_plots` (jax-Ka repo, `src/pkabench/cutoff_plots.py`, `gaps` mode) in the `radial-plots` environment, job 778035 on comp1400, 2026-11-01.

- Cluster output: `/u/oc/lina4225/_runtime/jax-Ka/pkabench/audits/cutoff-figures-v2/gaps/plots/gap_cutoffs.{pdf,png,svg,json}`, copied here as `fig.*` unchanged.
- Inputs (sha256 in `fig.json`): `audits/radial-error-v2-nearcomplete/anchor-analysis-v2/observations.csv` (terminal gaps, PypKa), `audits/radial-error-v2-nearcomplete/internal-anchor-analysis-v1/observations.csv` (internal gaps, PypKa), `audits/pinder-longgap-v1/results/ref_*.jsonl` (long gaps, pKAI).
- `fig.json` holds, per panel and metric, the 5 Å band median, 95th percentile and bootstrap upper bound (seed 20261008), and the radius those bands imply (`band_radius_A`) next to the radius in force.
- Regenerate: from `audits/cutoff-figures-v2`, `sbatch cutoff-plots.sbatch $PWD/components $PWD/gaps`, then copy the four files here.
