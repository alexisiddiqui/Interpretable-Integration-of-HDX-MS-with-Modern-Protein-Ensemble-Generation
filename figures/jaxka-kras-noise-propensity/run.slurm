#!/bin/bash
#SBATCH --clusters=srf_gpu_01
#SBATCH --partition=standard-gpu,old-standard-gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=24G
#SBATCH --time=01:00:00
#SBATCH --job-name=kras_noise
#SBATCH --output=/scratch/bulk/hussain/kras-noise-propensity-20261110/analysis.log
set -euo pipefail
cd /scratch/bulk/hussain/kras-noise-propensity-20261110
export PYTHONUNBUFFERED=1 OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 XLA_PYTHON_CLIENT_PREALLOCATE=false
export NOISE_MODEL=/scratch/bulk/hussain/tnf-gqt-retro/jax-ka-305b074/models/ogqt-allres15-within-hmask-50
/scratch/bulk/hussain/poisk-drsa-20261110/venv/bin/python analyse.py
