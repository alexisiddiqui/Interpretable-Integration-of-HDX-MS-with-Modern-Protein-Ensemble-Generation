---
type: decision
date: 2026-10-29
project: jax-Ka
status: active
---

## Decision

Sites near removed or unmodelled material are masked at a distance where the label error from that material falls below a noise target. The practical target is 0.1 pKa, and any error well under 0.5 pKa is acceptable. The component masks (buffers, glycans) are set tighter, at about 0.01 pKa for training and 0.001 pKa for evaluation, because their error was measured with PROPKA. PROPKA has finite interaction ranges, so its error reaches zero within about 22.5 Å and the stricter targets cost few sites. The gap masks keep the 0.1 pKa criterion, because they were measured with PypKa and pKAI, and PypKa's own numerical noise sits near 0.01 pKa.

## Alternatives considered

- Use 0.1 pKa for every mask. Rejected for the components. The PROPKA curves fall through 0.1 pKa at about 12.5 Å and through 0.001 pKa by about 20 Å, so the stricter targets move the radii by under 10 Å.
- Use 0.001 pKa for the gap masks. Rejected. PypKa deletion errors flatten at about 0.01 pKa out to 80 Å, so 0.001 cannot be resolved.

## Why

A mask keeps labels that depend on removed material out of the loss, and its radius trades label noise against lost supervision. PROPKA's hard cutoffs make the tight targets cheap for components. The same targets are not reachable for the gap masks, so those use the practical target.

## Consequences

- Buffers use 15 Å for training and 20 Å for evaluation. After removing all tested buffers, the largest change in ΔpKa was 0.0385 beyond 15 Å and 0.00208 beyond 20 Å (`experiments/1_benchmark/14_buffer_sensitivity.md`, `15_buffer_mask_revision.md`).
- Glycans use 20 Å for training and 25 Å for evaluation (`12_glycan_sensitivity.md`). These are deliberately conservative, about 5 Å beyond where the glycan PROPKA curve meets the 0.01 and 0.001 targets (about 17.5 and 20 Å). Glycans shield the protein surface from solvent and distort the conformation around them, and the PROPKA test captures neither, because it removes the glycan from fixed protein coordinates. Shielding was measured separately at the same fixed coordinates (`audits/glycan-protein-sasa-v1`, 29 complexes, 6,444 site observations across AB and free states). Titratable functional groups lost SASA only within 10 Å of the glycan (median 12 Å² within 5 Å). Whole residues lost at most 6.6 Å² between 10 and 15 Å and nothing beyond 15 Å. Geometric shielding therefore lies inside the 20 Å training radius, and the margin covers conformational distortion, which no test has measured. Other ligands (15/25 Å), exposed ions (25/25 Å) and buried metals (30/30 Å) follow the same scheme.
- Ligands and metals were measured in one PROPKA pilot (`audits/propka-components-v1`, `experiments/1_benchmark/06_missing_residue_policy.md`, 17 ligand and 11 metal complexes). Its script (`src/pkabench/propka_components.py`, hash matches the run manifest) right-justified component atom names. PROPKA 3.5.1 infers the element from name columns 13–14, so any component atom with a one- or two-character name lost its element. Protein atoms were written correctly.
  - Metals are unaffected in practice. PROPKA types ions by residue name, and every metal received its ION group and charge (Zn²⁺, Fe³⁺, Cu²⁺, Ca²⁺, Mn²⁺). Metal changes reached 1.376 pKa out to 20 Å and were zero from 25 Å, which sets the exposed-metal radius.
  - Small ligands were affected. Acetate, formate, succinate, pyruvate and PEG fragments lost their carboxylate or ether typing, so their removal effect was underestimated. Drug-like ligands with three-character names (for example `C01`, `N13`) were typed correctly.
  - The ligands were rerun with the corrected formatter from `buffer_pilot.py` (`audits/propka-components-v2-ligands`, same 39 tasks). Typing was restored in 12 of the 17 completed complexes (PEG, formate, succinate, pyruvate, MES and others gained their groups). Near-contact changes grew (AB pKa change up to 3.85 against 0.54 in v1), but the distance tail did not move. The largest ΔpKa change was 0.035 beyond 15 Å, 0.0017 beyond 20 Å and zero from 25 Å, the same tail as the buffers, so the 15/25 Å ligand radii stand.
  - The same 22 ligand complexes failed in both runs, 14 on component atom retention and 8 on CCD identifiers wider than the PDB residue-name field. The formatter did not cause them.
- Gap masks use the anchor-tier criterion: the upper 95% bound on the 95th-percentile error is below 0.1 pKa in each 5 Å band (`experiments/4_backbone/05_pinder_dataset.md`).
- The radii are operational uncertainty masks, not physical error bounds. A thesis sentence about them names the teacher the distance curve was measured with.
- Plots: `audits/buffer-propka-v2/plots/all_buffers_error_vs_distance`, `audits/glycan-propka-ccd-v1/plots/error_vs_distance` and `audits/radial-error-v2-nearcomplete/plots/error_vs_distance`, all on Coulson. They draw the 0.1 pKa line only. The component radii are drawn against the 0.01 and 0.001 targets in one figure, `figures/jaxka-component-cutoffs` (ligands, buffers, glycans, metals). The gap radii are drawn against the 0.1 target, one panel per tested gap length, in `figures/jaxka-gap-cutoffs` (appendix).
