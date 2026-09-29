# When Is an LLM Worth Calling?

A bounded research pilot on cost- and reliability-aware escalation in offline software-configuration optimization.

Start with **[STATUS.md](STATUS.md)**. The **[v7 development ablation](reports/pilot_report_v7.md)** completed all 15 real local-LLM continuations and 15 matched random controls. Prefix exclusion prevented copies but produced no material gain and one material harm versus each comparison baseline. The latest held-out routing evaluation remains the **[v6 pilot report](reports/pilot_report_v6.md)**. The latest version executes paired local-LLM and classical continuations on six additional software families, with five seeds per family, 10-label prefixes and 20-label logical budgets. Three development families fit the controller; three held-out families test the sealed policy. This remains an exploratory adaptation with insufficient evidence for broad generalization.

[Semantic admission](reports/admission_v6.md) narrowed the earlier [81-table registry audit](reports/registry_v5.md) to seven explicitly documented families. Six were selected by a frozen hash rule. Other candidate families remain unadmitted. The [v6 protocol](reports/protocol_v6.md) changes model proposals to one batch of ten and stays within the existing request/runtime caps. Raw data, real prompts/responses, token IDs, paired states, acquisition journals, fitted policies and figures live in `results/v6/`.

The earlier 20-group study remains unexecuted. Its proposed resource allowance has not been approved. Prior measured results and source freezes remain intact; do not pool different treatments or count variants/seeds as independent systems.

## Version history and evidence

| Version | Scope and disposition | Evidence |
|---|---|---|
| v1 | Classical pilot plus unconstrained local model; malformed responses and worker timeout; SQLite schema later found incorrect | results/classical, results/paired; reports/pilot_report.md |
| v2 | Constrained JSON format gate passed; interrupted when schema bug discovered; do not pool with v3 | results/v2; reports/protocol_v2.md |
| v3 | Explicit full schemas, corrected classical runs, real constrained binary proposals in batches of five | results/v3; reports/protocol_v3.md |
| v4 | Frozen larger-study design (admission blocked); measured model-free projection diagnostic on v3 prefixes | results/v4_projection_diagnostic; reports/protocol_v4.md |
| v5 | Expanded original-source registry, alias validation and finite-domain preparation; no new model calls/outcomes | data/registry_v5.json; reports/registry_v5.md |
| v6 | Six new family groups; real local single-batch continuations, paired controls, controller sealed before held-out acquisition | results/v6; reports/protocol_v6.md |
| v7 | Development-only prefix-exclusion mechanism; 15 real LLM pairs and 15 matched controls completed after explicit allowance | results/v7; reports/protocol_v7.md |

The [schema erratum](reports/schema_erratum.md) explains how a real SQLite option ending in `INDEX` was mistaken for an ignore marker. Earlier raw evidence is preserved; no old outcome is silently repaired. Synthetic feasibility fixtures are separate from software-quality aggregates.

- [Primary source audit](reports/source_audit.md), [decisions](reports/decisions.md), [attribution](THIRD_PARTY.md)
- [Corrected dataset manifest](data/manifest_v3.json), [pinned model files](artifacts/model_manifest.json)
- [Frozen v3 protocol](reports/protocol_v3.md), [limitations](reports/limitations.md)
- `results/v3/classical/`: corrected classical logs, source snapshot and ten-label prefixes
- `results/v3/requests.jsonl`: real prompts, raw bit strings, generated token IDs, grammar schedules, model identity, timestamps and token usage
- `results/v3/runs.jsonl`: paired labels, costs, projections, failures and final outcomes
- `results/v3/analysis/`: regenerated tables, policy choices and figures
- `tests/synthetic/`: synthetic logic tests only

## Reproduce analysis and verify evidence

Python 3.10.13 was used on Apple Silicon. For a fresh local environment:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.lock.txt
.venv/bin/python scripts/fetch_sources.py
```

Then, from this folder:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_v7.py
PYTHONPATH=src .venv/bin/python -m escalation.analyze_v7
.venv/bin/python scripts/diagnose_v7.py
.venv/bin/python scripts/report_v7.py
```

Token verification uses the pinned local tokenizer; if model/tokenizer files are absent, `scripts/fetch_model.py` retrieves official files under persistent download caps. Analysis and verification do not make model calls or acquire new objective labels. Historical v1 checks use the explicitly labeled legacy parser to reproduce what actually ran, not to endorse its schema.

## Collection entry points

For an explicitly authorized fresh experiment, the collection modules are:

```sh
PYTHONPATH=src .venv/bin/python -m escalation.study_v7 llm
```

They refuse to overwrite existing evidence. Do not delete outputs or reset ledgers to bypass caps. New collection after viewing results requires a new versioned plan, output namespace and authorized allowance. Exact executed source snapshots and their hashes are retained for both corrected classical and paired stages; current source may contain later bookkeeping/verification changes.

## Limits and interpretation

The original pilot allowed 100 attempts. The follow-up ledger initially allowed 100 attempts shared by v2/v3/v6; explicit v7 approval raised that cumulative cap to 113. All 113 are now used. Historical counts were never reset. The follow-up ledger carries v1 runtime so the cumulative 30-minute ceiling remains. Requests are serial; per-request timeout is 60 seconds in the follow-up. A dead worker stops collection before another reservation. No paid/remote inference client, credentials, remote code, cloud resource or publication.

Local inference reads official Qwen safetensors with HF offline flags and uses MPS when available, otherwise CPU. Cross-device generation/timing reproducibility is not guaranteed. The pinned SciPy 1.13.1 avoids the observed macOS 27 import failure. No third-party shell installer was executed. Source tables, papers, model weights and venv are Git ignored; URLs and checksums support retrieval.

The original corrected smoke used Apache and SQLite for development and x264 for testing. V6 uses three new development and three new held-out families; five seeds per family still give only three independent held-out groups. All variants/seeds stay grouped. Thresholds and preprocessing use development data only. Objective evaluations mean recorded-label acquisitions; no live Apache/SQLite/x264 software was benchmarked. Successful formatting does not establish useful optimization, and repeated seeds are not independent systems. See the current report before drawing conclusions.
