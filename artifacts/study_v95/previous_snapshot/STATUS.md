# STATUS — V94 fresh-family evaluation complete; reasoning check next

**Concrete result:** Qwen3's fixed non-thinking selection was worse than full-domain sequential 3NN in both fresh numerical engines: mean relative gain −10.21% SuperLU, −9.69% HiGHS; zero >=5% wins in ten pairs. Across V91/V94, all eight group means favor sequential 3NN (40 cases; six historical recorded groups plus two prospective native groups, not eight untouched groups). This is a scoped negative-result paper candidate, not Q2 readiness or a general claim about LLMs.

## What actually ran

- Frozen V94: two new native engine groups, five seeds each, B20/checkpoint10; 100 shared-prefix acquisitions and four continuations per case. **500 actual configuration acquisitions, 485 valid, 15 charged SuperLU worker crashes**. Physical execution journal: 1,474 starts, 1,459 returns, 26 planned repeats never started; 15 started solves did not return. All 1,455 vectors from successful workers were independently recertified. All 250 HiGHS acquisitions valid. All crashes occurred at panel size32 (posthoc association, cause not established).
- Qwen3-8B Q4_K_M, same pinned local model/runtime, reasoning off: **100 requests, 100 valid responses, no retries**, 100 generated tokens, 70,620 summed full-context tokens, 7,152 reported actual prefill tokens. Model lifecycle37.449s, peakRSS6,721,028,096bytes, exit0. Native lifecycle272.823s, below1,800s. Zero external spending.
- Secondary router precommit: added after prefixes/model choices but before ANY continuation outcome. Ridge/thresholds trained only on six older V91 development groups using group OOF predictions. Benefit and uncertainty both select never-call. No useful >=5% escalation missed in the new test, but no advantage over never/random/uncertainty and insufficient groups for broad routing inference.
- Default tests722 passed; explicit whole repository **749 tests passed in21.52s**. Prefix/model/native-budget replay and correctness audits passed. Figure PNG/SVG visually inspected. No experiment/model server remains running.

## Evidence and reproduction

Start `reports/research_readiness_v94.md`, `reports/numerical_v94.md`, `reports/router_numerical_v94.md`. Raw measurements/vectors/charges/crashes: `results/v94_native/`; real model traces: `results/v94_qwen/`. Summaries, policies, posthoc timing/noise audit and figures: `results/v94_analysis/`. Frozen protocol/source audit: `reports/protocol_v94.md`, `reports/protocol_v94.freeze.json`, `reports/source_audit_v94.md`. Secondary router protocol and decisions: `reports/protocol_v94_router_addendum.md`, `artifacts/study_v94/router_precommit.json`.

Reproduce saved-evidence checks: `.venv/bin/python scripts/analyze_numerical_v94.py`, then `scripts/evaluate_router_numerical_v94.py`, `scripts/cost_noise_numerical_v94.py`, `scripts/synthesize_numerical_v94.py`. Do not rerun exhausted collection outputs in place. Earlier root docs preserved in `artifacts/study_v94/previous_snapshot/`. Verify the V94 seal with `scripts/seal_numerical_v94.py --verify-only` after creation. Historical V93 diagnostics remain intact.

## Limits, open questions, next action

Cumulative real-model requests **3,818**. Recorded table acquisitions remain26,658. V94 adds500 native acquisitions: SuperLU250 and HiGHS250; earlier native counts unchanged (DuckDB78, H2299, Kanzi1265, RocksDB350). Downloads +2,451,935bytes: cumulative9,870,205,044 /10GiB, **867,213,196 remaining**. Model payload unchanged9,126,358,023 /9GiB, 537,318,393remaining. No paid/cloud/credential use, publication, push or contact.

Important unresolved limitation: pinned Qwen owner guidance recommends sampling and enabling thinking for reasoning; all current primary optimization evidence used a cheaper non-thinking forced-ID adaptation. **Next action: freeze a bounded reasoning-enabled/native-decoding comparison on existing DEVELOPMENT groups only**, using the same local weights and owner-informed sampling, before making broader model claims. Keep both new V94 groups out of further tuning. Full owner-recommended32K generation exceeds this laptop pilot's limits; any short thinking experiment must be labeled budget-constrained. Clean-machine/hardware replication and native crash diagnosis remain untested. Q2 acceptance/readiness cannot be guaranteed or reached by chasing a positive score.
