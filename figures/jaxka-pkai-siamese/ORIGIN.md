# jaxka-pkai-siamese

Two tables, not a figure: joint pKPDB/PINDER training of the native pKAI architecture against pKPDB-only training, with all-atom or backbone input. `table.tex` holds both (`tab:jaxka-pkai-joint`, `tab:jaxka-pkai-fraction`), in the booktabs style of the ch. 3 tables. Written 2026-11-02.

- Source: jax-Ka repo `experiments/3_paired_complex/48_pkai_joint_scale.md` (last changed in 31fc9d0). Values are transcribed from the note, not re-read from the run files.
- `tab:jaxka-pkai-joint`: atom16 encoding, 15 Å / 250 slots, 100% pool, 5.12e-4 cosine over 40 epochs. pKPDB, PINDER state and all-site paired MSE from "Cosine schedule and the 12 arms at 100%"; interface paired MSE from "Interface paired metrics". Released pKAI row from "Interface paired metrics" (pKPDB 0.324, state 0.0070, paired 0.0012 all sites, 0.0028 interface).
- `tab:jaxka-pkai-fraction`: atom16, batch 4,096, LR 8e-6 constant, cap 400. 10% and 50% from "Fraction scaling"; all four fractions from "75% and 100% (atom16)". pKPDB training sites from the same sections (154,539; 872,450; 1,306,448; 1,724,738).
- Runs: Isambard benchmark runtime, `training/pkai-joint-scale-v1` (10%) and `training/pkai-joint-scale-v1-f<pct>`; each run's `validation-v2.json` sits beside its `best.pt`.
- Validation: the frozen 5k-pilot pKPDB validation package and the 400-complex PINDER validation cohort (11,455 sites, 5,116 at the interface). Selection is on unweighted validation metrics; pKPDB-only arms select on pKPDB MSE alone and are scored on PINDER afterwards.
- Limits: seed 17 only. Joint training adds the PINDER state losses and the Siamese binding-shift loss together, so the comparison does not isolate the Siamese loss.
