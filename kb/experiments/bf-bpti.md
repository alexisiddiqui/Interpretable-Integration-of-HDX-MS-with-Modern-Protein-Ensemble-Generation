# bf-bpti: generate diversity with ±0 exclusions, then sample with ±2

The BPTI experiment separates generating a diverse candidate ensemble from sampling with the correct residue exclusions. Metainference with parallel-bias metadynamics (MI+PB) first uses ±0 exclusions. Four structures selected across that ensemble then seed production with ±2 exclusions. Each stage comprises four 250 ns replicas, so one two-stage route uses 2 μs of aggregate production simulation against approximately 1 ms in the Anton reference, a 500-fold reduction in simulated time. The comparison asks whether these short simulations recover the conformational basins sampled by Anton.

The restraints use experimental HDX-NMR protection factors. Anton supplies the structural reference for evaluation. It does not supply the restraint targets.

## Archives and sources

All archive paths below are relative to `/bitbucket/hussain/BioFeaturisers-production/BPTI/` on Pegasus-Gate. The compute nodes also mount this directory under `/vols/bitbucket/`. Access is recorded in [machines.yaml](machines.yaml).

| Stage | Archive | Principal sources |
|---|---|---|
| ±0 diversity generation | `variance-scaled-mi/20260911T215808Z/` | `mipb-250ns/provenance/run.sh`, `mipb-250ns/build/resolved/{system,protocol}.yaml`, `mipb-250ns/build/plumed/`, `mipb-250ns/completion.md` |
| Source-ensemble analysis | `variance-scaled-mi/20260911T215808Z/analysis/9abdde1511481f3b/` | `analysis_summary.json`, `pca_cartesian_ca_reference.npz` |
| ±2 production from diverse starts | `seq0-starts-seq2/20261018T135410Z/` | `scripts/{selection.json,prepare.py,run.sh}`, `prepared/{starts,settings}.json`, `runs/{mi,mmpb,u}/completion.json` |
| Matched-start comparison | `seq0-starts-seq2/20261018T135410Z/analysis/pca-comparison/` | `summary.json`, `replica-basin-summary.csv`, `bpti-five-ensemble-log-density-pca.png`, `bpti-second-basin-replica-traces.png` |

The second-stage archive preserves the source tree used by its scripts under `source/`. The later reconciled BPTI code and campaign scripts are in `/opig-shared/projects/hussian-simulation_hdx/_runtime/BioFeaturisers/worktrees/bpti-sync-20261018/` at `066fdb15c738b6bd617dda765e5a22a2cf8afe8f`. Its `hpc/BPTI/README.md` and `hpc/BPTI/provenance/cartesian-pca-uncommitted-20261018.patch` record the reconciliation with the earlier Pegasus worktree. The frozen campaign inputs determine the protocol used here.

## System and observations

- **Construct.** BPTI, 5PTI model 1, chain A, residues 1–58, with charged termini and disulfides Cys5–Cys55, Cys14–Cys38 and Cys30–Cys51. The curated starting structure has SHA-256 `b016284660ceda5c807dfa4e6f3561cdc976bbeca92a1fc3d39b3e424612dc2c`.
- **Solution.** Amber99SB-ILDN with TIP3P water, a dodecahedral box with 1.2 nm protein-to-edge padding, chloride neutralisation and no added salt. Temperature is 298 K and pressure 1 bar. Standard protonation states are assigned at nominal pH 7; BPTI has no histidines and all six cysteines are disulfide-bonded.
- **Dynamics.** GROMACS with PLUMED and the BioFeaturisers JAX callback. Production uses a 2 fs timestep, hydrogen-bond constraints, PME electrostatics and 1.0 nm electrostatic and van der Waals cutoffs. The thermostat is V-rescale (1 ps) and the barostat C-rescale (5 ps). The resolved protocol records the preparation stages; production replica counts and lengths are overridden by the campaign scripts.
- **Observations.** Forty-one residue-level HDX-NMR protection factors, stored as log10(PF) and converted to ln(PF) for metainference (`build/plumed/hdx_targets.json`). Only the measured residues are exchange-enabled. These are protection-factor restraints, not peptide uptake restraints.
- **Exclusions.** ±0 removes atoms in the probe residue from contact counting. ±2 also removes atoms in the two preceding and two following residues on the same chain. The saved `plumed/features/hdx_features.npz` bundles contain `excl_min_sep=0` for the source and `excl_min_sep=2` for the subsequent production. The implementation excludes pairs with same-chain sequence separation less than or equal to this value (`source/biofeaturisers/hdx/exclusion.py`, `exclusion_valid`).

