---
type: paper
citekey: bonomiMetadynamicMetainferenceEnhanced2016
year: 2016
read: false
pdf: kb/_pdf/@bonomiMetadynamicMetainferenceEnhanced2016.pdf
extraction: auto
needs_review: false
review_reason:
---

# Metadynamic Metainference: Enhanced Sampling of the Metainference Ensemble Using Metadynamics (2016)

## Main point

Metainference simulates N replicas in parallel and restrains replica-averaged forward-model predictions to ensemble-averaged data. Each datum carries uncertainty parameters that are sampled with the structures. These cover experimental noise, systematic error and forward-model error, plus the standard error from using finitely many replicas. Metainference does not solve sampling on its own, so the paper adds parallel-bias metadynamics (PBMetaD), with all replicas sharing one bias on the same CVs. The test system is alanine dipeptide in vacuo, with synthetic distance data.

## Claims

<!-- One bullet per claim, ending in a block ID. page is the 1-based PDF page index.
- The claim paraphrased in one sentence. ^c1
  - page: 1
  - quote: "verbatim text, 5 to 25 words"
  - quote_check: unchecked
  - reviewed: false
quote_check is written only by tools/kb-lint; reviewed only by me. -->
- Metainference integrates experimental information with prior knowledge and is designed to handle all sources of error in the data as well as sample heterogeneity. ^c1
  - page: 1
  - quote: "integrates experimental information with prior knowledge and deals with all sources of errors in the data as well as with sample heterogeneity"
  - quote_check: pass
  - reviewed: false
- In metainference, replicas of the system are modelled in parallel, and predicted observables are calculated as averages over the replicas. ^c2
  - page: 1
  - quote: "multiple replicas of the system are modelled in parallel so that experimental observables predicted from the models and calculated as averages over the replicas"
  - quote_check: pass
  - reviewed: false
- Models are generated using an energy function equal to the negative logarithm of the metainference posterior (Eq. 1). ^c3
  - page: 2
  - quote: "The generation of models is then guided by a score, or energy function, defined by the negative logarithm of the metainference posterior probability"
  - quote_check: pass
  - reviewed: false
- In the Gaussian noise model, each datum has an effective uncertainty that combines finite-replica error, experimental and systematic error, and forward-model error (Eq. 19). ^c4
  - page: 9
  - quote: "the statistical errors due to the use of a finite number of replicas, experimental and systematic errors, and errors in the forward model"
  - quote_check: pass
  - reviewed: false
- Without data or forward-model errors, metainference reduces to replica-averaged MaxEnt modelling, a harmonic restraint on the replica-averaged observable. ^c5
  - page: 9
  - quote: "our approach reduces to the replica-averaged MaxEnt modelling, in which a harmonic restraint couples the replica-averaged observable to the experimental data"
  - quote_check: pass
  - reviewed: false
- In that error-free limit, the restraint strength grows as N squared in the number of replicas, which the authors say the MaxEnt principle requires. ^c6
  - page: 9
  - quote: "The intensity of the restraint scales with the number of replicas as N2, i.e. more than linearly, as required by the MaxEnt principle"
  - quote_check: pass
  - reviewed: false
- With errors present, the restraint strength grows linearly in N and is modulated by the inferred data uncertainty. ^c7
  - page: 9
  - quote: "the intensity scales as N and it is modulated by the data uncertainty"
  - quote_check: pass
  - reviewed: false
- Without the PBMetaD bias, metainference runs of alanine dipeptide were not ergodic, and in 612 of 2400 runs one of the two minima was never visited. ^c8
  - page: 6
  - quote: "In 612 out of 2400 metainference runs, one of the two relevant minima was never visited during the entire course of the simulation"
  - quote_check: pass
  - reviewed: false
- Larger systems will need more slow degrees of freedom accelerated, and so more biased CVs. ^c9
  - page: 7
  - quote: "a greater number of slow degrees of freedom will need to be accelerated and thus included in the set of biased CVs"
  - quote_check: pass
  - reviewed: false
- The cost of MD, and so of metadynamic metainference, will increase with the size of the system. ^c10
  - page: 7
  - quote: "the computational cost required to run MD, and thus M&M, simulations will increase with the size of the system"
  - quote_check: pass
  - reviewed: false

