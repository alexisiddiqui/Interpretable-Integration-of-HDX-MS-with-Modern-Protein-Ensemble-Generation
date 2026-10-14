---
type: paper
citekey: wangProteinConformationGeneration2024
year: 2024
read: false
pdf: kb/_pdf/@wangProteinConformationGeneration2024.pdf
extraction: auto
needs_review: false
review_reason:
---

# Protein Conformation Generation via Force-Guided SE(3) Diffusion Models (2024)

## Main point

ConfDiff is an SE(3) backbone diffusion model trained on PDB structures only. Classifier-free guidance mixes a sequence-conditional score with an unconditional one to trade quality against diversity. A second guidance term adds an MD energy or force. Its target is the baseline generator's distribution tilted by a Boltzmann factor, and a network estimates the intermediate force on noisy coordinates. On 12 fast-folding proteins and BPTI, ConfDiff gave lower Jensen-Shannon distances to MD than Str2Str and EigenFold, and force guidance lowered energies with little change in those distances.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Existing score-based diffusion methods cannot properly use physical prior knowledge to guide generation, so their samples deviate from the equilibrium distribution. ^c1
  - page: 1
  - quote: "existing score-based diffusion methods cannot properly incorporate important physical prior knowledge to guide the generation process"
  - quote_check: pass
  - reviewed: false
- Structure databases hold few conformations per sequence, so the training distribution is not the equilibrium distribution and sits near energy minima. ^c2
  - page: 4
  - quote: "the training data distribution does not comply with the equilibrium distribution, but rather only containing a few data points near the potential energy minima"
  - quote_check: pass
  - reviewed: false
- A sequence-conditional score model guides an unconditional one by classifier-free guidance, trading conformation quality against diversity. ^c3
  - page: 2
  - quote: "Employing a sequence-conditional model to guide the unconditional model, we use classifier-free guidance on SE(3) to find a better trade-off between conformation quality and diversity"
  - quote_check: pass
  - reviewed: false
- The stated goal is to sample from an equilibrium distribution, written in Eq. 3 as the baseline generator's distribution multiplied by a Boltzmann factor of the OpenMM energy. ^c4
  - page: 4
  - quote: "our goal is to sample protein conformations from the equilibrium distribution"
  - quote_check: pass
  - reviewed: false
- The energy term on noisy coordinates is an intermediate energy, defined by an expectation over clean structures given the noisy ones (Eq. 4). ^c5
  - page: 4
  - quote: "We refer to Et as the intermediate energy function, capturing the dynamic changes in energy at various stages during the diffusion process"
  - quote_check: pass
  - reviewed: false
- The guided score subtracts the gradient of the intermediate energy, the intermediate force, scaled by a guidance strength (Eq. 6). ^c6
  - page: 5
  - quote: "where η is a hyperparameter controlling the strength of force guidance"
  - quote_check: pass
  - reviewed: false
- The authors describe force guidance as reweighting the generated conformations towards the equilibrium distribution. ^c7
  - page: 4
  - quote: "Utilizing prior information from the MD force field, our model successfully reweights the generated conformations to ensure they adhere better to the equilibrium distribution"
  - quote_check: pass
  - reviewed: false
- All compared models were trained on experimental PDB structures without MD trajectory data. ^c8
  - page: 6
  - quote: "All models are trained on experimental protein structures deposited in the Protein Data Bank (PDB) without using additional MD trajectory data"
  - quote_check: pass
  - reviewed: false
- Distributional fidelity was measured by Jensen-Shannon distance between generated samples and reference MD samples. ^c9
  - page: 7
  - quote: "use Jensen-Shannon distance (JS) to characterize the similarity between generated samples and reference samples from MD"
  - quote_check: pass
  - reviewed: false
- Energy and force guidance repair clashing structures but contract them towards local minima, which slightly worsens the distributional metrics. ^c10
  - page: 21
  - quote: "irrational conformations are rectified and structures tend to contract towards the local minimum"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $t$ | diffusion time, $t \in [0,1]$ | $\tau$ | $t$ is labelling time |
