# bf-moprp: paired-pH restrained sampling and basin-seeded unbiased dynamics

The MoPrP experiment compares conformational exploration at pH 4 and pH 7, then tests the persistence and connectivity of the sampled states with unbiased trajectories. Metainference and parallel-bias metadynamics generate candidates. The subsequent trajectories supply transition information for Markov state models (MSMs), and segment-level HDX constraints enter a maximum-calibre (MaxCal) refinement of those models. The restrained frame frequencies alone do not establish populations or pathways.

## Archive and provenance

The authoritative campaign is `moprp-paired-50ns-20260925-v1` under `/u/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/` on Coulson-Chemistry. The same directory is exposed under `/home/coulson/oc/lina4225/`. Paths below are relative to that campaign.

| Record | Path |
|---|---|
| pH 4 build | `builds/moprp_ph4/e989dc85f669/` |
| pH 7 build | `builds/moprp_ph7/b2dd4eee2b73/` |
| Resolved system and preparation | Each build's `resolved/{system,protocol,execution_profile}.yaml` |
| Applied MI-v2 inputs | Each build's `branches/mi-v2/{mi_cuda,mmpb_cuda}/replica_1/plumed_*.dat` and corresponding files for replicas 2–4 |
| Seed selection, preparation and run record | `seeded_apo/{README.md,select_seeds.py,build_seed.py,run_seeds.py}` |
| Selected seeds and run lists | `seeded_apo/seeds/seeds_manifest.json`, `seeded_apo/runs/task_list_*.txt` |
| MSM and MaxCal analysis | `seeded_apo/msm_build.py`, `seeded_apo/msm/ext12*` |

The archived resolved files, representative applied PLUMED inputs and seeded-run README were retrieved on 2026-11-03 to `.experiments/biofeat-methods-audit/`. The download is `moprp-protocol.tar.gz`, with a checksum in `SHA256SUMS`. The live BioFeaturisers checkout was clean at `9fa700db6599e120b852e74a1a3aa632e4969a2e`; this identifies the checkout inspected, rather than the code version of every historical run. Frozen run inputs determine the protocol. The local analysis mirror is `/Users/alexi/Coulson-Chemistry/moprp_seeded/`, with figures in the neighbouring `moprp_results/` directory.

`replacement-record.yaml` records that these builds replace the earlier reference campaigns by extending replica relaxation from 5 to 50 ns. The MI-v2 branch supplies the applied restraint settings. The 20 ns production stages in the generic resolved protocol are templates. The applied MI-v2 replica-1 MDPs at both pH values specify 50,000,000 steps at 0.002 ps (100 ns), with coordinates every 5000 steps (10 ps); the final logs of all four replicas at each pH reach 250 ns for MI and 500 ns for MI+PB, all with a `Finished mdrun` record. These continued lengths supersede the initial MDP duration.

## System and experimental observations

The construct is monomeric mouse PrP 122–230, represented by a 109-residue AlphaFold3 model (job `fold_2026_09_02_19_41_moprp109`, model 0). Local residue numbers 1–109 map to canonical PrP numbering by adding 121. The Cys178–Cys213 disulfide is retained. Structural analysis concentrates on the 101 HDX residues, PrP 123–223.

Both builds use Amber ff19SB, OPC3 water, a dodecahedral box with 1.4 nm padding, nominally 20 mM acetate buffer, neutralising ions and no added salt. The resolved temperature is 298.15 K and pressure 1 bar. The experimental D2O/pD condition is approximated with H2O and fixed protonation at the corresponding nominal pH; isotope effects are not modelled. PDB2PQR/PROPKA assigns protonation from the original AF3 structure. A single topology is retained for each pH throughout the campaign.

The MI-v2 actions restrain 77 residue-wise ln(PF) observations recovered through exPfact from the Moulick et al. dataset ([[@moulickPartiallyUnfoldedForms2015]]). The 24 residues without a determined value are excluded, and 28 of the 77 retained targets are ln(PF) = 0. The target vector is identical in the pH 4 and pH 7 applied PLUMED inputs. Thus the paired simulations change the physical model's pH-dependent protonation and buffer, while using the same experimental restraint vector. They are not fits to independently measured protection factors at both pH values. The build-bound coefficients are β_C = 0.105 and β_H = 0.601. Simulations contain explicit amide H and are unaffected by the synthetic-H error described in [[Sigmoid-switch BV forward model (BioFeaturisers)]].

## Preparation and restrained sampling

Preparation comprises minimisation, 20 ps restrained NVT, three 200 ps NPT stages with Cα restraint constants of 500, 50 and 5 kJ mol⁻¹ nm⁻², then 200 ps unrestrained NPT. Four replicas receive independent velocities and 50 ns relaxation. Dynamics use a 2 fs timestep after the 1 fs NVT stage, hydrogen-bond constraints, PME electrostatics, 1.0 nm electrostatic and van der Waals cutoffs, V-rescale temperature coupling (1 ps) and C-rescale pressure coupling (5 ps). These settings come from `resolved/protocol.yaml` and the system overrides.

