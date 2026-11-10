# Submitted archive

This repository publishes the exact harness that was evaluated in the QIQC
Challenge 2026 expert final.

| | |
|---|---|
| Archive | `artifacts/qiqc-final-deepseek.zip` |
| Size | 19,831 bytes |
| SHA-256 | `d5880b17adfcdffacb306ff75a5ce498f01f545e59fda50ea41cfb3cd32bde5e` |
| Runtime | `deepseek` |
| Newest member | `harness.json`, 2026-11-10 01:29 |

## Byte identity

Every runtime file inside the archive is byte-identical to the copy at the
repository root. Verified with `shasum -a 256` on both sides:

```
SAME  harness.json
SAME  adapter/run.sh
SAME  harness/cz_agent.py
SAME  harness/qsim.py
SAME  harness/runtime.py
SAME  harness/terminal.py
SAME  harness/README.md
SAME  harness/PLAYBOOK.md
```

The archive therefore contains 8 files in 2 directories. Nothing was edited,
reformatted, or re-licensed between evaluation and publication.

## Verify it yourself

```sh
shasum -a 256 -c SHA256SUMS.txt
```

All nine lines must report `OK`. The first line checks the archived bundle,
the remaining eight check the working tree against it.

## What this repository adds

These files are packaging, not run-time code, and are not part of the
evaluated archive:

- `LICENSE` — AGPL-3.0-only, covering our additions
- `NOTICE` — attribution and the retained upstream MIT notice
- `README.md` — what the harness does and how to run it
- `BUILD.md` — build and packaging steps
- `CHANGES.md` — diff against the Quantum-Harbor starter harness
- `SHA256SUMS.txt` — the checksums above

Upstream starter files (`adapter/run.sh`, `harness/terminal.py`,
`harness/README.md`) keep their original MIT notice and are not relicensed.

## Results

Full evaluation: 26 of 39 tasks passed, mean 3,356 s per task. Public set:
3 of 5 passed — CNOT decoder, Hamiltonian learning, and the net-zero CZ. Both
public misses are 1,800 s tasks that require heavy numerical modelling written
from scratch inside the run.
