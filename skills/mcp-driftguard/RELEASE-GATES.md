# Skill release gates — pre-publication checklist

**State: LOCAL ACCEPTANCE IN PROGRESS / NOT RELEASED.** Source-level tests and transport demonstrations have passed; production, clean agent-host integration and independent security closure have not. This checklist is a release gate, not a certification.

## Core gates

- [x] Record immutable Git commit and Go toolchain version (see FULL-SWEEP-2026-10-18.md)
- [x] Run `go test ./...` and `go vet ./...` against that commit (VPS, 61e3e3e)
- [x] Run `go build -o mcpdrift ./cmd/mcpdrift` (VPS, 61e3e3e)
- [x] Execute isolated HTTP and stdio unchanged PASS and intentional capability-drift FAIL; retain exit codes, source revision and test evidence (see CONFORMANCE-TRANSPORT-2026-10-18.md)
- [x] Exercise verifier exit codes 0–5 in local fixture and signature/tamper unit checks (see test_agent_skill.py; complete external artifact retest still open)
- [ ] Validate no credentials or token values persist in snapshots/reports
- [x] Test at least two independently implemented MCP endpoints with supported protocol behavior; retain reproducible evidence (TypeScript and Python SDK, basic discovery only; broader protocol matrix still pending)
- [ ] Confirm signed and unsigned baseline claims are distinguished clearly

## Transport and independent conformance gates

- [x] Run stdio discovery through an exact approved executable and complete argument vector, with no shell or inherited token; cover tool/resource/prompt inventory, 0/2/3 exit classifications, malformed JSON-RPC, ID mismatch and pagination cursor loops
- [x] Compare MCP Everything reference-server stdio inventory with previous HTTP inventory for the same unprivileged client capability context
- [x] Run versioned local conformance runner (Go unit/race/vet, docs, HTTP, stdio) on pinned source revision
- [ ] Demonstrate native stdio executable isolation under an independent OS sandbox and process-tree containment
- [ ] Obtain Horizon Shield's independent rerun confirmation for B0/B2/B6/B7 repaired inputs
- [ ] Complete malformed transport, authorization metadata and schema-classification fuzz suites beyond canonical JSON
- [ ] Verify hosted CI run and official release artifacts across Linux/macOS/Windows, with checksums and licensing

## Agent integration gates

- [ ] Parse skill metadata with target-agent compatibility checks
- [ ] Install in a clean Claude Code environment and execute approved read-only checks
- [ ] Install in a clean Cursor environment and execute approved read-only checks
- [ ] Install in a clean Codex environment and execute approved read-only checks
- [ ] Confirm injected MCP description cannot instruct the agent to execute tools, change endpoint, reveal credentials, or overwrite reference baseline
- [ ] Confirm failures are never reclassified as PASS, and REVIEW / FAIL do not trigger automatic approval
- [ ] Document support platform/architecture and safe binary installation mechanism

## Commercial / distribution gates

- [ ] Preserve full About, author, licence, third-party attribution, privacy and trademark boundaries
- [ ] Validate all names, ownership claims, third-party product descriptions and current marketplace policies
- [ ] Package no signing private keys, access tokens, customer evidence or proprietary service credentials
- [ ] Produce a truthful, reproducible demonstration and screenshots using only test fixtures
- [ ] Distinguish open-source skill from any paid product with actual added functionality
- [ ] Review Agensi seller terms, refund obligations, delivery model, payouts and corporate identity before listing
- [ ] Obtain human approval for each marketplace submission and paid listing

**Stop condition:** If any required gate fails or cannot be executed, report BLOCKED with evidence and do not label the artifact production-ready.
