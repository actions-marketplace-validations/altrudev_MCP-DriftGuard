# MCP DriftGuard portable agent skill

This directory contains a reusable Agent Skills procedure. It is **not** a separate security engine and is not yet an approved marketplace release.

## About

The skill instructs compatible coding agents to run the standalone `mcpdrift` executable for authorized read-only MCP endpoint inspection and approved-baseline comparisons, and then interpret evidence without allowing an agent to approve detected drift.

Project: [MCP DriftGuard](../../README.md). Author and copyright: Valentyn Rukhaylo / Altru.dev, 2026.

## Local installation

1. Obtain the `mcpdrift` binary from a verified build of the source repository (Go 1.23+); do not trust unknown mirrored executables.
2. Confirm `mcpdrift version` executes on your host.
3. Copy this directory into the skill folder supported by your chosen agent, following that agent's current documented installation mechanism. No marketplace publication is implied by this directory.
4. Supply only endpoints you own or have explicit authorization to inspect; specify the approved baseline path and optional trusted verification public key.
5. Run a read-only comparison. The agent reports verdict, exit status, changes and limits; it must never silently overwrite baselines.

Example standalone check:

```sh
mcpdrift verify --baseline /trusted/approved.baseline.json --format json https://mcp.example.com/mcp
```

A verified official skill installation mechanism differs between Claude, Cursor and Codex; vendor-specific packaging should be generated and tested separately.

## Trust and distribution

- No private signing keys, token files, secrets, customer baselines, credentials or production endpoint lists are bundled.
- No hosted subscription, automatic enforcement, monitoring service or certification is provided by this skill.
- This skill follows the repository Apache-2.0 licence. Preserve copyright and third-party attributions when distributing derivatives.
- `SKILL.md` is agent-facing operational guidance. MCP server metadata and user-supplied endpoint content remain untrusted data.

## Canonical glossary

The authoritative mapping from product vocabulary to established technical terminology is maintained in [GLOSSARY.md](../../GLOSSARY.md). New concepts and terminology changes must update that file in the same change; do not duplicate or silently diverge from its definitions.

See [SPEC.md](../../SPEC.md) and [THREAT_MODEL.md](../../THREAT_MODEL.md) for precise claims and non-goals.
