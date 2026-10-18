# Independent MCP SDK interoperability — VPS run, 2026-10-18

**System under test:** `altrudev/MCP-DriftGuard`, verified commit `fdeea470a92d23a252e0e9f37dcf2c94d0f924ff`.

**Host:** `vps-377a113a`, Linux x86_64, Go 1.26.8, Node.js v24.21.0. Executables and test server created in temporary directory `/tmp/mcpdrift-vps.lKwZlC`. No service configuration or production endpoint was changed.

**Independent implementation:** `@modelcontextprotocol/sdk@1.32.1` official TypeScript SDK, supplied stateless Streamable HTTP example at `127.0.0.1:3000/mcp`.

## Finding and repair

Before repair, `mcpdrift inspect` returned probe failure (exit 3) on the SDK's explicit HTTP 400 JSON-RPC response: unsupported `2026-07-28` version, supported through `2025-11-25`. The observer only recognized certain method-not-supported errors.

Repair: `internal/observe/modern.go` now permits legacy fallback on a **specific structured error** that explicitly identifies the rejected modern version and lists supported versions. Generic HTTP 400 and unrelated errors remain failures, not downgrade permissions.

After repair, actual CLI inspection of the independent SDK returned **exit 0**, identifying `stateless-streamable-http-server`, server version `1.0.0`, negotiated MCP protocol `2025-11-25`, and discovered advertised capabilities.

Added regression tests for the explicit unsupported-version response and generic error downgrade rejection. On commit above: `go test ./...`, `go vet ./...`, `go build -o ... ./cmd/mcpdrift` all passed.

## Limits

This is **one independent TypeScript implementation**, not two independent implementations. The Go test fixture is first-party. The test exercised discovery, negotiation and advertised inventories but does not establish full feature coverage, all authorization paths, or agent-host compatibility. Marketplace acceptance remains blocked on the other documented gates.

No secret credentials or production services were accessed.
