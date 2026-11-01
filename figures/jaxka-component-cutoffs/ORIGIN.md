# jaxka-component-cutoffs

Rendered on Coulson by `pkabench.cutoff_plots` (jax-Ka repo, `src/pkabench/cutoff_plots.py`) in the `radial-plots` environment, job 777567 on comp1400, 2026-10-31.

- Cluster output: `/u/oc/lina4225/_runtime/jax-Ka/pkabench/audits/component-cutoffs-figure-v1/plots/component_cutoffs.{pdf,png,svg,json}`, copied here as `fig.*` unchanged.
- Inputs (sha256 in `fig.json`): `audits/propka-components-v2-ligands/out/site_changes.csv` (ligands), `audits/buffer-propka-v2/site_changes.csv` (all buffers removed), `audits/glycan-propka-ccd-v1/site_changes.csv` (all glycans removed, native-eligible sites), `audits/propka-components-v1/site_changes.csv` (metals).
- Regenerate: `sbatch audits/component-cutoffs-figure-v1/cutoff-plots.sbatch audits/component-cutoffs-figure-v1`, then copy the four files here.
