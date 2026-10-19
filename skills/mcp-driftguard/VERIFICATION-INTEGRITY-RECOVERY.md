# Verification Integrity recovery — Phase 0/1 register

**State: LOCAL_EVIDENCE_VALIDATED at code commit `c0106079e73cba64a9bd61e7e741f8495a2319ae`; hosted CI and production release NOT approved.**

## Known defects and contradictions

| ID | Evidence | Root-cause class | Corrective acceptance | State |
|---|---|---|---|---|
| VI-01 | Historical claims of full sweep with only VPS checks | Verification authority confusion | Exact-revision gate rejects stale, missing or failed suites | Local repair tested |
| VI-02 | Hosted GitHub Actions formatting failures | Clean-run mismatch | Require formatting and successful hosted workflow on candidate SHA | Hosted CI pending |
| VI-03 | Reviewer B0/B2 JSON representation false positives | Canonicalization gaps | Independent Horizon Shield rerun exit 0 | External bounded retest observed |
| VI-04 | Reviewer B6 signed-to-unsigned downgrade | Trust downgrade | Independent rerun exit 5 with verify key | External bounded retest observed |
| VI-05 | Reviewer B7 missing bearer support | Credential path | Independent authorized and unauthenticated loopback rerun | External bounded retest observed |
| VI-06 | Reviewer B4b alternate wording rated LOW | Keyword-dependent classifier | Regression at MEDIUM plus independently sourced paraphrases | Exact-case regression only |
| VI-07 | Stdio descendant inherited pipe hangs | Cancellation tied to IO | 20s deadline and same-group child terminated | Bounded local regression |
| VI-08 | Test runner generated untracked Python bytecode | Test-harness self-contamination | Checker remains clean after mutation probes | Fixed and locally checked |
| VI-09 | Project release checklist reused historical checkmarks | Evidence freshness gap | Machine-produced current candidate status; human gate remains | In progress |

External evidence: https://github.com/aeoess/agent-governance-vocabulary/issues/177#issuecomment-6256999139

## DDC Radial review of repair

- **Identity/provenance:** Source SHA and evidence SHA are checked for agreement; untracked files invalidate the local evidence gate.
- **Authority:** The local checker only emits `LOCAL_EVIDENCE_VALIDATED` and always sets `release_authorized=false`; this is not a hosted CI or independent reviewer.
- **Representation:** All seven required suites are checked explicitly. Missing or nonzero result cannot be treated as PASS.
- **Contradiction:** Failed hosted CI cannot be overridden by a VPS PASS. Actual hosted acceptance remains UNVERIFIED.
- **Fault injection:** The seven mutation test groups include removal of each required suite, nonzero exit for each, stale SHA and false aggregate.
- **Failure domain:** Test-side bytecode output was detected as a dirty checkout and removed by changing runner behavior, not by disabling the gate.
- **Replay:** Local evidence can be regenerated with `python3 scripts/conformance_suite.py --output evidence.json` and verified with `python3 scripts/release_integrity.py --evidence evidence.json`.
- **Reversibility:** Only additive checker, tests and CI gate changes; revertible by commits. No production services changed.

**Radial disposition: PROCEED WITH CONSTRAINTS.** Phase 0/1 local controls are verified. A passing GitHub-hosted workflow on the exact candidate SHA, fully independent mutation oracle, wider security tests and formal release approval remain mandatory. No Frequency was invoked.
