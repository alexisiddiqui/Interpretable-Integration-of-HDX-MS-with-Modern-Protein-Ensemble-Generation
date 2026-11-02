# biofeat-bpti-matched-starts

Reused unchanged from the Pegasus BPTI matched-start analysis. This is the principal figure for the two-stage experiment. Five density panels compare the ±0 MI+PB source, ±2 MI+PB, ±2 MI, matched unbiased MD and Anton in a fixed Anton Cα PCA basis. The sixth panel shows second-basin occupancy in 10 ns windows. Each condition contributes four 250 ns replicas. The diversity source plus one subsequent condition totals 2 μs of production simulation.

- Placement: main-text BPTI figure in chapter 5.
- Source machine: Pegasus-Gate.
- Source directory: `/bitbucket/hussain/BioFeaturisers-production/BPTI/seq0-starts-seq2/20261018T135410Z/analysis/pca-comparison/`.
- Source image: `bpti-five-ensemble-log-density-pca.png`.
- Image SHA-256: `17dbac15225a1b055f0d0047cbc1c8a3f49cec9a4de82b934edc6d9dba9c6dc6`, verified against the remote file on 2026-11-01.
- Inputs: `runs/{mi,mmpb,u}/build/branches/matched-seq0-starts-250ns/` under the campaign root, and the source PCA archive `variance-scaled-mi/20260911T215808Z/analysis/9abdde1511481f3b/pca_cartesian_ca_reference.npz`. Its checksum is in `../biofeat-bpti-seq0-controls/analysis_receipt.yaml`.
- Starting frames and coordinate/checkpoint checksums: `starts.json`, copied from `prepared/starts.json`. Summary and per-replica results: `summary.json` and `replica-basin-summary.csv`, copied from the analysis directory.
- Plot code and original scheduler wrapper: `source/analyse-matched-pca.py` and `source/analyse-matched-pca.sbatch`, copied unchanged from the campaign's `scripts/` directory. The script records validation of the fixed projection, frame counts, periodic-boundary reconstruction and histogram coverage.
- Original build command on Pegasus: `sbatch /bitbucket/hussain/BioFeaturisers-production/BPTI/seq0-starts-seq2/20261018T135410Z/scripts/analyse-matched-pca.sbatch`. This also renders `biofeat-bpti-replica-retention`.
- Interpretation: the density panels use uniform frame counts and independent colour scales. The dashed basin boundary is PC1 < −0.55. The source occupies that basin in 48.03 % of frames, subsequent ±2 MI+PB in 44.45 %, ±2 MI in 44.88 %, matched unbiased MD in 35.62 %, and Anton in 14.42 %. These are sampling densities and frame fractions; equilibrium populations require a separate comparison accounting for the bias.
- Protocol: `kb/experiments/bf-bpti.md`.
