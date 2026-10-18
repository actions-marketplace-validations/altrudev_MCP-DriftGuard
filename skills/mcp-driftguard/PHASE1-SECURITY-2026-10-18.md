# Phase 1 security hardening verification — 2026-10-18

**Status: local security regression PASS; production release BLOCKED**

Pinned source revision: `8aa6b95fa27be6548aa90b6a46bcb331579cbce5`.
VPS: Linux amd64 `vps-377a113a`.

## Changes tested

- Authorization metadata downloads now reject bodies exceeding 1 MiB, instead of returning silently truncated data. Added tests for oversized bodies and the existing no-follow redirect policy.
- For Linux stdio transport, the launched child is assigned a new process group and the group receives SIGKILL during cleanup. Other operating systems retain parent-process termination only. This improves cleanup of descendants that remain in the group; descendants that detach or deliberately create new sessions are **not** comprehensively contained.
- Existing allowlists, minimal subprocess environment, discovery timeout and malformed JSON-RPC handling remain mandatory.

## Verified local commands

- `python3 scripts/conformance_suite.py --output security-phase1.json`: six gates PASS (unit, race, vet, documentation, HTTP, stdio).
- `gofmt -l .`: no findings.
- `GOOS=darwin GOARCH=arm64 go build ./cmd/mcpdrift`: PASS (cross compilation only).
- `GOOS=windows GOARCH=amd64 go build ./cmd/mcpdrift`: PASS (cross compilation only).

## Limits

- The Linux process-group cleanup implementation is compile- and regression-tested, but not yet independently validated against all child-tree escape strategies or host sandbox policies.
- Native macOS and Windows execution remains untested; cross-compilation does not establish compatibility.
- Authentication tests do not exhaust OAuth issuer redirection, DNS rebinding, authorization server metadata or sensitive-error redaction scenarios.
- The Federation B0/B2/B6/B7 independent rerun is still necessary.
- Full production sandbox, agent-host testing, release signing and legal review remain open.

**Do not label this result production security acceptance or formal certification.**
