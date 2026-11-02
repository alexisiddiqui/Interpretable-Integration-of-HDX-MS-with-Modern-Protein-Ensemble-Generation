---
type: method
project: 3-BioFeaturisers
status: draft
needs_review: false
review_reason:
code:
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/config.py#L95-L131
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/saxs/debye.py#L108-L126
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/saxs/debye.py#L129-L197
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/saxs/foxs.py#L28-L35
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/saxs/forward.py#L46-L58
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/saxs/fft.py#L50-L76
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/saxs/fft.py#L120-L170
sources:
  - "[[@debyeZerstreuungRontgenstrahlen1915#^c1]]"
  - "[[@schneidman-duhovnyFoXSWebServer2010#^c1]]"
  - "[[@schneidman-duhovnyFoXSWebServer2010#^c2]]"
  - "[[@schneidman-duhovnyFoXSWebServer2010#^c3]]"
  - "[[@schneidman-duhovnyFoXSWebServer2010#^c4]]"
  - "[[@schneidman-duhovnyFoXSWebServer2010#^c6]]"
  - "[[@waasmaierNewAnalyticalScatteringfactor1995#^c1]]"
---

<!-- Note name: Differentiable SAXS forward model (BioFeaturisers). Concepts: [[SAXS]], [[forward model]], [[ensemble reweighting]], [[guided diffusion]], [[restrained simulation]]. No recorded experiment uses this model yet. -->

## What it does

