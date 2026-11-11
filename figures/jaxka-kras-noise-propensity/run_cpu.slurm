#!/bin/bash
#SBATCH --clusters=srf_cpu_01
#SBATCH --partition=standard-cpu,high-opig-cpu
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --job-name=kras_noise_cpu
#SBATCH --output=/scratch/bulk/hussain/kras-noise-propensity-20261110/analysis.log
set -euo pipefail
cd /scratch/bulk/hussain/kras-noise-propensity-20261110
export NOISE_DEVICE=cpu JAX_PLATFORMS=cpu PYTHONUNBUFFERED=1 OMP_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
export NOISE_MODEL=/scratch/bulk/hussain/tnf-gqt-retro/jax-ka-305b074/models/ogqt-allres15-within-hmask-50
/scratch/bulk/hussain/poisk-drsa-20261110/venv/bin/python analyse.py
