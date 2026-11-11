#!/bin/bash
#SBATCH --job-name=poisk-ptx-control
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --time=00:30:00
#SBATCH --output=/scratch/bulk/hussain/poisk-protenix-control-20261110/logs/%A_%a.log
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=8 PYTHONDONTWRITEBYTECODE=1
cd /scratch/bulk/hussain/poisk-protenix-control-20261110
nvidia-smi --query-gpu=name,memory.total --format=csv
/scratch/bulk/hussain/_runtime/opig-adaptyv-2026/force-refold/protenix/env/bin/python -u control.py run
