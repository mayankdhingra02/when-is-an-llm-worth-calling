# STATUS — V38 executed and verified

Updated 2026-09-25. Resume from [V38 report](reports/size_prompt_v38.md), [frozen protocol](reports/protocol_v38_size_prompt.md), and relevant code. Pre-execution docs/receipts are preserved in `artifacts/history/v38_before_execution/`; preparation receipts remain historical.

**Concrete result:** 30/30 real local Qwen2.5-1.5B calls and 300 new recorded-vector acquisitions completed. The prespecified assigned-ID size-aware model improved feasible runtime **1.7534% versus exact joint3NN shortlist** (2 wins, 7 ties, 1 harm) and **2.0444% versus matched historical runtime-only LLM** (3 wins, 7 ties, no harm). Against runtime3NN across all 30 cases: **0 wins, 24 ties, 6 harms**. This is a limited positive prompt result, not evidence that paid inference or learned routing is useful.

## Executed and verified

Two exposed families (Brotli/lrzip), five seeds, three frozen presentations, ten-prefix/ten-continuation budget. Model owner digests and revision fixed; real CPU float32/greedy/grammar-constrained responses. No retry, timeout, malformed response, duplicate, projection or fallback. All 30 intended cases retained. All 150 comparisons reported. Selected sets changed in 13/30 cases; infeasible acquired vectors rose from 75 to 84 of 300.

Commands actually completed:
```
.venv/bin/python scripts/run_size_prompt_v38.py --preflight
.venv/bin/python scripts/run_size_prompt_v38.py
.venv/bin/python scripts/analyze_size_prompt_v38.py
.venv/bin/python scripts/analyze_size_prompt_v38.py --verify-only
.venv/bin/python -I -S scripts/verify_size_prompt_v38.py
.venv/bin/python -m pytest -q
.venv/bin/python scripts/audit_history_v30.py
```

258 tests passed in 1.99s. Independent Fraction checker agrees on 30 source-bound arms, 150 gains and 15 summaries. Token/provenance/budget replay passes. 3,586 frozen historical references pass. Figure rendered and inspected. Runtime warnings about unused sampling defaults are preserved in collection stderr; greedy frozen parameters were unchanged. No execution failure. Independent OS process listing was sandbox-unavailable; run exited0, provider cleanup executed and ledger is inactive.

## Evidence

- Results/raw responses/acquisition journal/CSV/figure: `results/v38_size_prompt/`.
- Actual report: `reports/size_prompt_v38.md`.
- Actual collection/analysis/test/verification logs and receipts: `artifacts/study_v38/`, including `executed_final_checks.json` (distinct from historical preparation-only `final_checks.json`).
- Exact approved extension and verbatim proceed instruction: `configs/authorization_v38.json`, bound to the frozen protocol. The direct reply to the preceding 30-call proposal was interpreted as approval and the bounds were restated before execution; no broader permission inferred.
- Frozen prompts: `data/size_prompt_v38.json`; independent verifier: `scripts/verify_size_prompt_v38.py`.

## Costs and remaining limits

New: 30 calls, 300 recorded-vector accesses, 55,302 input/600 output tokens; 229.090471 request seconds, 8.277166 startup seconds. Collection241.110346s plus analysis3.196673s =244.307020s. Logical evaluations600 across30branches include reused prefixes, not600new accesses. Historical collection remains counted; deployment estimates are separate in the report.

Cumulative runtime **2530.796723/3,600s**, remaining **1069.203277s**. Follow-up calls **230/230 exhausted** (330 including initial stage). Recorded accesses **9,608**; physical trials **1,274** unchanged. No new downloads, physical trials, spending, cloud, publication, push or external contact. No continuing task has been scheduled.

## What remains untested and next action

No new held-out families, credible learned-router advantage, physical validation of these selected rows, contemporaneously randomized prompt effect, application-approved size cap, or isolated-machine V38 replay. Two exposed families cannot support generalization. The V35.1 archive still reproduces V34 only.

**Single next action: review V38's complete comparison with Tim before proposing more collection.** Any extension should first establish an application-defined task and untouched families with opportunity beyond strong cheap controls; do not tune these exposed results until positive. No additional model call is authorized beyond230. All work needed for this concrete result is complete.
