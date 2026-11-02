# jaxka-relational-memory

Training-path cost of the relation-map GQT configurations (the arms of `jaxka-relational-edges`): attended edges per training graph, full-backprop GPU memory and step time against graph size. Rendered on the Coulson login node by `pkabench.relation_memory` (`render` mode, jax-Ka repo `src/pkabench/relation_memory.py`) in the `radial-plots` environment, 2026-11-02.

- Graphs: sampled on Isambard with `relation_memory sample` through the training loaders (`PinderSource` / `PkpdbSource` with the backbone table, batch-16 bucket policy), 50% pool training split, seed 20261102. 150 PINDER complexes (AB and free graphs) and 150 pKPDB structures for the edge counts; for each size bucket, the largest training PINDER complex.
- Measurements: Coulson comp1400, one A40 each, job 779030 (`relation-memory.sbatch`, `ogqt-main-7c3e3e9` environment, code snapshot `audits/relation-memory-v1/src3`). One process per configuration, buckets ascending. Each size: compile, one call for the measured peak (`peak_bytes_in_use`), then 10 timed calls, median reported. Model: `make_model` with each run's width and `production_variant`, orientation and dihedral inputs, fresh initialisation (the 65-parameter burial head omitted). Objective: `DropoutEngine`'s PINDER objective (dropout 0.1), 16 complexes × 2 states, the PINDER half of a training step.
- An earlier run without timing (jobs 778839 after 778838 was cancelled) gave the same peaks to 0.01 GiB; its tables are in `audits/relation-memory-v1/run1/` on Coulson.
- Files: `fig.*` (copied unchanged from `audits/relation-memory-v1/plots/relation_memory.*`), `edges.csv` (per graph: residue-graph edges, added sequence edges, full-attention pairs), `memory.csv` (per configuration and bucket: compiled footprint, measured peak, compile and step times), `slurm.csv` (recorded host memory of the 21 Isambard training jobs).
- Regenerate: on Coulson, `PYTHONPATH=<src> envs/radial-plots/bin/python -m pkabench.relation_memory render audits/relation-memory-v1`.

## Peak training memory

Every training batch is padded to a size bucket, so the largest bucket (1,536 residues) sets the training peak. Measured peak GPU memory of the full-backprop step there:

| Config | Parameters | Peak GPU, 1,536 residues (GiB) | Step time, 1,536 (ms) | Median attended pairs per graph | Slurm MaxRSS, mean of runs (GiB) |
|---|---|---|---|---|---|
| w64 | 139,745 | 7.34 | 115 | 78,518 | 21.4 (3) |
| w76 | 194,993 | 7.93 | 266 | 78,518 | 20.8 (3) |
| 1/1 | 148,065 | 7.54 | 132 | 78,518 | 19.5 (3) |
| 4/1 | 160,545 | 7.75 | 136 | 78,518 | 19.7 (3) |
| 6/1 | 168,865 | 7.82 | 138 | 78,518 | 18.7 (3) |
| 4/4 | 173,025 | 7.81 | 140 | 78,518 | 21.0 (1) |
| 6/4 | 181,345 | 7.94 | 141 | 78,518 | 21.8 (1) |
| 6/6 | 189,665 | 7.96 | 143 | 78,518 | 20.4 (3) |
| 4/1 full | 160,549 | 9.91 | 175 | 205,608 | 21.4 (1) |

GPU memory was not recorded during the Isambard training runs: `gres/gpumem` is listed in `AccountingStorageTRES` but no GPU gather plugin runs, so the field is empty. The only recorded peak is the batch step's host MaxRSS (`slurm.csv`, jobs matched by name or by the selection line of the job log). It is dominated by the 15 loader workers and prefetch, and varies more between seeds (16.1–22.6 GiB) than between configurations.

## Notes

- The ±1, ±2 sequence edges of the relation maps are always inside the 20 Å residue graph, so they add no edges: the eight graph configurations attend identical pairs, and relation maps change only which projection each edge reads. Full attention replaces layer 2 with every allowed residue pair (N² in the bound branch, within-chain in the free branch).
- Memory in the line panel is the compiled footprint (temporaries + arguments + outputs) of each size's executable. The measured peak is a running maximum over the process, so at small sizes it reports start-up overhead; from 640 residues the two agree within 2%.
- w76 is slow at every size (2.3× w64 at 1,536 residues). It uses 4 heads of 19 channels, not a multiple of 8. Its Isambard training jobs also took 35 min against 21 min for w64.
