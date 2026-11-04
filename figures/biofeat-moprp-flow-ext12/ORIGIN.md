# biofeat-moprp-flow-ext12

Reference figure set for the drift (flow) maps of the 144 MoPrP basin-seeded unbiased trajectories (24 × 20 ns + 120 × 100 ns, 12.48 μs). It is not yet planned as a thesis figure. Protocol in `kb/experiments/bf-moprp.md`.

- `seeded_flow_ext12_tau1ns`: mean displacement over τ = 1 ns per bin, divided by τ, on the 101-HDX-residue Cartesian PCA plane (left) and the JAX-ENT dihedral plane (right). Rows are runs at pH 4, runs at pH 7, and the pH 7 minus pH 4 difference for the same 72 seeds. Bins need at least 200 pairs from at least 3 runs. Arrows give direction and are coloured by speed; grey contours are unbiased MD log density; dark and mid green circles are the pH 4 and pH 7 basins.
- `seeded_flow_ext12_tau1ns_magcontours_signed`: the same field with speed as contour lines and arrow length proportional to speed; the bottom row is the signed speed change (blue faster at pH 4, red faster at pH 7).
- `seeded_flow_ext12_tau1ns_early_late`: pooling check, the drift from pairs starting before against after 20 ns.
- Source: local mirror `~/Coulson-Chemistry/moprp_results/` (copied 2026-11-03, byte-identical). SHA-256 prefixes: `24bfe66d` seeded_flow_ext12_tau1ns, `dfdf11f6` seeded_flow_ext12_tau1ns_magcontours_signed, `7c9882d5` seeded_flow_ext12_tau1ns_early_late.
- Code: `source/flow_map.py`, copied from `~/Coulson-Chemistry/moprp_seeded/`.
