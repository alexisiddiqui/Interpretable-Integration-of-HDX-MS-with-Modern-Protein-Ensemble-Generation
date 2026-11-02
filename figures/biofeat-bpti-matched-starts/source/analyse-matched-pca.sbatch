#!/usr/bin/env bash
#SBATCH --job-name=bpti-matched-pca
#SBATCH --clusters=swan
#SBATCH --partition=standard-cpu
#SBATCH --nodelist=naga03.cpu.stats.ox.ac.uk
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --chdir=/tmp
set -euo pipefail
export CAMPAIGN_ROOT=/bitbucket/hussain/BioFeaturisers-production/BPTI/seq0-starts-seq2/20261018T135410Z
export MPLCONFIGDIR=${CAMPAIGN_ROOT}/analysis/pca-comparison/cache/matplotlib
export XDG_CACHE_HOME=${CAMPAIGN_ROOT}/analysis/pca-comparison/cache
export OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
mkdir -p "$MPLCONFIGDIR"
/bitbucket/hussain/BioFeaturisers-multiarch/.runtime/plumed-jax-mpi-cuda12/env/bin/python "${CAMPAIGN_ROOT}/scripts/analyse-matched-pca.py"
