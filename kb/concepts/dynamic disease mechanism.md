---
type: concept
aliases:
  - dynamic disease mechanisms
  - disease as a population shift
  - pathogenic population shift
  - conformational disease mechanism
notation:
  - {symbol: '\pi_A', meaning: 'equilibrium population of conformational state A', units: null}
  - {symbol: 'G_A', meaning: 'free energy of conformational state A, -k_BT ln of its partial partition function', units: 'kJ mol^-1'}
  - {symbol: '\Delta G_{AB}', meaning: 'free-energy difference between conformational states, G_B - G_A', units: 'kJ mol^-1'}
  - {symbol: '\Delta\Delta G_{AB}', meaning: 'change in Delta G_AB caused by a perturbation such as a mutation, ligand or change of environment', units: 'kJ mol^-1'}
  - {symbol: '[L]', meaning: 'free concentration of a binding species L in the environment', units: 'M'}
  - {symbol: 'K_{L,A}', meaning: 'association constant of species L for conformational state A', units: 'M^-1'}
sources:
  - "[[@parraFrustrationPhysiologyMolecular2025#^c17]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c18]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c19]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c20]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c21]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c22]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c24]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c13]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c4]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c28]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c29]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c30]]"
  - "[[@parraFrustrationPhysiologyMolecular2025#^c12]]"
  - "[[@suttoEffectsOncogenicMutations2013#^c1]]"
  - "[[@suttoEffectsOncogenicMutations2013#^c5]]"
  - "[[@galpernProbingDarkEnergy2026#^c8]]"
  - "[[@galpernProbingDarkEnergy2026#^c13]]"
---

## Definition

