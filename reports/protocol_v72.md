# V72: exploratory constrained local LLM on RocksDB

Prepared after inspecting V71. This is a new prospective development experiment,
not a held-out test, SNAP2 replication, or claim of 400 effective configurations.
One system family and five repeated seeds cannot establish router generalization.
The model and prompt are fixed for this run; no tuning to obtain positive outcomes.

## Question and controls

From ALL V71 ten-evaluation prefixes (11,23,37,53,71), compare newly measured
RF-LCB, a cheap feature-only domain prior, and real local SmolLM3-3B Q4_K_M.
All arms get seven search evaluations, then three fresh confirmations of the
incumbent selected from their seventeen observations. Confirmations cannot alter
selection. Total20 per arm. Fifteen arms yield150 NEW physical acquisitions and
300 logical evaluations, including50 historical shared-prefix physical calls.
No new prefix calls, caching of new branch measurements, or uncharged probes.

RF is the unchanged V71 policy. The prior visits unobserved settings ordered by
cache capacity descending, block size ascending, restart interval ascending, then
ID. This deliberate cheap domain heuristic was chosen after V71 exposure; it is
exploratory, has no fitted thresholds, and its ordering never consults outcomes.
The prior retains the best observed incumbent just as other arms do.

The LLM sees only its own acquired vectors/timings, declared option levels and the
fixed workload description. Each native completion is constrained by finite GBNF
to a complete unused vector; no projection. Independent exact-byte validation
fails closed. Context is4096, output at most64 tokens/request, greedy sampling,
seed equal to prefix seed, repeat penalty1, prompt cache disabled, thinking off.
Seven sequential requests per prefix, maximum35 overall/2240 output tokens.
No preliminary generation probes, retries or additional model variants.
Native apply-template/tokenize/health requests are counted separately from model
generation. Every rendered prompt/token ID, grammar, payload, raw response and
available usage is saved. Missing usage remains unknown. Runtime seed requested,
not a promise of cross-device reproducibility. Real grammar compilation remains
untested before this run; the first charged request tests it.

Malformed, excluded or truncated completion: retain raw output, mark failure,
switch that arm to RF for its current and all remaining search steps, and count
every fallback. No further LLM requests for that prefix. Transport/server/grammar
engine error, context overflow or physical failure stops the whole collection;
preserve all attempted and unattempted denominators without retries. Do not
silently analyze completed seeds as the full intended study. Confirmations of
fallback-derived incumbents are not evidence of LLM-attributable benefit.

## Timing, provenance and resources

Same pinned V70/V71 measurement worker, trace, data, runtime and archive semantics.
The model stays resident for all new arms. At each search or confirmation round,
shuffle arm order using independent Random(seed+72000). No inference overlaps a
DB measurement. Record all decision costs, physical collection wall time and
server start time. Sequential inference can still cause thermal/OS/cache effects;
residency/order control does not eliminate this limitation. Prefixes were measured
without the model; this is historical-prefix reuse, not a fully fresh end-to-end
deployment evaluation. Fresh confirmations reduce selection-time noise; three
samples do not establish robust latency tails or production reliability.

Maximum stage1800 seconds (reserve before new requests/trials),120s/request or
physical trial, one server/request/worker, sampled server RSS8GiB and worker2GiB.
Owned server process group is terminated on completion/failure and by watchdog.
HTTP permits only hard-coded127.0.0.1 routes, bypasses proxies, no credentials.
Existing model/runtime hashes are frozen. Zero downloads, paid API/cloud spend,
remote publication, or system-wide changes. Prior V65 allowance is exhausted;
execute only following approval of this exact new35-call envelope. No inference
is implied by preparing this protocol. External resource controls still apply.

## Analysis fixed before collection

Primary descriptive result: each seed's median of its three incumbent confirmation
times; report all values and mean of the five seed medians. Paired improvement is
100*(control_ms-LLM_ms)/control_ms, against RF AND domain prior. Show selected
IDs/configurations, same-setting comparisons, provenance of selected incumbents
(prefix/LLM/fallback), and within-incumbent sample CV. Same-setting differences
are timing variation, not different optimization decisions. No significance test
over five seeds as independent systems. Use predeclared5% practical gain/harm flags
only as descriptive diagnostics, never as a validated decision threshold.

Report the hindsight best branch only as nondeployable; do not train/tune a router
on these five cases. Always-escalate versus never-escalate is measured here; all
broader policy/generalization claims remain untested. Retain negative results.
Separate new150 physical calls from historical50 prefix calls and planned300
logical per-arm charges. For incomplete collection report actual charges, never
claim planned budgets were consumed. Deployment estimates include only a chosen
branch, its decision overhead, confirmations, and explicit startup amortization;
no cost/latency generalization to real servers or API dollars.

## Commands

```
.venv/bin/python -m pytest -q tests
.venv/bin/python scripts/run_rocksdb_v72.py --approved-envelope-sha256 <approved-freeze-digest>
```

Review configs/study_v72.json and reports/protocol_v72.freeze.json before execution.
The one-shot output directory cannot be overwritten or resumed implicitly.
