#!/usr/bin/env python3
"""Agent-side access to the original task's MCP service; no proxy or scorer."""

import argparse
import asyncio
import json
import os
import pathlib


async def main():
    from mcp import ClientSession
    from mcp.client.streamable_http import streamable_http_client

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("list", "call", "batch"))
    parser.add_argument("tool", nargs="?")
    parser.add_argument("arguments", nargs="?", default="{}")
    args = parser.parse_args()
    servers = json.loads(os.environ["QIQC_MCP_SERVERS"])
    if len(servers) != 1 or servers[0]["transport"] != "streamable-http":
        parser.error("Expected one task MCP service from the runner")
    if args.action in ("call", "batch") and not args.tool:
        parser.error(args.action + " requires a tool name or a plan file")
    parameters = json.loads(args.arguments)
    if not isinstance(parameters, dict):
        parser.error("tool arguments must be a JSON object")
    async with streamable_http_client(servers[0]["url"]) as (reader, writer, _):
        async with ClientSession(reader, writer) as session:
            await session.initialize()
            if args.action == "batch":
                # One connection for a whole plan; payloads go to a file so the
                # transcript keeps only short summaries.
                plan = json.loads(pathlib.Path(args.tool).read_text())
                out_path = pathlib.Path(
                    os.environ.get("QIQC_BATCH_OUT", "/tmp/qsim-batch.jsonl")
                )
                failures = 0
                with out_path.open("w") as sink:
                    for step in plan:
                        result = await session.call_tool(
                            step["tool"], step.get("arguments") or {}
                        )
                        payload = result.model_dump(mode="json")
                        sink.write(
                            json.dumps({"tool": step["tool"], "call": step,
                                        "result": payload}) + "\n"
                        )
                        failed = bool(getattr(result, "isError", False))
                        failures += failed
                        print(
                            f"{step['tool']}: {'error' if failed else 'ok'} "
                            f"({len(json.dumps(payload))} B -> {out_path})",
                            flush=True,
                        )
                return 1 if failures else 0
            result = (await session.list_tools() if args.action == "list"
                      else await session.call_tool(args.tool, parameters))
            print(json.dumps(result.model_dump(mode="json")))
            if getattr(result, "isError", False):
                return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
