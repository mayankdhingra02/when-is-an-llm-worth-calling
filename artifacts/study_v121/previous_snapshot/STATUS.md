# STATUS — V119–V120 real external-table experiment complete

Resume here, then `reports/paired_adapters_v120.md`, `reports/protocol_v120.md`, and the relevant code. Do not reread the initial discovery report, rerun create-once collectors, reinterpret V119's invalid answers, or refit a controller on these outcomes and call it held-out. Both bounded inference stages finished and all owned servers stopped. No future background work is promised.

## Latest concrete result

On the original owner WordCount table (one Storm software family), five fixed optimization seeds, B20/checkpoint10:

| Adapter | Valid continuations | Mean gain vs batch3NN | Mean gain vs sequential3NN | Joint ≥5% wins |
|---|---:|---:|---:|---:|
| V119 original free-output interface | 0/5; five classical fallbacks | 0% fallback-policy gain | -1.425% fallback-policy gain | 0/5 valid |
| V120 constrained greedy interface | 5/5; zero fallbacks | +8.070% | +7.597% | 2/5 |

V120 also gains8.081% against the single B20 classical portfolio and12.587% against random search. Its descriptive success criterion fixed before the follow-up is met. Seed71 loses to batch/sequential/portfolio and seed23 ties all controls; neither is excluded. This is a concrete positive local-model selection result on recorded labels, not evidence of generalizing benefit-aware routing. The original frozen benefit and uncertainty controllers escalated0/5, missing both joint5% opportunities. Matched-rate random at zero provides no meaningful discrimination test.

V119's five real answers returned five-character configuration strings rather than the required candidate IDs. The strict parser rejected every answer. Its quality numbers describe the predeclared classical fallback, not successful LLM choices. V120 was explicitly frozen AFTER seeing that format failure and reused the existing V91 grammar-constrained one-token/ID adapter. It is exploratory on an exposed table. Template handling and decoding also changed; this is not an isolated causal grammar comparison or a measured automatic repair policy. Preserve both adapters and their costs.

## Why work could continue despite the prior admission block

The earlier checkpoint mistakenly treated V52's stronger original-correctness/measurement requirements as blocking every recorded-table experiment. Existing V41 studies already disclose unverified equal utility, per-row correctness and noise. V119 explicitly restored that limited scope before acquiring WordCount targets: optimize the authors' published latency column, without claiming physical end-to-end timing, production correctness or successful native execution. V52's stronger gates remain closed and unchanged.

Source selection preceded outcomes: owner DOI10.5281/zenodo.56238, exact member `bo4co_dataset/wc-5d-c5.csv`,1,080 unique vectors/1,024 deterministic feature-hash subset, five resource/parallelism knobs, no explicit workload-size/emission-wait/co-tenant knob. BSD-3-Clause deposit metadata and original archive hash were already verified. Throughput remains unparsed. V116's bounded exposure scan found no prior Storm optimization outcomes; deleted/external history and pretraining contamination are unknown. All Storm variants/seeds remain one group.

The owner archive still lacks per-attempt output-validation/failure logs and an executed-code manifest. Later-harness metric-substitution and8/10-minute description differences remain unresolved. These limitations restrict the claim, not the existence of this clearly labeled table-only experiment.

## Actual execution and cost

This continuation acquired **350 recorded outcomes**:50 shared prefixes +200 four-control continuations +50 V119 fallbacks +50 V120 valid continuations. Every logical arm has20 outcomes, sharing exactly the same prefix10. These are recorded-table accesses, not fresh Storm executions. Integrity replays use only already acquired cells and make no new optimizer acquisitions.

**55 real local model requests**:5 V119 plus50 V120, zero retries. Pinned owner Qwen3-8B Q4_K_M and llama.cppb11146 were hash-verified. 350 generated tokens/690 allocated; 7884 reported prefill tokens; zero missing response usage in these stages. V119 sampling seed1009, temperature0.7; V120 greedy request seed11. Optimization seeds11,23,37,53,71 are distinct from generation seeds.

V119 lifecycle32.480s, peak sampled RSS5,921,718,272 bytes. V120 lifecycle20.194s, peak6,196,396,032 bytes. Both below frozen900s/8GiB caps; normal server exits, no resource stops. Caps5 and50 requests reached exactly; no implicit retries/resampling or silent stage-limit increase. Zero new downloads, cloud calls, installs or external spending. Agent/electricity costs unpriced.

Research collection includes both adapters and all four controls. Retrospective deployment components count one V119 or ten V120 requests per escalation, plus the shared prefix and selected branch. They exclude loading, controller/oracle overhead and unknown native application runtime; no dollar break-even or real end-to-end latency savings are claimed. Do not treat discarded/failed research branches as free.

## Evidence and verification

