# V78 pre-execution failure and accounting checks

The pending frozen V78 collection has not executed. Its original freeze digest
remains 59766c399b902a0e9f9eb5f785e2eb5350e383810e368de53467fce3a3bdd440;
all referenced files were hash-verified unchanged. No new inference allowance was
received during these checks. No new model calls, Kanzi trials, objective labels,
downloads or external spending occurred.

## What actually ran

Nine new worker fault-injection tests exercise the actual frozen Python worker
with fake process outputs under pytest temporary directories. They cover:
compression exit failure; missing checksum; truncated stream header; wrong job
receipt; ignored-option warning; decompressor failure; wrong decoded bytes;
server-resource abort propagation; and valid-result-only product deletion.
Failures remain failures and retain diagnostic products. These fixtures are
explicitly synthetic and are never written to the research collection directory.

Two existing subprocess-supervisor tests also ran: real short Python child
processes test completion timestamps, timeout killing and monitor-error killing.
These are infrastructure tests, not Kanzi objective measurements. The mock abort
propagation test itself does not prove real JVM/model-server shutdown behavior.

Source inspection found that the frozen main replay validates choices but does
not cross-check all saved fallback, resource and accounting fields. A separate,
additive read-only verifier now checks those requirements without modifying
collection/policy code or its frozen scope. Nineteen new synthetic accounting
checks cover malformed-case denominators; incorrect fallback counts; missing,
extra or duplicate requests; elapsed/server-memory caps; prompt/parameter/usage
provenance; unknown usage remaining unknown; per-phase memory/time/files caps;
and duplicate selection-cost events. These tests include deliberately tampered
records; rejection is not evidence that measured historical data were corrupted.

Combined new tests: 28 passed. Focused worker plus existing supervisor tests:
11 passed. Full repository suite: 580 passed (see saved log for elapsed time).
The proposed addendum has not been applied to genuine V78 outputs because none
exist. Its live-output replay remains untested. No outcome, practical margin,
model, candidate, seed, prompt or decision rule was changed.

## Evidence and execution after approval

- `tests/synthetic/test_kanzi_v78_worker_failures.py`
- `tests/synthetic/test_kanzi_v78_receipt_audit.py`
- `src/escalation/kanzi_receipt_audit_v78.py`
- `scripts/verify_kanzi_v78_addendum.py`
- `artifacts/study_v78_failure_checks/`: test logs, supplementary code pins and
  historical seal verification.

After the currently pending batch is explicitly approved and completes:
```
.venv/bin/python scripts/analyze_kanzi_v78.py
.venv/bin/python scripts/verify_kanzi_v78_addendum.py
```
The first verifier replays choices/budgets; the second audits provenance/cost and
failure counters. Run neither on fabricated production records. Partial genuine
runs must remain partial; the complete-run verifiers intentionally reject them.
The new verifier is pinned before any V78 outcome is acquired, while the original
scope/digest stays unchanged for the user's pending approval.

This turn strengthened a prepared measurement pipeline. It produced no new
research effect estimate and does not establish paper or Q2 readiness. The prior
V77 classical result and V72 negative LLM result remain unchanged. The next
substantive collection is still V78, within its requested35-call/150-trial cap.
