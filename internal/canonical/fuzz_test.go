package canonical

import (
 "bytes"
 "encoding/json"
 "testing"
)

// Fuzz normalization's determinism across arbitrary untrusted schema bytes.
// Invalid JSON must return an error rather than panic or produce a trusted hash.
func FuzzCanonicalJSON(f *testing.F) {
 for _, seed := range []string{
  `{"properties":{"b":2,"a":1},"type":"object"}`,
  `{"type":"object","properties":{"a":1,"b":2}}`,
  `{"items":[true,false,null,1.23456789]}`,
  `{"a":1,"a":2}`, `{"a":`, `[]`, `null`, `{"x":"\\u0000"}`,
 } { f.Add([]byte(seed)) }
 f.Fuzz(func(t *testing.T, raw []byte) {
  a,e:=normalizeJSON(json.RawMessage(raw))
  if e!=nil {return}
  b,e:=normalizeJSON(a)
  if e!=nil {t.Fatalf("second normalization failed: %v",e)}
  if !bytes.Equal(a,b) {t.Fatalf("non-idempotent canonical JSON")}
 })
}
