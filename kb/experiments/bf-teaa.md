# bf-teaa: blind two-state ensemble from Boltz-2 and HDX (TeaA)

Protocol for the TeaA metadiffusion experiment in MaxENT-FK, as run on Isambard-AI 25–31 Oct 2026. The run record is in `examples/TeaA/RESULTS.md` of the MaxENT-FK repository (branch `teaa-iso-frame-uptake`, results commit `89f183c`; code commit `4a22611`). That record and every seed-42 number were produced with the synthetic amide H placed on the wrong side of the N (BioFeaturisers up to `43cc194`). Seed 43 was rerun with the corrected placement (BioFeaturisers `39b8069`, MaxENT-FK `39db4b3`, section 5). The reported result is the Fiedler-lobe run of 3 Nov (section 6), which also uses the corrected placement. Locations are in [biofeaturisers.md](biofeaturisers.md).

**Question.** Starting from the TeaA sequence and a Boltz-2 prediction, with no MD reference in any run, can a target-free hinge bias plus HDX guidance and MaxEnt reweighting produce an ensemble that fits the HDX data and recovers the open:closed populations?

## Design

- **System.** TeaA, 309 residues. Lobe I is residues 1–122, 207–249 and 284–309; lobe II is residues 123–206 and 250–283 (`examples/TeaA/cv/derived/residue_structural_mapping.csv`).
- **Target.** Synthetic HDX uptake from MD frames (15 open, 332 closed) at 40 % open : 60 % closed (`raw_data/iso_target_biofeat/manifest.json`). It is built with `examples/TeaA/generate_target.py --forward-model biofeat`, so the guidance forward model generated the target and carries no forward-model error. Timepoints are 10, 60, 600, 3600 and 7200 s; the forward model is BV with HDXrate intrinsic rates (pH 7.0, 300 K in the resolved configs of the seed-43 runs and 298.15 K in the pinned `run.yaml`; `steepness_h` 1.0). The target is scored on the heavy-atom Boltz topology, which has no amide H, so the hydrogen-bond term depends on the synthetic H placement ([Sigmoid-switch BV forward model](../methods/Sigmoid-switch%20BV%20forward%20model%20%28BioFeaturisers%29.md)).
- **Evaluation only.** The MD open and closed references (`examples/TeaA/cv/refs/`) enter the scoring and the answer key, never a run. Hinge states are lobe-II Cα RMSD after a lobe-I fit of at most 1.88 Å to open or 1.82 Å to closed.
- **Sampler.** Boltz-2 through MaxENT-FK, 200 diffusion steps, bf16, K = 50 structures per run, one GPU. Conditioning is `tmsa`: no MSA, and Boltz's own MSA-conditioned prediction (`TeaA_boltz_msa_pred_s42_model0.pdb`) as the only template. The template is a Boltz prediction, not an MD or crystal structure; the unguided pool it gives is unimodal at the Boltz intermediate (θ spread 0.6°).
- **Seeds.** Seeds 42 and 43 are separate pipelines. Every number for a seed derives from that seed's Boltz output, with disjoint seeds for history, continuation and refinement. Seed 43 was the reported result before the Fiedler-lobe run (section 6) because its hinge axis is built from unguided from-noise pools only; seed 42 is the development run on which the recipe was tuned (its axis uses earlier, partly HDX-guided pools).

## Protocol

Every run is `sbatch teaa_sdedit.sbatch <label> <seed> [flags] [key=value ...]` (`~/_submit/teaa_sdedit.sbatch`, which calls `~/_runtime/scripts/teaa_sdedit_pool.py` into `_runtime/runs/TeaA_sdedit/<label>_s<seed>_n<K>`). Overrides are dotted keys that need the full prefix `guidance.guidance_config.`; the listings below omit it. A key given without the prefix is accepted and not applied, and the run proceeds on the defaults (alpha 1.0, lambda 100). Compare `resolved_config.yaml` (written when a run completes) with the intended values before scoring. Starting config is `examples/TeaA/run.yaml`.

### 1. Unguided pools and the blind hinge axis

