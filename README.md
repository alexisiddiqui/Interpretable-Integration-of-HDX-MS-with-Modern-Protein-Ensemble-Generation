# Interpretable Integration of HDX-MS with Modern Protein Ensemble Generation

DPhil thesis repository: research projects, knowledge base, figures and the thesis itself.

| Folder | Contents |
|---|---|
| `thesis/` | LaTeX source of the thesis (`main.tex`, chapters, single `references.bib`) |
| `projects/` | One folder per research project; code, analyses and manuscripts as pinned submodules |
| `milestones/` | Confirmation of status (2025-11) as a submodule; the transfer report is superseded by the ValDX paper |
| `figures/` | One folder per figure, named by figure ID, with the script that makes it |
| `kb/` | Obsidian vault: claims, concepts, literature notes, decisions |
| `examples/` | Reference theses and their structure maps |

| Project | Chapter | Latex | Manuscript/Chapter Status |
|---|---|---|---|
| `projects/1-ValDX` | `thesis/chapters/03-valdx.tex` | `projects/1-ValDX/manuscript/main_omc.tex` | `manuscript` (post-review) |
| `projects/2-jaxENT` | `thesis/chapters/04-jaxent.tex` | `projects/2-jaxENT/manuscript/main.tex` | `draft-manuscript` (confirmation, outdated experiments) |
| `projects/3-BioFeaturisers` | `thesis/chapters/05-biofeaturisers.tex` | n/a | `none` (preliminary experiments) |
| `projects/4-jax-Ka` | `thesis/chapters/06-jax-ka.tex` | n/a | `none` (preliminary experiments) |

## Setup
```
git clone --recurse-submodules https://github.com/alexisiddiqui/Interpretable-Integration-of-HDX-MS-with-Modern-Protein-Ensemble-Generation.git
cd Interpretable-Integration-of-HDX-MS-with-Modern-Protein-Ensemble-Generation
# or, in an existing clone without submodules:
git submodule update --init
```

Build the thesis (needs latexmk and biber):
```
cd thesis && latexmk -pdf -outdir=build main.tex
```

After `git pull`, bring submodules to the pinned commits:
```
git submodule update --init
```
