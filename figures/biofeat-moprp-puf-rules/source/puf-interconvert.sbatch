#!/usr/bin/env bash
#SBATCH --job-name=moprp-puf-ic
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-ic-%j.out

# PUF1 <-> PUF2 candidate interconversion at each pH (puf_interconvert.py). Writes only here.
set -euo pipefail
here=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
/home/coulson/oc/lina4225/_runtime/msm-env/bin/python -u "$here/puf_interconvert.py" "$here/puf_cvs_tight.npz" "$here/puf_final.json" "$here/puf_interconvert.json"
