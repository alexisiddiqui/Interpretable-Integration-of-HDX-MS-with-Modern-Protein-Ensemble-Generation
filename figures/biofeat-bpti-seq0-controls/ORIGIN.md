# biofeat-bpti-seq0-controls

Reused unchanged from the Pegasus BPTI ±0 control analysis. The six panels compare unbiased MD, MI, PB, MI+PB with uniform frame weights, MI+PB with MI replica weights, and Anton. The MI+PB source covers the second Anton basin that the compact-start controls sample poorly. The plotted quantity is −ln(p/p_max), with independent colour scales; MI replica weights do not remove the time-dependent PB bias.

- Role: retained control figure in the BPTI experiment record.
- Source machine: Pegasus-Gate.
- Archive root: `/bitbucket/hussain/BioFeaturisers-production/BPTI/`.
- Source image: `variance-scaled-mi/20260911T215808Z/analysis/9abdde1511481f3b/density_cartesian_ca_pca_labelled.png`.
- Image SHA-256: `c42aa90d8fc4162c65925bfe91ec230748c6c2b9cd5b1af73fa8f9216eaa248a`, verified against the remote file on 2026-11-01.
- Input runs, reference trajectory, input checksums and analysis commands: `analysis_receipt.yaml`; panel definitions and frame counts: `analysis_summary.json`, copied alongside the image. The labelled export retains the original data and specifies the control names.
- Retrieve unchanged: `scp Pegasus-Gate:/bitbucket/hussain/BioFeaturisers-production/BPTI/variance-scaled-mi/20260911T215808Z/analysis/9abdde1511481f3b/density_cartesian_ca_pca_labelled.png figures/biofeat-bpti-seq0-controls/fig.png`.
- Protocol and figure sequence: `kb/experiments/bf-bpti.md`.
