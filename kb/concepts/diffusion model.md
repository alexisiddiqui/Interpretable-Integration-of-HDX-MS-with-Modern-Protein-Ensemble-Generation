---
type: concept
aliases:
  - diffusion models
  - score-based generative model
  - denoising diffusion
  - DM
notation:
  - {symbol: '\tau', meaning: 'diffusion time, from data (0) to noise (1)', units: null}
  - {symbol: 'f(x,\tau)', meaning: 'drift of the forward diffusion SDE', units: null}
  - {symbol: 'g(\tau)', meaning: 'diffusion coefficient of the forward SDE', units: null}
  - {symbol: '\nabla_x \log p_\tau(x)', meaning: 'score of the marginal density at diffusion time tau', units: null}
sources:
  - "[[@yimDiffusionModelsProtein2024#^c3]]"
  - "[[@yimDiffusionModelsProtein2024#^c4]]"
  - "[[@yimDiffusionModelsProtein2024#^c5]]"
  - "[[@yimDiffusionModelsProtein2024#^c2]]"
  - "[[@yimDiffusionModelsProtein2024#^c6]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c5]]"
  - "[[@abramsonAccurateStructurePrediction2024#^c7]]"
  - "[[@bmsb2012ch3#^c8]]"
  - "[[@bmsb2012ch4#^c6]]"
---

## Definition

A diffusion model learns to generate samples by reversing a process that progressively corrupts training examples with noise. Generation starts from noise and iteratively denoises it towards the learned distribution ([[@yimDiffusionModelsProtein2024#^c6]], [[@yimDiffusionModelsProtein2024#^c2]]). In a continuous formulation, a forward stochastic differential equation corrupts data into a simple noise distribution. A neural network estimates the score, the gradient of the log density at each noise level, needed to integrate the reverse SDE and generate samples.

## Equations

$$ dx = f(x,\tau)\,d\tau + g(\tau)\,dB_\tau $$
^eq-diffusion-forward

Source: [[@yimDiffusionModelsProtein2024#^c3]], Eq. (1), p. 4. Yim writes $t$ for diffusion time; canonical is $\tau$, because $t$ is HDX labelling time (notation: [[@yimDiffusionModelsProtein2024#Notation]]).

$$ dx = \left[f(x,\tau) - g(\tau)^2\, \nabla_x \log p_\tau(x)\right] d\tau + g(\tau)\,dB_\tau $$
^eq-diffusion-reverse

Source: [[@yimDiffusionModelsProtein2024#^c4]], Eq. (2), pp. 4–5; [[@yimDiffusionModelsProtein2024#^c5]] (score), p. 5.

## Derivation

Link to MD (ultra-light; all steps ours):
1. If the data distribution is Boltzmann, $p_0(x) \propto e^{-U(x)/k_BT}$ ([[Boltzmann distribution#^eq-boltzmann]]), then its score is $\nabla_x \log p_0(x) = -\nabla_x U(x)/k_BT$. That is the MD force divided by $k_BT$ ([[molecular dynamics#^eq-newton]]).
2. A diffusion model trained on equilibrium structures therefore learns, at $\tau \to 0$, a quantity proportional to a force field. Trained on PDB structures, which are not a Boltzmann sample, it learns a statistical potential instead (step ours). Such potentials are typically only crude approximations of physical potentials of mean force ([[@bmsb2012ch3#^c8]], p. 21) and are better understood as statistical constructs ([[@bmsb2012ch4#^c6]], p. 9); see [[knowledge-based potential]].

## Assumptions and limits

- The learned distribution reflects the training data. When the examples are PDB structures, it reflects conformations represented in a structural database rather than equilibrium populations under specified solution conditions. Sampled diversity therefore requires a separate assessment of populations, for example by reweighting against [[HDX-MS]].
- Using generated samples as a candidate ensemble makes the generator's distribution the prior $P_0$. Reweighting them is [[importance sampling]] from that prior. Correcting the generator's coarse-grained statistics while keeping its local detail is the idea of the [[reference ratio method]].
- Diffusion steps are not physical simulation time (ours). The diffusion time $\tau$ runs along an artificial noising process, so a denoising trajectory says nothing about kinetics ([[sampling coverage]]).
- A diffusion-based predictor samples a learned distribution, which need not be the physical solution ensemble. AF3's diffusion training "produces a distribution of answers" ([[@abramsonAccurateStructurePrediction2024#^c5]]), yet repeated random seeds "do not produce an approximation of the solution ensemble" ([[@abramsonAccurateStructurePrediction2024#^c7]]). Compare [[MSA subsampling]], which perturbs a predictor's input, and the [[Boltzmann generator]], which targets a specified Boltzmann distribution through generation and reweighting.
- Protein models diffuse over frames, torsions or other non-Euclidean spaces. The Euclidean form above is the template.
- A pretrained model can be steered at sampling time by adding a likelihood or energy gradient to the score ([[guided diffusion]]). The added term is a bias, like the maximum-entropy tilt, so guided samples are not equilibrium-weighted without a correction.

## Why it matters here

Diffusion models are the "modern ensemble generation" in the thesis title. Chapter 2 needs this one equation pair to explain how they generate structures, and step 1 above to connect them to MD and to the populations that reweighting estimates. Experimental guidance of diffusion is a later chapter's method.

Claims that use this term: [[Diffusion models generate protein structures through iterative denoising.]], [[Diffusion PSMs use end-to-end training to learn the distribution of complexes across proteins, ligands and nucleic acids.]], [[To stay efficient at the atomic level, diffusion PSMs iteratively refine structure representations into final coordinates.]], [[A generator's sampling distribution is a reference distribution, not automatically the physical equilibrium distribution.]], [[Diffusion models are trained to reverse a noising process and generate structures by progressively denoising random samples.]], [[Diffusion steps are not physical simulation time.]], [[Repeated random seeds of AlphaFold 3 do not approximate the solution ensemble.]], [[Experimental guidance adds the gradient of a data likelihood to a pretrained diffusion score at sampling time.]], [[PDB-trained diffusion models learn conformations represented in a structural database rather than equilibrium populations under specified solution conditions.]].

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L153`; the historical wording comes from this note before revision, and its evidence remains in the linked source notes and manuscript references.

The primary wording describes generation through its operations and states what distribution is learned. Sampling a model distribution is distinguished from recovering physical populations.

### Historical wording

> A diffusion model learns to generate samples by reversing a noising process. In words: training corrupts example structures with noise until they are pure noise, and a network learns to undo each step; generation starts from random noise and denoises it step by step ([[@yimDiffusionModelsProtein2024#^c6]], [[@yimDiffusionModelsProtein2024#^c2]]). Formally, a forward stochastic differential equation gradually corrupts data into simple noise, usually Gaussian. A reverse SDE, which needs the score (the gradient of the log density) at every noise level, carries noise back to data. A neural network is trained to estimate that score. Generation then integrates the reverse SDE, progressively modifying noisy samples toward clean examples.

> - The learned distribution is only as good as the training data. Structure databases over-represent crystallisable, low-energy states, so sampled diversity is not evidence of equilibrium populations. Those still have to be checked against experiment, for example by reweighting against [[HDX-MS]].

> - A diffusion-based predictor is generative but not an ensemble sampler. AF3's diffusion training "produces a distribution of answers" ([[@abramsonAccurateStructurePrediction2024#^c5]]), yet repeated random seeds "do not produce an approximation of the solution ensemble" ([[@abramsonAccurateStructurePrediction2024#^c7]]). Compare [[MSA subsampling]], which perturbs a predictor's input, and the [[Boltzmann generator]], which is trained toward the Boltzmann distribution and reweighted.
