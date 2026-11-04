#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-c
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=24G
#SBATCH --time=02:00:00
#SBATCH --array=0-1
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-c-%A_%a.out

# MaxCal C at pH 4, MSM cluster populations at both pH, heatmap and free-energy maps. Task 0 = lag 5 ns, task 1 = lag 2 ns.
set -euo pipefail
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
py=/home/coulson/oc/lina4225/_runtime/msm-env/bin/python
lags=(5 2); lag=${lags[$SLURM_ARRAY_TASK_ID]}
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
"$py" -u "$here/puf_c_heatmap.py" "$here/puf_cvs_tight.npz" "$here/puf_final.json" \
    "$c/seeded_apo/msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag${lag}/msm_weights.npz" "$lag" "$c/seeded_apo/qc/cartesian_features.npz" \
    "$c/figures/basin_frames/pca101_scores.npz" "$c/seeded_apo/basins_seed.json" "$here/moprp_puf_c_lag${lag}"
