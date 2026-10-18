# Federation response and production-readiness triage — 2026-10-18

## Independent Federation testing

Source: https://github.com/aeoess/agent-governance-vocabulary/issues/177#issuecomment-6252760895

Horizon Shield (`ogasurfproject-jpg`) independently tested commit `df37061ab323740f3d826f697e5565f4814c35a6` on Darwin arm64 with its own stateless MCP fixture and retained SHA-256 artifacts. It reported:

- B0/B2: semantically equal JSON key reorder/whitespace caused false FAIL.
- B6: supplying `--verify-key` did not require signed baseline; an unsigned drifted baseline returned PASS.
- B7: `MCPDRIFT_BEARER_TOKEN` was not forwarded to authenticated MCP RPC requests.
- B3: optional schema property widened input scope but classifier reported generic `changed` (still FAIL).
- B4/B5: hostile instruction in description and capability annotation downgrades scored only REVIEW.

These independent results are **the external reviewer's observations**, not production approval.

## Repairs completed and locally tested

Following review, GitHub code changes added semantic comparison for JSON schema and annotations, rejection of unsigned baselines when a public verification key is provided, bearer token injection for legacy and modern MCP POST calls, redirect rejection, and regression tests.

The VPS verified `go test ./...`, `go vet ./...`, `python3 scripts/check_docs.py`, and clean `gofmt -l .` at source revision `0c508db41f484d8db004b17aeb8d5dea4e7a2b66`.

**External follow-up is not yet complete.** Horizon Shield must rerun original B0/B2/B6/B7 vectors and compare exact outcomes. B3/B4/B5 policy classification still needs design and tests. Protect against authorization leakage on redirects and reject incomplete metadata/inventory.

## New free-resource test

Installed `@modelcontextprotocol/inspector@2.11.0` in a temporary VPS test prefix. Inspector CLI independently listed **14** tools from the reference Everything Server. DriftGuard's earlier scan listed **13**. The difference was only `get-roots-list`, which Everything gates on advertised client `roots` capability. This is **capability-context-dependent inventory**, not yet a demonstrated parsing defect. A production verifier must record client capabilities alongside inventory and establish how comparable snapshots will be produced.

## Model comparison

Installed `qwen3:1.7b` alongside `qwen2.5:0.5b-instruct` on the existing loopback Ollama instance. On the current five-case restricted-agent harness, first Qwen3 run returned **2/5** expected model decisions and **3/5** completed allowlisted checks; two safe requests produced no valid action and were not executed. The old 0.5B model had scored **3–4/5** decisions across prior runs and completed 5/5 allowed-or-denied executor cases. This is a small non-equivalent prompting/token-budget comparison, **not** a reliable model ranking. No model may authorize its own tool permissions or baseline replacement. Benchmark again with structured tool calls, pinned prompts, seeds, token budgets, latency and repeated trials before selecting a default.

## Required gates before release

1. Independent regression rerun of Federation fixtures and fixes.
2. Comprehensive signed/unsigned downgrade and trust-key custody matrix, including signature-bearing artifact replacement.
3. Bearer credential and auth metadata transport tests including cross-origin redirects and logging redaction.
4. Semantic schema-change classifier and annotation/hostile-description severity policy.
5. Capability-context snapshot binding and Inspector cross-oracle tests.
6. Bounded pagination, malformed JSON/SSE, TLS rotation, errors/timeout, and fuzz/race tests.
7. Pinned Agent Skills validator and official clean-install tests across supported agent hosts.
8. Signed/checksummed versioned binaries, licensing/NOTICE packaging and clean-hardware install checks.
9. Separate model-compliance vs executor-enforcement reporting and adversarial prompt-injection suite.

**Status: RELEASE BLOCKED.**
