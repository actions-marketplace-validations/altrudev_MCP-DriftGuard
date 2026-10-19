#!/usr/bin/env python3
"""Offline, bounded extreme-limit verification. No real MCP endpoints or paid services."""
import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SIZES = (10, 100, 1000, 10000)

def invoke(argv, environment=None, timeout=35):
    start = time.monotonic()
    try:
        result = subprocess.run([str(x) for x in argv], cwd=ROOT, env=environment,
                                capture_output=True, timeout=timeout)
        return {"exit": result.returncode, "seconds": round(time.monotonic() - start, 3),
                "stdout_sha256": hashlib.sha256(result.stdout).hexdigest(),
                "stdout_bytes": len(result.stdout), "stderr_bytes": len(result.stderr),
                "stdout": result.stdout}
    except subprocess.TimeoutExpired:
        return {"exit": 124, "seconds": round(time.monotonic() - start, 3),
                "stderr_bytes": 0, "stdout_bytes": 0, "stdout": b""}

def invoke_mcp(exe, fixture, size, mode, operation, baseline=None):
    args = [str(size), mode]
    env = os.environ.copy()
    approved_args = [str(fixture), *args]
    env["MCPDRIFT_STDIO_ALLOWED_EXEC"] = sys.executable
    env["MCPDRIFT_STDIO_ALLOWED_ARGS_JSON"] = json.dumps(approved_args)
    argv = [exe, operation, "--stdio-exec", sys.executable,
            "--stdio-args-json", json.dumps(approved_args)]
    if operation == "inspect":
        argv += ["--format", "json"]
    if operation == "baseline":
        argv += ["--output", baseline]
    if operation == "verify":
        argv += ["--baseline", baseline]
    return invoke(argv + ["stdio"], env)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="10,100,1000,10000")
    ap.add_argument("--output", help="write JSON evidence to file")
    opts = ap.parse_args()
    sizes = [int(x) for x in opts.sizes.split(",")]
    if not sizes or len(set(sizes)) != len(sizes) or any(x not in ALLOWED_SIZES for x in sizes):
        ap.error("sizes must be unique and selected from 10,100,1000,10000")
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    evidence = {"format": "mcpdrift-extreme-limits/v1", "commit": commit,
                "platform": platform.system(), "arch": platform.machine(),
                "limits": {"max_tools": 10000, "page_size": 100, "per_command_timeout_seconds": 35,
                           "max_parallel_cases": 1},
                "tests": [], "passed": False}
    with tempfile.TemporaryDirectory(prefix="mcpdrift-extreme-") as directory:
        home = Path(directory)
        exe = home / "mcpdrift"
        fixture = home / "server.py"
        build = invoke(["go", "build", "-o", exe, "./cmd/mcpdrift"], timeout=90)
        if build["exit"]:
            raise RuntimeError("Go binary build failed")
        shutil.copyfile(ROOT / "examples/stress-fixture/server.py", fixture)
        fixture.chmod(0o700)
        for size in sizes:
            baseline = home / ("approved-%s.json" % size)
            inspect = invoke_mcp(exe, fixture, size, "normal", "inspect")
            discovered = None
            if inspect["exit"] == 0:
                try:
                    discovered = len(json.loads(inspect["stdout"])["tools"])
                except (ValueError, KeyError, TypeError):
                    pass
            save = invoke_mcp(exe, fixture, size, "normal", "baseline", baseline)
            before = baseline.read_bytes() if baseline.exists() else None
            unchanged = invoke_mcp(exe, fixture, size, "normal", "verify", baseline)
            (home / "stress.drift").touch()
            drift = invoke_mcp(exe, fixture, size, "normal", "verify", baseline)
            (home / "stress.drift").unlink()
            case = {"kind": "inventory_scale", "tools": size, "discovered": discovered,
                    "inspect_exit": inspect["exit"], "baseline_exit": save["exit"],
                    "unchanged_exit": unchanged["exit"], "drift_exit": drift["exit"],
                    "baseline_unchanged": before is not None and baseline.read_bytes() == before,
                    "seconds": {"inspect": inspect["seconds"], "baseline": save["seconds"],
                                "unchanged": unchanged["seconds"], "drift": drift["seconds"]},
                    "stdout_digest": inspect.get("stdout_sha256")}
            case["passed"] = (discovered == size and inspect["exit"] == 0 and save["exit"] == 0
                              and unchanged["exit"] == 0 and drift["exit"] == 2
                              and case["baseline_unchanged"])
            evidence["tests"].append(case)
            print("scale", size, "PASS" if case["passed"] else "FAIL", flush=True)
        for mode in ("missing", "cursor-loop", "wrong-id", "malformed"):
            result = invoke_mcp(exe, fixture, 10, mode, "inspect")
            case = {"kind": "malformed_discovery", "mode": mode,
                    "exit": result["exit"], "seconds": result["seconds"],
                    "passed": result["exit"] == 3}
            evidence["tests"].append(case)
            print("negative", mode, "PASS" if case["passed"] else "FAIL", flush=True)
    evidence["passed"] = all(x["passed"] for x in evidence["tests"])
    rendered = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if opts.output:
        Path(opts.output).write_text(rendered)
    else:
        print(rendered)
    return 0 if evidence["passed"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
