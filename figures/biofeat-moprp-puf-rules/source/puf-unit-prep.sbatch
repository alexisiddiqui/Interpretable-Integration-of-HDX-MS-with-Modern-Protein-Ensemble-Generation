#!/usr/bin/env bash
#SBATCH --job-name=moprp-unit-prep
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=48G
#SBATCH --time=01:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules/puf-unit-prep-%j.out

# Stage 2b: select the 12 unit-off seeds and build each at both pH with build_seed.py. New paths only, seeds/unit_off and runs/{ph4,ph7}/unit_off.
set -euo pipefail
source /home/coulson/oc/lina4225/_HPC/install/BioFeat/activate.sh
rules=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules
campaign=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
figures="${campaign}/figures"; here="${campaign}/seeded_apo"
export OMP_NUM_THREADS=1 JAX_PLATFORMS=cpu PYTHONPATH="${figures}:/home/coulson/oc/lina4225/BioFeaturisers${PYTHONPATH:+:${PYTHONPATH}}"
py="${BIOFEAT_PLUMED_PYTHON}"
for t in ph4 ph7; do [[ ! -e "${here}/runs/${t}/unit_off" ]] || { echo "runs/${t}/unit_off exists"; exit 1; }; done
[[ ! -e "${here}/runs/task_list_unit_off.txt" && ! -e "${here}/build_jobs_unit_off.txt" ]] || { echo "unit_off lists exist"; exit 1; }
"${py}" "${rules}/select_unit_seeds.py" "${figures}" "${figures}/basin_frames/pca101_scores.npz" "${rules}/puf_final.json" "${rules}/puf_stage0_mipb.npz" \
    "${here}/seeds/unit_off" "${here}/seeds_unit_off_manifest.json"
n=0
for target in ph4 ph7; do
    build="$(cat "${campaign}/${target}-build-path.txt")"
    for seed in "${here}"/seeds/unit_off/seed_*.pdb; do
        name="$(basename "${seed}" .pdb)"; n=$((n + 1))
        echo "${seed} ${build} ${here}/runs/${target}/unit_off/${name} $((20261104 + n))" >> "${here}/build_jobs_unit_off.txt"
        echo "${target}/unit_off/${name}" >> "${here}/runs/task_list_unit_off.txt"
    done
done
xargs -P "${SLURM_CPUS_PER_TASK:-24}" -L 1 "${py}" "${here}/build_seed.py" < "${here}/build_jobs_unit_off.txt"
echo "built $(wc -l < "${here}/build_jobs_unit_off.txt") systems"
