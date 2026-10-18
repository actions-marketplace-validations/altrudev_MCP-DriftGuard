# Installation and verification

**Release state:** pre-release source checkout. Cross-compiled platform binaries have been built in an internal temporary test environment, but are **not published as signed downloadable releases**. Do not download binaries from unverified mirrors.

## Requirements

- Git and Go **1.23 or newer** for building from source
- Network access to explicitly authorized MCP endpoints
- On Unix-like systems: an ordinary terminal and a secure location for reference baselines
- For agent-skill integration: an agent supporting portable Agent Skills and its documented skill discovery mechanism

## Build the CLI from source

```sh
git clone https://github.com/altrudev/MCP-DriftGuard.git
cd MCP-DriftGuard
go test ./...
go vet ./...
go build -o mcpdrift ./cmd/mcpdrift
./mcpdrift version
```

On Windows, use `go build -o mcpdrift.exe ./cmd/mcpdrift` and `.\\mcpdrift.exe version` in PowerShell.

**Important:** Until version stamping is added to the release workflow, `version` may report `dev`; record the checked-out Git commit for exact provenance.

## Safe isolated smoke test (no service subscription)

From the repository root:

```sh
python3 skills/mcp-driftguard/test_agent_skill.py
```

Requires Python 3.10+. The script builds temporary binaries, starts a disposable loopback MCP server, runs PASS, intentional FAIL and error-path checks, and returns `deterministic_pass: true` when its acceptance conditions hold. The script is **not a certification** or substitute for testing real external implementations.

## Verify an authorized endpoint

```sh
./mcpdrift inspect --format json https://example.org/mcp
./mcpdrift baseline --output candidate.baseline.json https://example.org/mcp
```

The candidate must be independently reviewed and approved before being used as the trust reference. Do **not** treat generation as approval.

```sh
./mcpdrift verify --baseline approved.baseline.json --format json https://example.org/mcp
```

For signed baselines, supply `--verify-key /trusted/key.pub.pem`, with the public key sourced through an independently trusted channel. Keep all private signing keys and authorization tokens outside the repository. If the endpoint requires a bearer token, supply it via `MCPDRIFT_BEARER_TOKEN` in a protected environment.

Exit codes: 0 PASS; 1 REVIEW; 2 FAIL; 3 incomplete/error; 4 baseline/key artifact error; 5 hash/signature verification failure. **Codes 3–5 are never PASS.**

## Install the portable agent skill

The CLI and the skill are separate components. Installing `SKILL.md` does not install or run the Go verifier.

Copy the `skills/mcp-driftguard` folder into the project or user skill directory supported by your *specific agent*, following that agent's current official documentation. Make the built `mcpdrift` binary available on `PATH`, or invoke it using an absolute trusted path. Confirm `mcpdrift version` works in the agent execution environment.

Do not claim Claude, Cursor or Codex acceptance until an authenticated, real-agent discovery and execution test is recorded. See [external testing guide](skills/mcp-driftguard/EXTERNAL-TESTER.md).

## Docker and GitHub Action

The repository includes a Dockerfile and `action.yml`. Both are source integrations requiring separate container/action acceptance before production use. They are not evidence of a published container image or official GitHub Marketplace listing.

## Licensing

The CLI, source and skill in this repository are Apache-2.0 licensed, subject to the repository [LICENSE](LICENSE) and [NOTICE](NOTICE). Do not bundle credentials or private keys. Optional future commercial services must state their **own** terms and must not retroactively revoke rights granted to published Apache-2.0 code.

See the [canonical glossary](GLOSSARY.md), [threat model](THREAT_MODEL.md) and [security policy](SECURITY.md).
