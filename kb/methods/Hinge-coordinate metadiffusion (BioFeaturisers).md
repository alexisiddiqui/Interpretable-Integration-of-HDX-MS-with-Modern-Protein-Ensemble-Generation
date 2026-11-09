---
type: method
project: 3-BioFeaturisers
status: draft
needs_review: true
review_reason: The cv_metad bias code (MaxENT-FK commit 4a22611, branch teaa-iso-frame-uptake) is on Isambard and not pushed, so the code links below cover only the HDX guidance and MaxEnt refit at the pinned submodule commit; add links for the bias after pushing and updating the submodule.
code:
  - projects/3-BioFeaturisers/meta-diffusion@02d90d7:src/maxent_fk/guidance/config.py#L42-L46
  - projects/3-BioFeaturisers/meta-diffusion@02d90d7:src/maxent_fk/guidance/config.py#L186-L189
  - projects/3-BioFeaturisers/meta-diffusion@02d90d7:src/maxent_fk/guidance/hook.py#L1350-L1362
sources:
  - "[[@barducciWelltemperedMetadynamicsSmoothly2008#^c5]]"
---

<!-- Note name: Hinge-coordinate metadiffusion (BioFeaturisers). Concepts: [[guided diffusion]], [[diffusion model]], [[enhanced sampling]], [[ensemble reweighting]], [[maximum entropy principle]], [[HDX protection-factor model]]. Experiment: kb/experiments/bf-teaa.md. -->

## What it does

Guidance from HDX data alone cannot make a diffusion model leave the conformation it settles on early. Applied at every step, the per-atom HDX gradient is incoherent across atoms and overshoots, and the TeaA ensemble never left the Boltz intermediate. A bias on a single collective variable acts coherently on every atom and can push the ensemble into states the sampler would not otherwise reach. The method therefore separates two jobs. The bias supplies coverage of a collective variable. The HDX data then decide which of the covered states are populated.

The method has two parts, and the second needs only a differentiable coordinate, not the first. Part A constructs the coordinate from the model's own fluctuations (a hinge angle, with no MD reference), and is optional if the coordinate is known. Part B biases the denoising along that coordinate, refines the covered structures against the HDX data, and reweights them with MaxEnt. Its populations come from the reweighting, not from the bias. Guided diffusion samples are not equilibrium-weighted ([[guided diffusion]]), so the bias is not read as a free-energy estimate.

## Part A: constructing the hinge coordinate

The coordinate is the rotation of one body of the protein relative to the other, so it needs a split into two bodies. The reported TeaA run takes the split from Boltz's pair representation, as the two signs of the Fiedler vector of the graph Laplacian of the pair norm thresholded at its 95th percentile (lobe I 169 residues, lobe II 140, agreeing with the earlier hand split on 0.929 of residues; [[bf-teaa]] §6). Its purpose is to give the bias a direction in which the model's own conformational variation is largest, without using a reference structure.

1. Draw about 150 unguided structures from noise. Fifty give a poorly determined axis; 150 give a stable one (bootstrap cosine, 5th percentile 0.49 against 0.83).
2. Take the medoid (lowest mean all-Cα RMSD) as the base.
3. For every structure, fit body I onto the base and find the rotation that carries the base's body II onto the structure's body II. Write it as a rotation vector.
4. The hinge axis is the principal direction of those rotation vectors, signed so that most of the pool has positive angle. The angle $\theta$ of a structure is its rotation-vector component along the axis, in degrees.

For seed 43 the axis holds 49 % of the rotation variance and comes only from three unguided from-noise pools. The MD open and closed references are used afterwards, to print an answer key, and never to build the axis.

## Part B: metadiffusion, refinement and reweighting