1. Unguided from noise: `cvf_ung_noise 42 --conditioning tmsa --from-noise --unguided`. For seed 43, three pools of 50 (`ung_noise_s43`, `_s44`, `_s45`, same flags). One run is about 3 min.
2. `analysis/blind_axis.py` fits lobe I of every structure onto a base, takes the Kabsch rotation of lobe II, and uses the principal direction of the rotation vectors as the hinge axis. θ is the rotation-vector component along that axis, in degrees.
   - Base is the pool medoid: `cvf_ung_noise_s42_n50` model 20 for seed 42, `ung_noise_s43_s43_n50` model 6 for seed 43.
   - Axes are `[0.347, 0.938, 0.007]` (seed 42) and `[0.163, 0.917, −0.363]` (seed 43); the seeds agree at cos 0.98 after aligning the two base frames (`blind_axis_s43.json`).
   - The seed-43 axis is computed from the three unguided from-noise pools only.
   - The seed-42 axis is computed from 5630 structures in the pool sets named in `POOL_SETS` in `blind_axis.py`, taken from earlier campaigns (rows of `TeaA_cv/cv_values.csv`). By each run's `resolved_config.yaml`, about 1960 of them (35 %) come from HDX-guided runs: `hs_*` guided and `e_*`/`l1f02` variants (1350), `it1..3` (450) and `lgvC..E` plus the smoke run (160); the 150 `nmaG_..._bvcal` structures have no config on disk and are probably guided as well. Another 1500 (`hs_*`) and 450 (`it1..3`) were re-seeded from single structures ranked by HDX gain against the target (`hdx_seeds.py`, `iter_rank.py`). The 260 `lgv` structures were seeded from the 50 blind structures closest to the open MD reference (`near_open_seeds.py`: "references used for selection"). The remaining 2940 (`blind_all`) and 180 (`blind1_open`) are unguided.
   - The seed-42 axis is therefore not blind in the strict sense; the seed-43 axis is. Checked 2026-11-01 by recomputing the seed-42 axis on the same base from subsets of the pool (read-only; the stored axis is reproduced exactly from the full pool, cos 1.0000):

     | Pool subset | n | cos to stored axis | angle |
     |---|---|---|---|
     | unguided runs, without `lgv` | 3470 | 0.9928 | 6.9° |
     | `blind_all`, `blind1_open`, unguided `nmaG`, from-noise pool | 3320 | 0.9925 | 7.0° |
     | `blind_all` and from-noise pool | 2990 | 0.9858 | 9.7° |
     | from-noise pool alone | 50 | 0.9974 | 4.2° |

     The stored axis is 4.4° from the MD open-state rotation axis, and the unguided-only axes are 6–8° from it. The unguided-only axis is 7° from the stored one; the seed-43 axis is 11.8° from it (cos 0.979 after aligning the base frames). Random 150-structure subsets of the unguided pool give a median of 10° from the stored axis (5th percentile cos 0.961).

### 2. Step 1: metadiffusion along the hinge (`cv_metad`)

Overrides common to every round (`~/_runtime/patch_test/pre_metad/metad_common_cap1.txt`):

```
cv_metad=true  cv_metad_base=<base pdb>  cv_metad_axis=[<axis>]
cv_force_fit=1-122,207-249,284-309  cv_force_measure=123-206,250-283
cv_force_window=[0.7,0.75]  cv_force_alpha=0.3
cv_metad_height=1.0  cv_metad_sigma=3.0  cv_metad_kt=100.0  cv_metad_cap=1.0
cv_metad_history=<history csv>
gradient_every_step=true  residue_boltz_cap=null
alpha_schedule.start_frac=1.5  alpha_schedule.stop_frac=1.6
```

The window `[0.7, 0.75]` is denoising steps 140–149 of 200. In it, each structure moves by −alpha · dV/dθ · dθ/dx_Cα, rescaled per structure to at most `cv_metad_cap` Å per atom, and one Gaussian is then deposited at its θ with height h₀ exp(−V/kT). The HDX alpha window is empty (start_frac 1.5 is beyond the end of the schedule), so no HDX force acts in this step.

1. Four rounds from noise, `metad_r1..r4 42 --conditioning tmsa --from-noise` with the overrides above. The history CSV (`TeaA_cv/metad_history.csv`) carries the deposits from round to round. Seed 43 is `metad43_r1..r4` with `metad_history_s43.csv`. Seed-42 round 1 ran with `cv_metad_cap=0.1`, which is inert; it is not part of the step-1 union.
2. Eight continuation rounds, `cont_c1..c8` (seeds 101–108; seed 43 uses 301–308). Each is seeded from the previous round's 50 structures at step 140: `--seed-dir ~/_runtime/processed/TeaA_metad_seeds/c<N> --start-step 140 --diffusion-seed <s> --conditioning tmsa` plus the same overrides, history carried. The seed directories are symlinks to the previous round's models (`c1` links to `metad_r4`). One round is about 2 min.
3. The history files hold 6000 deposits each (12 rounds × 50 structures × 10 window steps).
4. Step-1 output is the union of rounds 2–4 and c1–c8 (550 structures), not the last round. Union θ range is −46..+22° (seed 42) and −43..+25° (seed 43).

