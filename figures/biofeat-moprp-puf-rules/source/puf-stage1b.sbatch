#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-s1b
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-s1b-%j.out

# Frame-based pH comparison of the band runs (puf_stage1b.py). Reads the stored measures and seed structures, writes only here.
set -euo pipefail
source /home/coulson/oc/lina4225/_HPC/install/BioFeat/activate.sh
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
export OMP_NUM_THREADS=4
"${BIOFEAT_PLUMED_PYTHON}" -u "$here/puf_stage1b.py" "$here/puf_final.json" "$here/puf_cvs_tight.npz" "$c/seeded_apo/qc/cartesian_features.npz" \
    "$here/puf_stage1_rig.npz" "$c/seeded_apo/runs" "$here/puf_stage1b.json"
