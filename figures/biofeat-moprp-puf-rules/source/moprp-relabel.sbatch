#!/usr/bin/env bash
#SBATCH --job-name=moprp-relabel
#SBATCH --partition=oc
#SBATCH --nodelist=comp1400
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=16
#SBATCH --mem=96G
#SBATCH --time=02:00:00
#SBATCH --output=/home/coulson/oc/lina4225/_runtime/moprp_relabel/relabel-%j.out

# Redraw the MoPrP figure sets with the structural state names. Each figure is made by the script and arguments that made
# the original (recovered from the session that made them); relabel_run.py replaces text only, at save time.
# RELABEL_MAP set: apply that map. Unset: draw unchanged and write the text inventory. RELABEL_OUT: output folder name.
# The main MSM free-energy map comes from msm_build.py itself, so the main model is rebuilt into the output folder, never over msm/;
# its maximum-likelihood results match the original exactly. The summary is redrawn from the original report (msm_summary_replot.py),
# because the rebuild resamples the Bayesian intervals.
set -euo pipefail
c=/home/coulson/oc/lina4225/_runtime/BioFeaturisers/cuda-86/campaigns/moprp-paired-50ns-20260925-v1
s=$c/seeded_apo; R=/home/coulson/oc/lina4225/_runtime/moprp_puf_rules; W=/home/coulson/oc/lina4225/_runtime/moprp_relabel
out=$W/${RELABEL_OUT:-out}; mkdir -p "$out/msm_main"
py=/home/coulson/oc/lina4225/_runtime/msm-env/bin/python
export OMP_NUM_THREADS=2 OPENBLAS_NUM_THREADS=2 MKL_NUM_THREADS=2
pca=$c/figures/basin_frames/pca101_scores.npz
EQ=qc/task_list_ext100_100ns.npz,qc/task_list_ext100b_100ns.npz,qc/task_list_ext100c_100ns.npz
ED=qc/task_list_ext100_dihedrals.npz,qc/task_list_ext100b_dihedrals.npz,qc/task_list_ext100c_dihedrals.npz
cfgs="cartpca10_all-kmall_k100_lag2 cartpca10_all-kmall_k100_lag5 cartpca10_all-kmall_k200_lag5 cartpca10_tica10all-unbiased_k100_lag2 cartpca10_tica10all-unbiased_k100_lag5 distpca10_tica10all-unbiased_k100_lag2 distpca10_tica10all-unbiased_k100_lag5"
dirs=""; for x in $cfgs; do dirs="$dirs msm/ext6_$x msm/ext12_$x"; done
cd "$s"

step() { local n=$1; shift; if env RELABEL_INVENTORY="$out/inv_$n.jsonl" "$@" > "$out/$n.log" 2>&1; then echo "$n ok"; else echo "$n FAILED"; fi; }
r=("$py" -u "$W/relabel_run.py")

step msm_main env MSM_EMBED=none MSM_KMEANS_FIT=all MSM_FEATURE_SET=all MSM_FEATURES="$s/qc/cartpca10_features.npz" MSM_K=100 MSM_LAG_NS=5 \
    OMP_NUM_THREADS=4 "${r[@]}" msm_build.py qc/task_list_half1_20ns.npz qc/task_list_half1_dihedrals.npz "$EQ" "$ED" "$pca" basins_seed.json "$out/msm_main" &
step msm_plots env MSM_PLOTS_DATA="ext6 = 6 × 100 ns + 6 × 20 ns seeds per basin and pH; ext12 = 12 × 100 ns per non-folded basin and pH" \
    "${r[@]}" msm_plots.py "$out/msm_ext12" msm/ext12_cartpca10_all-kmall_k100_lag5 $dirs &
step macro "${r[@]}" macro_structure.py qc/cartesian_features.npz "$pca" basins_seed.json "$out/macro_structure_ext12_maxcal2" 15 \
    msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag5/msm_report.json &
step segment "${r[@]}" segment_maxcal_plots.py "$out/segment_maxcal_ext12" msm/ext12seg_q0.5_cartpca10_all-kmall_k100_lag5 \
    msm/ext12seg_q0.3_cartpca10_all-kmall_k100_lag2 msm/ext12seg_q0.3_cartpca10_all-kmall_k100_lag5 msm/ext12seg_q0.5_cartpca10_all-kmall_k100_lag2 \
    msm/ext12seg_q0.5_cartpca10_all-kmall_k100_lag5 &
step fes2 "${r[@]}" fes_maxcal_plots.py msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag5 basins_seed.json "$out/fes_maxcal2_k100_lag5" &
step paths "${r[@]}" trajectory_paths.py "$EQ" "$ED" qc/task_list_half1_20ns.npz qc/task_list_half1_dihedrals.npz "$pca" basins_seed.json "$out/seeded_paths_ext12" &
step flow "${r[@]}" flow_map.py qc/task_list_half1_20ns.npz "$pca" basins_seed.json "$out/seeded_flow_ext12_tau1ns" 1.0 qc/task_list_half1_dihedrals.npz \
    --extend "$EQ" "$ED" --compare-early-late 20 &
step flow_signed "${r[@]}" flow_map.py qc/task_list_half1_20ns.npz "$pca" basins_seed.json "$out/seeded_flow_ext12_tau1ns_magcontours_signed" 1.0 \
    qc/task_list_half1_dihedrals.npz --extend "$EQ" "$ED" --magnitude-contours --signed-delta &
step cartpca "${r[@]}" torsion_pca.py qc/cartesian_features.npz basins_seed.json "$out/cart_pca_unbiasedfit_ext12" cart none &
step puf_plots "${r[@]}" "$W/src/puf_plots.py" "$R/puf_cvs_tight.npz" "$R/puf_final.json" basins_seed.json "$out/moprp_puf" &
step puf_clusters "${r[@]}" "$W/src/puf_clusters.py" "$R/puf_cvs_tight.npz" "$R/puf_final.json" basins_seed.json "$out/moprp_puf" &
step msm_summary "${r[@]}" "$W/msm_summary_replot.py" msm/ext12_cartpca10_all-kmall_k100_lag5/msm_report.json "$out/msm_ext12_main_summary.png" &
for lag in 5 2; do
    step puf_c_lag$lag "${r[@]}" "$R/puf_c_heatmap.py" "$R/puf_cvs_tight.npz" "$R/puf_final.json" \
        "msm/ext12seg2_q0.5_cartpca10_all-kmall_k100_lag${lag}/msm_weights.npz" "$lag" qc/cartesian_features.npz "$pca" basins_seed.json "$out/moprp_puf_c_lag${lag}" &
done
wait
ls "$out"/*.png | wc -l
