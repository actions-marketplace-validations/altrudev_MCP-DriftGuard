package canonical

import "testing"

func TestHashOrderIndependentForTools(t *testing.T) {
	a := Snapshot{Format: "mcpdrift-snapshot/v1", Endpoint: "https://x/mcp", Tools: []Tool{{Name: "b"}, {Name: "a"}}}
	b := Snapshot{Format: "mcpdrift-snapshot/v1", Endpoint: "https://x/mcp", Tools: []Tool{{Name: "a"}, {Name: "b"}}}
	ha, _ := Hash(a)
	hb, _ := Hash(b)
	if ha != hb {
		t.Fatalf("hash differs: %s != %s", ha, hb)
	}
}

func TestObservedAtExcludedFromHash(t *testing.T) {
	a := Snapshot{Format: "mcpdrift-snapshot/v1", ObservedAt: "one", Endpoint: "https://x/mcp"}
	b := a
	b.ObservedAt = "two"
	ha, _ := Hash(a)
	hb, _ := Hash(b)
	if ha != hb {
		t.Fatal("observation time changed identity hash")
	}
}

func TestNormalizeNeverMutatesOriginalSnapshot(t *testing.T) {
 original:=Snapshot{
  ObservedAt:"2026-10-18T00:00:00Z",
  Tools:[]Tool{
   {Name:"z",InputSchema:[]byte(`{ "b": 1, "a": 2 }`)},
   {Name:"a",Annotations:[]byte(`{ "destructiveHint": false, "readOnlyHint": true }`)},
  },
  Resources:[]Resource{{Name:"z",URI:"https://z"},{Name:"a",URI:"https://a"}},
  Prompts:[]Prompt{{Name:"z"},{Name:"a"}},
 }
 schema:=string(original.Tools[0].InputSchema)
 annotation:=string(original.Tools[1].Annotations)
 normalized,err:=Normalize(original)
 if err!=nil {t.Fatal(err)}
 if normalized.Tools[0].Name!="a" {t.Fatal("normalization did not sort")}
 if original.Tools[0].Name!="z" || original.Tools[1].Name!="a" || string(original.Tools[0].InputSchema)!=schema || string(original.Tools[1].Annotations)!=annotation {
  t.Fatal("normalization mutated original tools")
 }
 if original.Resources[0].Name!="z" || original.Prompts[0].Name!="z" || original.ObservedAt=="" {t.Fatal("normalization mutated source snapshot")}
}
