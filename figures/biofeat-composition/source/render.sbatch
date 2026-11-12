#!/bin/bash
#SBATCH --partition=high-opig-cpu
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
#SBATCH --time=00:30:00
#SBATCH --job-name=thesis-biofeat
#SBATCH --output=render-%j.log
set -euo pipefail
export MPLCONFIGDIR="$PWD/mpl" OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
py=/scratch/bulk/hussain/opig-adaptyv-2026-writeup/.tools/pymol/env/bin/python
"$py" source/render_moprp.py inputs/basins/frames101_trim out/structures
python source/moprp_basins.py inputs out/structures out
python source/moprp_main.py inputs out
python source/teaa_main.py inputs/teaa out inputs/teaa
q=inputs/seeded/qc
EQ=$q/task_list_ext100_100ns.npz,$q/task_list_ext100b_100ns.npz,$q/task_list_ext100c_100ns.npz
ED=$q/task_list_ext100_dihedrals.npz,$q/task_list_ext100b_dihedrals.npz,$q/task_list_ext100c_dihedrals.npz
python source/moprp_flow.py source/flow_map_original.py "$q/task_list_half1_20ns.npz" inputs/basins/pca101_scores.npz inputs/seeded/basins_seed.json out/moprp_flow_main 1.0 "$q/task_list_half1_dihedrals.npz" --extend "$EQ" "$ED" --magnitude-contours --signed-delta --contour-planes pca
