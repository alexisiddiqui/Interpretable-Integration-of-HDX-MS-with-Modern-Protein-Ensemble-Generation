# jaxka-component-cutoffs

Rendered on Coulson by `pkabench.cutoff_plots` (jax-Ka repo, `src/pkabench/cutoff_plots.py`, `components` mode) in the `radial-plots` environment, job 778035 on comp1400, 2026-11-01. First rendered as job 777567; the per-bin summaries are unchanged.

- Cluster output: `/u/oc/lina4225/_runtime/jax-Ka/pkabench/audits/cutoff-figures-v2/components/plots/component_cutoffs.{pdf,png,svg,json}`, copied here as `fig.*` unchanged.
- Inputs (sha256 in `fig.json`): `audits/propka-components-v2-ligands/out/site_changes.csv` (ligands), `audits/buffer-propka-v2/site_changes.csv` (all buffers removed), `audits/glycan-propka-ccd-v1/site_changes.csv` (all glycans removed, native-eligible sites), `audits/propka-components-v1/site_changes.csv` (metals).
- Regenerate: from `audits/cutoff-figures-v2`, `sbatch cutoff-plots.sbatch $PWD/components $PWD/gaps` (renders this figure and `jaxka-gap-cutoffs`), then copy the four files here.