**Bias.** Biasing acts only in a short window of the denoising, steps 140 to 149 of 200 ($\sigma$ about 3.4 to 1.5 Å). Pushes applied earlier are erased by the trunk, and below about 1.5 Å the hinge is frozen. In the window every residue moves with its Cα along $-\alpha\,\mathrm{d}V/\mathrm{d}\theta\,\mathrm{d}\theta/\mathrm{d}x_{C\alpha}$, rescaled per structure so that no atom moves more than the cap, and one Gaussian is then deposited per structure at its $\theta$ (equations below). The height rule is the well-tempered one, which lowers deposits where the bias is already high ([[@barducciWelltemperedMetadynamicsSmoothly2008#^c5]]). The HDX term is switched off in the window.

**Rounds.** One round from noise starts every structure at $\theta \approx 0$, so the range grows only about 1° per round. Four rounds from noise are followed by eight continuation rounds. Each continuation round re-noises the previous round's 50 structures to step 140 with a fresh random seed and carries the deposit history. The output is the union of rounds 2 to 4 and the continuation rounds (550 structures), not the last round. Round 1, which starts with an empty history, is not part of the union.

**Refinement.** The bias covers $\theta$, but the structures it produces fit the HDX data poorly (floor 0.011 for the unrefined seed-43 union against 0.0035 after refinement, both before the amide-H fix; 0.0028 after refinement with the fix), because a rigid rotation does not set the intra-lobe packing that the contact forward model keys on. A stratified subset (at most 25 per 6° bin of $\theta$) is therefore re-denoised from step 150, below $\sigma$ of 1.5 Å, with the ordinary HDX guidance at a low weight ($\alpha = 0.25$, normalised to the Boltz displacement, torsion projection, $\lambda = 1000$). Higher weights lowered pLDDT and let MaxEnt put weight on distorted structures. Structures below pLDDT 0.7 are removed.

**Reweighting.** MaxEnt is fitted over the refined union with a uniform prior, and the weight on each range of $\theta$ gives the populations. A state label from $\theta$ (open below −5°, closed above +5°, otherwise intermediate) is an evaluation device. Recovery is scored as in JAX-ENT, 100(1 − √JSD) over a strict support, and is never a loss.

## Equations

With $\mathbf{w}(x)$ the rotation vector of the body-II rotation after fitting body I onto the base, and $\hat{\mathbf{a}}$ the first right singular vector of the matrix whose rows are the pool's rotation vectors,

$$ \theta(x) = \frac{180}{\pi}\,\mathbf{w}(x)\cdot\hat{\mathbf{a}} $$
^eq-theta

The bias is a sum of Gaussians in $\theta$ with width $\sigma_\theta$, deposited at the $\theta_j$ the structures had when each was added,

$$ V(\theta) = \sum_j h_j \exp\!\left(-\frac{(\theta-\theta_j)^2}{2\sigma_\theta^2}\right) $$
^eq-bias

and the height of each new Gaussian falls with the bias already present, with $V$ in deg²,

$$ h_j = h_0 \exp\!\left(-\frac{V(\theta_j)}{k_{\mathrm{B}}T_\theta}\right) $$
^eq-height

where $k_{\mathrm{B}}T_\theta$ (the code's `cv_metad_kt`) is a temperature in deg², not a physical one. In each window step, each residue is displaced with its Cα by

$$ \Delta x_{C\alpha} = -\alpha\,\frac{\mathrm{d}V}{\mathrm{d}\theta}\,\frac{\partial\theta}{\partial x_{C\alpha}} $$
^eq-move

with $\mathrm{d}V/\mathrm{d}\theta$ in degrees and $\partial\theta/\partial x$ in deg/Å, so the product is read as a displacement in Å. The code then rescales the displacement per structure to at most the cap (equation form from the `cv_metad` description in `config.py`).

## Implementation notes

- **Settings used for TeaA.** $\alpha = 0.3$, $h_0 = 1$ deg², $\sigma_\theta = 3°$, $k_{\mathrm{B}}T_\theta = 100$ deg², cap 1.0 Å, window [0.7, 0.75] of 200 steps. A cap of 0.1 Å is inert (0.4°/step against the 1.2°/step restoring pull of the denoiser along the hinge); 1.0 Å works.
- **Which settings carry over.** The sequence of steps carries over to any system whose motion is one rigid-body hinge. The window, cap and $\sigma_\theta$ were set by diagnostics on TeaA and need the same diagnostic on a new system. The refinement weight and the 150-structure pool were tuned on seed 42, with the uncorrected amide-H placement, and not tested on a second protein.
- **Coordinates the bias accepts.** `cv_metad_kind` is `hinge` (this method, needing a base structure, an axis and the fit and measure residue ranges) or `torsion` (one or more periodic dihedrals under an n-dimensional bias). RMSD and contact coordinates are available only as a spring (`cv_force`), with no deposits or history. If the coordinate is known, Part A is skipped by setting the base and axis directly.
- **Blind status.** The seed-43 axis is built from unguided from-noise pools only and is the reported result. The seed-42 axis was built from earlier pools, about a third HDX-guided and some seeded from structures chosen by distance to the open MD reference; recomputing it from unguided pools alone moves it 7° (cos 0.993), less than the 12° between the seed-42 and seed-43 axes.
- **Template.** The only template is Boltz's own MSA-conditioned prediction (`tmsa` conditioning). It is not an MD or crystal structure, and the unguided pool it produces is unimodal at the Boltz intermediate ($\theta$ spread 0.6°).
- **Target.** The HDX target is synthetic and made with the guidance's own forward model, so there is no forward-model error ([[HDX protection-factor model]]). Under this forward model the true open and closed pools themselves fit best at 0.49 open, which sets the resolution of any population comparison.
- **What the populations can show.** In the corrected seed-43 rerun the refined MaxEnt weights split 0.459 open, 0.106 intermediate and 0.435 closed against a target of 0.40 : 0 : 0.60, with the open side peaking at −18 to −12° and the closed side at +6 to +12°. Strict recovery is 74.7 % against 54.0 % for the unguided control reweighted the same way. Before the fix the same recipe gave 0.410 : 0.280 : 0.310 and 58.3 %, no better than its control (58.1 %), and the open-side angle sat on a plateau from −15° to −39°. The corrected result is one run per configuration with a MaxEnt effective sample size of 16 of 234, and the open-closed ratio is inside the 0.49 resolution limit above. MaxEnt effective sample sizes in these runs are 11 to 19 of about 240, so per-structure fit floors can reward distortion, and the pLDDT filter and the pool-level checks stay in the recipe.
- **Amide H.** The target and all Boltz structures have no amide H, so the hydrogen-bond term needs the synthetic placement. Up to BioFeaturisers `43cc194` it was on the wrong side of the N, which made the term near inert ([Sigmoid-switch BV forward model](Sigmoid-switch%20BV%20forward%20model%20%28BioFeaturisers%29.md)). Seed 43 was rerun with `39b8069` (bf-teaa.md, section 5); seed 42 was not.

Protocol and run records are in `kb/experiments/bf-teaa.md`. Claims that use this method are not yet written.
