# Interpretable Integration of HDX-MS with Modern Protein Ensemble Generation

DPhil thesis repository: research projects, knowledge base, figures and the thesis itself.

| Folder | Contents |
|---|---|
| `thesis/` | LaTeX source of the thesis (`main.tex`, chapters, single `references.bib`) |
| `projects/` | One folder per research project: pinned code submodule, analyses, manuscript |
| `milestones/` | Transfer (2024-10) and confirmation (2025-11) of status materials |
| `figures/` | One folder per figure, named by figure ID, with the script that makes it |
| `kb/` | Obsidian vault: claims, concepts, literature notes, decisions |
| `examples/` | Reference theses and their structure maps |

| Project | Chapter |
|---|---|
| `projects/1-ValDX` | `thesis/chapters/03-valdx.tex` |
| `projects/2-jaxENT` | `thesis/chapters/04-jaxent.tex` |
| `projects/3-BioFeaturisers` | `thesis/chapters/05-biofeaturisers.tex` |
| `projects/4-jax-Ka` | `thesis/chapters/06-jax-ka.tex` |

## Setup
```
git clone --recurse-submodules <this-repo>
cd thesis && latexmk -pdf -outdir=build main.tex
```
