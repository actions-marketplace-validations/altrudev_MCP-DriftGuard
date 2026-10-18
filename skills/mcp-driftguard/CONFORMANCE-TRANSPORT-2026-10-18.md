# MCP DriftGuard — transport and conformance evidence (2026-10-18)

**Status: LOCAL CONFORMANCE PASS / PRODUCTION RELEASE BLOCKED**

## Immutable source and environment

Code revision exercised for the complete six-gate run: `65987f516ac95ee0732087c85108f485ca3a9138`.

Host: `vps-377a113a` Linux amd64, Go 1.26.8, Node.js 24.21.0, Python 3.14.4.
Reference server: `@modelcontextprotocol/server-everything` 1.0.0, executed locally, with no production connections or paid services.

## Stdio implementation and command authority

The Go CLI now supports `inspect`, `baseline` and `verify` with `--stdio-exec ABSOLUTE_PATH`, optional `--stdio-args-json '[]'` and literal endpoint `stdio`. The observer speaks MCP initialize/initialized then paginates tool/resource/prompt inventory; it does not call tools.

The subprocess requires an exact executable path match to `MCPDRIFT_STDIO_ALLOWED_EXEC` and explicit full-argv approval by `MCPDRIFT_STDIO_ALLOWED_ARGS_JSON` when arguments are nonempty. There is no shell. Its environment does not inherit bearer tokens or arbitrary operator credentials. Stdout parsing is bounded to 4 MiB per message and protocol pagination is bounded. Discovery uses a 20-second context deadline. These measures do **not** constitute arbitrary-code sandboxing.

## Six-gate conformance run

`python3 scripts/conformance_suite.py --output conformance.json` produced `mcpdrift-conformance-evidence/v1` with `passed: true`. All six suite exit codes were zero:

1. Go package unit tests.
2. Go race-enabled unit tests.
3. Go vet static analysis.
4. Documentation and glossary structure gate.
5. Isolated HTTP baseline/PASS/FAIL/error acceptance.
6. Isolated stdio baseline/PASS/FAIL/authorization and negative-input acceptance.

Additional `gofmt -l .` check returned no unformatted files.

### Stdio-specific negative and safety cases

- Exact approved executable: inspect with one tool, resource and prompt returned 0.
- New unauthorized export tool: verify returned 2.
- Unapproved executable: return 3.
- Unapproved executable arguments: return 3.
- Invalid JSON argument array: return 3.
- Malformed JSON-RPC reply: return 3.
- Wrong JSON-RPC response ID: return 3.
- Repeated pagination cursor: return 3.
- Synthetic parent `MCPDRIFT_BEARER_TOKEN`: not visible in fixture subprocess.
- Stored approved baseline bytes: unchanged.
- Deliberately hanging single-process stdio fixture: observed timeout at ~20.0 seconds and exit code 3 (manual non-CI test).

## Independent protocol implementation cross-check

The official Everything reference server was independently exercised through stdio. Under the same read-only, minimal MCP client capability context, the stdio discovery result matched an earlier successful HTTP inspection in **all three inventory categories**: **13 tools, 7 resources, 4 prompts**. This is a cross-transport inventory check, not a formal MCP specification conformance result; reference-client capabilities can change exposed tool lists.

## SHA-256 checksums (VPS artifacts)

- Built Go CLI, `mcpdrift`: `1a304b5967e029e9c9f8344d09344a11160821988cbfb9715de393178edc84bd`
- Official Everything stdio JSON snapshot, `everything-stdio-fullauth.json`: `73e1e0fc23eedc4f0d1162d1fbfd33b150be3df2b4791112ddb7afcff04bd952`
- Versioned consolidated conformance JSON, `conformance-fullauth.json`: `73bc90fa9aa1b59d25f429ba1d9195f01552c7acf76793f25769578c02d17ade`

These files were generated locally on the VPS for this run. They are not published as signed release artifacts. Evidence JSON includes source commit, platform, checks and their stdout/stderr digests.

## Limitations and release stop conditions

- The Horizon Shield Federation B0/B2/B6/B7 rerun was requested but not yet independently confirmed at the time of this report.
- No verified end-to-end Claude/Codex/Cursor host installation; local Qwen action selection remains a separate failed reliability gate.
- Stdio process-tree containment, OS sandboxing and platform resource controls are incomplete; an allowed executable may itself execute untrusted code or spawn processes.
- No authenticated production OAuth acceptance matrix, full malformed-transport fuzzing, native Windows/macOS runtime checks, or signed downloadable releases.
- The edited GitHub Actions workflow was tested through its underlying suite on VPS; no hosted GitHub Actions run is claimed.
- A production-grade independent security review and manual licensing/terminology review remain open.

**Release decision: BLOCKED**, notwithstanding local PASS.