The applied MI-v2 inputs use `MGAUSS`, `STRIDE=10`, `AVERAGING=100`, `SIGMA0=2.5`, `SIGMA_MIN=0.5`, `SIGMA_MAX=10`, `OPTSIGMAMEAN=SEM` and `SIGMA_MEAN0=0.001`. The HDX calculation uses the reverse-VJP callback. [[Metainference and parallel-bias metadynamics (BioFeaturisers)]] explains the force path and replica weighting.

Five collective variables bias sheet contacts, two structural displacements and two helicity measures. In input order they are `contacts_beta1_beta2`, `disp_puf2_unit`, `disp_beta1`, `helicity_alpha3_cterm` and `helicity_alpha1`. MI+PB uses Gaussian widths 2.0, 0.025 nm, 0.02 nm, 0.25 and 0.25, height 0.1 kJ mol⁻¹, pace 1000 steps and bias factor 6. Four walkers share history through `WALKERS_MPI`. The applied upper displacement walls are 3 and 2.5 nm, and lower helicity walls are 9 and 7, each with κ 500 in the action's units. The restraint's `REWEIGHT` argument receives the sum of PB and both wall energies. PB-only settings in the resolved system use height 0.2 and pace 500 and must be distinguished from the MI+PB override.

## Basin-seeded unbiased trajectories

A Cartesian Cα PCA fitted on the 20 aligned 2L39 NMR models defines the basin-selection plane on PrP 123–223. Three basins from each pH's MI+PB ensemble supply six source groups. Twenty-four frames per group are selected with temporal spacing, and each is rebuilt at both target pH values. This prepares 288 systems. Half 1 uses the 12 even-numbered seeds per group and pH (144 runs); the odd-numbered half remains an independent held-out set in the retrieved record. Prepared systems and completed production are separate counts.

Each seed is solvated and equilibrated with restraints referenced to its own structure. Minimisation, 20 ps NVT and three 200 ps restrained NPT stages precede unrestrained production, so equilibration totals 0.62 ns. Production uses neither MI nor PLUMED and initially lasts 20 ns, with protein trajectories saved every 10 ps. Fixed protonation is inherited from the target-pH build. Seed-wise PROPKA diagnostics reveal structural dependence in the assigned states, so the comparison is conditional on these fixed topologies.

The `ext6` set extends six seeds per source-group and pH cell to 100 ns. `ext12` extends the remaining non-folded half-1 seeds to the same length. In the retrieved completed record, 120 trajectories reach 100 ns and 24 folded-start trajectories remain at 20 ns, giving 12.48 μs of seeded production. Four 500 ns unbiased reference replicas at each pH provide additional folded-state coverage. Analyses replace the short version of each extended trajectory, avoiding duplicate frames. QC checks whole molecules, disulfide integrity, constraint warnings, thermodynamic traces and structural drift.

## MSM and HDX-constrained MaxCal

The analysis compares Cartesian and distance features, direct clustering and TICA, state counts and lag times. The principal Cartesian construction uses 10 PCs fitted on unbiased MD, k-means with 100 microstates, and lags of 2 or 5 ns. `msm_build.py` fits reversible maximum-likelihood models on the connected count set and Bayesian models using statistically effective counts. Implied timescales and Chapman–Kolmogorov tests diagnose lag and state dependence. Some macrostate tests fail, so the record does not establish convergence of every inferred rate.

The original PCA basin names are historical labels. Contact analysis shows that they do not map directly onto the experimental PUF assignments. The later analysis therefore constrains segment-opening observables rather than assigning an experimental opening free energy to a whole PCA circle. Native Cα contact fractions define β1 opening (`b1_rest`) and β2-region opening (`b2_seg`), with the principal threshold Q = 0.5. EX2 opening free energies use the open-to-closed probability ratio.

The two-constraint analysis uses pH 4 HDX opening free energies of 2.2 ± 0.2 kcal mol⁻¹ for β1 and 3.1 ± 0.5 for the β2 region. MaxCal is repeated over Bayesian models and experimental-error draws. The pH 4 correction multipliers are transferred to pH 7, where equivalent PUF population measurements are absent. The resulting pH comparison depends on that transfer assumption. The fixed-pH simulations do not reproduce the populations estimated from the in vitro HDX data. At pH 4 the MSM gives opening free energies of about 0.4 kcal mol⁻¹ for β1 and 1.8 for the β2 region, against 2.2 and 3.1.

The selected two-constraint model directories are `msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag5` and the corresponding `lag2` directory. Structural diagnostics and weighted landscapes are `macro_structure_ext12_maxcal2` and `fes_maxcal2_k100_lag*` in the local results mirror. Earlier `ext6`, `ext12mc` and single-constraint `ext12seg*` results remain sensitivity comparisons. They should not be combined as estimates of the same constrained model.

## Basin structure against the experimental PUFs