| $\mathbf{x}_t = [\mathbf{T}_t, \mathbf{R}_t]$ | backbone frames (translations, rotations) at diffusion time $t$ | — | |
| $q_0(\mathbf{x}_0)$ | distribution of the baseline (unguided) generator | $P_0(x)$ | the generator is the prior |
| $p_0(\mathbf{x}_0) = q_0(\mathbf{x}_0) e^{-k\mathcal{E}_0(\mathbf{x}_0)}/Z$ | energy-tilted target, called "the equilibrium distribution" (Eq. 3) | $P(x)$ | equals Boltzmann only if $q_0$ is flat |
| $\mathcal{E}_0(\mathbf{x}_0)$ | OpenMM potential energy (Amber ff14SB, GBn2) | $U(x)$ | calligraphic in source |
| $k$ | inverse temperature factor | — | write $1/k_BT$ |
| $Z$ | normaliser of the tilted target | — | not the configurational partition function |
| $\mathcal{E}_t(\mathbf{x}_t)$ | intermediate energy (Eq. 4) | — | |
| $\nabla_{\mathbf{x}_t} \mathcal{E}_t(\mathbf{x}_t)$ | intermediate force (Eq. 5) | — | MD force at $t=0$, zero at $t=1$ |
| $\eta$ | force or energy guidance strength | — | 1.3 to 1.5 in experiments |
| $\gamma$ | classifier-free guidance weight | — | clashes with canonical $\gamma$ (data-term weight) |
| $s_\theta(\mathbf{x}_t, t)$ | baseline score (CFG mixture) | — | write $\hat\nabla_x \log p_\tau(x)$ |
| $h_\psi(\mathbf{x}_t, t)$ | network for the intermediate force | — | |
| $f_\phi(\mathbf{x}_t, t)$ | network for the intermediate energy (CEP) | — | |

## What I use from it

Chapter 2, "Experimental Guidance of Diffusion Models":
- Physics rather than data as the guidance term (^c1, ^c6). It is the energy and force counterpart of the likelihood guidance in ExEnDiff, and the same noisy-intermediate problem appears as the intermediate energy (^c5).
- The tilted target $q_0 e^{-k\mathcal{E}_0}/Z$ (^c4) shows a guided sampler targeting the generator distribution times a Boltzmann factor, which is the structure of [[importance sampling]] from the generator as prior. This links to [[diffusion model]] and the [[maximum entropy principle]].
- Classifier-free guidance as the other main form of [[guided diffusion]] (^c3); its displayed equation is on p. 3.
- PDB training is not equilibrium sampling (^c2, ^c8).
- Evaluation against MD by Jensen-Shannon distance on fast folders and BPTI (^c9), and the quality against distribution trade-off (^c10).

## Disagreements / limitations

- **"Reweighting" without weights.** The authors say the model "successfully reweights the generated conformations" (^c7), but no importance weights are computed. The tilt is applied through an approximate guidance term. They note that $p_0$ "gives a more accurate estimate through importance sampling" (p. 4), yet do not report reweighted estimates.
- **Target is not the Boltzmann distribution.** Eq. 3 multiplies the generator distribution by $e^{-k\mathcal{E}_0}$. This equals the [[Boltzmann distribution]] only if $q_0$ is uniform; otherwise the PDB-derived bias, which already favours minima (^c2), is counted on top of the energy.
- **Guidance strength above one.** Experiments used "guidance strength η = 1.3 for both force and energy guidance" (p. 17) and 1.5 for BPTI force guidance. With $\eta \neq 1$ the implicit target is $q_t e^{-\eta k \mathcal{E}_t}$, a tempered tilt, not Eq. 3.
- **Constant $k$ handled loosely.** Eq. 6 writes $-\eta \nabla \mathcal{E}_t$, while the implicit density it names carries $e^{-\eta k \mathcal{E}_t}$. The force-network target in Eq. 7 also drops the $1/k$ of Eq. 5. Treat $k$ as absorbed into $\eta$.
- **Approximate physics.** Energies come from implicit solvent after side-chain packing and restrained minimisation (p. 17), and force guidance acts only on Cα translations (p. 6). The intermediate expectation is estimated over a batch of the model's own samples.
- **Small test systems and indirect fidelity.** Tests were 12 fast-folding proteins (10 to 80 residues) and BPTI (58 residues). Fidelity was judged by Jensen-Shannon distances on projected features (^c9), and guidance slightly worsened some of these (^c10). Force guidance gave JS distances close to the unguided base model (Table 1, p. 7).
- **No experimental data.** Guidance is by force field only, so ConfDiff gives no route for experimental observables. The comparison with ExEnDiff is guidance by physics against guidance by data.
