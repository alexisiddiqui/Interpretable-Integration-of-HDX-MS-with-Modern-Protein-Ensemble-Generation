#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-s2b
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-s2b-%j.out

# Stage 2b: qc_prepare.sh on the 24 unit-off runs, then the fixed tests (puf_stage2b.py). qc_analyse.py is not used, because it looks seeds up in
# seeds_manifest.json, which has no unit_off entries; puf_stage2b.py makes the same bond and LINCS checks. Writes run qc/ folders and results here.
set -euo pipefail
source /home/coulson/oc/lina4225/_HPC/install/BioFeat/activate.sh
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
export QC_NS=100 OMP_NUM_THREADS=1 JAX_PLATFORMS=cpu
export PYTHONPATH="${c}/figures:/home/coulson/oc/lina4225/BioFeaturisers${PYTHONPATH:+:${PYTHONPATH}}"
sed "s#^#${c}/seeded_apo/runs/#" "${c}/seeded_apo/runs/task_list_unit_off.txt" | xargs -P 24 -L 1 bash "${c}/seeded_apo/qc_prepare.sh"
"${BIOFEAT_PLUMED_PYTHON}" -u "$here/puf_stage2b.py" "$c/figures/basin_frames/pca101_scores.npz" "$here/puf_final.json" "$here/puf_stage1_rig.npz" "$c" \
    "$here/puf_stage2b.json" "$here/puf_stage2b_rig.npz"
