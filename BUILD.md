# Build and run

There is no compile step. The harness is plain Python 3 and is started
through the shell entrypoint.

## Requirements

- Python 3.10 or newer
- `numpy` (used by `harness/cz_agent.py`)
- `scipy` (used by `harness/cz_agent.py` for least-squares fits)
- `mcp` (Model Context Protocol Python SDK, used by `harness/qsim.py`
  and `harness/cz_agent.py`)

No other packages are required. Dependencies are provided by the
runner image; they are not vendored here.

## Entrypoint

```
sh adapter/run.sh
```

`adapter/run.sh` executes `harness/runtime.py`, which reads
`harness.json` and launches the native CLI selected there.

## Environment contract

Provided by the platform runner:

| Variable | Meaning |
| --- | --- |
| `QIQC_TASK_INPUT` | path to the task statement |
| `QIQC_MODEL_URL` | model gateway base URL |
| `QIQC_MODEL_TOKEN` | gateway token |
| `QIQC_MODEL` | model name |
| `QIQC_MCP_SERVERS` | JSON array of task MCP servers |
| `QIQC_AGENT_TIMEOUT` | wall-clock budget in seconds |

Optional: `QIQC_MODEL_PROTOCOL`, `QIQC_RUNTIME_STATE`,
`QIQC_OUTPUT`, `QIQC_TRAJECTORY`, `QIQC_BATCH_OUT`,
`QIQC_CZ_STATE`.

## Minimal smoke test

With a stub CLI on `PATH` that prints one line
`{"type":"final","text":"ok"}` and exits 0:

```
QIQC_TASK_INPUT=/tmp/task.md \
QIQC_MODEL_URL=https://example.test/v1 \
QIQC_MODEL_TOKEN=tok \
QIQC_MODEL=deepseek-v4 \
QIQC_AGENT_TIMEOUT=60 \
QIQC_OUTPUT=/tmp/answer.txt \
QIQC_TRAJECTORY=/tmp/traj.jsonl \
sh adapter/run.sh
```

Expected: exit code 0 and `/tmp/answer.txt` written.