Restrained sampling and guided generation need a predicted scattering profile that can be differentiated with respect to every atom position. The Debye sum gives that profile from coordinates ([[@debyeZerstreuungRontgenstrahlen1915#^c1]]), and FoXS adds the two solvent terms that a protein profile needs, the displaced solvent and the hydration layer ([[@schneidman-duhovnyFoXSWebServer2010#^c2]]). BioFeaturisers implements the FoXS profile in JAX so that one function serves reweighting, metainference and metadiffusion ([[forward model]]). Two kernels evaluate the same sum. The direct kernel sums over all atom pairs and is the reference. An opt-in grid kernel replaces the pair sum with a Fourier transform and is faster for large structures after a long first call.

SAXS reports the whole-molecule average of the orientation-averaged scattering ([[SAXS]]). It constrains overall size and shape and does not report which residues move, so it complements residue-level HDX restraints and does not replace them. No experiment recorded in the chapter uses it yet.

## Equations

The profile is a double sum over atom pairs at distance $r_{ij}$, weighted by the pair's form factors and $\mathrm{sinc}(x) = \sin x / x$,

$$ I(q) = \sum_{i}\sum_{j} f_i(q)\, f_j(q)\, \mathrm{sinc}(q\, r_{ij}) $$
^eq-saxs-debye

Source: [[@schneidman-duhovnyFoXSWebServer2010#^c1]], the Debye formula as FoXS uses it. The $i = j$ terms are the squared form factors and are added separately in the code.

Each atom has one effective form factor that combines the vacuum factor, the displaced-solvent factor and a hydration term weighted by the atom's solvent-accessible fraction $s_i$,

$$ f_i(q) = f_i^{\mathrm{vac}}(q) - c_1 f_i^{\mathrm{exc}}(q) + c_2\, s_i\, f^{\mathrm{w}}(q) $$
^eq-saxs-ff

Source: [[@schneidman-duhovnyFoXSWebServer2010#^c2]] and [[@schneidman-duhovnyFoXSWebServer2010#^c3]], where $c_1$ scales the excluded volume (default 1) and $c_2$ the hydration-layer density (default 0). The default table (`ff_table = pyfoxs`) uses united-atom form factors that already include the bound hydrogens, as FoXS does. The alternative `waasmaier_kirfel` table builds the vacuum factors from the five-Gaussian parametrisation ([[@waasmaierNewAnalyticalScatteringfactor1995#^c1]]) and then needs explicit treatment of hydrogen.

Expanding the square of this sum gives the six partial profiles of FoXS, which allows $c_1$ and $c_2$ to be fitted after the expensive sum has been computed once,

$$ I(q) = I_{aa} - c_1 I_{ac} + c_1^2 I_{cc} + c_2 I_{as} - c_1 c_2 I_{cs} + c_2^2 I_{ss} $$
^eq-saxs-six

The labels are those of the code (`saxs_combine`), where $a$ is the vacuum factor, $c$ the excluded volume and $s$ the hydration layer, and each $I_{xy}$ is the Debye sum with $f_x$ and $f_y$ in place of the effective factors. For an ensemble, the partials (or equivalently the profiles, because the combination is linear in them at fixed $c_1$ and $c_2$) are averaged over frames, with the ensemble weights when they are given.

The solvent-accessible fraction $s_i$ is taken from a smooth accessible-area model of the coordinates (`differentiable_sasa`, sharpness 10 by default), so hydration also responds to a coordinate change. With `differentiable_sasa` off, $s_i$ is a fixed input.

## Implementation notes

- **Defaults.** $q$ from 0.01 to 0.50 Å$^{-1}$ in 300 points, $c_1 = 1$, $c_2 = 0$, and an optional grid search of $c_1$ over 0.95 to 1.12 and $c_2$ over 0 to 4 (`SAXSConfig`). The search ranges match the FoXS fit ([[@schneidman-duhovnyFoXSWebServer2010#^c6]]). The fit is a post hoc step outside the differentiable path, which treats $c_1$ and $c_2$ as runtime parameters.
- **Direct kernel.** The atom list is padded to a multiple of `chunk_size` (512) and swept in blocks of $B \times B$ atoms, so the largest array is $B \times B \times n_q$ and the full distance matrix is never stored. A custom pullback gives the coordinate gradient. The default `pairwise_backend` is `direct`.
- **Grid kernel (`pairwise_backend="fft"`).** Each atom's form-factor channels are spread onto a regular grid with a normalised Gaussian stencil (default spacing 4 Å, Gaussian width 0.75 of the spacing, so 3 Å, and a radius of 3 cells). The density is Fourier transformed, and the profile at each $q$ is the inner product of the density's power spectrum with the transform of $\mathrm{sinc}(q\,r)$ on the grid distances, scaled by $\exp[(\sigma q)^2]$ to undo the Gaussian smoothing, where $\sigma$ is the stencil width. The cost scales with the grid size and not with the square of the atom count. The form factors are written as a low-rank sum of atom-type curves plus one solvent channel (at most 64 channels), and the kernel needs one transform per channel. A custom analytic pullback gives the coordinate gradient. The correction is exact only for an untruncated isotropic Gaussian, and the finite stencil leaves a small residual bias (`SAXS_FFT_ACCELERATION_RESEARCH_HANDOFF.md`).
- **Measured speed and accuracy.** On 1scj (2512 atoms, 300 $q$ values, 8 frames, one GPU, grid spacing 4 Å) the steady-state profile takes 0.24 s on the grid kernel against 0.68 s on the direct kernel, and profile plus coordinate gradient takes 0.21 s against 0.63 s, a speed-up of about three. The first call takes 17 to 23 s on the grid kernel against 1.7 to 2.5 s direct, because of compilation. Profile error against the direct kernel is $2\times10^{-4}$ (relative $L_2$) and the coordinate gradient has cosine 0.99999 to the direct one (`profiling/results/endpoint_saxs_fft_trajectory_phase2/results.json`). These are single-structure and short-trajectory results at one size. The earlier research handoff found a CPU crossover between 500 and 1500 atoms and did not recommend production use on a GPU without a long-lived test; the trajectory result above (2026-08-16) is the later measurement, made after the handoff (2026-08-05). Neither covers larger structures on a GPU, so the speed-up should not be extrapolated.
- **Reference check.** Benchmark scripts compare the direct kernel with FoXS in `benchmarking/SAXS/`. This note records no agreement figures from them.
- **What the model cannot do.** The profile is a single-structure calculation averaged over frames, so it carries no information about the rate of any motion, and it is unaffected by exchange timing. The hydration parameters are calibrated per dataset, so a fitted $c_1$ and $c_2$ can absorb a mismatch between ensemble and data in the same way fitted BV coefficients can ([[model misspecification]]).
