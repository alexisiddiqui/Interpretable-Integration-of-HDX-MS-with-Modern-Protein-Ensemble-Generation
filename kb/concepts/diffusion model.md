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
  - "[[@bmsb2012ch3#^c8]]"
  - "[[@bmsb2012ch4#^c6]]"
---

## Definition

A diffusion model learns to generate samples by reversing a noising process. A forward stochastic differential equation gradually corrupts data into simple noise, usually Gaussian. A reverse SDE, which needs the score (the gradient of the log density) at every noise level, carries noise back to data. A neural network is trained to estimate that score. Generation then integrates the reverse SDE, progressively modifying noisy samples toward clean examples.

## Equations

$$ dx = f(x,\tau)\,d\tau + g(\tau)\,dB_\tau $$
^eq-diffusion-forward

Source: [[@yimDiffusionModelsProtein2024#^c3]], Eq. (1), p. 4. Yim writes $t$ for diffusion time; canonical is $\tau$, because $t$ is HDX labelling time.

$$ dx = \left[f(x,\tau) - g(\tau)^2\, \nabla_x \log p_\tau(x)\right] d\tau + g(\tau)\,dB_\tau $$
^eq-diffusion-reverse

Source: [[@yimDiffusionModelsProtein2024#^c4]], Eq. (2), pp. 4–5; [[@yimDiffusionModelsProtein2024#^c5]] (score), p. 5.

## Derivation

Link to MD (ultra-light; all steps ours):
1. If the data distribution is Boltzmann, $p_0(x) \propto e^{-U(x)/k_BT}$ ([[Boltzmann distribution#^eq-boltzmann]]), then its score is $\nabla_x \log p_0(x) = -\nabla_x U(x)/k_BT$. That is the MD force divided by $k_BT$ ([[molecular dynamics#^eq-newton]]).
2. A diffusion model trained on equilibrium structures therefore learns, at $\tau \to 0$, a quantity proportional to a force field. Trained on PDB structures, which are not a Boltzmann sample, it learns a statistical potential instead (step ours). Such potentials are typically only crude approximations of physical potentials of mean force ([[@bmsb2012ch3#^c8]], p. 21) and are better understood as statistical constructs ([[@bmsb2012ch4#^c6]], p. 9); see [[knowledge-based potential]].

## Assumptions and limits

- The learned distribution is only as good as the training data. Structure databases over-represent crystallisable, low-energy states, so sampled diversity is not evidence of equilibrium populations. Those still have to be checked against experiment, for example by reweighting against [[HDX-MS]].
- Using generated samples as a candidate ensemble makes the generator's distribution the prior $P_0$. Reweighting them is [[importance sampling]] from that prior. Correcting the generator's coarse-grained statistics while keeping its local detail is the idea of the [[reference ratio method]].
- Protein models diffuse over frames, torsions or other non-Euclidean spaces. The Euclidean form above is the template.

## Why it matters here

Diffusion models are the "modern ensemble generation" in the thesis title. Chapter 2 needs this one equation pair to explain how they generate structures, and step 1 above to connect them to MD and to the populations that reweighting estimates. Experimental guidance of diffusion is a later chapter's method.

Claims that use this term: [[Diffusion-based PSMs have emerged as a powerful alternative to traditional structure prediction methods.]], [[Diffusion PSMs use end-to-end training to learn the distribution of complexes across proteins, ligands and nucleic acids.]], [[To stay efficient at the atomic level, diffusion PSMs iteratively refine structure representations into final coordinates.]].