### 3. Step 2: late-HDX refinement

1. Seeds: a θ-stratified subset of the step-1 union, at most 25 structures per 6° bin, split into five seed sets `TeaA_step2_seeds/k1..k5` (245 structures for seed 42, 234 for seed 43, of which 233 pass the pLDDT filter below), as symlinks into the step-1 runs. The seed-43 selection is `~/_runtime/patch_test/seed2/make_seeds_s43.py`; no script for the seed-42 selection was found.
2. Re-denoise from step 150 with HDX guidance:

```
refa025_k<i> <201..205> --seed-dir ~/_runtime/processed/TeaA_step2_seeds/k<i> \
  --start-step 150 --diffusion-seed <s> --conditioning tmsa \
  alpha_schedule.start_value=0.25  alpha_schedule.normalize_to_boltz=true \
  alpha_schedule.start_frac=0.75  alpha_schedule.stop_frac=1.0 \
  residue_boltz_cap=1.0  residue_boltz_floor_frac=0.25 \
  gradient_projection=torsion  projection_renormalize=true  projection_max_angle_deg=10 \
  lambda_schedule.start_value=1000  gradient_every_step=true
```

   Seed 43 uses seeds 401–405 and `refa025s43_k<i>`, submitted with `~/_runtime/patch_test/seed2/submit_step2_s43.sh`. One run is about 13–15 min. The MaxEnt refit runs every 5 steps, with 3 residue-split replicates (80 % train, `sequence_cluster` split).
3. Control: the same seed sets with `--unguided` (`ctl_k1..5`, `ctls43_k1..5`). Alpha 1.0 and 0.5 (`ref_k*`, `refa05_k*`) were run for seed 42 only.
4. Filter: structures with pLDDT below 0.7 are removed before scoring (run copies in `TeaA_sdedit_filt/*_p70`; for seed 43, `~/_runtime/patch_test/seed2/make_filt_s43.py`).

### 4. Step 3: reweighting and evaluation

1. MaxEnt over the union of the five refined pools, uniform prior, λ 100 and 1000: `analysis/teaa_scan_score.py` (batch wrapper `scan_score.sbatch`), with `SCAN_DUMP` set to write the per-structure weights (`TeaA_cv/sweep_a0.25_blind.csv`, `sweep_s43_a0.25_blind.csv`, and `sweep_s43fx_a0.25_blind.csv` for the rerun). `sweep_*_withref.csv` adds the true open and closed pools to the union.
2. Weight against θ, `analysis/weight_vs_theta.py`; pool-level checks with 6° θ bins as uniform-weight pools, pairwise mixtures and a simplex fit, `analysis/theta_bin_mix.py` (batch wrapper `theta_bin_mix.sbatch`) and `scan_pairmix.py`. These scripts default to the seed-42 axis. For seed 43 set `BLIND_AXIS_JSON` to `blind_axis_s43.json`; results scored without it use the seed-42 axis, whose 6° bins differ from the seed-43 bins.
3. Population recovery, `analysis/recovery.py`. This is the JAX-ENT definition (`jaxent.src.analysis.pf_variance`, `state_population`): base-2 Jensen–Shannon divergence over a strict support, recovery = 100 (1 − √JSD), with state from blind θ (open below −5°, closed above +5°, otherwise neither; target 0.40 / 0.60 / 0). It is an evaluation metric, never a loss.
4. Geometry: `theta_eval.py`, `hinge_eval.py`, and `landscape_plots.py` for the Cα PCA (fit on the MD open and closed frames with equal state weighting) and the RMSD landscapes.

Analysis scripts and score dumps are under `~/_runtime/analysis/` (`TeaA_cv/` for the dumps); the runs are under `/scratch/u6xq/hussain.u6xq/_runtime/runs/TeaA_sdedit/`, and the dump paths point at the home-directory copy of `_runtime/runs`.

## Settings that changed the outcome

- Per-atom HDX guidance applied every step never left the Boltz intermediate; a spring on the hinge coordinate moves the ensemble only inside steps 140–149 (above σ ≈ 3.4 Å the trunk erases the push, below σ ≈ 1.5 Å the hinge is frozen).
- A cap of 0.1 Å on the bias move is inert (0.4°/step against the 1.2°/step restoring pull); 1.0 Å works.
- 150 structures are needed for the blind axis (bootstrap cos 5th percentile 0.49 for 50, 0.83 for 150).
- HDX alpha 0.25 in the refinement fits as well as 1.0 and 0.5 without wrecked structures (at 1.0 eight structures with pLDDT 0.48–0.57 kept 5 % of the weight).

