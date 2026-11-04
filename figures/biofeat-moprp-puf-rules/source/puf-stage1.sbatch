#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-s1
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-s1-%j.out

# Stage 1 fixed tests on the held-out seeds (puf_stage1.py). Runs after moprp-seed-qc.sbatch has written qc/whole.xtc. Writes only here.
set -euo pipefail
source /home/coulson/oc/lina4225/_HPC/install/BioFeat/activate.sh
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
export OMP_NUM_THREADS=4
"${BIOFEAT_PLUMED_PYTHON}" -u "$here/puf_stage1.py" "$c/figures/basin_frames/pca101_scores.npz" "$here/puf_final.json" "$here/puf_cvs_tight.npz" \
    "$c/seeded_apo/qc/cartesian_features.npz" "$c" "$c/seeded_apo/runs/task_list_half2_ph7_3.txt" "$here/puf_stage1.json" "$here/puf_stage1_rig.npz"
