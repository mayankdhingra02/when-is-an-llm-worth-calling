# STATUS — V97 complete; V98 stopped at request deadline

**Latest complete scientific result:** V97 ran250validnativeconfigurationacquisitions and50validlocalQwen3requests. LLM mean relative gain was−1.52% against batch3NN,−2.77% against sequential3NN and+12.62% against random; zero>=5% wins over either strong control in five paired seeds. This is an exploratory restricted-domain follow-up on an exposed SuperLU system. See `reports/numerical_v97.md` and `reports/research_readiness_v97.md`.

**V98 is incomplete, not a reasoning result.** The separately frozen final-answer-reserve procedure made2requests: one valid nonthinking response and one thinking request that timed out at120s. Its thinking final-answer phase never ran.34 of36intended conditions were unattempted. No retry, reconstructed output or shifted success criterion. See `reports/research_readiness_v98.md` before interpreting V98 summaries.

## What ran and what the evidence means

V97:50shared-prefix labels +200continuation labels; B20/checkpoint10, five fixed seeds, four arms.750physicalstarts/returns, all750savedsolutions independently certified. Every prefix/shortlist/selection/budget replayed. Native collection79.429s; model lifecycle17.143s, peakRSS6,152,175,616bytes, exit0.50generatedtokens,34,620summedcontext/3,507reportedactualprefill. No failures/retries/downloads. Frozen benefit/uncertainty policies and matched-rate random all choose never; no useful>=5% benefit missed. Hindsight oracle+0.41% is non-deployable and small compared with descriptive timing variation. Prior V94/V96 records remain unchanged.

V98: six previously exposed recorded-data groups,18oldprefixes, thinking/nonthinking (36conditions), shuffled before outcomes. Planned thinking512tokens plus separate128-token final answer; nonthinking128tokens. All responses would be real native-decoded Qwen3 output with strict ten-ID parsing. The second request timed out before its thought response returned. Only sac seed11 nonthinking completed; its quality tied both strong controls. sac seed71 thinking failed; all other conditions unattempted.

V98 actual lifecycle171.554s; peakRSS5,285,511,168bytes; serverexit0. The120sHTTPdeadline stopped collection, not the1800slifecycle or8GiBRSSguard. Allocated output640tokens; returned20output/3,306actualprefill tokens. Missing-response output/prefill totals UNKNOWN, not zero. Server log contains incomplete prompt-progress/cancellation but no final timing/output record. `usage_completeness.json` qualifies response-only empty sums in `phase_costs.json`.

All36 intended policy arms were accounted for with360additional charged recorded-table accesses, including explicitly classical fallback for failed/unattempted cases. These−2.58% policy means mostly describe fallback, not reasoning ability. Never aggregate them as36completedLLM trials or a new six-system reasoning result. Replay verified every saved cell/branch with zero new calls. Full tests766passed in28.07s. Both stages' figures were inspected; same-environment deterministic report rendering replayed byte-for-byte.

A read-only memory snapshot during V98 showed about95MiBfree and4.84GiBcompressor storage plus heavy wired memory. This and slow prefill suggest pressure but do not prove exact causality. No other applications were closed or settings changed. The user was asked asynchronously to close unused Chrome tabs/apps before more inference; no response has been received. All owned model/experiment processes have exited.

## Artifacts and reproduction

V97 raw: `results/v97_native/`, `results/v97_qwen/`; analysis/figures: `results/v97_analysis/`; protocol/code/data/model freeze: `reports/protocol_v97.freeze.json`. V97 seal SHA9c368dd80c6a0f19ee42d88a90ff6c553163a65de3cae8769c240291a1fce883 (1,590files,35historicalcheckpoints).

V98 raw requests/responses/controls/missing-case logs: `results/v98_reasoning/`. Acquired cells, complete intended denominator, coverage and usage: `results/v98_analysis/`. Frozen protocol/model/data/code: `reports/protocol_v98.freeze.json`. Execution, test, memory, replay and seal receipts: `artifacts/study_v98/`. The source audit verifies the existing budget-forcing method and documented native endpoint; no copied s1 code/model or newly downloaded payload.

Safe V98 saved-evidence replay:
```
.venv/bin/python scripts/verify_reasoning_v98.py
.venv/bin/python scripts/report_reasoning_v98.py
.venv/bin/python scripts/audit_interruption_v98.py
.venv/bin/python scripts/seal_reasoning_v98.py --verify-only
```
Do NOT rerun `analyze_reasoning_v98.py` into existing results: that is the once-only charged acquisition step. Do not implicitly resume completed/interrupted model batches. Latest snapshot-aware sealer preserves all historical root-document versions. V97's full checkpoint is saved at `artifacts/study_v98/previous_snapshot/STATUS.md`.

## Remaining limits and single next action

Cumulative real-model requests **3,895**; recorded-table accesses **27,378**. Native numerical acquisitions790 acrossV94/V96/V97, with physical solves counted separately. Older native counts unchanged (DuckDB78physical,H2299,Kanzi1265,RocksDB350). Downloads9,870,221,104bytes /10GiB;867,197,136remaining. Model payload9,126,358,023bytes /9GiB unchanged. No external spending, new credentials, cloud resources, publishing, pushing or author contact.

**Single immediate next action: free local RAM before another bounded inference attempt.** Preserve V98's failure. A smaller4096context is feasible by saved preflight arithmetic: maximumprompt3306 +512thinking +128final +16control =3962tokens. This is not an executed fix or guarantee; any new attempt must freeze its changed configuration and check the actual final prompt before generation. No silent timeout/cap increases or fabricated responses.

The original benefit-prediction hypothesis, final-answer-reserved reasoning quality, independent-machine replication and broader held-out-system evidence remain unestablished. No second host is connected. Do not claim Q2 readiness, treat fallback quality as LLM achievement, or start another unchanged memory-constrained batch without a reason to expect a different execution outcome.
