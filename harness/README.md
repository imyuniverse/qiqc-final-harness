# QIQC starter harness

adapter/run.sh starts harness/runtime.py, which runs the native CLI named by
harness.json inside the isolated task container. There is no HTTP fallback.

harness.json only needs the runtime, for example {"runtime": "codex"}.
Allowed runtimes: codex, deepseek, pi. Optional fields: entrypoint (default
adapter/run.sh), name and description. The platform checks the supported runtime
version window and protocol and numbers your uploads v1, v2, ... automatically.