- Precollection protocols/configs/code hashes: `reports/protocol_v119.md`, `protocol_v119.freeze.json`, `protocol_v120.md`, `protocol_v120.freeze.json` (79 files for V120).
- Dataset/version manifest: `data/manifest_v119.json`; exact source member `data/raw_v119/wc-5d-c5.csv`.
- All prefixes,250 classical acquisition events and frozen policy masks: `results/v119_classical/`; model-input hash seal: `artifacts/study_v119/model_inputs.freeze.json`.
- Real prompts/templates/starts/responses/errors/runtime/tokenization: `results/v119_reasoning/`, `results/v120_qwen/`.
- Each50-event continuation journal, arm states, comparisons and figures: `results/v119_analysis/`, `results/v120_analysis/`.
- Combined result/cost and correctly labeled two-adapter figure: `results/v120_synthesis/`, `reports/paired_adapters_v120.md`.
- Full logs/replay/test/reproducibility receipts: `artifacts/study_v119/`, `artifacts/study_v120/`.

Actual collection commands (create-once; do not repeat against existing output):

```sh
.venv/bin/python scripts/run_table_classical_v119.py
.venv/bin/python scripts/collect_table_model_v119.py
.venv/bin/python scripts/evaluate_table_v119.py
.venv/bin/python scripts/collect_table_model_v120.py
.venv/bin/python scripts/evaluate_table_v120.py
```

Safe saved-evidence replay:

```sh
.venv/bin/python scripts/verify_table_model_v119.py
.venv/bin/python scripts/verify_table_model_v120.py
.venv/bin/python scripts/report_table_v119.py
.venv/bin/python scripts/report_table_v120.py
.venv/bin/python scripts/synthesize_table_v120.py
.venv/bin/python -m pytest tests -q
.venv/bin/python scripts/seal_tables_v120.py --verify-only
```

Final suite: **902 passed**,14 third-party deprecation warnings,30.18s. Synthetic fixtures cover objective poisoning, unused targets, charged failed acquisitions, missing usage and altered grammar/prompt/sampling/duplicate-response rejection; they are excluded from measured results. Source/request replay independently verified both arms, all five prefixes, controls and charged B20 labels. Reports/data/figures reproduced byte-identically; figures visually inspected. No inference/native job remains running.

## Interpretation and single most important next action

**Freeze this exact constrained adapter for replication on additional independently grouped software families, with development/test roles selected before opening new targets.** One positive family and a failed transferred controller cannot establish a useful generalizing router. All Storm variants are now exposed; additional Storm seeds/variants cannot become a new independent test group. Fit a model/interface/metric-matched controller only on development families and keep the future evaluation untouched. Do not select datasets, seeds or thresholds for positive gains.

The next source audit can work within this limited published-label scope; it need not first solve V52's stronger original-run validation problem. Confirm actual software-family/workload identity, feasible configuration schema, objective direction and license before using another owner's recorded table. Report unresolved original-run reliability. A separate causal adapter ablation and fresh native replication remain untested. This is material progress toward a paper, not a claim of Q2 readiness or acceptance.

V114–V117's older six-family findings remain:0/36 joint5% wins and0/36 portfolio5% wins; observed portfolio headroom0.568%; mean sign sensitive to OpenVPN. Do not pool the new exploratory adapter as a confirmatory seventh-family replication of the old interface. A universal no-benefit statement is now plainly inappropriate.

Native portability still needs the private `output/v113_replication/` second-host packet (90 charged acquisitions/270 solves). Only this Mac is available; do not bypass the source-host guard. V113 observed ≥5% apparent differences in5/8 identical-configuration contrasts; native timing claims remain noisy. NGINX V111 retains its failure stop, V112 remains unmeasured. No external contact, upload or spending is authorized.

## Cumulative accounting and integrity

Cumulative real model requests **4,029**; recorded-table acquisitions **28,808**. Numerical native880; NGINX81 charged attempts/35,853,130 byte-valid responses; DuckDB78,H2299,Kanzi1,265,RocksDB350 unchanged. Keep units distinct and historical missing usage unknown.

Downloads unchanged9,876,339,919/10GiB,861,078,321 bytes remaining; model payload9,126,358,023/9GiB. No new system changes, publishing, remote push, cloud provisioning, credentials access or author contact.

Combined V120 seal follows immutable V118 manifest SHA256 `0a87d2c43c7afff35d70642bb16201ad0629f185bfd36d67cc5386cb53d034aa`. Prior root documents are preserved under `artifacts/study_v119/previous_snapshot/`. Historical manifests and raw evidence remain unchanged. The current seal/receipt under `artifacts/study_v120/` binds source, both real batches, implementation, tests, results and this checkpoint;47 historical checkpoints remain verifiable.
