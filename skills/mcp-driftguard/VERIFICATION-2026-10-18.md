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
