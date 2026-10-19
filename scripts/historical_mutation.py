#!/usr/bin/env python3
"""Verify historical regression tests detect deliberately reintroduced defects.
Runs mutations only in disposable source copies. Never edits the working tree.
"""
import io
import json
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CASES=[
 ("B0_B2_JSON_CANONICAL","internal/diff/diff.go",
  "if !rawEqual(at.InputSchema, bt.InputSchema) {",
  "if !bytes.Equal(at.InputSchema, bt.InputSchema) {",
  "./internal/diff","TestSemanticallyIdenticalJSONIsNotDrift"),
 ("B6_SIGNED_DOWNGRADE","internal/baseline/baseline.go",
  'if len(publicKey) > 0 && a.Signature == nil {',
  'if false && len(publicKey) > 0 && a.Signature == nil {',
  "./internal/baseline","TestVerificationKeyRejectsUnsignedBaseline"),
 ("B4B_PARAPHRASE","internal/diff/diff.go",
  '"before any other tool", ',
  '"not-present-in-input", ',
  "./internal/diff","TestFederationB4bParaphrasedAuthorityInstruction"),
]
def main():
    revision=subprocess.check_output(["git","rev-parse","HEAD"],cwd=ROOT,text=True).strip()
    output={"format":"mcpdrift-historical-mutation/v1","revision":revision,"cases":[]}
    for name,path,needle,replacement,pkg,test in CASES:
        with tempfile.TemporaryDirectory(prefix="mcpdrift-mutation-") as temp:
            target=Path(temp)
            archive=subprocess.run(["git","archive","--format=tar",revision],cwd=ROOT,
                                   capture_output=True,check=True).stdout
            with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
                for item in bundle:
                    destination=(target/item.name).resolve()
                    if not destination.is_relative_to(target.resolve()):
                        raise ValueError("unsafe archived path")
                bundle.extractall(target,filter="data")
            source=target/path
            original=source.read_text()
            count=original.count(needle)
            if count!=1:
                output["cases"].append({"case":name,"passed":False,"reason":"mutation anchor count "+str(count)})
                continue
            source.write_text(original.replace(needle,replacement,1))
            completed=subprocess.run(["go","test",pkg,"-run","^"+test+"$","-count=1"],
                                     cwd=target,capture_output=True,text=True,timeout=90)
            output["cases"].append({"case":name,"passed":completed.returncode!=0,
                                    "test_exit":completed.returncode,
                                    "failure_excerpt":(completed.stdout+completed.stderr)[-450:]})
        print(name,"DETECTED" if output["cases"][-1]["passed"] else "NOT DETECTED",flush=True)
    output["passed"]=len(output["cases"])==len(CASES) and all(x["passed"] for x in output["cases"])
    print(json.dumps(output,indent=2,sort_keys=True))
    return 0 if output["passed"] else 1
if __name__=="__main__":
    raise SystemExit(main())
