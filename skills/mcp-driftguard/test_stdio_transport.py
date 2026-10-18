#!/usr/bin/env python3
"""Disposable end-to-end stdio MCP acceptance. Never launches arbitrary user executables."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
def call(args, env=None, cwd=None, timeout=35):
    return subprocess.run(list(map(str,args)),cwd=cwd or ROOT,env=env,text=True,
                          capture_output=True,timeout=timeout)

def main():
    results={}
    with tempfile.TemporaryDirectory(prefix="mcpdrift-stdio-") as td:
        t=Path(td); exe=t/"mcpdrift"; fixture=t/"server.py"
        build=call(["go","build","-o",exe,"./cmd/mcpdrift"])
        if build.returncode:raise RuntimeError(build.stderr)
        shutil.copyfile(ROOT/"examples/stdio-fixture/server.py",fixture)
        fixture.chmod(0o700)
        env=os.environ.copy();env.pop("MCPDRIFT_FIXTURE_DRIFT",None)
        env["MCPDRIFT_STDIO_ALLOWED_EXEC"]=str(fixture)
        common=["--stdio-exec",fixture]
        baseline=t/"approved.json"
        r=call([exe,"inspect",*common,"--format","json","stdio"],env)
        results["inspect"]=r.returncode
        if r.returncode==0:
            snap=json.loads(r.stdout)
            results["inventory"]=tuple(len(snap[x]) for x in ("tools","resources","prompts"))==(1,1,1)
        r=call([exe,"baseline",*common,"--output",baseline,"stdio"],env)
        results["baseline"]=r.returncode
        before=baseline.read_bytes() if baseline.exists() else b""
        r=call([exe,"verify",*common,"--baseline",baseline,"stdio"],env)
        results["unchanged"]=r.returncode
        (t/"drift.enabled").touch()
        r=call([exe,"verify",*common,"--baseline",baseline,"stdio"],env)
        results["drift"]=r.returncode
        results["detected_added_tool"]="export_customer_database" in r.stdout
        (t/"drift.enabled").unlink()
        env2=dict(env);env2["MCPDRIFT_STDIO_ALLOWED_EXEC"]=str(t/"unapproved")
        r=call([exe,"inspect",*common,"stdio"],env2)
        results["unapproved_executable"]=r.returncode
        r=call([exe,"inspect","--stdio-exec",fixture,"--stdio-args-json","not-json","stdio"],env)
        results["bad_args"]=r.returncode
        for mode in ("--malformed","--wrong-id","--repeated-cursor"):
            r=call([exe,"inspect",*common,"--stdio-args-json",json.dumps([mode]),"stdio"],env)
            results[mode]=r.returncode
        secret_env=dict(env);secret_env["MCPDRIFT_BEARER_TOKEN"]="synthetic-stdio-secret"
        r=call([exe,"inspect",*common,"--stdio-args-json",json.dumps(["--env-probe"]),"--format","json","stdio"],secret_env)
        results["env_secret_isolated"]=r.returncode==0 and "credential-leaked" not in r.stdout and "synthetic-stdio-secret" not in r.stdout
        results["baseline_unchanged"]=baseline.read_bytes()==before
    expected={"inspect":0,"inventory":True,"baseline":0,"unchanged":0,"drift":2,
              "detected_added_tool":True,"unapproved_executable":3,"bad_args":3,
              "baseline_unchanged":True,
              "--malformed":3,"--wrong-id":3,"--repeated-cursor":3,
              "env_secret_isolated":True}
    results["pass"]=all(results.get(k)==v for k,v in expected.items())
    print(json.dumps(results,indent=2,sort_keys=True))
    return 0 if results["pass"] else 1

if __name__=="__main__":raise SystemExit(main())
