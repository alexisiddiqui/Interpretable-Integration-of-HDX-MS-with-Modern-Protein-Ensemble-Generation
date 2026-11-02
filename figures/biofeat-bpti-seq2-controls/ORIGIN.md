# biofeat-bpti-seq2-controls

Reused unchanged from the Pegasus BPTI ±2 control analysis with analysis ID `d626a1195e9fb72b`. The six panels compare unbiased MD, MI, PB, MI+PB with uniform frame weights, MI+PB with MI replica weights, and Anton. The MI and MI+PB ensembles from the original starts remain concentrated in the main basin, motivating the diverse starts used in the subsequent two-stage protocol.

- Role: retained control figure in the BPTI experiment record.
- Source machine: Pegasus-Gate.
- Archive root: `/bitbucket/hussain/BioFeaturisers-production/BPTI/`.
- Source image: `variance-scaled-mi/seqsep2-20261002T184948Z/analysis/d626a1195e9fb72b/density_cartesian_ca_pca.png`.
- Image SHA-256: `834276cdf20262ff3455d2bc5e517cddc87b9fd1bffbf261703a47a4e5814e68`, verified against the remote file on 2026-11-01.
- Input runs, reference trajectory, input checksums and analysis commands: `analysis_receipt.yaml`; panel definitions and frame counts: `analysis_summary.json`, copied alongside the image.
- Variant identity: the archived relabelled version names this MI+PB arm “MI+PB smoother” and the PB-only control “PB-hard”. The later analysis `a1dbc4b861a14e56` uses an MI+PB arm with PB height 0.2 kJ mol⁻¹ and pace 500, replacing the 0.1 kJ mol⁻¹ and pace 1,000 settings used by the smoother arm. This figure preserves the earlier comparison. The original export is used because the later relabelled copy of the same analysis clips axis labels.
- Interpretation: −ln(p/p_max) uses independent colour scales. The MI uncertainty profiles differ between exclusion models; the ±0 and ±2 control figures therefore compare the recorded protocols. MI replica weights do not remove the time-dependent PB bias.
- Retrieve unchanged: `scp Pegasus-Gate:/bitbucket/hussain/BioFeaturisers-production/BPTI/variance-scaled-mi/seqsep2-20261002T184948Z/analysis/d626a1195e9fb72b/density_cartesian_ca_pca.png figures/biofeat-bpti-seq2-controls/fig.png`.
- Protocol and figure sequence: `kb/experiments/bf-bpti.md`.
