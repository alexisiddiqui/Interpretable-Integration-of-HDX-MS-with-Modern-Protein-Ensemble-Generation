# Fiedler-lobe (fully blind) stage 1 for TeaA — 2026-11-03

Goal: replace the hand lobe split (examples/TeaA/cv/cvs.yaml, lobe I = fit, lobe II = measure) with lobes from
the Boltz pair representation, re-derive the blind hinge axis, re-run the seed-43 stage-1 metad recipe.
All paths below are on Isambard (`ssh u6xq.aip2.isambard`); `F=~/_runtime/analysis/fiedler`.
Python commands run from `$REPO` with `OMP_NUM_THREADS=4 uv run --no-sync python` (login node, numpy only).

## 1. Fiedler lobes
```
R=~/_runtime/runs/TeaA_beta
python ~/_runtime/analysis/beta/latent_cov.py --recommended \
  --dumps $R/bstmsa_b0_s42_n50/pair_dump $R/bstmsa_b0_s43_n50/pair_dump --out $F/latent
python $F/make_lobes.py $F/latent/latent_thresh95_unnorm_per_residue.csv     # log: $F/make_lobes.log
```
- --recommended = pair norm thresholded at its 95th percentile, L = D - A, Fiedler u2; last recycle
  (recycle_03; final_z reproduces it). Tokens = residues 1-309 (default `--tokens lobes`; the hand lobes only
  select the protein residues 1-309, they partition 1-309, residue 310 is dropped as in the project convention).
- The two dumps give identical u2 (trunk is seed-independent; per-dump agreement 0.929 each).
- Rule: sign of the mean sign-aligned u2; LARGER block = lobe I (fit), smaller = lobe II (measure).
- RAW (used by the pipeline): lobe I 169 = 1-74,77,83-122,208-247,295,297-309 (segments 74,1,40,40,1,13);
  lobe II 140 = 75-76,78-82,123-207,248-294,296 (segments 2,5,85,47,1). Agreement with hand lobes 0.929.
  All 22 disagreements are hand-lobe-I residues moved to lobe II: 75-76,78-82,207,248-249,284-294,296.
  Islands < 3 residues: lobe I {77, 295}, lobe II {75-76, 296}. Mechanically fine (CA Kabsch over sets).
- Variant lobes_fiedler_min3.yaml (NOT used): runs < 3 residues flipped to the other lobe, weakest first
  (smallest mean |u2|), re-segmenting after each flip -> flips 295 (I->II), 75-76 (II->I);
  lobe I 170 = 1-77,83-122,208-247,297-309; lobe II 139 = 78-82,123-207,248-296; agreement 0.932.
- Files: $F/lobes_fiedler.yaml (+ lobes_fiedler_mapping.csv; cvs.yaml format, regions.file -> mapping csv),
  $F/lobes_fiedler_min3.yaml (+ _mapping.csv), $F/lobes_fiedler.json (raw lists, ranges, segments, u2 vector,
  min3 flips), $F/latent/ (latent_cov CSVs + plots).
- The hook takes the lobes as range strings (cv_force_fit / cv_force_measure overrides), no repo edit needed.

## 2. Blind axis
```
S=~/_runtime/runs/TeaA_sdedit
AXIS_POOLS=all python $F/blind_axis_fiedler.py --lobes $F/lobes_fiedler.yaml --out $F/blind_axis_fiedler.json \
  $S/ung_noise_s43_s43_n50 $S/ung_noise_s44_s44_n50 $S/ung_noise_s45_s45_n50          # log: $F/blind_axis_fiedler.log
python $F/compare_theta.py                                                             # log: $F/compare_theta.log
BLIND_AXIS_JSON=$F/blind_axis_fiedler.json python $F/theta_eval_fiedler.py label=run_dir ...
```
- blind_axis_fiedler.py = copy of ~/_runtime/patch_test/seed2/blind_axis_s43.py with --lobes/--out; the
  pivot "linker" = residues on both sides of every lobe-label change (pivot is diagnostic only; the hook
  uses base + axis). JSON also stores lobe_I/lobe_II.
- theta_eval_fiedler.py = copy of ~/_runtime/analysis/theta_eval.py that reads the lobes from the JSON
  (the original hard-codes the hand lobes, so it must NOT be used with the Fiedler JSON) and prints
  open(<-5)/closed(>+5) counts.
- Base unchanged: ung_noise_s43 model_6 (medoid by all-CA RMSD, lobe-independent).
- Axis [0.11455, 0.81281, -0.57115]; a . a_s43 = +0.972; frac var 0.515; bootstrap |cos| median 0.988 (5th 0.902).
- Answer key: theta(open ref) -18.4, theta(closed ref) +9.7 (s43: -20.3 / +9.1); |cos| MD open->closed 0.971.
- **Sign convention: OPEN = NEGATIVE theta, CLOSED = POSITIVE theta** (same as seed 43).
- 550 metad-union structures (metad43_r2..r4 + cont43_c1..c8): r(theta_F, theta_s43) = 0.9988,
  slope 0.935, intercept -0.04; open(<-5) 231 vs 241, closed(>+5) 161 vs 171. Per-structure: $F/compare_theta_union.csv.
- 150 unguided: theta_F sd 0.63 (s43 0.64), r 0.968, slope 0.95; per pool sd 0.67/0.71/0.47.

