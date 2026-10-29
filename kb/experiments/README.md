# Remote experiments

This index connects thesis projects to experiments on other machines. [BioFeaturisers / MaxENT-FK](biofeaturisers.md) and [jax-Ka](jax-ka.md) have initial location entries. Machine access requirements live in [machines.yaml](machines.yaml). Each machine has an SSH alias and a project root; All three machines were reached on 2026-10-29 and their top-level layout mapped (see each project file).

## Completing the locations

1. Record each machine's working SSH alias and any required connection steps in `machines.yaml`. Keep credentials in the existing authentication configuration, outside the repository. Record `last_verified_at` only after a successful connection.
2. Replace each `root: null` with an absolute remote project directory. Add separate location entries when repositories or experiment collections occupy different directories.
3. Identify individual experiments and whether their runs are replicated or split across machines. Give each experiment a stable ID independent of its machine and identify the authoritative location when known.
4. Record the project's existing inspection command, selected output paths and relevant thesis figure IDs. Keep paths relative to the experiment's remote root where possible.

Coulson-Chemistry and Pegasus-Gate require Cisco VPN. Isambard uses Clifton auth: run `clifton auth` (the certificate lasts about 12 hours), then `ssh hussain.u6xq@u6xq.aip2.isambard`. Project `u6xq` has replaced the earlier `s5h`. The earlier spelling `Pegausus-Gate` is retained as an alias, not a verified hostname.

Same-Wi-Fi SSH for tunnel-accessible machines is not fully configured, and VS Code port forwarding is unimplemented. Record either route against the relevant machine only once its details are known. A VS Code tunnel name alone does not establish a working SSH route.

## Experiment entries

Add entries to the project's `experiments` frontmatter list using this shape. The example is a template, not an existing run.

```yaml
experiments:
  - id: <stable-experiment-id>
    status: <primary / in progress / ...>
    question: <what the experiment tests>
    locations:
      - machine: coulson
        root: <absolute-experiment-directory>
    authoritative_location: null
    status_command: null
    artifacts: []
    figures: []
```

Use machine IDs from `machines.yaml` and figure IDs from `figures/`. Leave unknown fields as `null` or empty lists. Keep project locations above as discovery roots; experiment locations identify the specific run collections.

## Inspecting results and preparing figures

Inspect through an available connection and record the observation time, machine, run IDs, completion evidence, code commit and uncommitted changes, configuration and input identifiers. If a machine is unreachable, report the last observation and its age; its experiment state remains unknown without fresh evidence. Keep changing status observations and downloaded inputs under the gitignored `.experiments/` directory at the repository root.

Retrieve selected outputs into staging and check their checksums, expected run coverage, numerical validity and compatible datasets, units and configurations before combining them. File availability alone does not establish completion or scientific validity.

Use the existing [figure workflow](../../figures/README.md) to generate panels through `figures/<fig-id>/make.py` or `make.tex`, or record unchanged manuscript figures in `ORIGIN.md`. Preserve source run IDs, input checksums and the build command beside the figure. Inspect the rendered output before using it in the thesis. Refreshing experiment observations must not silently replace figure inputs.

The index currently provides the handoff for locating experiments. Automated inspection, transfer and validation commands can be added once working connections and project-specific commands have been recorded.
