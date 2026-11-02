# jaxka-coordinate-gradients

Cost of the coordinate-only gradient for the relation-map GQT configurations: GPU memory and time against complex size. Rendered on the Coulson login node by `pkabench.relation_memory` (`render-coord` mode, jax-Ka repo `src/pkabench/relation_memory.py`) in the `radial-plots` environment, 2026-11-02.

- Gradient: parameters fixed, d(sum of squared predicted shifts)/d(backbone coordinates) for one complex in the bound and free states, no dropout. Features are rebuilt from coordinates by the structural endpoint (`pkanet.differentiable.StructureFeatures`; `pkanet.relational.RelationalStructureFeatures` appends the backbone table and isolates chains in the free state), then each configuration's production forward (`model_inputs` with its `production_variant`).
- The rebuild uses dense N × N candidate pairs, so every configuration scales quadratically here, including the graph ones. These curves describe the current implementation, not an online feature computation tuned for coordinate gradients.
- Complexes: for each size bucket, the largest training PINDER complex (the same complexes as `jaxka-relational-memory`), unpadded.
- Measurements: Coulson comp1400, one A40, job 779031 (`relation-coord.sbatch`, `ogqt-main-7c3e3e9` environment, code snapshot `audits/relation-memory-v1/src3`). One process per configuration, sizes ascending. Each size: compile, one call, then 10 timed calls, median reported. Memory is the compiled footprint (temporaries + arguments + outputs); the measured peak is a running maximum and reports start-up overhead below about 640 residues. Fresh initialisations.
- Files: `fig.*` (copied unchanged from `audits/relation-memory-v1/plots/coordinate_gradients.*`), `coord.csv` (per configuration and size: footprint, measured peak, compile and gradient times).
- Regenerate: on Coulson, `PYTHONPATH=<src> envs/radial-plots/bin/python -m pkabench.relation_memory render-coord audits/relation-memory-v1`.

| Config | Memory, 1,500 residues (GiB) | Gradient time, 1,500 (ms) | Gradient time, 1,024 (ms) |
|---|---|---|---|
| w64 | 1.46 | 87 | 30 |
| w76 | 1.52 | 1,150 | 204 |
| 1/1 | 1.62 | 84 | 35 |
| 4/1 | 1.63 | 86 | 35 |
| 6/1 | 1.63 | 86 | 35 |
| 4/4 | 1.62 | 86 | 35 |
| 6/4 | 1.63 | 86 | 35 |
| 6/6 | 1.62 | 86 | 36 |
| 4/1 full | 1.61 | 67 | 29 |

- Full attention is the fastest configuration on this path: every configuration already works on dense pairs, and its layer 2 is a dense product where the graph layers gather neighbours.
- w76 is slow at every size (13× w64 at 1,500 residues). It uses 4 heads of 19 channels, not a multiple of 8. Its Isambard training jobs also took 35 min against 21 min for w64.
