#!/usr/bin/env bash
#SBATCH --job-name=moprp-flow-split
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=48G
#SBATCH --time=00:45:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_relabel/flow-split-%j.out
# Flow map with speed contours on the PCA plane and direction arrows on the dihedral plane (flow_map.py --contour-planes pca),
# relabelled with relabel_map.json. Inputs and other arguments as seeded_flow_ext12_tau1ns_magcontours_signed.
set -euo pipefail
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1; W=/home/coulson/oc/lina4225/_runtime/moprp_relabel
EQ=qc/task_list_ext100_100ns.npz,qc/task_list_ext100b_100ns.npz,qc/task_list_ext100c_100ns.npz
ED=qc/task_list_ext100_dihedrals.npz,qc/task_list_ext100b_dihedrals.npz,qc/task_list_ext100c_dihedrals.npz
export OMP_NUM_THREADS=4 RELABEL_MAP=$W/relabel_map.json
cd $c/seeded_apo
/home/coulson/oc/lina4225/_runtime/msm-env/bin/python -u $W/relabel_run.py $W/src/flow_map.py qc/task_list_half1_20ns.npz $c/figures/basin_frames/pca101_scores.npz \
    basins_seed.json $W/out/seeded_flow_ext12_tau1ns_pca_contours 1.0 qc/task_list_half1_dihedrals.npz --extend "$EQ" "$ED" \
    --magnitude-contours --contour-planes pca --signed-delta
