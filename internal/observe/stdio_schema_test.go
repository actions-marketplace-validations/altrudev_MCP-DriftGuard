package observe

import (
	"encoding/json"
	"github.com/altrudev/MCP-DriftGuard/internal/canonical"
	"github.com/altrudev/MCP-DriftGuard/internal/diff"
	"testing"
)

func TestStdioToolWireSchemaPreserved(t *testing.T) {
	wire := []byte(`{"tools":[{"name":"list_profiles","inputSchema":{"type":"object","properties":{"dg_probe":{"type":"string"}}},"annotations":{"readOnlyHint":true}}]}`)
	tools, err := decodeStdioTools(wire)
	if err != nil {
		t.Fatal(err)
	}
	if len(tools) != 1 {
		t.Fatalf("tools=%d", len(tools))
	}
	var schema map[string]any
	if err := json.Unmarshal(tools[0].InputSchema, &schema); err != nil {
		t.Fatal(err)
	}
	properties, ok := schema["properties"].(map[string]any)
	if !ok || properties["dg_probe"] == nil {
		t.Fatalf("schema lost: %s", tools[0].InputSchema)
	}
	if len(tools[0].Annotations) == 0 {
		t.Fatal("annotations lost")
	}
}

func TestStdioToolSchemaMutationChangesCanonicalJSON(t *testing.T) {
	before, err := decodeStdioTools([]byte(`{"tools":[{"name":"list_profiles","inputSchema":{"type":"object","properties":{}}}]}`))
	if err != nil {
		t.Fatal(err)
	}
	after, err := decodeStdioTools([]byte(`{"tools":[{"name":"list_profiles","inputSchema":{"type":"object","properties":{"dg_probe":{"type":"string"}}}}]}`))
	if err != nil {
		t.Fatal(err)
	}
	a, _ := json.Marshal(canonical.Snapshot{Tools: before})
	b, _ := json.Marshal(canonical.Snapshot{Tools: after})
	if string(a) == string(b) {
		t.Fatal("schema mutation produced identical snapshot")
	}
}

func TestStdioSchemaMutationTriggersVerificationFailure(t *testing.T) {
	before, err := decodeStdioTools([]byte(`{"tools":[{"name":"list_profiles","inputSchema":{"type":"object","properties":{}}}]}`))
	if err != nil {
		t.Fatal(err)
	}
	after, err := decodeStdioTools([]byte(`{"tools":[{"name":"list_profiles","inputSchema":{"type":"object","properties":{"dg_probe":{"type":"string"}}}}]}`))
	if err != nil {
		t.Fatal(err)
	}
	result := diff.Compare(canonical.Snapshot{Tools: before}, canonical.Snapshot{Tools: after})
	if result.Match || len(result.Changes) == 0 {
		t.Fatalf("false PASS for schema mutation: %+v", result)
	}
	found := false
	for _, c := range result.Changes {
		if c.Path == "tools.list_profiles.input_schema" {
			found = true
		}
	}
	if !found {
		t.Fatalf("schema authority change missing: %+v", result.Changes)
	}
}
