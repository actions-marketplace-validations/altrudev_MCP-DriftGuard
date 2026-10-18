# Full sweep — independent SDK integration, 2026-10-18

Verified runtime: `vps-377a113a`, Go 1.26.8, Node v24.21.0, temporary isolated directories only.

Verified code revision: `61e3e3ee7fbfa2db1b3ccc7224b7aab6127f45c3`.

## Scope and results

- Git checkout clean before repairs; Go test, vet and build passed.
- Existing Go fixture demonstrated baseline PASS, capability drift FAIL, error handling, and signed-baseline verification in prior recorded tests.
- Independent official TypeScript SDK `@modelcontextprotocol/sdk@1.32.1` stateless HTTP server: inspection succeeded, protocol negotiated as `2025-11-25`.
- Independent Python `mcp` SDK FastMCP stateless HTTP server: initially returned HTTP 400, JSON-RPC error code `-32600`, explicitly rejected protocol `2026-07-28` and advertised supported versions. Safe protocol fallback patched to recognize this bounded, explicit signal; subsequent CLI inspection passed (exit 0).
- Python server reported `independent-python-mcp`, version `1.30.0`, and negotiated `2025-11-25`.
- Regression tests cover both `-32000` (TypeScript) and `-32600` (Python) explicit version rejections, and forbid fallback on unrelated errors.
- At verified commit, `go test ./...`, `go vet ./...`, and CLI build all passed.

## Release blockers

- Real agent execution is unverified: Claude Code, Cursor, and Codex executables were not installed at the start of the sweep. Agent prompts, invocation safety and clean-install workflows must be tested rather than inferred from SKILL.md parsing.
- Wider protocol semantics, authentication, metadata redirection and adversarial input testing need dedicated acceptance evidence.
- No marketplace submission has occurred, and no paid feature set has been independently validated.
- Formal versioned release binaries and signatures/checksums are not yet published.

## Recommendation

Keep Go as the deterministic verification engine and package only minimal portable agent instructions/adapters. No Go rewrite needed. Mark **basic two-SDK discovery interoperability passed**, not full compatibility certification.