Moulick et al. ([[@moulickPartiallyUnfoldedForms2015]], p. 25237) describe PUF1 (ΔG_op 2.2 ± 0.2 kcal mol⁻¹, m_op 0.4) as disorder in β1, the β1–α1 loop and the C-terminal region of α3. PUF2 (ΔG_op 3.1 ± 0.5, m_op 0.8) is a disruption or detachment of α1 and β2 from the α2–α3 core. If the two forms are sequential, PUF2 also carries the PUF1 features. α1 is divided between the classes at residue level. Arg147 and Tyr148 exchange with m_op 0.4, whereas Tyr149–Asn152 show m_op 0.7 and Asp143–Asp146 exchange fast without denaturant dependence (p. 25236).

The historical PCA basin labels are retired here in favour of structural names. The β1-detached arm covers the old "PUF2" and "PUF3" basins, the β1–loop–α1 band runs along the arm's lower edge through the old "PUF3-like" basin, and the α2–α3 lobe is the old "PUF1" basin. PUF1 and PUF2 now refer only to the experimental forms. File names and the seed groups (pH 4 #2 and #3, pH 7 #2 and #3) keep their original identifiers.

The pH 7 free-energy minimum on the β1-detached arm lies at PC (87.5, 17.5), at 0.65 kcal mol⁻¹ against 1.7 at the neighbouring pH 4 bin. The table gives native Cα contact fractions relative to Folded for frames run at pH 7, with the `macro_structure.py` definitions, circles of radius 10 and plain frame averages. G is the MSM free energy in the 5-unit bin at the circle centre.

| Region (PC1, PC2) | β1 | β1–α1 loop | α1 | β2 | α3 C | α1+β2 ↔ core | loop ↔ α3 | G (kcal mol⁻¹) |
|---|---|---|---|---|---|---|---|---|
| Halfway from Folded (37, −8) | 0.59 | 0.95 | 0.95 | 0.85 | 0.99 | 0.99 | 0.94 | 0.77 |
| β1-detached arm, near (60, 0) | 0.12 | 0.84 | 0.92 | 0.67 | 0.95 | 0.97 | 0.75 | 1.39 |
| pH 7 minimum (85, 15) | 0.05 | 0.71 | 0.90 | 0.61 | 0.93 | 0.93 | 0.54 | 0.90 |
| β1-detached arm, far end (92.5, 42.5) | 0.04 | 0.76 | 0.89 | 0.60 | 0.93 | 0.96 | 0.75 | 1.59 |
| β1–loop–α1 band (77.5, −27.5) | 0.07 | 0.70 | 0.88 | 0.59 | 0.89 | 0.85 | 0.49 | 3.04 |
| α2–α3 lobe (12.5, −77.5) | 1.09 | 1.11 | 1.04 | 0.99 | 0.97 | 0.89 | 1.07 | 2.55 |

Native contacts alone separate three regions. β1 detaches abruptly at PC1 ≈ 40, and the arm beyond that lies on one β1-detachment coordinate. The fall in β2 along that arm comes from the lost β1–β2 sheet, because at the pH 7 minimum β2 keeps 0.96 of its contacts with the core and 0.02 of those with β1. The α2–α3 lobe keeps β1 and instead disorders the α2–α3 loop (0.58). No frame opens the α1+β2 packing on the core at Q < 0.5. This contact set is a weak test of α1, however, because 31 of its 36 contacts belong to β2 and α1 has only five native Cα contacts with the core.

### Paper-derived rules

To test α1 directly, we added rigid-body measures. Each frame is superposed on the disulfide-proximal core (175–187, 201–216), and a segment counts as displaced beyond the 99th percentile of Folded frames, pooled over pH. Comparing this core-fit RMSD with the RMSD after superposing the segment on itself separates displacement from disorder. Frames align with `msm_weights.npz` to within 1e-5 PC units, and the same frames reproduce the ML opening free energies of the selected model (at pH 4, β1 0.52 and β2 region 1.93 from the MSM, 2.20 and 3.10 after MaxCal). Maps, scripts and the rule table are in `figures/biofeat-moprp-puf-rules/`.

| Rule | ΔG MSM, pH 4 / 7 | ΔG MaxCal, pH 4 / 7 | Frames, pH 4 / 7 | Runs, pH 4 / 7 | Median PC, pH 4 / 7 | Main source |
|---|---|---|---|---|---|---|
| β1 alone | 0.82 / 1.15 | 3.63 / 3.80 | 23176 / 22879 | 33 / 32 | (84, 17) / (86, 21) | pH 4 #3 seeds, about half |
| β1 + loop + α1 N | 2.60 / 2.41 | 3.90 / 7.65 | 3134 / 3780 | 12 / 13 | (56, −30) / (61, −24) | pH 7 #3 seeds, all |
| β1 + loop + α3 C (PUF1 text) | none | none | 0 / 0 | 0 / 0 | | |
| α1 + β2 off, core intact (PUF2 text) | 3.35 / 2.12 | 3.47 / 5.99 | 662 / 679 | 18 / 14 | (60, −27) / (81, 10) | pH 7 #3 seeds, 94–99 % |
| α1C–β2 unit off, β1 kept | 2.34 / 3.71 | 1.99 / 3.90 | 882 / 159 | 17 / 13 | (20, −32) / (28, −26) | Mixed |
| α3 C off or disordered, β1 kept | 2.06 / 2.44 | 1.92 / 2.56 | 1814 / 1038 | 3 / 5 | (22, −13) / (5, −2) | pH 4 #1 seeds, all |

