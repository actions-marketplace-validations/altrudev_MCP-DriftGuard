# Extreme Limits Laboratory v1 — bounded acceptance evidence

**Status: local synthetic extreme-test PASS. Production release: BLOCKED.**

## Pinned execution

Source revision: `115c2ca974840c451ac18401a57e6e3da394c9b5`.

Test runner: `python3 scripts/extreme_limits.py --output extreme-measurements.json`.
Unified runner: `python3 scripts/conformance_suite.py --output conformance.json`.
Execution environment: Linux amd64 VPS `vps-377a113a`, synthetic local stdio fixtures, no customer systems, network dependencies or paid services.

## Bounded scale observations

Each workload starts a disposable MCP JSON-RPC stdio server with 100 tools per page and a total inventory of the specified size. Each case asserts complete discovery, baseline creation, unchanged verifier PASS (0), unexpected added tool FAIL (2), and baseline byte immutability.

| Tools | Inspect time (s) | Baseline time (s) | Clean verify (s) | Drift verify (s) | Verdict |
|---:|---:|---:|---:|---:|---|
| 10 | 0.033 | 0.039 | 0.032 | 0.031 | PASS |
| 100 | 0.034 | 0.033 | 0.035 | 0.033 | PASS |
| 1,000 | 0.042 | 0.044 | 0.047 | 0.046 | PASS |
| 10,000 | 0.136 | 0.137 | 0.151 | 0.154 | PASS |

These short times reflect local synthetic fixtures on one VPS. They do not establish remote-network latency, arbitrary real MCP server performance, or throughput across OS architectures.

## Concurrency and malformed protocol

- 20 simultaneous logical verification requests, bounded to four worker processes, all returned exit 0 against a shared read-only approved baseline. Original baseline bytes remained unchanged.
- Missing inventory, repeated cursor, incorrect JSON-RPC ID and malformed response each returned probe failure (exit 3), rather than reporting a false PASS.
- Workload cap is 10,000 tools, 100-page pagination, four concurrent workers, with an outer per-command timeout of 35 seconds. No CPU/memory sabotage, fork bombs or production endpoints were exercised.

## Final consolidated conformance

The seven-gate conformance runner passed: Go unit, Go race, vet, documentation, HTTP acceptance, stdio acceptance and extreme-limit suite.

SHA-256 of VPS artifacts:
- `extreme-measurements-verified.json`: `6eb84b25a970c266c148ebe1107cf6ec2f19835326f7cad7983d2b99f419b933`
- `extreme-conformance-verified.json`: `7116262b4d85821596aaf472d64ee88419f8677ea2cf0ea04ed9e1cb0807a717`

These retained files are in the VPS test directory; they are not signed release assets.

## Unverified release conditions

- No exhaustive real-world JSON Schema complexity/memory pressure, malformed SSE/HTTP fuzzing or OAuth/DNS rebinding stress evidence.
- No 100-concurrent-job soak run, long-duration endurance test, deliberately low-resource host verification or independently administered platform matrix.
- No independently confirmed Federation B0/B2/B6/B7 rerun at this report's preparation.
- Native macOS/Windows and Claude/Codex/Cursor agent-host acceptance, release signatures and legal sign-off remain open.

The laboratory expands measurable coverage; it does not authorize production release or imply universal compatibility.