### 5. Seed 43 rerun with the corrected amide H

The synthetic-H error made the hydrogen-bond term near inert for every structure without H atoms, which includes the target (built on the Boltz topology) and all Boltz output. The target and the guided step 2 were therefore regenerated for seed 43, with BioFeaturisers `39b8069` vendored into MaxENT-FK (`externals/biofeaturisers`, commit `39db4b3`, local to Isambard and not pushed).

- **Rerun.** Target (`~/_submit/teaa_gentarget.sbatch`, writing over `raw_data/iso_target_biofeat/`; the earlier files are in `~/_runtime/analysis/TeaA_cv/pre39b8069/`), five refinement jobs (`refa025s43fx_k1..5`, seeds 401–405, `~/_runtime/patch_test/seed2/submit_step2_s43fx.sh`), the pLDDT filter (234 structures pass, against 233 before) and scoring (`jobs_score_s43fx.txt`, dumps `*_s43fx_*` in `TeaA_cv/`).
- **Not rerun.** The step-1 union (550 structures) and the unguided pools, because the bias and the unguided sampler use no HDX term. The union and the unguided control were re-weighted against the new target (`metad_s43fx_blind_weights.csv`, `step2_s43fx_ctl_blind.csv`).
- **Discarded batch.** A first set of refinement jobs (7960205 to 7960209) ran without the override prefix and is kept as `*_BAD_overrides_not_applied`; it is not scored.

Seed-43 results on the seed-43 axis (target 0.40 open : 0 intermediate : 0.60 closed). Strict recovery is the JAX-ENT definition above; the two-state figure is the same measure with the intermediate state removed.

| MaxEnt, λ 1000 (λ 100) | Before the fix (`43cc194`) | Corrected (`39b8069`) |
|---|---|---|
| Refined, open : intermediate : closed | 0.410 : 0.280 : 0.310 | 0.459 : 0.106 : 0.435 |
| Refined, strict recovery % | 58.3 (57.4) | 74.7 (70.1) |
| Refined, two-state recovery % | 85.6 | 90.3 |
| Unguided control, strict recovery % | 58.1 (62.5) | 54.0 (58.3) |
| Step-1 union alone, strict recovery % | 88.6 | 84.0 |
| Pool-level bin simplex, strict recovery % | 74.7 | 69.0 |
| Refined fit floor, ESS | 0.00345, 19.1 | 0.00280, 16.0 |

- Before the fix the refined ensemble did not beat its own unguided control on strict recovery. After it, refinement is about 20 points above the control at λ 1000.
- The union alone and the bin simplex are slightly worse after the fix, so the gain is specific to the refined ensemble.
- The open-side weight peaks at −18 to −12° (key −20.3°), against −30 to −36° before. The closed side peaks at +6 to +12° (key +9.1°). The 0 to +6° bin carries 0.002.
- The true open and closed pools still fit best at 0.49 open (0.485 before), so the forward model does not separate 0.40 from 0.50 open and 0.459 is inside that limit.
- One run per configuration with an ESS near 16; alpha 0.25 and λ were set on the pre-fix model and not retuned; the target changed with the model.

### 6. Regeneration of the corrected seed-43 refinement, and the Fiedler-lobe run (reported)

Both were run on 3 Nov 2026 and are recorded on Isambard in `~/_runtime/analysis/fiedler/NOTES.md` and `~/_runtime/analysis/fiedler/s43fx/REPORT.md` (copies in `figures/biofeat-teaa-landscape-F/source/`).

