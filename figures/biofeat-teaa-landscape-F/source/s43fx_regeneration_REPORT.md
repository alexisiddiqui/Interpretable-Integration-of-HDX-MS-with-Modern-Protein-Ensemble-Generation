# s43fx regeneration (current forward model), 2026-11-03

Dropped (pLDDT<0.7): refined 0/234 (k1-5 47,47,47,47,46 all kept); controls 0 dropped (dry-run; scored as raw ctls43_k*, as in the s43 scoring, since ctls43_k*_p70 never existed). Stale dangling dirs refa025s43fx_k*_p70 from the deleted runs were renamed to *.stale_dangling (not deleted) so make_filt_s43.py could write the new ones.
Jobs: refine refa025s43fx_k1-5 = 8051545-49 (13-16 min, clean). Scoring: blind 8052161, withref 8052162, ctl 8052164, orig-rescore 8052165, bins(s43 axis) 8052166, bins(Fiedler axis) 8052167.

| lambda 1000 unless noted | s43fx (hand theta) | s43fx (Fiedler theta) | orig s43 rescored (hand theta) | Fiedler run |
|---|---|---|---|---|
| uniform MSE | 0.00837 | 0.00837 | 0.00770 | 0.0073 |
| floor (ESS) | 0.00380 (18.0) | 0.00380 (18.0) | 0.00353 (14.5) | 0.0027 (15.5) |
| control floor | 0.01155 | 0.01155 | same ctl 0.01155 | 0.0110 |
| joint floor / refined keep | 0.00235 / 0.51 | 0.00235 / 0.51 | not run | 0.0021 / 0.67 |
| open fraction (<-5) | 0.443 | 0.441 | 0.387 | 0.42 |
| within +-5 | 0.233 | 0.223 | 0.365 | 0.155 |
| open peak bin | -24..-18 (0.196) | -24..-18 (0.240) | -36..-30 (0.165) | -24..-18 |
| closed peak bin | +6..+12 (0.201) | +6..+12 (0.180) | +6..+12 (0.186) | +12..+24 |
| strict JSD rec % (two-state) | 61.6 (84.9) | 62.7 (85.8) | 51.3 (82.1) | 70.3 (91.8) |
| uniform JSD strict (two-state) | 57.5 (78.0) | 57.1 (79.0) | 57.9 (78.5) | - |
| control MaxEnt JSD strict (two-state) | 54.0 (76.3) | 54.2 (76.6) | - | - |
| pool best pair (f_open, MSE) | -15/+9 (0.40, 0.00693) | -15/+9 (0.45, 0.00722) | not run | -21/+21 (0.55, 0.00669) |
| pool simplex MSE; masses | 0.00684; -33 .11, -15 .31, +9 .55, +21 .04 | 0.00707; -15 .46, +9 .45, +21 .10 | not run | 0.00645 |

lambda 100 floor: s43fx 0.00429 (ESS 33.8), orig rescored 0.00431, ctl 0.01252, joint 0.00301.

Weight vs theta, lambda 1000, 6-deg bins (weight, n), s43fx pools:

| bin | hand theta | Fiedler theta |
|---|---|---|
| <-36 | 0.000 (4) | 0.000 (3) |
| -36..-30 | 0.019 (13) | 0.005 (5) |
| -30..-24 | 0.063 (20) | 0.030 (24) |
| -24..-18 | 0.196 (20) | 0.240 (22) |
| -18..-12 | 0.104 (30) | 0.096 (27) |
| -12..-6 | 0.060 (26) | 0.070 (27) |
| -6..0 | 0.194 (31) | 0.196 (35) |
| 0..+6 | 0.041 (33) | 0.041 (33) |
| +6..+12 | 0.201 (28) | 0.180 (28) |
| +12..+18 | 0.114 (21) | 0.136 (25) |
| +18..+24 | 0.007 (7) | 0.006 (5) |
| >+24 | 0.002 (1) | 0.000 (0) |

Files: ~/_runtime/analysis/fiedler/s43fx/ (sweep_*.csv, wvt_s43axis_*.txt, wvt_Faxis_*.txt, filt.txt); logs ~/_logs/s43fxR_*; scripts ~/_submit/s43fx_re/.
