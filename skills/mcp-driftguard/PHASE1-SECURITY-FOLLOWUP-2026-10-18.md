# Phase 1 security acceptance follow-up — 2026-10-18

**Local security acceptance: PASS. Production release: BLOCKED.**

## Verified source and host

Code revision exercised against full six-suite acceptance: `dbcf371bd4eb0d6b0e8f41e1c419fe7001104fed`. Linux amd64 VPS `vps-377a113a`. This document and the release-gate checklist were committed subsequently without executable source changes.

## Security improvements and observations

1. OAuth metadata body limit: reject responses exceeding 1 MiB, rather than accept truncated JSON. Tests use synthetic oversized HTTP responses.
2. Cross-origin issuer approval: discovered authorization server issuer metadata at a different origin is fetched only when its origin is explicitly configured in `MCPDRIFT_ALLOWED_AUTH_ISSUERS`. Exact scheme/host/port matching; path-bearing approval entries and userinfo-bearing issuer URLs are not accepted. An unapproved synthetic issuer was not contacted. This is an SSRF mitigation, **not** a complete DNS/network isolation guarantee.
3. Linux stdio process-group cleanup: launch the subprocess in a separate process group and terminate the group on completion. A synthetic subprocess that forked a child revealed that the first implementation could hang beyond the configured deadline because the child kept the stdout pipe open; the outer test timed out after 35 seconds. Fixed with a context-deadline callback that kills the process group independently of the output scanner. The repeated test then completed at approximately the configured 20-second deadline with exit 3, and the test confirmed the same-group child was no longer running.
4. Fail-closed incomplete stdio inventory: an advertised `tools`, `resources` or `prompts` category must return its corresponding JSON array, including the empty array when no entries exist. Missing/null inventory is now a probe error. A synthetic omitted-tool-array fixture returned exit 3.
5. Existing stdio executable and entire argument-vector allowlists, minimal environment, no-shell launch and signature/transport regression gates remain in force.

## Full local suite results

`python3 scripts/conformance_suite.py --output security-phase1-final.json` returned `passed=true` for all six suites:

- `go_unit`: PASS.
- `go_race`: PASS.
- `go_vet`: PASS.
- `docs`: PASS.
- `http_acceptance`: PASS.
- `stdio_acceptance`: PASS, including process-group descendant termination regression.

`gofmt -l .` reported zero unformatted files. The VPS working tree was clean before the evidence-only follow-up commit. The local Ollama service was active.

Cross-compilation (not native execution) passed for Darwin ARM64 and Windows AMD64.

## SHA-256 of tested artifacts (VPS)

- `security-phase1-final.json`: `d8c0a17909ff8a40329dd1999aeb18c8402b75ccaf335bbd31e20fced573b3fb`.
- Darwin ARM64 cross-compiled binary `security-darwin`: `9d66bc53d7f796cf566c85f64461c5171c0c23dfe74998700ef7c5940a301bd3`.
- Windows AMD64 cross-compiled binary `security-win.exe`: `979aa343016cae210d0e6c2102ed48ff4382a90c9559d0aa785a355063dcb95f`.

These artifacts are on the VPS and have not been published as signed releases.

## Unresolved production blockers

- Linux process-group cleanup does not sandbox filesystem/network access or descendants that deliberately detach into other sessions or groups.
- OAuth remains incompletely tested across real issuers, DNS changes, network policy, credentials, proxies, TLS identity and metadata error redaction.
- No independent Horizon Shield rerun acceptance for repaired B0/B2/B6/B7 vectors.
- Native Windows/macOS execution, clean agent-host integration and signing/installation evidence are pending.
- No formal certification, production operator deployment review, or final legal/third-party attribution sign-off.

**Release decision remains BLOCKED.**
