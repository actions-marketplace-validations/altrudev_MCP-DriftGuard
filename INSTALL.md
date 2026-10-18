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

## Experimental local MCP stdio transport

DriftGuard can inspect a local MCP server over stdin/stdout with the same snapshot and baseline verifier as HTTP. This transport is **pre-release**. It does not execute discovered MCP tools, but starting a local executable itself is a privileged action.

**Only launch an executable you have inspected and approved.** The verifier requires an exact, absolute executable allowlist via `MCPDRIFT_STDIO_ALLOWED_EXEC`, plus an independently authorized argument vector via `MCPDRIFT_STDIO_ALLOWED_ARGS_JSON` if nonempty; it never passes commands to a shell. Process arguments must come from a trusted operator, never from an LLM or MCP server metadata. The subprocess receives a minimal environment (no inherited bearer token), and its discovery session has a deadline.

For the disposable Python fixture (Linux/macOS example):

```sh
chmod u+x examples/stdio-fixture/server.py
FIXTURE="$(pwd)/examples/stdio-fixture/server.py"
export MCPDRIFT_STDIO_ALLOWED_EXEC="$FIXTURE"

./mcpdrift inspect --stdio-exec "$FIXTURE" --format json stdio
./mcpdrift baseline --stdio-exec "$FIXTURE" --output stdio.candidate.json stdio
./mcpdrift verify --stdio-exec "$FIXTURE" --baseline stdio.candidate.json stdio
```

For trusted executable arguments, independently approve the exact ordered arguments before invoking the CLI:\n\n```sh\nexport MCPDRIFT_STDIO_ALLOWED_ARGS_JSON='["--safe-option"]'\n./mcpdrift inspect --stdio-exec "$FIXTURE" --stdio-args-json '["--safe-option"]' stdio\n```\n\n**Both the executable path and every argument must match the trusted allowlist.** If no argument authorization is configured, only the empty argument vector is accepted. Never approve a generic interpreter with attacker-controlled script paths or flags. The endpoint argument must be exactly `stdio`; the full executable path and argument vector are committed into the snapshot's endpoint identity. This does not authenticate executable contents; pin a binary digest and review changes in the operator's deployment process.

Reproducible local test, without external services:

```sh
python3 skills/mcp-driftguard/test_stdio_transport.py
```

**Remaining limitations:** no production-grade OS sandbox or child-process-tree isolation, resource controls are incomplete, Windows stdio execution has not been independently exercised, and the model cannot grant executable permissions. Do not use stdio mode on untrusted executables.
