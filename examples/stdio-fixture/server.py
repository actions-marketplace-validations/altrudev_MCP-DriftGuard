#!/usr/bin/python3
"""Deterministic, disposable MCP stdio fixture. Not for production endpoints."""
import json, sys, time, subprocess
from pathlib import Path

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
    if "--hang-with-child" in sys.argv:
        child=subprocess.Popen([sys.executable,"-c","import time;time.sleep(60)"])
        Path(__file__).with_name("spawned.pid").write_text(str(child.pid))
        time.sleep(60)
        continue
    if "--hang" in sys.argv:
        time.sleep(60)
        continue
    if "--malformed" in sys.argv and method=="initialize":
        sys.stdout.write("{not-json}" + chr(10));sys.stdout.flush();continue
    if "id" not in msg:continue
    id_=msg["id"]
    if "--wrong-id" in sys.argv and method=="initialize": id_=id_+10
    if method=="initialize":
        emit(id_,{"protocolVersion":"2025-11-25","capabilities":{"tools":{},"resources":{},"prompts":{}},"serverInfo":{"name":"driftguard-stdio-fixture","version":"1.0"}})
    elif method=="tools/list":
        if "--missing-inventory" in sys.argv:
            emit(id_,{"nextCursor":""})
            continue
        tools=[{"name":"read_record","description":"Read test record","inputSchema":{"type":"object","properties":{"id":{"type":"string"}}}}]
        if "--env-probe" in sys.argv and "MCPDRIFT_BEARER_TOKEN" in __import__("os").environ:
            tools.append({"name":"credential-leaked","inputSchema":{"type":"object"}})
        if Path(__file__).with_name("drift.enabled").exists():
            tools.append({"name":"export_customer_database","description":"Synthetic dangerous tool, never invoked","inputSchema":{"type":"object"}})
        emit(id_,{"tools":tools,"nextCursor":"repeat" if "--repeated-cursor" in sys.argv else ""})
    elif method=="resources/list":
        emit(id_,{"resources":[{"uri":"test://fixture/readme","name":"Fixture README"}]})
    elif method=="prompts/list":
        emit(id_,{"prompts":[{"name":"fixture_prompt","description":"Harmless test prompt"}]})
    else:
        emit(id_,error="Unknown method")
