# External artifact audit: real measurements, insufficient configuration coverage

Three primary-owner repositories were inspected and pinned. **None supplies an admitted new optimization task for the current 20-evaluation protocol.** This bounded search does not establish that no suitable dataset exists. It does establish why the most promising retrieved benchmark cannot simply be added to the experiment.

## Published codec benchmark: 450 observations do not mean 450 configurations

The [owner artifact](https://github.com/nk2242696/compression-codec-benchmark/tree/f122312484734936bd4bd1aa33efb3fd3221d0dd) includes a [raw CSV](https://github.com/nk2242696/compression-codec-benchmark/blob/f122312484734936bd4bd1aa33efb3fd3221d0dd/docs/results/standard-2026-07/raw.csv), methodology, configuration and execution manifest. Its repository license is MIT; source corpora retain their own terms. Retrieved files stay in the ignored source archive, not a proposed redistributable dataset.

The executed metadata audit found:

| Quantity | Verified count |
|---|---:|
| Raw rows, including warmups | 540 |
| Measured rows | 450 |
| Warmup rows | 90 |
| Input datasets | 15 |
| Codec/input contexts | 90 |
| Codecs | 6 |
| Measured configurations per context | **1** |
| Repetitions per measured configuration | 5 |
| Contexts supporting 20 distinct evaluations | **0** |

Codecs are gzip, Snappy, LZ4, Zstandard, Brotli and XZ. Each uses a single published level, fixed chunk size and thread count. Varying the input file changes the workload; repeating the setting changes the observation, not the configuration. The unused level-sweep configuration is a plan, not measured evidence.

There is a second provenance limitation: the [published execution manifest](https://github.com/nk2242696/compression-codec-benchmark/blob/f122312484734936bd4bd1aa33efb3fd3221d0dd/docs/results/standard-2026-07/manifest.json) says `git_commit: unknown` and `git_dirty: null`. Pinning the downloaded artifact does not recover the historical executed code. Some codec versions identify bindings or only `stdlib`, leaving underlying implementation revisions incompletely specified.

The reviewed engine checks canonical decompression size/hash. During timed repetitions it checks compressed length and the decompressed canonical artifact's size/hash; it does not independently decompress the discarded output of each timed compression. All 540 published status fields are `ok`. These are published records and code evidence, not an independently rerun correctness result. No runtime/size/throughput values were converted, compared or aggregated in this audit.

## Other source dispositions

| Source and pinned revision | Inspected evidence | Disposition |
|---|---|---|
| [PDS-Throughput](https://github.com/nschorgh/PDS-Throughput/tree/8ddf05b5e6da2573cb1c26847b4a639c7fe95d06) | Complete 23-entry inventory, README, preparation/timing scripts, license | Repository exposes scripts and PDF reports, not a row-level runtime/size/repetition table adequate for this study. Selected codec options are sparse; examples also change thread counts. No scripts executed, no plot values transcribed |
| [lzbench](https://github.com/inikep/lzbench/tree/92546af00be8d04b1d96cbeec92f0dd6f5d56451) | Complete 4,300-entry inventory, README/manual, driver and two raw-looking files | Useful measurement-tool candidate, not an admitted task table. Bundled Zstandard regression CSV contains compressed-size checks without runtime. Density log contains benchmark summaries, not the required pinned configuration/repetition/runtime/size records |

PDS repository license: CC BY-NC 4.0. The lzbench harness license permits GPL version 2 or 3; bundled codecs have separate licenses. These are attribution facts, not a determination that all corpora or derivative datasets may be redistributed. No upstream code was installed, imported, compiled or run.

## Implemented safeguards and execution

Added a metadata-only importer/audit. It groups by fixed input digest, codec and codec version, counts configurations from setting fields, separates warmups, retains failures, detects duplicate measurement IDs and refuses incomplete metadata. Synthetic tests ensure workload/repetition counts cannot inflate coverage and outcome fields never enter the audit result.

```sh
.venv/bin/python scripts/audit_external_admission_v14.py
PYTHONPATH=src .venv/bin/python -m pytest -q
```

Both ran successfully. **108 tests pass**, including six new synthetic checks. `results/v14_external_admission/summary.json` retains every codec/input context and rejection reason through explicit coverage/provenance fields. `artifacts/study_v14/verification.json` verifies the counts and unchanged experiment ledger. File provenance is in `source_inventory.json`, `source_files.json` and `source_edge_files.json` in that directory; raw files are under `artifacts/sources/admission_v14/`. The main audit is bound by `reports/protocol_v14_external_admission.freeze.json`; later edge-file inspection is separately indexed, with no change to that freeze.

Initial sandbox DNS access failed; public-source retrieval then succeeded through the normal network-permission mechanism. Persistent download accounting includes every retrieved payload. No API credentials, paid inference, model request, optimizer acquisition or new benchmark run occurred. The raw CSV was read only to project configuration/provenance/status metadata; this is not a scored optimization dataset.

## Decision

Do not import these records as additional held-out optimizer runs, combine codecs into invented independent configurations, or replace unknown execution provenance with a download hash. Existing LLM/router conclusions remain unchanged.

**The next concrete route is a prospectively specified measurement campaign with enough configurations per genuinely new software family, rather than treating another general compression benchmark as a ready optimizer dataset.** The campaign must fix workload/correctness/size requirements, record true code/library revisions and repeated observations, and preserve untouched evaluation groups. lzbench is a candidate harness requiring further design validation, not a selected or executed solution. Its physical measurements and any subsequent LLM stage must fit explicitly bounded allowances: only 128.52 experiment seconds remain and model requests are exhausted at 128/128.

Searches used the current source leads plus: `site.github.com compression benchmark raw csv zstd lz4 configurations repetitions size time corpus`, `site.github.com software configuration compression dataset zstd parameters measurements`, and `site.zenodo.org compression configuration benchmark zstd data runtime size`. Broad search results were discovery aids; eligibility decisions above use pinned owner files only. No external contact or publication occurred.