A dynamic disease mechanism is a pathogenic perturbation, usually a mutation, that acts by changing *which conformations the protein populates* (and how quickly it moves between them), rather than only by unfolding it or creating a new structure. In its simplest form it is a [[population shift]]: the native [[structural ensemble]] is reweighted. Mutations can upset the balance between global stability and local instability that function relies on ([[@parraFrustrationPhysiologyMolecular2025#^c17]]). Local frustration is what drives interconversion between native conformations ([[@parraFrustrationPhysiologyMolecular2025#^c13]]), so a mutation that retunes frustration retunes the populations.

The shift can go either way:

- **The functional state is destabilised, or competing states gain weight.** p53 R248Q raises frustration, which goes with more conformational heterogeneity and higher aggregation propensity ([[@parraFrustrationPhysiologyMolecular2025#^c20]]). cTnC C84Y remotely alters N-domain dynamics and favours the Ca²⁺-"primed" state ([[@parraFrustrationPhysiologyMolecular2025#^c21]]).
- **The wrong state becomes too stable.** AADC P330L makes the *open* catalytic loop less frustrated, so the loop stays open and catalysis fails ([[@parraFrustrationPhysiologyMolecular2025#^c18]]). Desmin Glu353dup creates a minimally frustrated, over-stabilised dimer interface that blocks polymerisation ([[@parraFrustrationPhysiologyMolecular2025#^c19]]). Oncogene mutations gain function by *relieving* frustration and disrupting allosteric communication ([[@parraFrustrationPhysiologyMolecular2025#^c24]]).
- **Both at once, between states.** Cancer mutations in kinases may raise frustration in the inactive state and lower it in the active state ([[@parraFrustrationPhysiologyMolecular2025#^c22]]). All oncogenic EGFR mutants shift the kinase domain towards the active conformation ([[@suttoEffectsOncogenicMutations2013#^c1]]), and that equilibrium has been linked to EGFR's oncogenic potential ([[@suttoEffectsOncogenicMutations2013#^c5]]).

Together these show that **losing frustration can be as harmful as gaining it**. Disease is not only destabilisation; it can be the wrong state becoming too stable (synthesis ours, from the cases above). Frustration is kept because function needs it, at the cost of folding stability ([[@galpernProbingDarkEnergy2026#^c8]]). A mutation that "fixes" it can remove the function.

## Equations

$$ \pi_A = \frac{Z_A}{Z} = \sum_{j \in A} w_j, \qquad \frac{\pi_B}{\pi_A} = e^{-\Delta G_{AB}/k_BT}, \qquad \Delta G_{AB} = G_B - G_A, \quad G_A = -k_BT \ln Z_A $$
^eq-state-population

Source: derived here (steps 1–2 and 6 below) from [[Boltzmann distribution#^eq-boltzmann]] and [[Boltzmann distribution#^eq-helmholtz]]; $Z_A$ is the partition function restricted to state $A$. No source in the vault states it in this form.

$$ \frac{\pi_B'}{\pi_A'} = \frac{\pi_B}{\pi_A}\, e^{-\Delta\Delta G_{AB}/k_BT} $$
^eq-population-shift

Source: derived here (step 3). A perturbation with $\Delta\Delta G_{AB} < 0$ favours $B$. Every $1.4\ \text{kcal mol}^{-1}$ ($5.7\ \text{kJ mol}^{-1}$) at 298 K changes the ratio about tenfold.

$$ \Delta G_{AB}(\{[L]\}) = \Delta G_{AB}^{0} - k_BT \sum_{L} \ln \frac{1 + K_{L,B}[L]}{1 + K_{L,A}[L]} $$
^eq-environment-linkage

Source: derived here (steps 4–5); this is the standard ligand-linkage (binding-polynomial) result written for several species. $\Delta G_{AB}^{0}$ is the value with none of the species present.

## Derivation

1. From [[Boltzmann distribution#^eq-boltzmann]], the probability of state $A$ (a set of conformations, i.e. a basin of the [[conformational free-energy landscape]]) is $\pi_A = Z_A/Z$, with $Z_A = \int_{x \in A} e^{-U(x)/k_BT}\,dx$ (step ours).
2. Defining $G_A = -k_BT\ln Z_A$, by analogy with [[Boltzmann distribution#^eq-helmholtz]], gives $\pi_B/\pi_A = e^{-(G_B - G_A)/k_BT}$ (step ours).
3. A mutation changes $U(x) \to U'(x)$ and so $\Delta G_{AB} \to \Delta G_{AB} + \Delta\Delta G_{AB}$. Substituting into step 2 gives ^eq-population-shift (step ours). Nothing structural has to change: the conformations in $A$ and $B$ can be identical before and after, and only their weights move.
4. Let a species $L$ bind one site with association constant $K_{L,A}$ while the protein is in state $A$. Summing over bound and unbound forms gives $Z_A([L]) = Z_A(0)\,(1 + K_{L,A}[L])$ (step ours; ideal dilute solution, a single site, no cooperativity).
5. Substituting into step 2 gives one logarithmic term per species. If species bind independently and do not compete, their factors multiply, so the terms add: ^eq-environment-linkage (step ours).
6. In [[ensemble reweighting]], each conformer $j$ carries a weight $w_j$ ([[maximum entropy principle]]), so a state's population is the sum of its conformers' weights, $\pi_A = \sum_{j \in A} w_j$ (step ours). This is the quantity HDX-informed reweighting estimates.

## Assumptions and limits

- **Equilibrium only.** Populations do not describe kinetic mechanisms: folding traps, aggregation nucleation and the rate of switching between states. Aggregation is also concentration-dependent and usually irreversible, so a small shift toward an aggregation-prone [[high-energy intermediate]] can matter far more than its population suggests (our reasoning; see [[protein misfolding and aggregation]]).
- **States are a modelling choice.** $\pi_A$ depends on how conformations are assigned to $A$ and $B$. Two-state pictures (open/closed, active/inactive) are coarse.
- **The linkage equation is idealised.** It assumes ideal activities, single non-competing sites and no cooperativity. Crowding, non-specific weak interactions and membranes violate these, and they act on every state, not just at binding sites (our reasoning; needs a primary source before going in the thesis).
- **Context dependence.** Within this framework a mutation's effect is a $\Delta\Delta G_{AB}$ *relative to a stated environment*, and it can differ between environments when the mutation touches a site that a species binds (see below).

## Why it matters here

**HDX constrains population estimates through a forward model.** State equilibria such as AADC open/closed, the cTnC primed state and kinase active/inactive provide candidate explanations for changes in protection. [[Ensemble reweighting]] estimates their populations against [[HDX-MS]] under the stated solution conditions, candidate conformations and forward-model assumptions. A single structure does not specify these populations. Comparing mutant and wild-type uptake can constrain a population-shift hypothesis; any inferred $\Delta\Delta G_{AB}$ depends on the state definition and equilibrium model used to interpret it (step 6).

**Link to the local-environment theory.** Local frustration measures how well a residue's *local environment* stabilises it.

- Highly frustrated contacts are destabilising in isolation and are held in place by the rest of the structure or by a partner. Binding regions are frustrated when the partners are separated ([[@parraFrustrationPhysiologyMolecular2025#^c4]]). IκBα is more frustrated alone than in complex with NFκB ([[@parraFrustrationPhysiologyMolecular2025#^c28]]). Calmodulin's Ca²⁺-binding Asp residues look frustrated only because the ion is not modelled ([[@parraFrustrationPhysiologyMolecular2025#^c30]]).
- So frustration is not a property of the sequence alone. It depends on context ([[@parraFrustrationPhysiologyMolecular2025#^c29]]).
- In the terms of ^eq-environment-linkage, a frustrated site is where some species $L$ is likely to bind the states unequally ($K_{L,A} \neq K_{L,B}$). Highly frustrated sites are therefore both where state-selective binding acts and where mutations most easily push the equilibrium either way (our reading).
- The evolutionary counterpart is dark energy in [[@galpernProbingDarkEnergy2026]]. It marks sites where mutations change function without a matching change in folding stability, which is where population-shift mutations would sit. Because dark energy uses a global $\Delta\Delta G$ or a single fixed structure ([[@galpernProbingDarkEnergy2026#^c13]]), such shifts are exactly what it *cannot* see directly. The residual native entropy $N_{native} > 1$ in [[@galpernInformationtheoreticArgumentRestriction2026]] is the room for these shifts to happen in.

**The cocktail problem (our reading).** ^eq-environment-linkage says that *every* species which binds the two states unequally shifts their populations. So no protein has "a" population, only populations conditional on its environment.

- **In vitro**, the environment is the buffer: salts and pH, cofactors and metals (PLP for AADC, Ca²⁺/Mg²⁺ for cTnC, Zn²⁺ for p53), the protein's own concentration (oligomers, aggregation) and, for HDX, D₂O and the labelling temperature. Even a "minimal" buffer is a cocktail. HDX-reweighted populations are therefore populations *in that buffer*, and the conditions belong in the result. Titrating a species and refitting would estimate $K_{L,A}$ against $K_{L,B}$ directly.
- **In vivo**, the cocktail grows. It includes binding partners (TnI for cTnC, Kapβ2 for FUS, DNA for p53, NFκB for IκBα), chaperones that recognise frustrated sites ([[@parraFrustrationPhysiologyMolecular2025#^c12]]), post-translational modifications (e.g. [[Millisecond HDX-MS showed tau hyperphosphorylation releases the global fold and exposes the aggregation-prone H2 region.]]), crowding and membranes. A mutation can look neutral in purified protein and be pathogenic in the cell, or the reverse, if its $\Delta\Delta G_{AB}$ depends on a partner that is missing in vitro. The desmin and FUS phenotypes both involve partners or assembly.
- **For generators**, AlphaFold2, BioEmu and isolated-chain MD all model one chain in solvent. Their priors therefore show partner sites as frustrated and can't represent states that only a partner or cofactor selects. Reweighting can move weight toward the *measured* environment, but only among conformations the prior already contains. This is another reason why [[Useful ensemble generation requires quantifying the relative populations of each state, not only generating structures.]]

Related: [[protein dynamics]], [[allostery]], [[protein misfolding and aggregation]], [[conformational free-energy landscape]].

Claims that use this term: [[Static structures alone cannot explain many biological phenomena; dynamics underlie disease mechanisms and drug response.]], [[Oncogenic mutations alter conformational free-energy landscapes and shift the equilibrium between active and inactive states.]], [[Cancer-causing p53 mutants have crystal structures nearly identical to wild type but very different DNA binding and pathologies.]], [[Kinases and their inhibitor resistance mutations often preserve drug-binding sites while shifting conformational equilibria.]], [[High-energy intermediates are sparsely populated yet play critical roles in disease pathogenesis.]], [[Conformational conversion of oligomeric intermediates can limit the rate of protein aggregation.]], [[Quantifying state populations requires experimental measurements of protein dynamics.]].

## Wording history

Primary wording follows `thesis/chapters/01-introduction.tex#L126`; the historical wording comes from this note before revision, and its evidence remains in the linked source notes and manuscript references.

The primary wording separates measured uptake from inferred populations and free-energy differences. The state-equilibrium interpretation is retained as a model-dependent use of the measurement.

### Historical wording

> **Populations are what HDX reweighting measures.** AADC open/closed, the cTnC primed state and kinase active/inactive are exactly the state equilibria that [[ensemble reweighting]] against [[HDX-MS]] can quantify (step 6). A single structure can't show them: cancer-causing p53 mutants, for example, crystallise almost identically to wild type. Comparing mutant and wild type by differential HDX is in effect a measurement of $\Delta\Delta G_{AB}$-type changes.
