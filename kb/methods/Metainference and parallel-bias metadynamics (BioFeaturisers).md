---
type: method
project: 3-BioFeaturisers
status: draft
needs_review: false
review_reason:
code:
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/examples/PLUMED/topology_pipeline/pipeline.py#L1105-L1179
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/examples/PLUMED/topology_pipeline/plumed_templates/pbmetad.dat#L1-L2
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/examples/PLUMED/topology_pipeline/plumed_templates/hdx_metainference.dat#L1
  - projects/3-BioFeaturisers/code@39b8069:integrations/plumed/biofeat_pycv/callback.py#L342-L384
  - projects/3-BioFeaturisers/code@39b8069:biofeaturisers/backends/torch_backend.py#L117-L141
sources:
  - "[[@pfaendtnerEfficientSamplingHighDimensional2015#^c2]]"
  - "[[@pfaendtnerEfficientSamplingHighDimensional2015#^c5]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c2]]"
  - "[[@bonomiMetadynamicMetainferenceEnhanced2016#^c4]]"
  - "[[@alamdariEfficientSamplingHighDimensional2021#^c5]]"
---

## Purpose and components

Experimental restraints alter which structures are favoured, while a history-dependent bias promotes exploration of the chosen collective variables. BioFeaturisers combines these operations through GROMACS and PLUMED. Its JAX endpoint supplies the HDX predictions and coordinate derivatives; PLUMED supplies the metainference error model and the parallel-bias metadynamics action. The [[Sigmoid-switch BV forward model (BioFeaturisers)]] is therefore shared with reweighting and guided generation, while the sampling algorithm is implemented by the simulation engine.

The replica-averaged restraint and its uncertainty model are defined in [[metainference#^eq-metainference-energy]]. Parallel-bias metadynamics constructs low-dimensional biases on several collective variables, with conditional weighting that accounts for their coupling ([[@pfaendtnerEfficientSamplingHighDimensional2015#^c2]], [[@pfaendtnerEfficientSamplingHighDimensional2015#^c5]]). Combining them adds the metainference energy and the sampling bias to each replica's dynamics ([[@alamdariEfficientSamplingHighDimensional2021#^c5]]). The Gaussian equation in [[Hinge-coordinate metadiffusion (BioFeaturisers)]] describes the generator's own bias and does not define the PLUMED parallel-bias action.

## Observation and force path

The pipeline prepares a topology-bound feature bundle and an ordered vector of experimental targets. A `PYCVINTERFACE` action evaluates those observables from the current protein coordinates. `METAINFERENCE` receives the matching components, uses `NOISETYPE=MGAUSS`, and samples uncertainty parameters alongside the replicas. Protection-factor observations are expressed as ln(PF); peptide-uptake observations use the uptake endpoint. The observation type and the target order are fixed at build time.

The production reverse-VJP path receives PLUMED's forces on the observable components and contracts them with the JAX coordinate derivatives in `plumedApplyVJP`. This computes the atomic force without transferring a full observable-by-coordinate Jacobian. The alternative forward path returns coordinate derivatives explicitly. The callback endpoint takes coordinates in nm and returns derivatives with respect to those coordinates; the internal forward model uses its own coordinate conversion. The force contraction must retain that conversion.

The PyTorch wrapper is a separate consumer of the same JAX endpoint. Its custom autograd function evaluates endpoint values in the forward pass and calls `values_and_vjp` with output cotangents in the backward pass (`torch_backend.py`, lines 117–141). It is the bridge used by a PyTorch generator, rather than an additional forward-model definition.

## Combining the restraint and bias

The pipeline exposes four conditions: unbiased MD, metainference alone (MI), parallel-bias metadynamics alone (PB), and their combination (MI+PB). `PBMETAD` uses shared-walker history through `WALKERS_MPI`. Its collective variables, widths, height, deposition pace, bias factor and grids are resolved from the system configuration.

For MI+PB, `METAINFERENCE` receives the sampling bias as an extra argument with `REWEIGHT`. Where the protocol includes walls, the pipeline first sums the wall and PB energies and passes that total bias. MI alone has no reweighting argument. The pipeline enforces this pairing (`pipeline.py`, lines 1110–1133). This weighting corrects the replica average used by the restraint. A plot pooled over a time-dependent trajectory still needs an appropriate bias correction before it can be interpreted as equilibrium populations.

The generated action uses `AVERAGING=100`, records the uncertainty state in `MISTATUS`, and can print per-observable uncertainty diagnostics, replica weights and effective replica counts. Evaluation stride and uncertainty bounds are protocol settings. Values from one experiment should not be substituted for another.

## Experiment-specific implementations

[[bf-bpti]] records the two-stage ±0/±2 design, three disulfide-dihedral CVs, variance-scaled uncertainty bounds, matched controls and production budget. Its basin-coverage figures use frame counts and establish sampling coverage and retention.

[[bf-moprp]] records the paired pH builds, resolved MI-v2 restraint and bias inputs, and the separate basin-seeded unbiased trajectories. The seeded trajectories support transition-based analysis; the restrained ensemble's weights alone do not establish a pathway.
