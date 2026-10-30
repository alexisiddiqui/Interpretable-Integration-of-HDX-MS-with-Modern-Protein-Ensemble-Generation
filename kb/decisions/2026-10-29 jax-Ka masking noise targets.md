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
- Glycans use 20 Å for training and 25 Å for evaluation (`12_glycan_sensitivity.md`). These are deliberately conservative, about 5 Å beyond where the glycan PROPKA curve meets the 0.01 and 0.001 targets (about 17.5 and 20 Å). Glycans shield the protein surface from solvent and distort the conformation around them, and the PROPKA test captures neither. It removes the glycan from fixed protein coordinates and does not measure the change in protein SASA. It recorded only the glycan's own SASA and exposed fraction. Other ligands (15/25 Å), exposed ions (25/25 Å) and buried metals (30/30 Å) follow the same scheme; no error-against-distance plot for them has been located.
- Gap masks use the anchor-tier criterion: the upper 95% bound on the 95th-percentile error is below 0.1 pKa in each 5 Å band (`experiments/4_backbone/05_pinder_dataset.md`).
- The radii are operational uncertainty masks, not physical error bounds. A thesis sentence about them names the teacher the distance curve was measured with.
- Plots: `audits/buffer-propka-v2/plots/all_buffers_error_vs_distance`, `audits/glycan-propka-ccd-v1/plots/error_vs_distance` and `audits/radial-error-v2-nearcomplete/plots/error_vs_distance`, all on Coulson. They draw the 0.1 pKa line only.
