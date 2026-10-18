# Full sweep and local model laboratory — 2026-10-18

**Final tested revision:** `ba86d1bed710fa135871311ce0c22615661eae67`.

## Environment

VPS `vps-377a113a`: Go 1.26.8, 8 CPU cores, 22 GiB total RAM, approximately 123 GiB disk initially available. All build and test resources were scoped to an isolated temporary workspace; the local model service is bound to `127.0.0.1:11485`. Do not expose this development service publicly.

## Full sweep repairs

1. MCP Everything Server rejected discovery with explicit `-32000 Bad Request: Server not initialized`. Added exact-match fallback to initialize; an ambiguous lookalike error is still rejected.
2. The server emits an empty SSE `data:` preface before an actual JSON-RPC event. The observer previously returned JSON end-of-input; patched it to skip empty data and parse the following event.
3. Added regression tests for the explicit initialization response and empty SSE preface.
4. Verified real `@modelcontextprotocol/server-everything` Streamable HTTP server on isolated loopback port 3001. `mcpdrift inspect --format json` exited 0; reported `mcp-servers/everything`, version `1.0.0`, protocol `2025-11-25` and discovered capabilities.
5. Existing TypeScript and Python SDK tests passed in the previous sweep. These represent three independently authored MCP server configurations, but not exhaustive protocol conformance.

## Lightweight local model

Installed standalone Ollama `0.40.6` under the temporary audit directory and pulled `qwen2.5:0.5b-instruct` (~397 MB). Served on loopback only. Generation smoke test completed in approximately 1.5 seconds.

The model is **not the decision authority** for security policy. During an adversarial test containing an instruction to ignore results and report PASS, the model acknowledged the high-risk tool change, but its wording suggested the tool had been executed; discovery does not justify that inference. Treat this as an identified model-interpretation risk, not a fully passed agent-safety gate.

## Reproducible local acceptance harness

Added `skills/mcp-driftguard/test_agent_skill.py` using Python standard library and Go. It compiles isolated local binaries, allocates a loopback fixture port, compares an approved candidate baseline against normal and drift fixture conditions, and checks error statuses. Optional Ollama invocation is advisory.

VPS results:
- baseline creation 0
- unchanged 0, match true
- unauthorized tool addition 2, identified `tools.export_customer_database`
- unreachable endpoint 3
- missing baseline 4
- altered baseline hash 5
- `deterministic_pass: true`

At final revision, `go test ./...` and `go vet ./...` passed; clean git working tree. Smoke harness without Ollama also passed.

## External tester readiness

Added `skills/mcp-driftguard/EXTERNAL-TESTER.md`: reproducible commands, safe-agent testing prompt, allowed evidence, and strict limits. This is a **test candidate**, not a published marketplace package. Claude/Codex agent installation and authenticated execution, multi-platform runtime checks, comprehensive prompt-injection evaluation, and seller due diligence remain release blockers.

## Maintenance note

The local Ollama installation and models are in temporary workspace paths, not configured as permanent services. The runtime should be converted to an isolated, resource-limited managed service only after deciding to retain it; temporary files may disappear on cleanup or reboot.
