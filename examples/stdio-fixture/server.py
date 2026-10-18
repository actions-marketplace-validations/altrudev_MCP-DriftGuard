#!/usr/bin/python3
"""Deterministic, disposable MCP stdio fixture. Not for production endpoints."""
import json, os, sys

def emit(id_, result=None, error=None):
    message={"jsonrpc":"2.0","id":id_}
    if error is not None: message["error"]={"code":-32601,"message":error}
    else: message["result"]=result
    sys.stdout.write(json.dumps(message,separators=(",",":"))+"\n")
    sys.stdout.flush()

for raw in sys.stdin:
    try:
        msg=json.loads(raw)
    except ValueError:
        continue
    method=msg.get("method")
    if "id" not in msg:continue
    id_=msg["id"]
    if method=="initialize":
        emit(id_,{"protocolVersion":"2025-11-25","capabilities":{"tools":{},"resources":{},"prompts":{}},"serverInfo":{"name":"driftguard-stdio-fixture","version":"1.0"}})
    elif method=="tools/list":
        tools=[{"name":"read_record","description":"Read test record","inputSchema":{"type":"object","properties":{"id":{"type":"string"}}}}]
        if os.getenv("MCPDRIFT_FIXTURE_DRIFT")=="1":
            tools.append({"name":"export_customer_database","description":"Synthetic dangerous tool, never invoked","inputSchema":{"type":"object"}})
        emit(id_,{"tools":tools})
    elif method=="resources/list":
        emit(id_,{"resources":[{"uri":"test://fixture/readme","name":"Fixture README"}]})
    elif method=="prompts/list":
        emit(id_,{"prompts":[{"name":"fixture_prompt","description":"Harmless test prompt"}]})
    else:
        emit(id_,error="Unknown method")
