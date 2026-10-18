# Agent and binary packaging smoke test — 2026-10-18

VPS temporary workspace: `/tmp/mcpdrift-vps.lKwZlC` (not published or hosted).

- Installed `@openai/codex@0.163.0` to a scoped temporary npm prefix; `codex --version` returned `codex-cli 0.163.0`.
- `codex login status` reported **Not logged in**. Therefore no authenticated agent invocation, skill discovery or prompt-injection acceptance test has passed. Do not mark agent integration as complete.
- `claude` and `cursor` were not installed during the sweep.
- Cross-compiled Go CLI using `CGO_ENABLED=0`, `-trimpath` and `-ldflags='-s -w'` to Linux amd64, Linux arm64, macOS arm64 and Windows amd64 temporary binaries.
- Created `SHA256SUMS` for the four binaries; `sha256sum -c SHA256SUMS` returned OK for all four.
- These are build/byte-integrity smoke checks, **not** executable platform acceptance tests or signed official releases. Only Linux amd64 executable behavior was previously verified on VPS.
- Do not publish marketplace claims of platform compatibility until each target is tested, distribution provenance/signing is defined, and clean installation is proven.
