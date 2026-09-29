# STATUS — V99 interrupted; V97 remains latest complete comparison

V99 tried the user-requested repeat with context4096. One real request timed out at120s; zero responses,35/36 conditions unattempted. No retries. Lifecycle130.239s; peak modelRSS5,769,822,208bytes; cleanup exit-9. Missing token usage remains unknown. All36 intended fallback arms retained with360 charged table accesses; independent saved-evidence replay passed.

Evidence: `results/v99_reasoning/`, `results/v99_analysis/`, `artifacts/study_v99/`; assessment `reports/research_readiness_v99.md`. Protocol freeze SHA695bfa304f4a8fbd617acbba7f2262c8ba950976bf987c8b6ad3082cfe2fc710. Raw empty response journal was explicitly initialized after shutdown, never fabricated. Targeted V98/V99 tests:5passed; no full-suite rerun yet.

Cumulative model requests3,896; recorded-table accesses27,738; native numerical configurations790. Downloads9,870,221,104bytes /10GiB, modelpayload9,126,358,023bytes /9GiB unchanged. No new downloads/spending/cloud/publication. No owned inference process remains.

Next: freeze a small load-mode-none feasibility test before any further full batch. Source: saved local runtime help. Keep4096context/120sHTTP/8GiBRSS. No new objective labels needed. This is resource feasibility, not reasoning-quality evidence.

V97 remains latest completed comparison:250validnativeacquisitions,50validmodelcalls, mean LLMgain-1.52%vsbatch,-2.77%vssequential,+12.62%vsrandom,zero>=5% wins over either strong control. Exposed development system only; learned-router/generalization and Q2 readiness unsupported.

Saved-evidence replay (no inference/new labels):
```
.venv/bin/python scripts/verify_reasoning_v99.py
.venv/bin/python scripts/audit_usage_v99.py
.venv/bin/python scripts/seal_reasoning_v99.py --verify-only
```
Do not rerun once-only analyze/collect scripts into existing results. Prior checkpoint preserved in artifacts/study_v99/previous_snapshot/STATUS.md. Latest snapshot-aware sealer preserves earlier documents.
