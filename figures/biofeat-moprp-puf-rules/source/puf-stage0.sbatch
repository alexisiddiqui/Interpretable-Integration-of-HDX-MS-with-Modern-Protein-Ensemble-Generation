#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-s0
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-s0-%j.out

# Stage 0: rule variables on the MI+PB frames (puf_stage0.py). Reads the campaign, writes only here.
set -euo pipefail
source /home/coulson/oc/lina4225/_HPC/install/BioFeat/activate.sh
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
export OMP_NUM_THREADS=4
"${BIOFEAT_PLUMED_PYTHON}" -u "$here/puf_stage0.py" "$c/figures/basin_frames/pca101_scores.npz" "$here/puf_final.json" "$c" "$here/puf_stage0_mipb.npz"
