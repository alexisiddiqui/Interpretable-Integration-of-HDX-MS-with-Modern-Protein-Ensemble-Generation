# Knowledge base

Obsidian vault for the thesis. Open **this folder** (`kb/`) as the vault, not the repository root.

## Folders
| Folder | Contents | Note name |
|---|---|---|
| `chapters/` | One hub note per chapter: the argument in order, linking to its claims | `03-valdx` |
| `claims/` | One claim per note | The claim as a full sentence |
| `concepts/` | Definitions and background ideas | Concept name |
| `methods/` | Mathematical and experimental methods | Method name; project (methods may differ between projects) |
| `papers/` | Literature notes | `@<citekey>` (matches `thesis/references.bib`) |
| `decisions/` | Why a method, parameter or dataset was chosen | `YYYY-MM-DD <decision>` |
| `inbox/` | Unsorted notes; triage weekly | anything |
| `_templates/` | Note templates (set as the Templates folder in Obsidian) | — |

## Rules
- One idea per note.
- Put links inside the body text where they are used, not in "related" lists.
- Every claim needs at least one `evidence` entry (a figure ID or a `[[@citekey]]`) before its status leaves `draft`.
- Chapter hub notes list claims in argument order, so each hub reads straight through as an outline of the chapter.
- Figures are referred to by their ID (the folder name under `figures/`) everywhere: KB, `.tex` and analyses.