α1 moves as a rigid helix. Its self-fit RMSD stays at 0.02–0.04 nm across the basins, while its N-terminal half reaches 0.84–0.86 nm from the core in the β1–loop–α1 band against 0.33–0.44 in Folded. Simulation therefore supports α1 displacement and gives no sign of α1 unfolding. With β1 still closed, the displacement forms a continuous shoulder rather than a separate state, and in unbiased MD α1 N exceeds 0.6 nm in 10.1 % of frames at pH 4 against 1.2 % at pH 7. One 400 ns block holds much of that signal (36 %). The other seven pH 4 blocks range from 0 to 17 %, and no pH 7 block exceeds 4 %.

The PUF1 text rule has no frames, because α3 C disorder does not co-occur with β1 detachment. α3 C opens near Folded in three to five runs, so that feature is neither joined to the other two nor well sampled. The closest PUF1 candidate is instead β1 + loop + α1 N, which matches the m_op 0.4 segments 127–132 and 133–148. It forms the β1–loop–α1 band, at an MSM ΔG of 2.60 at pH 4 against 2.2 ± 0.2. The closest PUF2 candidate lies in the same band with α1 and β2 also shifted and the core intact, at 3.35 at pH 4 against 3.1 ± 0.5. Its frames nearly all have β1 displaced as well (91 % at pH 4, 99 % at pH 7), as the sequential reading of PUF2 expects, but β2 moves by only about 0.1–0.2 nm from Folded, which is a shift and not a detachment.

Both candidates rest almost entirely on the 12 pH 7 #3 seeds at each target pH. No Folded-seeded or unbiased frame reaches them with β1 displaced, so their MSM free energies inherit the seeding and their agreement with experiment may be coincidental. MaxCal does not preserve the agreement, giving 3.90 and 3.47 at pH 4 with the order inverted.

The pH 7 minimum is a mixture that the PCA plane does not resolve. Within 5 PC units of it, 75 % of frames are β1 alone, whereas 72 % of the MSM weight meets the PUF2 text rule (0 % at pH 4), carried by microstates of the pH 7 #3 seeds and a few runs. The same seeds relax differently at the two pH values. Over the last 20 ns, β1 stays further out at pH 7 (1.68 against 1.35 nm) while loop and α1 N sit closer to native (0.87 against 1.03, 0.66 against 0.81). These 12 paired differences are trends (Wilcoxon p = 0.034–0.052, uncorrected across the comparisons made), and they are the most direct evidence so far of pH-dependent behaviour in this state.

The swap of labels suggested by the seeded-run README would not have resolved the assignment. The α2–α3 lobe has α1 shifted with β1 kept, which is at most a partial non-sequential PUF2 signature, and its core is distorted (0.17–0.20 nm against 0.09), whereas PUF2 requires an intact core. The β1-detached arm matches neither PUF, and it is the state that the MSM overpopulates (0.82 against 2.2).

Three parts of the analysis depend on these definitions. The β2-region MaxCal target of 3.1 was applied to `b2_seg`, whose open frames are all β1-open and keep a β2–core Q of 0.80–0.81 against 0.92 in Folded, so it constrains a subset of β1 detachment and not PUF2. The absence of PUF1↔PUF2 events was counted between the old PCA circles, so the sequential-or-parallel question has been repeated below on structurally defined states. Finally, neither candidate is more populated at pH 4 in the MSM (2.60 against 2.41, 3.35 against 2.12). β1 alone, α3 C opening and the α1C–β2 unit shift with β1 kept do favour pH 4. The unit shift has the largest pH difference, but its scale is set by the 99th-percentile threshold, which alone would place Folded-like frames near 2.9 kcal mol⁻¹.

### Transitions between structural states

Because a state's position on the PCA plane differs between pH values, transitions were counted from the rule labels on the raw trajectories, not from PCA circles or the MSM. Labels were smoothed by a 1 ns rolling majority, a stay had to last at least 1 ns, and the frames between stays were ignored. The pattern is unchanged at 0.5 and 2 ns.

