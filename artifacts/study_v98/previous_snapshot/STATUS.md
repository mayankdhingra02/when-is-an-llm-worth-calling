# STATUS — V97 paired follow-up complete; research goal remains open

**Concrete result:** In the separately frozen restricted-domain SuperLU experiment, all250 native configuration acquisitions and50 real local Qwen3 requests completed successfully. LLM mean relative gain was−1.52% against batch3NN,−2.77% against sequential3NN and+12.62% against random. Zero of five cases improved>=5% against either strong control. Read `reports/numerical_v97.md` and `reports/research_readiness_v97.md`. This is an exploratory follow-up on an exposed system, not a new independent test group or established Q2 readiness.

## What actually ran

- Seeds11,23,37,53,71; B20/checkpoint10;240 predefined configurations.50 fresh shared-prefix acquisitions and200 fresh continuation acquisitions. Four continuations per prefix: batch3NN, sequential3NN, random and real Qwen3. No V94/V96 timings or prior model choices substituted.
- All250 configuration acquisitions valid,0workerfailures;750physicalstarts/750returns. All750 saved solution vectors independently certified. The verifier reconstructed every prefix, shortlist, model token choice and branch under its budget.
- Real Qwen3-8B Q4_K_M, pinned owner weights/runtime, unchanged prompt/forced-ID procedure, reasoning off:50requests/50responses,50generatedtokens,34,620summedfullcontext/3,507reportedactualprefilltokens.0retries. Localmodel lifecycle17.143s, startup1.034s, peakRSS6,152,175,616bytes, exit0.
- Native collection79.429s across both phases, under600s. No inference overlapped solver timing. Peak sampled native worker RSS105,299,968bytes. No downloads, installations or paid/cloud calls; electricity/hardware cost unknown.
- Frozen transferred benefit/uncertainty thresholds both make0calls, so matched-rate random also makes0calls. No>=5%benefit missed. This degeneracy is not predictive success. The non-deployable hindsight oracle averages+0.41% over sequential3NN.
- Timing variation remains material: median within-acquisition relative range3.35%;69repeatedconfigs have median range2.04%. No confidence interval or equivalence claim from one system/five seeds. V94/V97 mean differences cannot isolate one changed parameter because domain, trajectories and timing changed.
- Full tests:763passed in35.99s. PNG/SVG visually checked; deterministic rendering wrapper fixes SVG identifiers/time metadata and is checked separately for byte-identical replay. Earlier source limitation and all V94/V95/V96 results remain preserved.

## Evidence and commands

Raw logs: `results/v97_native/` and `results/v97_qwen/`. Summary, costs, policies, usage and figures: `results/v97_analysis/`. Frozen scientific protocol/code/model/data hashes: `reports/protocol_v97.freeze.json`; report code was also pinned before model calls/continuation labels in `artifacts/study_v97/precontinuation_analysis_pin.json`. Dataset/version manifest, execution logs, tests and replay receipts: `artifacts/study_v97/`.

Safe saved-evidence replay, with no new native or model executions:
```
.venv/bin/python scripts/analyze_numerical_v97.py
.venv/bin/python scripts/cost_noise_numerical_v97.py
.venv/bin/python scripts/reproduce_report_v97.py
.venv/bin/python scripts/seal_numerical_v97.py --verify-only
```
Use the rendering wrapper for deterministic SVG metadata; calling the underlying report script alone may change timestamps/element IDs. The collection runner refuses completed output. Do not reopen exhausted V94/V95/V96/V97 batches. Latest seal resolves historical root documents using explicit snapshots; previous complete checkpoint is `artifacts/study_v97/previous_snapshot/STATUS.md`.

## Limits and next action

Cumulative real-model requests **3,893**. Recorded-table acquisitions **27,018** unchanged. Native numerical acquisitions: V94500 +V96diagnostic40 +V97paired250 =790; physical-solve counts remain separate. Older native counts unchanged (DuckDB78physical,H2299,Kanzi1265,RocksDB350). Downloads9,870,221,104bytes /10GiB,867,197,136remaining. Model payload9,126,358,023bytes /9GiB unchanged. External spendUSD0. No model or experiment process remains running, and no remote publication/contact occurred.

**Next locally actionable experiment:** separately freeze and test a development-only reasoning procedure with an explicit final-answer reserve. V95's completed bounded batch had no valid thinking answers, so that methodological question remains unresolved. Use real outputs, count all requests, verify runtime support against primary sources and preserve V95. No extra approvals are needed for ordinary implementation within current authorized local caps.

Independent-machine replication and additional independent systems remain outstanding; no second configured host is connected. The original benefit-aware predictor has not demonstrated useful discrimination. Do not claim a positive result, generalize to all LLMs or declare journal readiness from this run. Low-level diagnosis is not part of the next stage.
