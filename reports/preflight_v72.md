# V72 implementation and execution readiness

The paired local-model experiment is implemented and frozen, but **not run**.
No new model requests or research measurements were made during this preparation.
All 516 tests passed in 2.66 seconds, including 11 new synthetic policy/guard tests.
The suite's three tiny native fixture cases remain separate from research data.
The previous V71 evidence seal verified all 4,144 files; read-only replay again
verified all 203 V70/V71 trials and every V71 decision and charge.

The runner reuses all five saved ten-evaluation prefixes, isolates branch inputs,
and compares fresh RF-LCB, feature-only domain prior, and real local SmolLM3 arms.
Seven search plus three confirmations fit each inclusive20 budget. Finite-vector
grammar excludes duplicates; independent parsing rejects malformed/truncated
responses. Such failures use explicitly counted RF fallbacks. Transport/resource
failure stops collection while preserving unattempted cases. Full raw provenance,
physical receipts, decision time and separate generation/HTTP counts are saved.

`reports/protocol_v72.freeze.json` SHA256:
`34044827e05860507cab9706ddca0755ea58e50e8b9abc56d966373765eb58b4`.
It pins 105 files, including runtime/model binaries and inputs. Descriptive analysis
and replay scripts have their own pre-collection freeze. An invalid authorization
token was actually tested: rejected before creating a collection directory.

The requested new envelope is at most35 local generation requests,64 tokens each
(2240 maximum),150 physical DB evaluations,1800 seconds, no retries, downloads or
external spending. V65's exhausted five-call allowance is not silently renewed.
Approval of this concrete scope was requested in the task; no answer was available
at preparation time. This is an allowance blocker, not missing model access.

Remaining empirical unknowns: native grammar compilation/sampling, real model
proposal validity and usefulness, end-to-end resource behavior under joint model
residency, paired gains versus RF AND the cheap prior, and all generalization and
router claims. Unit tests and a frozen protocol cannot establish those results.

The wider journal-quality goal remains incomplete. If approved, execute once and
report all five intended seeds regardless of outcome. Do not retune a failed model
or task after inspection merely to create a positive finding.