No Folded-start run opens. Across the Folded seeds and unbiased MD, 0 of 34,432 frames pass the β1 threshold at either pH, so the forward path from Folded is not observed. The Folded↔β1-alone events come from seeds that began detached and cross back and forth near the threshold (pH 4 #2 at both pH values, and pH 7 #3 at pH 4).

Within those seeded runs the states connect as a chain. β1 alone exchanges with the β1–loop–α1 band (11 and 16 events at pH 4, 12 and 20 at pH 7), and the band almost never connects directly to Folded (3 events at pH 4, none at pH 7). Inside the band, the PUF1 and PUF2 candidates interconvert at pH 4 (5 and 3 events across 3 and 2 runs) and barely at pH 7 (1 and 0), although the held-out seeds show exchange at both pH values (see the Stage 1 result). The α2–α3 lobe instead exchanges with Folded (31 and 41 events at pH 4, 17 and 26 at pH 7) and connects to the arm and band only rarely (5 events at pH 4, none at pH 7), so it is a separate branch. This topology is compatible with a sequential Folded, β1, band order, but because no single run traverses it from Folded, it does not establish that order.

The 12 half-1 pH 7 #3 seeds appeared to leave the band differently at the two pH values, but the held-out seeds did not replicate this under the fixed tests, so it is not reported as a result (see the Stage 1 result). α1 N returns before β1 in most runs at both pH values (7 of 12 and 9 of 12), so the order of return does not differ (Fisher p = 0.47). What differs is which segments return at all. β1 returns in 5 of 12 runs at pH 4 and none at pH 7, whereas the loop returns in none at pH 4 and 5 of 12 at pH 7 (p = 0.037 each). Runs end in β1 alone in 2 of 12 at pH 4 against 8 of 12 at pH 7 (p = 0.036). These comparisons were chosen after seeing the data and are uncorrected, and at a stricter return threshold (90th percentile of Folded-like frames) nothing returns at pH 4.

### MaxCal on structural observables and MSM populations

The two-constraint MaxCal was repeated at pH 4 with the structural labels as observables (jobs 780859 and 780861 on `comp1400`). The published per-frame microstates were reused, and rebuilding the published model reproduced its prior weights exactly and its MaxCal weights to 1e-13, at lags 5 and 2 ns. The selected variant, C, sets β1 displaced to 2.2, the PUF1 candidate to 2.2 and the PUF2 candidate to 3.1. It has no exact solution, because β1 displaced contains the PUF1 candidate and no microstate exceeds 0.60 in that label. Its best compromise is the exact MaxCal solution for the values it reaches, which are 1.96, 2.37 and 3.17 kcal mol⁻¹, each within about 1.2 standard errors of experiment, at 1.6 times the KL of the published model. Bayesian intervals keep all 200 samples. No MaxCal is applied at pH 7, because the pH 4 multipliers do not transfer for these observables.

| Cluster | MSM pH 4, % [95 %] | MSM pH 7, % [95 %] | MaxCal C pH 4, % [95 %] | ΔG MSM pH 4 / pH 7 | ΔG C pH 4 |
|---|---|---|---|---|---|
| Folded-like | 67.2 [57.0, 73.1] | 80.9 [48.1, 88.5] | 84.5 [81.1, 86.1] | 0 / 0 | 0 |
| β1 alone | 19.7 [13.8, 26.5] | 12.1 [6.6, 22.0] | 0.15 [0.11, 0.39] | 0.73 / 1.13 | 3.74 |
| β1 + partial | 3.1 [1.6, 6.3] | 0.7 [0.3, 2.0] | 1.1 [0.8, 2.3] | 1.82 / 2.83 | 2.57 |
| PUF1 candidate | 1.0 [0.5, 2.3] | 0.4 [0.2, 1.1] | 1.8 [1.1, 2.7] | 2.47 / 3.09 | 2.28 |
| PUF2 candidate | 0.2 [0.1, 0.6] | 2.7 [0.5, 26.2] | 0.5 [0.1, 1.7] | 3.42 / 2.01 | 3.07 |
| β1 kept, core distorted | 4.0 [3.2, 5.0] | 1.4 [0.8, 1.8] | 5.0 [3.9, 6.2] | 1.67 / 2.39 | 1.68 |
| β1 kept, α3 C off | 2.9 [2.2, 3.7] | 1.6 [1.0, 2.1] | 3.7 [2.8, 4.8] | 1.85 / 2.32 | 1.85 |
| β1 kept, unit off | 1.9 [1.3, 3.0] | 0.2 [0.1, 0.3] | 3.3 [2.1, 6.4] | 2.12 / 3.60 | 1.92 |

The table gives lag 5 ns, with ΔG in kcal mol⁻¹ against Folded-like. C reaches the HDX values by removing the β1-detached arm while keeping the band, so β1 opening then occurs mostly in the band. The candidates differ little in structure (β2 0.28–0.33 against 0.20 nm, α1 C 0.57–0.60 against 0.47–0.50 nm), and the band rests on the 12 pH 7 #3 seeds.

Two pH differences hold at both lags, with 95 % intervals that do not overlap. β1-kept core distortion is 2.3–2.8 times more populated at pH 4, and the β1-kept unit shift is 7–10 times more populated at pH 4. In that unit-shift cluster α1 N sits 0.87–0.90 nm from the core with β1 near native, which is α1 displacement without β1 detachment, and it draws on 17 runs from several sources at pH 4. α3 C off separates at lag 5 only. No β1-displaced cluster separates by pH at either lag, including the candidates, and the PUF2 candidate at pH 7 is poorly determined (2.7 % at lag 5 and 0.9 % at lag 2, with an interval reaching 26 %). These intervals describe the MSM's sampling error and do not include the dependence on seeding.

### PUF1 and PUF2 candidate interconversion

Interconversion was measured from the structural labels on the raw trajectories (job 780866), because the 100-microstate MSM mixes the two labels. Milestoning counts only stays in the two candidates and assigns each frame to the last one visited. A core-set Markov model on the eight labels gives free-energy differences and mean first-passage times, with whole runs bootstrapped within source groups.

| Measure (1 ns stays, β2 threshold 0.25 nm) | pH 4 | pH 7 |
|---|---|---|
| Milestoned events, PUF1 to PUF2 / PUF2 to PUF1 | 5 / 4 | 1 / 0 |
| Runs with an event | 3 | 1 |
| Rate PUF1 to PUF2, μs⁻¹ [95 %] | 6.8 [2.2, 16] | 0.95 [0.02, 5.3] |
| Rate PUF2 to PUF1, μs⁻¹ [95 %] | 73 [20, 188] | 0 [0, 48] |
| ΔG PUF2 relative to PUF1, kcal mol⁻¹, bootstrap at 1 ns lag | 1.2 [0.5, 2.7] | 0.5 [−0.2, 1.0] |
| MFPT PUF1 to PUF2, 1–10 ns lag, μs | 1.5–6.8 | 3.6–13 |
| MFPT PUF2 to PUF1, 1–10 ns lag, μs | 0.15–0.95 | 0.9–7.3 |

These data do not resolve a pH dependence of interconversion. The rate intervals overlap and treat events as independent although they come from three runs and one run. At pH 7 the PUF2 candidate is held by one run in the 1 ns count, and it is absent from about a third of the bootstrap samples. With 0.5 ns stays the pH difference disappears (16 and 15 events against 11 and 10, in five runs at each pH), so much of the count is fast shuttling near the rule boundary. With 2 ns stays only three events remain at pH 4 and one at pH 7.

The PUF2 candidate at pH 4 also depends on its β2 threshold. Raising it from 0.25 to 0.30 nm cuts its committed time from 54.6 to 2.9 ns, and at 0.35 nm it vanishes, whereas the pH 7 stay of about 40 ns survives. At pH 4 the candidate is therefore a β2 shift of about 0.25–0.30 nm within the band, which is not a separate conformation. The MFPTs grow about fourfold or more with lag, so they are bounds on order of magnitude rather than rates. The most stable number is the pH 4 free-energy difference, 1.07–1.15 kcal mol⁻¹ across lags against 0.9 from experiment, although its interval is wide and it holds only at the 0.25 nm threshold. Measuring interconversion properly would need new unbiased runs seeded from both candidates at both pH values.

## Follow-up campaign plan

Agreed on 2026-11-04. Stages 0 and 1 are complete, and Stage 1 did not pass its gate. Stage 2b is approved and replaces Stage 2 as the next step. Stages 2 and 3 are not approved, and each `comp1400` job needs separate approval. Throughput is about 100 ns/day per run at 8 runs per A40, on the four A40s of `comp1400`.

| Stage | Purpose | Runs | Simulation | Wall time | GPU-hours |
|---|---|---|---|---|---|
| 0 | Fix the rules and project them onto the MI+PB frames to build the seed pool | none | none | minutes | none |
| 1 | Replicate the band behaviour with the held-out pH 7 #3 seeds | 24 | 2.4 μs | about 1 day | about 70 |
| 2 | Measure interconversion, with 24 PUF1 and 24 PUF2 candidate frames at both pH values for 100 ns | 96 | 9.6 μs | about 3 days | about 275 |
| 2b (optional) | Test the lifetime of the α1C–β2 unit shift with β1 kept, with 12 frames at both pH values | 24 | 2.4 μs | about 1 day | about 70 |
| 3 | Repeat `puf_interconvert.py` with the fixed rules, a run-level bootstrap and paired seed tests | none | none | minutes | none |

At current rates Stage 2 should yield about 33 PUF1 to PUF2 events at pH 4, about 5 at pH 7, and at least about 24 exits from the PUF2 candidate at each pH. That resolves a 3–4-fold rate difference, which needs 8–13 events per pH. A 2-fold difference needs about 33 per pH, and roughly twice that with clustering within runs. Stage 2 selects frames by rule, with temporal spacing and at most about three frames per source run. The β2 threshold for the PUF2 candidate is still to be chosen, with 0.30 nm recommended.

The campaign cannot show Folded opening into the band, because seeding from the band says nothing about that direction. Results stay conditional on the fixed protonation of each topology, and rates describe the sampled band.

### Stage 1 tests, fixed before the runs

The held-out set is the 12 odd-numbered pH 7 #3 seeds at each target pH, run for 100 ns. All 24 pH 7 #3 seeds come from one MI+PB walker within a 4.7 ns window, at least 100 ps apart, so the test covers fresh velocities and nearby frames, not structurally independent starts. Each test compares pH 4 with pH 7 across the 12 seeds, using a two-sided Fisher test.

1. β1 returns in more runs at pH 4 (half 1, 5 of 12 against 0 of 12).
2. The loop returns in more runs at pH 7 (half 1, 0 of 12 against 5 of 12).
3. More runs end in β1 alone at pH 7 (half 1, 2 of 12 against 8 of 12).

A segment has returned when its core-fit RMSD, as a 1 ns rolling mean, stays below its threshold for 5 ns. Thresholds are the 99th percentile of half-1 Folded-like frames, namely β1 0.80, loop 0.76 and α1 N 0.78 nm, and a segment already below threshold over the first 2 ns does not count as returning. A run ends in β1 alone when its last 1 ns stay has that label, under the rule thresholds in `puf_final.json`. Rules, thresholds and code stay as in `source/puf_transitions.py`. If the direction of tests 1–3 does not replicate, the claim that pH changes how the band relaxes is dropped and Stage 2 is reconsidered.

### Stage 0 result

The rule variables were projected onto the 100,004 MI+PB frames at each pH (job 780867). The PUF1 text rule has no frames at either pH, so even the biased ensemble does not join α3 C disorder to β1 detachment. The PUF1 candidate is absent at pH 4 and appears at pH 7 in 1793 frames of walker 1 alone, so the β1–loop–α1 band has a single origin among the walkers. The PUF2 candidate has 85 frames at pH 7 with β2 above 0.25 nm, all from walker 1, and none at either pH above 0.30 nm. No MI+PB frame moves β2 beyond 0.35 nm, although `disp_puf2_unit` was biased.

MI+PB therefore adds no diversity to the PUF1 or PUF2 seed pools for Stage 2, and a PUF2 pool at 0.30 nm would rest on the one seeded pH 7 run. The unit shift with β1 kept is different. It has 1553 frames at pH 4 (mostly walker 3, in 30 five-nanosecond windows) and 1051 at pH 7 (all four walkers, in 43 windows), which gives Stage 2b a varied seed pool.

### Stage 1 result

The half-1 contrast in which segments return did not replicate under the fixed tests, so it is not reported as a result. Whether pH changes how the band relaxes remains open, because these tests can detect only a large effect on rare events. All 24 held-out runs completed 100 ns (job 780868), with no LINCS warnings and a longest bond of 0.22 nm. The analysis (jobs 781323 and 781324) first recovered the half-1 counts from the stored measures and matched the stored measures of all 24 even seeds to 2 × 10⁻⁷ nm from the raw trajectories. Thresholds and rules were the fixed ones.

| Test | Half 1, pH 4 / pH 7 | Held out, pH 4 / pH 7 | Held-out Fisher p | Direction |
|---|---|---|---|---|
| 1. β1 returns, expected more at pH 4 | 5 / 0 of 12 | 0 / 1 of 12 | 1.00 | reversed |
| 2. Loop returns, expected more at pH 7 | 0 / 5 of 12 | 1 / 2 of 12 | 1.00 | same, weak |
| 3. Ends in β1 alone, expected more at pH 7 | 2 / 8 of 12 | 4 / 6 of 12 | 0.68 | same, weak |

Test 1 reversed and tests 2 and 3 kept their direction with far smaller gaps, so the fixed criterion is not met. Pooling both halves gives p = 0.19, 0.048 and 0.039, but half 1 chose these comparisons, so the pooled values are biased towards a difference and are not evidence for one. Twelve runs per pH cannot exclude a modest pH effect on which segments return. They do show that the half-1 contrast was not a reproducible feature of these seeds. α1 N returns in 6 of 12 runs at both pH values, as it did at similar rates in half 1, and this is the one return behaviour that holds across the halves.

Other half-1 contrasts also fail to carry over. Folded-like frames reverse, from 7.4 % at pH 4 and under 0.1 % at pH 7 in half 1 to under 0.1 % at pH 4 and 2.8 % at pH 7, carried by two runs. The PUF1 and PUF2 candidates now exchange at both pH values (8 and 9 events at pH 4, 7 and 6 at pH 7), which removes the near absence of exchange at pH 7. At pH 4, 14 of the 17 events come from seed 23, whereas the 13 at pH 7 are spread over five runs.

The β2 threshold result also reverses. Held-out frames that meet the PUF2 candidate rule total 142 ns in 11 runs at pH 4 and 58 ns in 12 runs at pH 7 above 0.25 nm, 25.7 ns in 5 runs and 2.0 ns in 6 runs above 0.30 nm, and 1.0 ns in 3 runs and none above 0.35 nm. The long pH 7 stay seen earlier is therefore one run, and the larger MSM population of the PUF2 candidate at pH 7 should not be read as a pH effect. Above 0.30 nm the candidate is brief at both pH values, which fits a small β2 shift within the band and not a separate state, so a rate between the PUF1 and PUF2 candidates may not be a meaningful quantity.

Stage 1 does not test the unit-off and core-distorted population differences, because no held-out run makes a 1 ns stay in either state. All 24 seeds still come from one walker within 4.7 ns, so these results describe that region of the band alone.

### Frame-based comparison of the band runs

The fixed tests reduce each run to a yes or no, which discards most of the information for transient states, since β1 returned in only 6 of 48 runs. pH 4 and pH 7 were therefore compared on all frames, using 22 measures fixed before any was computed, namely occupancy, exit rates, transition rates and mean segment displacement (job 781368). Each seed starts from the same frame at both pH values, so pH was compared within seed pairs by an exact sign-flip test, and intervals resample whole pairs. The 12 held-out pairs are the primary set, with Benjamini–Hochberg correction across the 22 measures.

No measure passes (smallest q = 0.74). This is inconclusive and is not evidence that pH has no effect, because the intervals are wide. The 95 % interval on the pH difference in occupancy spans 52 percentage points for β1 alone and 38 for the PUF1 candidate, so even a twofold difference in occupancy could go undetected.

β1 shows why single sets mislead here. Its mean displacement is 0.24 nm higher at pH 4 in the held-out pairs (p = 0.034) and 0.28 nm lower at pH 4 in half 1 (p = 0.032), which nets to −0.02 nm across all 24 pairs. Differences between sets of 12 are therefore as large as any pH signal in β1. In the held-out runs the loop, α1 N, α1 C and β2 relax together at both pH values (the loop from 1.18 to about 1.01 nm, α1 N from 0.94 to about 0.80 nm), while β1 stays at 1.6–2.0 nm against a return threshold of 0.80 nm. The runs are still relaxing at 100 ns, so they sample only the early part of this process.

One lead is worth a future test. The β1 + partial state lasts longer at pH 4 and the PUF1 candidate lasts longer at pH 7, with similar values in both halves (mean stay 10.6 against 6.4 ns and 9.4 against 6.4 ns for β1 + partial, 6.8 against 10.2 ns and 6.4 against 9.2 ns for the PUF1 candidate). Across all 24 pairs these exit-rate differences give p = 0.053 and 0.116, and neither survives correction. The pattern was picked out after seeing the table, and 12 of the 22 measures share a sign between the halves, about what chance gives, so it is a hypothesis to fix in advance and not a result.

### Stage 2b design, fixed before the runs

Stage 2b tests the one pH population signal that has not been tested on new runs, the larger unit-off population at pH 4. In the existing runs this state holds 32.6 ns of committed time with 12 exits at pH 4, against 3.1 ns with 1 exit at pH 7. Stays last about 3 ns, and most entries and exits connect to Folded-like frames (9 of 14 entries and 9 of 12 exits at pH 4), so 100 ns covers many lifetimes and also measures re-entry.

The state sits close to its threshold, which is the weakness that undermined the PUF2 candidate. MI+PB unit-off frames have a median unit RMSD of 0.48 nm against a threshold of 0.45 nm, with 90 % of them between 0.46 and 0.53 nm. One primary measure therefore uses no threshold, and seeds come from the upper half of each pool.

Twelve frames are each run at both target pH values for 100 ns, giving 24 runs, with six frames from each MI+PB pool. A frame must carry the exact unit-off label (β1 kept, core intact, α3 C kept), lie at or above its pool's median unit RMSD, and belong to a block of at least 20 frames, where a block allows gaps under 2 ns. Walkers are taken in turn, largest block first, with frames on one walker at least 5 ns apart. The pH 4 pool limits this design, because 1288 of its 1339 frames come from walker 3, so most pH 4 seeds will share that walker. Runs are in `runs/{ph4,ph7}/unit_off/seed_NN` and use the existing build, ladder and production protocol.

Measures use all frames at 100 ps with the labels and 1 ns stays of `source/puf_stage1b.py`. pH is compared within seed pairs by an exact sign-flip test on pooled values, and intervals resample whole pairs.

Primary measures, with Benjamini–Hochberg correction across the two:

1. Unit-off occupancy over the run, expected higher at pH 4.
2. Mean unit core-fit RMSD over the run, expected higher at pH 4. This uses no threshold.

Secondary measures, reported without a claim: exit rate from unit off, Folded-like to unit-off rate, unit-off occupancy with a 0.50 nm threshold, Folded-like occupancy, core-distorted occupancy and mean α1 N core-fit RMSD.

The signal is supported if at least one primary measure has q < 0.05 in the expected direction and the other has the same direction. It is not supported if the 95 % interval on the pH 4 to pH 7 occupancy ratio lies below 2, because the existing signal is 7–10-fold. Any other outcome is inconclusive and is reported as such.