## 1. Generate the diverse ensemble with ±0

The source is the variance-scaled MI+PB arm `mipb-250ns` of campaign `20260911T215808Z`, run as four 250 ns replicas. The production label is `variance-scaled-250ns`; trajectories are saved every 10 ps, giving 25,001 frames per replica and 100,004 frames in the pooled ensemble. The archived completion report accepts the production with no failures.

Parallel-bias metadynamics acts on the three disulfide χ3 dihedrals, Cβ–Sγ–Sγ–Cβ. Gaussian widths are 0.14, 0.17 and 0.14 rad for Cys5–Cys55, Cys14–Cys38 and Cys30–Cys51, respectively. The height is 0.1 kJ mol⁻¹, deposition pace 1,000 MD steps (2 ps), and bias factor 10 at 298 K. Each periodic coordinate spans −π to π with 200 grid bins; the replicas share the bias through `WALKERS_MPI` (`build/plumed/plumed_mmpb_cuda.dat`, lines 3–6).

Metainference uses `NOISETYPE=MGAUSS`, `STRIDE=10`, `AVERAGING=100`, `OPTSIGMAMEAN=SEM` and `SIGMA_MEAN0=0.001`. The MI+PB action includes `pb.bias` with `REWEIGHT`. The residue-specific uncertainty schedule scales base values of 2, 10 and 20 for σ_min, σ₀ and σ_max by each residue's standard deviation in ln(PF), divided by the median residue standard deviation. The ±0 profile is `unbiased-pf-variance/20260911T214212Z-ziz03/variance_scaled_floor2.yaml`; the applied arrays are preserved in `build/resolved/system.yaml` and the PLUMED input. The profile-construction script is `_install_scripts/BioFeaturisers/BPTI/make-variance-scaled-mi-profile.py` under the Pegasus project root.

## 2. Select diverse starts and switch to ±2

Four cluster representatives are selected from all 100,004 source MI+PB frames in variance-normalised Cα PC1/PC2 space, with one representative from each replica and at least 55 ns between their acquisition times. Selection has no basin restriction or time truncation (`prepared/starts.json`). The PCA basis is the archived Anton reference basis.

| New replica | Source replica | Source time (ns) | PC1 | PC2 |
|---|---|---|---|---|
| 1 | 4 | 187.18 | −0.8383 | −0.2786 |
| 2 | 1 | 249.52 | −0.7943 | 0.2262 |
| 3 | 3 | 52.24 | −0.0701 | −0.4014 |
| 4 | 2 | 131.80 | 0.0634 | 0.0847 |

Each complete solvated frame is extracted from the raw trajectory and checked against its corrected protein trajectory. New velocities use seeds 931001–931004, followed by a 1 ps unbiased warmup. Every condition receives identical warmed coordinates and checkpoints for each start. Both MI and PB histories start afresh (`scripts/prepare.py`, lines 40–75).

The second stage uses the existing ±2 feature bundle and variance-scaled MI uncertainty profile from `variance-scaled-mi/seqsep2-20261002T184948Z/mipb-250ns/build/`. The per-residue uncertainty arrays therefore change with the exclusion model; this is not a comparison holding every MI parameter fixed. PB coordinates, widths, height, pace and bias factor remain as above (`scripts/prepare.py`, lines 20–27; `prepared/settings.json`).

Three matched conditions each run four 250 ns replicas from these starts.

- **±2 MI+PB (`mmpb`).** Retains HDX metainference and parallel-bias metadynamics.
- **±2 MI (`mi`).** Retains HDX metainference with no PB bias.
- **Unbiased (`u`).** Removes both HDX metainference and PB bias, testing what the generated starting diversity retains under the force field alone.

