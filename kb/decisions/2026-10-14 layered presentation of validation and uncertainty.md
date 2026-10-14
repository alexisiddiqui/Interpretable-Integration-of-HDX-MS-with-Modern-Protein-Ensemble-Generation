---
type: decision
date: 2026-10-14
project:
status: active
---

## Decision

Chapter 2 §2.4 presents validation and uncertainty in three layers, and the vault encodes each layer in a fixed way.

| Layer | Where in the vault | Evidence rule | Thesis treatment |
|---|---|---|---|
| 1a. Established method applied silently (MSE, a train/validation split, gradient optimisation, k-means) | No note; at most an alias on an existing concept | None | Used without citation, as a loss function is |
| 1b. Established principle whose upshot the thesis states ([[model averaging]], dependence-aware [[data splitting]], [[model selection]] versus evaluation, [[error covariance]] weighting) | Concept note, `## Definition`, with one general source | `basis: stated`; a claim leaves draft once a block passes the lint | One citation, then one sentence restating the upshot in HDX terms |
| 2. What integrative biophysics does, and where it diverges from layer 1 | A `## In integrative practice` section in the concept note | Paper blocks; any survey-style statement is `inferred` and scoped to "the studies examined" | Credit what each check achieves, then name what it leaves open |
| 3. Our application or contribution | `## Why it matters here` in the concept, plus a method note | `draft` until a figure ID or a posted-preprint quote | Marked "(revised ValDX only)", "(jaxENT, draft)" or "(ours)" |

The `## In integrative practice` section is new. The lint does not police section names, so no schema change is needed.

## Alternatives considered

- Cite nothing for layer 1b, as for MSE. Rejected. The thesis bridges statistical learning and integrative structural biology, and the upshot of averaging or of dependence-aware partitioning is exactly what the second field lacks. One citation each makes the bridge visible.
- Put layer 2 in claim notes only. Rejected. A claim is one sentence; the divergence from layer 1 needs the comparison laid out next to the principle it diverges from.
- Describe the field's validation as uniformly poor. Rejected. Crystallography has cross-validated since the free R value, cross-link and SAXS refinements withhold restraints, and HDXer and XylE test sensitivity to parameters and to omitted peptides. The defensible statement is that no HDX ensemble-integration study examined partitions the data around peptide dependence.

## Why

The two §2.4 subsections on uncertainty and cross-validation sit on established statistics that the integrative literature applies unevenly. Without a fixed layering, a reader cannot tell which sentences are textbook, which describe the field, and which are ours. The layering also fixes the evidence each kind of sentence needs, so the lint can enforce it.

## Consequences

- New concepts [[experimental uncertainty]], [[model averaging]], [[cooperative unfolding unit]], [[model selection]] and [[error covariance]] follow the table.
- Two general sources remain to be acquired: a statistical-learning text for averaging and nested selection, and a source on validation with dependent observations. Until then the layer 1b claims that need them stay draft.
- Method notes carry layer 3 for ValDX splitting and consensus, and for jaxENT observation weighting, selection and evaluation design.
- The jaxENT manuscript describes a legacy selection path; the vault records the current policy and flags the manuscript for update rather than the other way round.
