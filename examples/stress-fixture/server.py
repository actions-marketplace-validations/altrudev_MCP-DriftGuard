#!/usr/bin/python3
"""Bounded, synthetic MCP stdio inventory server. No network access or tool calls."""
import json
import sys
from pathlib import Path

size = int(sys.argv[1]) if len(sys.argv) > 1 else 10
if size not in (10, 100, 1000, 10000):
    raise SystemExit("unsupported scale")
mode = sys.argv[2] if len(sys.argv) > 2 else "normal"
marker = Path(__file__).with_name("stress.drift")

def reply(identifier, result):
    sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": identifier, "result": result}, separators=(",", ":")) + "\n")
    sys.stdout.flush()

for line in sys.stdin:
    try:
        request = json.loads(line)
    except ValueError:
        continue
    if "id" not in request:
        continue
    method = request.get("method")
    identifier = request["id"]
    if method == "initialize":
        reply(identifier, {"protocolVersion": "2025-11-25", "capabilities": {"tools": {}},
                          "serverInfo": {"name": "driftguard-stress", "version": "1"}})
    elif method == "tools/list":
        if mode == "missing":
            reply(identifier, {})
            continue
        if mode == "cursor-loop":
            reply(identifier, {"tools": [], "nextCursor": "stuck"})
            continue
        if mode == "wrong-id":
            reply(identifier + 1, {"tools": []})
            continue
        if mode == "malformed":
            sys.stdout.write("{broken-json\n")
            sys.stdout.flush()
            continue
        cursor = request.get("params", {}).get("cursor", "")
        page = int(cursor) if cursor else 0
        page_size = 100
        end = min(page + page_size, size)
        tools = [{"name": "tool_%05d" % i, "description": "Synthetic read-only test %d" % i,
                  "inputSchema": {"type": "object", "properties": {"value": {"type": "string"}}}}
                 for i in range(page, end)]
        if end == size and marker.exists():
            tools.append({"name": "unexpected_export", "inputSchema": {"type": "object"}})
        output = {"tools": tools}
        if end < size:
            output["nextCursor"] = str(end)
        reply(identifier, output)
    else:
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": identifier,
                                     "error": {"code": -32601, "message": "unsupported"}}) + "\n")
        sys.stdout.flush()
