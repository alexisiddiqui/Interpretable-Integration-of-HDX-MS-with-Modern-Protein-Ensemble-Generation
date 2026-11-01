# jaxka-component-cutoffs

Rendered on Coulson by `pkabench.cutoff_plots` (jax-Ka repo, `src/pkabench/cutoff_plots.py`, `components` mode) in the `radial-plots` environment, job 778202 on comp1400, 2026-11-01. Earlier renders (jobs 777567, 778035) drew the ligand panel from the 17 complexes that completed in `propka-components-v2-ligands`; this one uses all 39 from `propka-components-v4-ligands`.

- Cluster output: `/u/oc/lina4225/_runtime/jax-Ka/pkabench/audits/cutoff-figures-v3/components/plots/component_cutoffs.{pdf,png,svg,json}`, copied here as `fig.*` unchanged.
- Inputs (sha256 in `fig.json`): `audits/propka-components-v4-ligands/out/site_changes.csv` (ligands), `audits/buffer-propka-v2/site_changes.csv` (all buffers removed), `audits/glycan-propka-ccd-v1/site_changes.csv` (all glycans removed, native-eligible sites), `audits/propka-components-v1/site_changes.csv` (metals).
- Regenerate: from `audits/cutoff-figures-v3`, `sbatch cutoff-plots.sbatch $PWD/components $PWD/gaps` (renders this figure and `jaxka-gap-cutoffs`), then copy the four files here.
