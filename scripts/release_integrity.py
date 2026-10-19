#!/usr/bin/env python3
"""Read-only release evidence gate. Never converts an absent check into PASS."""
import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("go_unit","go_race","go_vet","docs","http_acceptance","stdio_acceptance","extreme_limits")

def assess(evidence, expected):
    failures=[]
    if evidence.get("commit") != expected:
        failures.append("evidence commit differs from candidate")
    if evidence.get("passed") is not True:
        failures.append("conformance aggregate not PASS")
    suites=evidence.get("suites")
    if not isinstance(suites,dict):
        return failures+["missing suite evidence"]
    for name in REQUIRED:
        result=suites.get(name)
        if (not isinstance(result,dict) or type(result.get("exit")) is not int
                or result["exit"] != 0):
            failures.append("required suite absent or failed: "+name)
        elif not all(isinstance(result.get(key),str) and len(result[key]) == 64
                     and all(ch in "0123456789abcdef" for ch in result[key])
                     for key in ("stdout_sha256","stderr_sha256")):
            failures.append("missing or malformed output digest: "+name)
    return failures

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--evidence",required=True)
    parser.add_argument("--commit",help="immutable candidate commit; defaults to checkout HEAD")
    args=parser.parse_args()
    actual=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    expected=args.commit or actual
    failures=[]
    if actual != expected:
        failures.append("checkout HEAD differs from candidate")
    if subprocess.check_output(["git","status","--porcelain"],cwd=ROOT,text=True).strip():
        failures.append("checkout has uncommitted changes")
    try:
        obj=json.loads(Path(args.evidence).read_text())
        failures+=assess(obj,expected)
    except (OSError,ValueError) as error:
        failures.append("unreadable or invalid evidence: "+str(error))
    # Hosted CI is separately required. This local check is never release authorization.
    print(json.dumps({"schema":"mcpdrift-release-integrity/v1","commit":expected,
        "verdict":"BLOCKED" if failures else "LOCAL_EVIDENCE_VALIDATED",
        "failures":failures,"hosted_ci":"UNVERIFIED","release_authorized":False},indent=2))
    return 1 if failures else 0

if __name__=="__main__":
    sys.exit(main())