## 3. Stage-1 chain (~/_submit/fiedlerF/)
- make_overrides.sh -> metad_common_F.txt: seed-43 overrides (patch_test/seed2/metad_common_s43.txt) with ONLY
  cv_force_fit/cv_force_measure (RAW Fiedler lobes) and cv_metad_axis replaced (base identical).
- fiedlerF_sdedit.sbatch: copy of ~/_submit/teaa_sdedit.sbatch (job name fiedF, logs ~/_logs/fiedF_<jid>.out/.err)
  + echo of lobes/axis/answer key, in-job seed-dir build for cont rounds (symlinks to the previous round's 50
  PDBs, `ls | sort` order, as seed2/submit_cont.sh), history snapshot to $F/history_snapshots/.
- chain.sh <from> <to> [after_jid]: steps 1-4 = metadF_r1..r4_s52_n50 (from noise, seed 52, tmsa),
  5-12 = contF_c1..c8_s501..508_n50 (--seed-dir ~/_runtime/processed/TeaA_metad_seeds_F/c<i>, --start-step 140,
  --diffusion-seed 500+i, tmsa), each afterok on the previous. History $F/metad_history_F.csv (hook rewrites it).
- Commands: `./make_overrides.sh; ./chain.sh 1 1; ./chain.sh 2 12 8047392`; after the outage `./chain.sh 6 12`.
  Job ids (also ~/_submit/fiedlerF/jobs.txt): metadF_r1 8047392, r2 8047506, r3 8047507, r4 8047508,
  contF_c1 8047509 — all COMPLETED (2.5-3.5 min each; history 500 -> 2500 deposits; c1 log shows
  "seed dir .../TeaA_metad_seeds_F/c1 from metadF_r4_s52_n50: 50 structures" and 2000 history deposits loaded).
  ~16:51-17:18 the /home NFS mount was unreadable (Permission denied on /home/u6xq): contF_c2 8047510 FAILED
  in 3 s with no log, c3-c8 8047511-8047516 were cancelled by --kill-on-invalid-dep. Nothing was written for
  c2 (no run dir, no seed dir, history unchanged at 2500). Resubmitted c2-c8: 8048752 (c2, no dependency since
  c1 had completed), 8048770 (c3), 8048772, 8048773, 8048774, 8048775, 8048776 (c8), each afterok on the previous.
  If the chain breaks again: fix, then `./chain.sh <step> 12` (step 5+i = contF_c<i>); remove nothing, the
  script refuses to overwrite an existing run dir.
- Deviations from the seed-43 recipe: --cpus-per-task=72 (resource only); jobs chained with afterok instead of
  hand submission; runs from the current repo HEAD (24ac1bd at r1, clean tree), not the Oct-30 tree.
- Finished rounds (theta_F; $F/eval_F_r1-c1.txt): r1 +0.3 sd 3.6 [-6.5,6.5] open 5/closed 2; r2 -1.5 sd 5.9
  21/13; r3 -0.2 sd 6.4 19/16; r4 -0.6 sd 6.7 [-11.7,10.2] 20/15; c1 -1.0 sd 10.9 [-16.8,13.6] 23/24, pLDDT
  0.967 -> 0.949. Seed 43 for comparison (s43 axis): r4 -1.0 sd 7.4 [-12.2,10.0]; c1 -2.0 sd 11.0 [-16.7,13.3].

## 4. Evaluating a finished round
```
~/_submit/fiedlerF/eval_F.sh <label> ~/_runtime/runs/TeaA_sdedit/<run> <jobid>
# or directly:
BLIND_AXIS_JSON=$F/blind_axis_fiedler.json python $F/theta_eval_fiedler.py [--hist] lab=<run_dir> ...
```
Hinge counts: open = theta < -5, closed = theta > +5 under blind_axis_fiedler.json (open is negative).
Union for stage 2 (as seed 43): metadF_r2..r4 + contF_c1..c8 (550 structures).

## 5. Stages 2-3 on the Fiedler union (2026-11-03)
- union_theta_F.py -> union_theta_F.csv (550; 1 out of range at +24.7); make_seeds_F.py (rng 7, <=25/6-deg bin)
  -> step2_seeds_F.csv (236; path,theta,plddt,bin) + processed/TeaA_step2_seeds_F/k1..k5 (48,47,47,47,47).
- ~/_submit/fiedlerF/submit_step2_F.sh (refa025s43 overrides verbatim): refa025F_k1..5_s601..605 8049941/43/45/47/49,
  ctlF_k1..5_s611..615 8049942/44/46/48/50 (controls on seeds 61x, s43 reused 40x). make_filt_F.py: 0 dropped.
- Scoring (jobs_score_F.txt): F_metad 8049979, F_blind 8050281, F_withref 8050282, F_ctl 8050283,
  F_bins 8050284 (fiedlerF/theta_bin_mix_F.sbatch -> theta_bin_mix_F.py). weight_vs_theta_F.py / theta_bin_mix_F.py
  = copies reading lobes from the axis JSON. Outputs out/wvt_*.txt, out/filt_F.txt, figs_F.py -> out/F_*.png.
- Refined union: uniform 0.0073, floor l1000 0.0027 (ESS 15.5); ctl 0.0110; joint 0.0021, refined keep 0.67.
  wvt l1000: open 0.419 / mid 0.155 / closed 0.426; strict JSD 70.3% (2-state 91.8%). Closed peak +12..+24.
- teaa_scan_score hingeO/hingeC columns still come from hinge_eval.py (hand lobes, RMSD rule): diagnostic only.
