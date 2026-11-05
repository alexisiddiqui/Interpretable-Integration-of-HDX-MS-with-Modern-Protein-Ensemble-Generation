# PINDER recipe comparison

Run4 → hmask → dRSA, with contact AP, antibody/antigen partner discrimination and binding-shift MAE.

Regenerate from the repository root with Python, NumPy and Matplotlib installed.

```sh
python figures/jaxka-pinder-recipe-comparison/make.py
```

The shared implementation is `figures/jaxka_pinder.py`. Frozen source reports and their SHA-256 hashes are in the companion `jaxka-pinder-ablations/inputs/` and `source.json`. Regeneration verifies the input hashes and uses no remote service or inference. `plotted-data.csv` maps each point to its source file and field. Outputs are `fig.pdf`, `fig.svg` and `fig.png`; `caption.md` defines the evaluation and comparisons.
