# Skill release gates — pre-publication checklist

**State: NOT VERIFIED / NOT RELEASED.** This checklist is normative for the marketplace packaging sprint, not an assertion that tests passed.

## Core gates

- [x] Record immutable Git commit and Go toolchain version (see FULL-SWEEP-2026-10-18.md)
- [x] Run `go test ./...` and `go vet ./...` against that commit (VPS, 61e3e3e)
- [x] Run `go build -o mcpdrift ./cmd/mcpdrift` (VPS, 61e3e3e)
- [ ] Execute clean PASS and intentional capability-drift FAIL fixture scenarios; capture stdout, stderr and exit statuses
- [ ] Verify exit codes 0–5, including corrupted baseline, wrong signature and probe failure
- [ ] Validate no credentials or token values persist in snapshots/reports
- [x] Test at least two independently implemented MCP endpoints with supported protocol behavior; retain reproducible evidence (TypeScript and Python SDK, basic discovery only; broader protocol matrix still pending)
- [ ] Confirm signed and unsigned baseline claims are distinguished clearly

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
