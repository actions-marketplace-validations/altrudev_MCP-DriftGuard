# Federation security acceptance sprint — 2026-10-18

## Scope and pinned evidence

Independent source: [Horizon Shield's B0–B7 findings](https://github.com/aeoess/agent-governance-vocabulary/issues/177#issuecomment-6252760895).

Locally verified source commit: `e4f8e954574aad9a236738b5fab6629e2b653f3d` (VPS `vps-377a113a`). This is **local development verification**, not independent closure.

## Repairs and regression tests

| Federation finding | Mitigation | Status |
| --- | --- | --- |
| B0/B2: semantically equivalent JSON produced false FAIL | Canonical-value JSON comparison insensitive to object key order/whitespace in schema and annotations | Unit regression passed; original reviewer fixture rerun pending |
| B6: signed to unsigned baseline replacement accepted with `--verify-key` | Explicit trusted public key requires a signed baseline | Unit regression passed; original fixture rerun pending |
| B7: bearer authorization header absent | Attach bearer on MCP modern/legacy POST; prohibit redirects to avoid forwarding token | Header regression passed; original fixture rerun pending |
| B3: optional additional property under `additionalProperties:false` was generic changed | Detect widening and preserve HIGH classification | Unit regression passed |
| B4: manipulative description change scored LOW | Recognize specified instruction-injection phrases for MEDIUM classification | Unit regression passed, broader semantic detection not proven |
| B5: readOnlyHint true→false and destructiveHint false→true REVIEW | Raise recognized authority expansion to HIGH / FAIL | Unit regression passed |

Tests do **not** establish that an arbitrary malicious description is reliably identified or that all JSON Schema transformations are correctly ordered.

## Verified commands and outcomes

On the pinned commit:

- `gofmt -l .`: no unformatted Go files.
- `go test -race ./...`: PASS.
- `go vet ./...`: PASS.
- `python3 scripts/check_docs.py`: structural PASS; human technical/legal review still required.
- `python3 skills/mcp-driftguard/test_agent_skill.py`: `deterministic_pass: true`.

## Outstanding blockers

1. Independent Horizon Shield reproduction of B0/B2/B6/B7 on repaired revision. Do not mark externally accepted before reviewer evidence.
2. Authentication over redirect and TLS edge cases, issuer metadata SSRF boundaries, log redaction and full OAuth matrix.
3. Complete schema and capability delta policy, beyond current heuristics.
4. Protocol conformance, pagination, malformed SSE/JSON, timing and fuzz testing.
5. Agent-host acceptance and reliable local-model decision performance.
6. Release packaging with reproducible cross-platform execution evidence.

No marketplace or production rollout approved.
