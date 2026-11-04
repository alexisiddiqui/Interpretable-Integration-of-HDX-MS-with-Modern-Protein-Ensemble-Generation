#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-maxcal
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --array=0-1
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-maxcal-%A_%a.out

# Two-constraint MaxCal on structural observables (puf_maxcal.py), from the published per-frame microstates.
# Array task 0 = lag 5 ns (selected model), task 1 = lag 2 ns (sensitivity). Reads the campaign, writes only here.
set -euo pipefail
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
msm=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1/seeded_apo/msm
py=/home/coulson/oc/lina4225/_runtime/msm-env/bin/python
lags=(5 2); lag=${lags[$SLURM_ARRAY_TASK_ID]}
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
"$py" -u "$here/puf_maxcal.py" "$here/puf_cvs_tight.npz" "$here/puf_final.json" \
    "$msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag${lag}/msm_weights.npz" "$lag" "$here/puf_maxcal_lag${lag}.json" "$here"
