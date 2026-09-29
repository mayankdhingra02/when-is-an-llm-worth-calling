# Status — 2026-09-25: V32 fresh physical reliability check completed

## Resume here

**New concrete result:** fresh timing changed Zstandard's mean cheap-versus-random gain from +0.4990% to −0.1032%; LZ4 stayed near +0.59%; zlib uses identical settings. The equal-family point estimate fell from +0.3637% to +0.1612%. These small historical differences should not be treated as stable benefit labels without measurement uncertainty. No significance, equivalence or LLM/router claim.

Read [V32 report](reports/reliability_v32.md), [frozen protocol](reports/protocol_v32_reliability.md), and relevant code. This was one bounded remeasurement of fixed V17 selections, not a larger grid, new software family or retuned optimizer. All systems remain exposed. Do not reread the full literature or rerun until a preferred sign appears.

## What actually ran

- All fifteen V17 cases retained: zstd/lz4/zlib × five fixed seeds. Their cheap, random and historical hindsight selections collapse to seven configuration IDs.
- Twenty shuffled rounds × seven settings = **140 new physical compression/decompression trials**, all successful. No warmups, retries, omissions or new optimizer/model decisions.
- Ten cheap/random cases use identical settings and share observations; the other five cases represent only three distinct configuration pairs. These are not fifteen independent timing comparisons.
- Original workload and executable/library hashes verified; every output round-tripped exactly and matched historical compressed size/hash. Size caps unchanged.
- **220 tests passed in 1.35 seconds** before freeze. Seventy-one input references frozen before physical collection.
- Independent selection/Decimal checks passed; all 140 retained compressed payloads decoded again and compared byte-for-byte with the workload. Thirty comparisons, 120 statistics and ninety round counts verified.
- Read-only replay passed; all **2,313 historical/current frozen references** passed integrity checks. Figure visually inspected. No job remains active or scheduled.

## Findings and limits

Fresh gains of cheap settings over random from ratios of medians: zstd −0.1032%, lz4 +0.5866%, zlib 0%. The paired-round 10th–90th percentile ranges cover both signs for all three distinct nonidentical setting pairs. These are descriptive ranges, not confidence intervals. The three LZ4 case wins share one configuration pair, not three independent confirmations.

The fixed historical hindsight reference's mean gain over cheap in zstd changed from +0.5373% to −0.4289%. This is a reference ranking change, not negative true headroom; the fresh full grid was not measured and no new oracle winner selected. A later session cannot identify whether noise, interference, temperature or other drift caused the change. Outlying timings remain in the data. Seven configurations produce six distinct outputs; identical bytes do not prove equal runtime.

V31's nine zero-shortlist-headroom cases remain a separate recorded-table finding. No new LLM behavior, successful learned routing, application-approved utility, new-family generalization or fresh optimizer result was tested in V32. One small archive and CLI/API boundaries limit deployment relevance.

## Commands and evidence

```sh
.venv/bin/python scripts/prepare_reliability_v32.py
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/collect_reliability_v32.py
.venv/bin/python scripts/analyze_reliability_v32.py
.venv/bin/python scripts/verify_reliability_v32.py
.venv/bin/python scripts/analyze_reliability_v32.py --verify-only
.venv/bin/python scripts/audit_history_v30.py
```

Collection refuses restart/overwrite. The independent verifier's first run charged computation; its --verify-only mode performs no recompression or new objective measurement.

- `results/v32_reliability/`: charged starts, raw trials, progress (140/140), seven-setting summaries, all fifteen cases, PNG/SVG figure.
- `artifacts/sources/live_v32/outputs/`: 140 real compressed payloads, Git ignored.
- `artifacts/study_v32/`: prepared schedule, tests, collection/analysis/independent verification logs, decode records, costs, historical integrity and final checks.
- `data/reliability_v32.json`: every old case/role mapping, deduplicated settings and source bindings.
- `reports/protocol_v32_reliability.freeze.json`: frozen inputs.
- `artifacts/history/v32_before_execution/`: previous STATUS/README and ledgers.
- V26 ZIP unchanged: historical V25 reconstruction, not a V32 package.

No experiment or verification failures occurred. No dependencies, downloads, models or system settings changed.

## Costs and next action

Collection 6.730717208 seconds; analysis/figure 0.544801625; independent decode/verification 0.733595375. Total added experimental computation **8.009114208 seconds**. Global ledger **2,276.095609129 / 3,600 seconds**, **1,323.904390871 remaining**, active_since null.

New physical trials140; historical physical total **1,274**. Recorded optimizer acquisitions remain **8,308**. These extra reliability repetitions are real research cost outside the old20-evaluation optimizer budget; deploying them would incur extra measurement cost. Independent re-decoding checks stored bytes, not another compression objective sample. Model allowance remains **200/200** follow-up requests (300 including original stage), exhausted. No new allowance inferred. Downloads unchanged; external spend USD0. No cloud, remote push, publication or contact.

**Single next action:** freeze a quality-constrained development task, practical minimum gain and measurement-repetition budget before collecting new LLM routing labels. Set that measurement rule using development evidence and reserve untouched families for evaluation. Retain strong classical comparators and uncertainty; do not continue remeasuring these cases toward a favorable sign. Fresh real inference needs a new bounded allowance or compatible provenance-checked cache.
