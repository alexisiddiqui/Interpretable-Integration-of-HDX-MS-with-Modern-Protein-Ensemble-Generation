# 06 jax-Ka

Chapter hub for `thesis/chapters/06-jax-ka.tex`. Moved from the §1.7 hub on 2026-10-14; argument order not yet set. Its place in the thesis is the pH thread ([[01-introduction]] §1.1 D3, §1.2 group 2, §1.3 group 2), and [[prion protein|MoPrP]] carries it. A pKa model that differentiates through backbone coordinates is a second forward model of the kind ch. 5 builds. The titration models (PROPKA, PypKa, constant-pH MD, pKAI, KaML) are introduced in the chapter preface, not in [[02-background]] §2.5.

Status sentence: in progress (frozen relational default, interface experiments open). **decision**: full research chapter, short chapter, or appendix. `DEADLINES.md` has no entry for it.

## Detail moved from §1.7

- A backbone-only pKa predictor, the orientation Graph Query Transformer (oGQT) with relational edges: a spatial residue graph plus explicit ±1 and ±2 sequence edges, a separate key and value projection per relation, and titratable-site query tokens. Trained on pKPDB (PypKa labels) and PINDER complexes labelled by pKAI in the bound and free states, with a binding-shift loss and a burial auxiliary. Its readout differentiates through backbone coordinates. Stub (`projects/4-jax-Ka/code` `models/ogqt-relational-50-frozen`).
- What the current results test: that relational edges improve backbone-only pKa prediction (selection error 0.649 to 0.632 over three seeds at 50% of the pool, `experiments/4_backbone/08_frozen_relational.md`); that an experimental-pH auxiliary adds nothing (the head learns crystal against EM, not pH; `07_handoff.md`).
- The earlier Kd-ratio numbers (under 9% all-atom, 30% backbone, under 20% transformer) are not in the current records and are dropped.
- Application to test: which MoPrP sites change protonation between pH 4 and pH 7, and whether they sit in the regions that unfold.

## Drafting sources

- `projects/4-jax-Ka/code` experiment records (`experiments/4_backbone/`); chapter tex comments (`06-jax-ka.tex`).
- `kb/inbox/2026-10-14 pKa chapter 6 preface.bib` for the preface papers, pending Zotero import.
