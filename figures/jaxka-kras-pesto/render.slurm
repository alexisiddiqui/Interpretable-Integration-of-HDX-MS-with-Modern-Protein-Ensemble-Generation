#!/bin/bash
#SBATCH --clusters=srf_cpu_01
#SBATCH --partition=standard-cpu,high-opig-cpu
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:30:00
#SBATCH --job-name=kras_pesto
#SBATCH --output=/scratch/bulk/hussain/kras-pesto-20261111/render.log
set -euo pipefail
cd /scratch/bulk/hussain/kras-pesto-20261111
export PYTHONDONTWRITEBYTECODE=1
/scratch/bulk/hussain/opig-adaptyv-2026-writeup/.tools/pymol/env/bin/python -c 'import pymol; pymol.finish_launching(["pymol","-cq"]); import runpy; runpy.run_path("render_pymol.py",run_name="__main__"); pymol.cmd.quit()'
/scratch/bulk/hussain/writeup-render2/venv/bin/python compose.py