The production label is `matched-seq0-starts-250ns`, with 10 ps trajectory spacing and 25,001 frames per replica. MI-containing conditions use a CUDA reverse-VJP callback and HDX stride 10. An isolated 20 ps preflight contributes neither coordinates nor histories to production (`scripts/run.sh`, lines 73–101). All three archived completion records accept all four replicas.

## 3. Evaluate coverage and retention against Anton

`scripts/analyse-matched-pca.py` projects all ensembles onto the same archived Anton Cα PCA basis without refitting. All 58 Cα atoms are aligned to the curated 5PTI structure. PC1 and PC2 explain 21.9 % and 13.6 % of the reference variance. The reference panel contains 4,125 frames and is labelled 1.03 ms. The source-trajectory reprojection reproduces the archived scores exactly; extracted starting structures are independently checked after periodic-boundary reconstruction.

The five-ensemble figure compares the ±0 MI+PB source, ±2 MI+PB, ±2 MI, matched unbiased runs and Anton. The plotted quantity is −ln(p/p_max) from uniform frame counts, with independent colour scales. It shows sampled conformational coverage. MI replica weights alone do not remove the time-dependent PB bias, so these panels are sampling densities, not equilibrium free-energy estimates.

The second basin is defined by Anton PC1 < −0.55. Starts 1 and 2 begin in that basin. The analysis reports pooled occupancy, per-replica traces, 10 ns windows and sensitivity to boundaries at −0.65 and −0.45 (`scripts/analyse-matched-pca.py`, lines 65–124).

| Ensemble | Second-basin frames, full run (%) | Final 50 ns (%) |
|---|---|---|
| ±0 MI+PB source | 48.03 | 70.89 |
| ±2 MI+PB | 44.45 | 36.96 |
| ±2 MI | 44.88 | 39.18 |
| Matched unbiased | 35.62 | 22.37 |
| Anton reference | 14.42 | — |

These frame fractions quantify coverage and retention of the second basin. Recovery of Anton's basin locations and recovery of its populations are separate comparisons.

## Figures

The two-stage comparison is the main-text BPTI figure, and the replica traces go in the appendix. The earlier ±0 and ±2 controls remain in the experiment record. All four figures are copied unchanged into `figures/`, with source paths and checksums in their `ORIGIN.md` files.

| Figure ID | Placement | Comparison and purpose |
|---|---|---|
| [biofeat-bpti-matched-starts](../../figures/biofeat-bpti-matched-starts/fig.png) | Main text | Principal two-stage result. The ±0 source, ±2 MI+PB, ±2 MI, matched unbiased MD and Anton share a fixed PCA basis; 10 ns occupancy windows show how second-basin coverage changes after restart. |
| [biofeat-bpti-replica-retention](../../figures/biofeat-bpti-replica-retention/fig.png) | Appendix | Traces for each of the four starts distinguish retention of starting diversity from visits by other replicas. |
| [biofeat-bpti-seq0-controls](../../figures/biofeat-bpti-seq0-controls/fig.png) | Experiment record | ±0 unbiased, MI, PB and MI+PB against Anton. The MI+PB source covers both principal basins and supplies the diverse starts. |
| [biofeat-bpti-seq2-controls](../../figures/biofeat-bpti-seq2-controls/fig.png) | Experiment record | ±2 controls from the original starts. MI and MI+PB remain concentrated in the main basin, motivating the separate diversity stage. This is analysis `d626a1195e9fb72b`, before the stronger-PB MI+PB variant. |

The density plots use independent colour scales, so matching colours do not establish matching populations. The 500-fold comparison follows from the two production stages recorded above; the principal figure labels the Anton reference as 1.03 ms but does not display the two-stage simulation budget.

## Simulation-time comparison

The diversity stage contributes 4 × 250 ns = 1 μs. One subsequent ±2 condition contributes another 1 μs. The resulting 2 μs route uses 500-fold less aggregate production simulation than a rounded 1 ms Anton reference, or approximately 515-fold less than the figure's 1.03 ms label. This counts the diversity stage as part of the method. It excludes preparation and preflight and is a simulated-time comparison; it does not measure wall-clock or GPU-hour speedup. Running all three second-stage controls makes the combined production total 4 μs.

## Gaps

- A bias-corrected population comparison with Anton is needed to extend the basin-coverage result to population recovery.
