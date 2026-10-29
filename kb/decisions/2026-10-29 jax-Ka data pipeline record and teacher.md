---
type: decision
date: 2026-10-29
project: jax-Ka
status: active
---

## Decision

The jax-Ka data pipeline is described as one pipeline, from what was run, and pKAI is its teacher.

- **Record.** Where the build specification and a later note or run output disagree, the later note and the run output are the record. `experiments/00_shared.md` is the original specification. Its preparation table (reject ligands, glycans and metals) and its 10/20 Å gap rule were replaced by the strip-and-mask policy (`07_stripped_reference_policy.md`, `15_buffer_mask_revision.md`) and the calibrated gap rule (`4_backbone/05_pinder_dataset.md`).
- **One pipeline.** Benchmark structures and pretraining pools share the same preparation and masking. They differ in scale, in training and evaluation radii, and in which labels are attached.
- **Teacher.** pKAI labels PINDER and is the training teacher, because it agrees more closely with PypKa. pKPDB supplies PypKa labels directly. pKAI+ is not a teacher. It is scored as a method in the benchmark and compared on PKAD.
- **pKPDB versions.** Its labels come from PypKa versions whose API changed over the years, so they are not equivalent to our PypKa 2.10.0 teacher configuration. The thesis states this in one sentence. Across the whole dataset, a version difference is likely to matter less than an error in preparing the structures.

## Alternatives considered

- Describe benchmark and pretraining as separate pipelines. Rejected; the code path and masks are shared.
- Leave the teacher open between pKAI and pKAI+. Rejected. The gap calibration measured both, but the labels used for training are pKAI's.
- Reproduce the historical pKPDB settings before using its labels. Rejected as disproportionate to the effect.

## Why

The thesis describes what was done, and the specification only recorded what was planned. Naming one teacher also fixes what the student is trained to imitate and so what its accuracy is bounded by.

## Consequences

- The chapter 6 hub states pKAI as the teacher and PypKa as the benchmark reference.
- The historical-equivalence caveat appears once, in the pKPDB description (`experiments/1_benchmark/18_historical_pkpdb_settings.md` holds the evidence).
