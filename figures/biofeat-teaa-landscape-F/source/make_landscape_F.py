"""Make fiedler/landscape_plots_F.py from landscape_plots_s43fx.py: Fiedler-run pools, weights, axis and lobes for theta."""
from pathlib import Path

A = Path.home() / "_runtime/analysis"
src = (A / "landscape_plots_s43fx.py").read_text()
reps = [
    ('OUT = A / "landscapes_s43fx"', 'FD = RT / "analysis/fiedler"\nOUT = FD / "landscapes_F"'),
    ('''    "metad_union": {"runs": [S / f"metad43_r{k}_s43_n50" for k in (2, 3, 4)]
                    + [S / f"cont43_c{k}_s30{k}_n50" for k in range(1, 9)],
                    "weights": A / "metad_s43fx_blind_weights.csv"},
    "refined_a025": {"runs": sorted(SF.glob("refa025s43fx_k*_p70")),
                     "weights": A / "sweep_s43fx_a0.25_blind.csv"},
    "control": {"runs": sorted(S.glob("ctls43_k*")),
                "weights": A / "step2_s43fx_ctl_blind.csv"},''',
     '''    "metad_union": {"runs": [S / f"metadF_r{k}_s52_n50" for k in (2, 3, 4)]
                    + [S / f"contF_c{k}_s50{k}_n50" for k in range(1, 9)],
                    "weights": FD / "metad_F_blind_weights.csv"},
    "refined_a025": {"runs": sorted(SF.glob("refa025F_k*_p70")),
                     "weights": FD / "sweep_F_a0.25_blind.csv"},
    "control": {"runs": sorted(SF.glob("ctlF_k*_p70")),
                "weights": FD / "step2_F_ctl_blind.csv"},'''),
    ('_info = json.load(open(A / "blind_axis_s43.json"))',
     '_info = json.load(open(FD / "blind_axis_fiedler.json"))\n'
     'THFIT = np.array([i for i, r in enumerate(RES) if r in set(_info["lobe_I"])])\n'
     'THMEAS = np.array([i for i, r in enumerate(RES) if r in set(_info["lobe_II"])])'),
    ('''    R1, t1 = kabsch(X[FIT], _B[FIT])
    Y = X @ R1.T + t1
    R2, _ = kabsch(_B[MEAS], Y[MEAS])''',
     '''    R1, t1 = kabsch(X[THFIT], _B[THFIT])
    Y = X @ R1.T + t1
    R2, _ = kabsch(_B[THMEAS], Y[THMEAS])'''),
    ('("Refined α0.25, uniform (234, pLDDT≥0.7)"', '("Refined α0.25, uniform (236, pLDDT≥0.7)"'),
    ('("Control, uniform (234)"', '("Control, uniform (236)"'),
    ("TeaA seed 43 (corrected amide H)", "TeaA Fiedler lobes (corrected amide H)"),
    ("Seed 43 (corrected amide H)", "TeaA Fiedler lobes (corrected amide H)"),
]
for a, b in reps:
    n = src.count(a)
    assert n >= 1, (a[:60], n)
    src = src.replace(a, b)
(A / "fiedler/landscape_plots_F.py").write_text(src)
print("wrote", A / "fiedler/landscape_plots_F.py")