## Notation

| Source | Meaning in this source | Canonical | Note |
|---|---|---|---|
| $X_r$ | coordinates of replica $r$ | $x$ | $\mathbf{X} = [X_r]$ is all replicas |
| $N$ | number of replicas | — |  |
| $N_d$ | number of data points | — |  |
| $d_i$ | experimental datum $i$ | $s_i^\text{exp}$ | $\mathbf{D} = [d_i]$ is $s^\text{exp}$ |
| $f_i(X_r)$ | forward model for observable $i$ | $s_i(x;\theta)$ | no forward-model parameters written |
| $f_i(\mathbf{X})$ | replica average $\frac{1}{N}\sum_r f_i(X_r)$ | — | same letter as the per-replica forward model, no bar |
| $\tilde f_{r,i}$ | average of $f_i$ over infinitely many replicas | — | marginalised in Eq. 19 |
| $\sigma^B_{r,i}$ | uncertainty from random and systematic data error and forward-model error | — | the [[nuisance parameter]] |
| $\sigma^\text{SEM}_{r,i}$ | standard error of the mean from finite $N$ | — | scales as $1/\sqrt{N}$ |
| $\sigma_{r,i}$ | effective uncertainty, $\sigma_{r,i}^2 = (\sigma^\text{SEM}_{r,i})^2 + (\sigma^B_{r,i})^2$ | $\sigma_i$ |  |
| $p(X_r)$ | prior on the state of replica $r$ (force field) | $P_0(x)$ |  |
| $E_{MI}$ | metainference energy, $-k_BT \log p$ | — | $E^G_{MI}$ Gaussian, $E^{OUT}_{MI}$ outliers |
| $S(X)$ | collective variables biased by PBMetaD | $\xi(x)$ |  |
| $V_{PB}(S,t)$ | parallel-bias metadynamics potential | — |  |

## What I use from it

For "Experimentally Restrained Simulations and Metainference" in Chapter 2:
- what [[metainference]] is: replicas, replica averages and per-datum uncertainties (^c1, ^c2, ^c4);
- the posterior and energy as the source writes them, Eq. 1 on p. 2 and Eq. 19 on p. 9 (^c3, ^c4);
- the [[nuisance parameter]] $\sigma^B$ that absorbs [[forward model]] error alongside experimental error (^c4);
- the link to the [[maximum entropy principle]]: the error-free limit is replica-averaged MaxEnt, with $N^2$ against $N$ scaling (^c5–^c7);
- why [[enhanced sampling]] is added: plain metainference was not ergodic even for alanine dipeptide (^c8);
- limits and costs: CV choice and system size (^c9, ^c10).

The M&M energy (Eq. 6, p. 3) is the metainference energy plus one PBMetaD bias per replica. Replicas share the bias as multiple walkers, and forward-model averages are reweighted to the unbiased ensemble (Eq. 7).

## Disagreements / limitations

- **Toy test only.** The benchmark is alanine dipeptide in vacuo with synthetic distance data generated from a known target. It says nothing about proteins, real experimental noise or a realistic forward model.
- **Forward-model error is not tested.** The synthetic data come from the same distances the model predicts. Systematic error is simulated by corrupting 20% of data points, so "forward-model error" is covered only in the sense of outlying data.
- **Accuracy depends on the prior and the data.** The paper reports that the absolute error depends on the accuracy of the prior and on how informative the data are (p. 6). Few of the 36 distances could separate the two minima.
- **The MaxEnt link is a limit.** The reduction to MaxEnt (^c5, ^c6) holds only when data and forward-model errors are zero. With errors, the restraint scales only as N (^c7), so my reading is that the measured averages are no longer enforced exactly. The paper does not state this.
- **CV choice is unsolved.** PBMetaD eases the problem of choosing CVs by allowing many of them. It does not remove the need to guess the slow modes (^c9).
- **Replicas cost compute.** More replicas improve the average and sampling, but each replica is a full simulation. The authors advise spending resources on more replicas, not on parallelising each one (p. 7). Cost still grows with system size (^c10).
- **Comparison with RAM is the authors' own.** They say RAM uses a constant restraint chosen "as strong as possible" and cannot easily include errors (p. 3). This is their framing of a competing method.
