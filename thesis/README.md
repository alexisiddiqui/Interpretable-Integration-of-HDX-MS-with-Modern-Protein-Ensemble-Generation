# Thesis

Build from this folder with `latexmk -pdf -outdir=build main.tex` (biber is required for the bibliography).

- `chapters/NN-<name>.tex` — one file per chapter; chapters 03–06 map to `projects/1-4`.
- `references.bib` — the single bibliography. Citation keys double as KB literature note names (`kb/papers/@<citekey>.md`).
- Figures are pulled from `../figures/<fig-id>/fig.pdf`.
