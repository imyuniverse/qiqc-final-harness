# Changes relative to the Quantum-Harbor starter harness

## Added files

- `harness/cz_agent.py` — measured-in-situ solver for the tunable-coupler
  net-zero CZ task: square-step cryoscope fit of the flux-line settling
  poles, 2-D |11>-|02> chevron for alpha_2 and J, mirrored net-zero
  trajectory with rational-inverse predistortion, shot-measured
  conditional-phase loop to pi, verification, and submission through the
  task's own `submit_final_answer`.
- `harness/PLAYBOOK.md` — documentation of the solver's physics and
  acceptance checks.

## Modified files

### `harness/runtime.py`

- Task-facing prompt additions for the CZ task (solver guidance).
- Budget discipline: an explicit time table at the top of the prompt,
  a 60%/70% milestone for one-shot lock/reveal tasks, an 80% stop-and-
  submit rule, an "insurance submission" rule, a ban on guessing or
  brute-forcing platform internals (hashes, digests, UUIDs, artefact
  names) with hashes computed via `hashlib`, and a ban on probing
  undocumented service behaviour.
- Terminal-event handling: a DeepSeek run that already emitted a
  `final` event is no longer converted into an infrastructure failure
  when a provider error is printed afterwards; the verifier scores the
  scientific outcome instead.
- Prompt guidance for the batch client (`qsim.py batch`) with the
  constraint that batch may be used only when the task documents a
  per-request identifier or guarantees ordered results.

### `harness/qsim.py`

- New `batch` action: run a JSON plan of tool calls over one MCP
  session, print one short summary line per call, and write full
  payloads to `QIQC_BATCH_OUT`. Keeps large results out of the
  transcript. Existing `list` and `call` behaviour is unchanged.

### `harness.json`

- `runtime` set to `deepseek`.
- Added `name` and `description`.

## Unchanged upstream files

`adapter/run.sh`, `harness/terminal.py`, `harness/README.md`.
