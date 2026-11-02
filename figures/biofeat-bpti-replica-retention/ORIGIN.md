# biofeat-bpti-replica-retention

Reused unchanged from the Pegasus BPTI matched-start analysis. The three panels trace the four starting structures under ±2 MI+PB, ±2 MI and unbiased MD. Starts 1 and 2 begin in the second basin. The traces show whether pooled coverage reflects retention of the selected starts or visits from other replicas.

- Placement: appendix supporting the chapter 5 BPTI result.
- Source machine: Pegasus-Gate.
- Source image: `/bitbucket/hussain/BioFeaturisers-production/BPTI/seq0-starts-seq2/20261018T135410Z/analysis/pca-comparison/bpti-second-basin-replica-traces.png`.
- Image SHA-256: `8ad4a74b916e74f20cd9814edc8381e5a4d88f511b21acdb3ef6b0c680d00d16`, verified against the remote file on 2026-11-01.
- Inputs, starting-frame checksums, numerical results and original plot code are shared with `biofeat-bpti-matched-starts` and preserved in that figure's folder.
- Original build command on Pegasus: `sbatch /bitbucket/hussain/BioFeaturisers-production/BPTI/seq0-starts-seq2/20261018T135410Z/scripts/analyse-matched-pca.sbatch`.
- Reading: colour identifies the same start across panels. Each point is a 1 ns mean PC1. The dashed line marks PC1 = −0.55; shading marks the final 50 ns. Legend percentages are frame fractions in the second basin during that interval, calculated before the 1 ns averaging.
- Protocol: `kb/experiments/bf-bpti.md`.