- **Regeneration.** The corrected seed-43 refinement runs of section 5 (jobs 7960257–7960261) were deleted, and `~/_submit/s43fx_re/submit.sh` reran them with the same seed sets, overrides, diffusion seeds 401–405, regenerated target and BioFeaturisers `39b8069` (jobs 8051545–8051549, scored 8052161–8052167). The record does not say why the first runs were deleted. The regenerated pool scores differently, so the section 5 refined numbers and `biofeat-teaa-landscape-s43fx` cannot be reproduced from the runs on disk.
- **Fiedler lobes.** The hand lobe split is replaced by lobes from Boltz's pair representation. The pair norm (last recycle) is thresholded at its 95th percentile, and the sign of the Fiedler vector of its graph Laplacian splits residues 1–309, with the larger block as lobe I (169 residues, fitted) and the smaller as lobe II (140, measured). It agrees with the hand split on 0.929 of residues, and the 22 differences are hand-lobe-I residues moved to lobe II. Two seeds' pair dumps give the same vector.
- **Fiedler axis.** Built from the same three unguided pools and base (`ung_noise_s43` model 6) with the Fiedler lobes (`blind_axis_fiedler.json`). It holds 0.515 of the rotation variance, its bootstrap |cos| has median 0.988 (5th percentile 0.902), and it lies at cos 0.972 to the seed-43 axis. Answer key, open −18.4°, closed +9.7°. The 150 unguided structures have θ from −2.2 to +1.8° (sd 0.63°).
- **Stage 1.** Seed-43 overrides with only the lobes and axis replaced, run as `metadF_r1..r4_s52_n50` (from noise, seed 52) and `contF_c1..c8_s501..508_n50`, chained with `afterok` from repository HEAD `24ac1bd` (job ids in the notes). The union of rounds 2–4 and c1–c8 has 550 structures with θ from −41.0 to +24.7°.
- **Stage 2.** At most 25 structures per 6° bin (rng 7) give 236 seeds in five sets. Refinement `refa025F_k1..5` uses the seed-43 overrides verbatim with diffusion seeds 601–605, and the control `ctlF_k1..5` uses seeds 611–615 on the same seed sets. The pLDDT filter removes none.
- **Scoring.** Jobs 8049979 (union), 8050281 (refined), 8050282 (refined with in-state pools), 8050283 (control) and 8050284 (θ bins and in-state mixtures). Weight against θ from `weight_vs_theta_F.py` (`~/_runtime/analysis/fiedler/out/wvt_*.txt`).

| Fiedler run | λ 1000 | λ 100 |
|---|---|---|
| Refined, open : intermediate : closed | 0.419 : 0.155 : 0.426 | 0.453 : 0.153 : 0.394 |
| Refined, strict recovery % (two-state) | 70.3 (91.8) | 69.5 (88.5) |
| Refined, fit floor (ESS) | 0.00268 (15.5) | 0.00350 (32.8) |
| Control, open : intermediate : closed | 0.357 : 0.408 : 0.235 | 0.454 : 0.243 : 0.302 |
| Control, strict recovery % (two-state) | 48.6 (82.7) | 60.1 (82.9) |
| Control, fit floor (ESS) | 0.0110 (5.1) | 0.0119 (27.4) |
| Union alone, open : intermediate : closed | 0.592 : 0.113 : 0.295 | 0.550 : 0.136 : 0.314 |
| Union alone, strict recovery % (two-state) | 67.1 (77.1) | 66.9 (79.8) |
| Union alone, fit floor (ESS) | 0.0108 (22.8) | 0.0116 (32.2) |
| Refined with in-state pools, fit floor (ESS) | 0.00213 (18.5) | 0.00294 (83.7) |

Uniform weights give 58.4 % (refined), 59.2 % (control) and 59.8 % (union). The refined λ 1000 weight peaks at −24 to −18° (0.188, containing the open reference) and at +12 to +24° (0.342, beyond the closed reference at +9.7°). On the MD PCA plane 9.8 % of the refined weight lies inside the MD open 95 % region and 7.7 % inside the closed one, against 40.0 and 59.5 % for the MD mixture (`figures/biofeat-teaa-landscape-F/summary.csv`).

In-state mixtures (20 open and 20 closed `TeaA_inState` structures, uniform inside each pool) fit the target with MSE 0.0110 at 0 open, 0.00591 at 0.40, a minimum of 0.00572 at 0.491, 0.00573 at 0.50 and 0.0114 at 1. These are Boltz structures near each reference, not the target's MD frames, so the minimum MSE is not zero. The refined pool reaches a lower floor (0.0027) than any in-state mixture.

| Same-settings comparison, λ 1000 | Section 5 run (deleted) | Regeneration | Fiedler run |
|---|---|---|---|
| open : intermediate : closed | 0.459 : 0.106 : 0.435 | 0.443 : 0.233 : 0.324 | 0.419 : 0.155 : 0.426 |
| Strict recovery % (two-state) | 74.7 (90.3) | 61.6 (84.9) | 70.3 (91.8) |
| Control strict recovery % | 54.0 | 54.0 | 48.6 |
| Fit floor (ESS) | 0.0028 (16.0) | 0.0038 (18.0) | 0.0027 (15.5) |
