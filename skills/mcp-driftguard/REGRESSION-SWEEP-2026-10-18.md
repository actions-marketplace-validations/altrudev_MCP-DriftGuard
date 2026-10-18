# Free-resource + local agent regression sweep — 2026-10-18

## VPS environment and scope
Host: `vps-377a113a`. Tested source revision before this evidence commit: `d2d4cc458bd563606a6d65cb68fd8c6363710c35`. All MCP servers were isolated on loopback; no real customer endpoint was probed.

## Independent MCP compatibility
`mcpdrift inspect --format json` completed successfully (exit 0) against:
- Official TypeScript MCP SDK example: negotiated `2025-11-25`, enumerated 1 tool, 1 resource, 1 prompt.
- Python FastMCP fixture using the official Python MCP SDK: negotiated `2025-11-25`, enumerated 1 tool, 0 resources, 0 prompts.
- Official Everything reference server: enumerated 13 tools, 7 resources and 4 prompts.

These are **basic discovery and inventory enumeration** checks, not exhaustive compatibility/certification.

## Local-model continuity repair
The previously started temporary Ollama process did not survive session turnover. Confirmed its existing binaries and `qwen2.5:0.5b-instruct` model were present, then installed/enabled user-level `mcpdrift-test-ollama.service`.

- Loopback-only binding `127.0.0.1:11485`
- `Restart=on-failure`
- `MemoryMax=3G`, `CPUQuota=200%`
- `OLLAMA_NUM_PARALLEL=1` and `OLLAMA_MAX_LOADED_MODELS=1`
- Observed service `active` and API version `0.40.6` after activation

**Operational caveat:** runtime and model files remain under `/tmp/mcpdrift-vps.lKwZlC`, so this is not durable across temporary-directory cleanup. Do not represent it as a permanent production service or guarantee it survives every reboot.

## Repeated local-model decisions
Restricted-agent tests performed once after restoration plus three repeats:
- initial: model correct 4/5; executor enforced 5/5
- repeat 1: model correct 3/5; executor enforced 5/5
- repeat 2: model correct 3/5; executor enforced 5/5
- repeat 3: model correct 3/5; executor enforced 5/5

Every run retained an unchanged baseline. In the malicious requests the executor blocked unauthorized operations even when the small model did not produce the expected refusal. **Model-compliance gate remains failed**. This constrained executor is a test design with predefined caller capability grants; not a production-grade generalized permission system.

## CI improvement
Added `python3 skills/mcp-driftguard/test_agent_skill.py` to GitHub Actions CI. Reran locally on the VPS:
- documentation structural check: PASS
- self-contained PASS/FAIL/error-path harness: `deterministic_pass: true`
- `go test ./...`: PASS
- `go vet ./...`: PASS

**CI workflow was edited and locally exercised; an actual hosted GitHub Actions run was not checked in this sweep.**

## Remaining release blockers
Real authenticated Claude/Codex skill integration; adversarial prompt-injection matrix with systematic traces; production-grade caller authorization and isolation; clean installs on all target platforms; third-party commercial terms and publication approval. No claim of full security or certification.

## Follow-up: persistent local model storage and cloud isolation

After the sweep, migrated the existing Ollama executable tree and model cache from temporary paths to the persistent user-owned directory `/home/ubuntu/.local/share/mcpdrift-test/`, without changing unrelated services. Updated the enabled `mcpdrift-test-ollama.service` to use those paths, restarted it and verified `active (running)`, Ollama API version `0.40.6`, and presence of `qwen2.5:0.5b-instruct`. The service remains bound to `127.0.0.1:11485`, subject to `MemoryMax=3G` and `CPUQuota=200%`. Set `OLLAMA_NO_CLOUD=true` and verified the systemd environment value.

**Continuity limit:** auto-start configuration and persistence have been checked, but no VPS reboot or network disruption was performed; do not claim end-to-end recovery was tested.
