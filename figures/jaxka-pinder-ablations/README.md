# PINDER supporting ablations

Six panels cover negative construction, ANM discrimination and perturbation sensitivity, 50% width/relation scaling, and seed-17 data/schedule scaling at widths 64 and 128.

```sh
python figures/jaxka-pinder-ablations/make.py
```

Requires Python, NumPy and Matplotlib. The shared builder is `figures/jaxka_pinder.py`. It reads the checked-in `inputs/` snapshots and verifies their SHA-256 hashes against `source.json`. No remote access, training or inference is needed. The companion recipe figure uses these same inputs.

`plotted-data.csv` records extracted metrics, source files and field paths, including the scaling pKa metrics used in the experiment note. `scaling-audit.json` records completion, selected epochs, actual epochs, schedule, masking coverage and validation support. The builder checks successful exits, zero fallback counts in every training epoch, consistent checkpoint epochs, identical pool-manifest hashes across the 50% dRSA export and full-data runs, and evaluation sample counts.

Raw JSON values are retained where available. ANM and 50% width/relation values are extracted from saved gate tables at their reported four-decimal precision. Seeds are descriptive replicates, without confidence intervals or significance tests. Full-data results here cover widths 64 and 128 at seed 17 only.

Full-data reports were retrieved from Isambard `_runtime/jax-Ka/pkabench/audits/datascale-v1/` together with saved protocols, histories, selections and resource records. The source receipt is `.experiments/jaxka-pinder-2026-11-05/receipt.json`. Earlier ablations came from `.experiments/jaxka-binder-isambard-2026-11-04/`. `figures/fetch_jaxka_pinder.py` can retrieve the saved full-data reports again; it launches no jobs. Retrieval is separate from figure regeneration.

Outputs are vector `fig.pdf` and `fig.svg`, plus `fig.png`. `caption.md` defines each panel.
