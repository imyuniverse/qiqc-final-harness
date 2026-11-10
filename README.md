# qiqc-final-harness

QIQC Challenge 2026 final submission harness.
Team **Universal** · entrant **Ma Yuzhe**.

Full evaluation: **26 / 39 tasks**, average 3356 s per task.
Public tasks: 3 / 5 (logical CNOT decoder, Hamiltonian learning, net-zero CZ).

## Design

The harness has two layers.

**General layer** — identical for every task. `harness/runtime.py` builds the
task prompt, launches the native CLI named by `harness.json`, enforces the
wall-clock budget, and guarantees a valid submission exists before the run
ends. `harness/qsim.py` gives the agent a small client for the task's MCP
service (`list`, `call`, `batch`).

**Solver layer** — task-specific physics. Only one task has a dedicated
solver: `harness/cz_agent.py`, a measured-in-situ chain for the
tunable-coupler net-zero CZ task (cryoscope fit of the flux-line settling,
|11>-|02> chevron for the coupling, mirrored net-zero trajectory with
rational-inverse predistortion, shot-measured conditional-phase loop to pi,
verification, submission). `harness/PLAYBOOK.md` documents the physics.

Everything else runs on the general agent. That split is why failures are
diagnosable: a task either lacks a solver, or the delivery layer lost the
answer.

## Layout

```
adapter/run.sh        entrypoint (executes harness/runtime.py)
harness.json          runtime selector (deepseek)
harness/runtime.py    prompt assembly, CLI launch, timeout and submission guards
harness/qsim.py       MCP client: list / call / batch
harness/cz_agent.py   net-zero CZ solver (only task with a dedicated solver)
harness/terminal.py   terminal-event validation for the native CLI
harness/PLAYBOOK.md   physics and acceptance checks of the CZ solver
BUILD.md              requirements, entrypoint, environment contract
CHANGES.md            differences from the upstream starter harness
NOTICE                licensing: AGPL-3.0-only plus upstream MIT retention
LICENSE               AGPL-3.0 full text
```

## Running

See [BUILD.md](BUILD.md). There is no compile step; the entrypoint is
`sh adapter/run.sh` and the platform supplies the environment variables.

## License

Team additions and modifications are released under **AGPL-3.0-only**
(see `LICENSE`). Files derived from the MIT-licensed Quantum-Harbor starter
harness keep their original MIT terms and are not relicensed; the split is
described in `NOTICE`.

## Note on evaluation data

This repository contains no hidden task materials and no private evaluation
records.
