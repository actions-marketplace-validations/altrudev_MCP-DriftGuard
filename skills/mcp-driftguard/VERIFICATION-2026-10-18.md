# Prometheus verification record — 2026-10-18

Repository: `altrudev/MCP-DriftGuard`

Tested commit: `013aeaafe5fe29dbb931d1cc44e023bc8e20f764`

Execution environment: connected `prometheus` host, Linux amd64, Go 1.26.8. Audit cloned into temporary `/tmp/mcpdrift-audit.s837p3/repo`; test fixture bound to loopback only.

## Confirmed results

- `go test ./...`: PASS (all tested packages; command and demo packages report no test files).
- `go vet ./...`: PASS (exit 0).
- `go build -o .../mcpdrift ./cmd/mcpdrift`: PASS; executable verified with `mcpdrift version` (reports `dev`).
- Local example server baseline creation: PASS, exit 0.
- Local unchanged live observation vs approved fixture baseline: PASS, exit 0. JSON: `{"match":true,"risk":"NONE","score":0,"changes":null}`.
- Local changed example server (`MCPDRIFT_DEMO_DRIFT=1`): FAIL as expected, exit 2. JSON reports HIGH capability addition `tools.export_customer_database`, score 35.
- Unreachable loopback endpoint: probe failure exit 3, with connection refused stderr.
- Missing baseline path: artifact failure exit 4.
- Tampered baseline hash: integrity failure exit 5, with canonical hash mismatch stderr.

No secrets, production endpoints, or signing keys were used.

## Still unverified — blocking marketplace release

- REVIEW-level exit code 1; distinct signed-baseline test with a trusted key.
- Independent MCP implementation interoperability and pagination/auth metadata edge cases.
- Agent integration in actual Claude Code, Cursor and Codex hosts, including injection resistance.
- Clean-machine installation, portability and agent skill metadata acceptance.
- Marketplace submissions, terms, payout due diligence and truthful commercial packaging.

This record is a scoped local executable verification, **not** independent interoperability certification, a security audit of all paths, or production acceptance. Never extrapolate fixture PASS to unaudited production endpoints.

## Follow-up signed-baseline and REVIEW investigation

- `keygen` generated a temporary Ed25519 keypair: exit 0.
- A signed baseline was created against the isolated loopback fixture: exit 0.
- Verification with the matching public key returned PASS, exit 0.
- Modifying the signed artifact's server metadata without updating its canonical hash returned integrity rejection, exit 5.
- A temporary demo server variant changed self-reported server version from `1.0.0` to `1.0.1`; the observed verification still returned PASS, exit 0. **This does not establish correct REVIEW behavior.** The discrepancy requires source investigation before declaring version-metadata drift detection functional. The changed process did start, but the comparison may not have reached or retained the altered field. Do not claim this gate passed.
- All test key materials and modified fixture files were kept in temporary paths outside the GitHub repository.

Remaining gate: reproduce REVIEW exit 1 with an actual lower-risk difference; diagnose the version-change discrepancy and add a regression test if reproducible.

## Verified regression repair — commit 693f6ee11412e249aa2419ed02cb9f2bc0c0a0ba

Root cause of the unexpected version-change PASS: the observer retained `server.version`, but `internal/diff/diff.go` did not compare it. Added explicit LOW-severity `server.version` comparison and a regression unit test.

On Prometheus at this commit, `go test ./...`, `go vet ./...`, and the CLI build all passed. A real loopback example server reporting version `1.0.1` was compared against the previously created baseline at version `1.0.0`; the executable returned `match:false`, `risk:LOW`, `score:5`, `server.version` change and **exit status 1 (REVIEW)**.

Signed-baseline creation, matching public-key verification, and tampered signed-baseline rejection also passed on the prior revision.

Remaining independently unverified gates: cross-implementation MCP interoperability; installed-agent behavior for Claude Code, Cursor and Codex; safe packaging on clean hosts; marketplace terms and human-approved publication.
