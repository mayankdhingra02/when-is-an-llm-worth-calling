# Review evidence and safe verification

The pilot has not demonstrated useful LLM escalation or a useful benefit router. Start with the [discussion note](review_note.md). The small formatting result includes counterexamples; it is not an optimization-quality result. This entrypoint consolidates completed work without adding an experiment or changing a frozen analysis.

| Claim for discussion | Actual evidence | Interpretation limit |
|---|---|---|
| Development-fitted benefit and uncertainty policies escalate on 0 of 15 held-out cases; always escalation has higher mean loss | [V6 policies](../results/v6/policies.csv), [report](pilot_report_v6.md), [protocol](protocol_v6.md) | Three held-out families; seeds are repeated observations. No demonstrated nonzero-rate discrimination. |
| All nine V19 responses select the first displayed ten; reversed display changes all ten configurations, reversed IDs preserve all ten | [Raw requests](../results/v19_order_probe/requests.jsonl), [frozen inputs](../data/order_probe_v19.json), [response table](../results/v19_order_probe/response_table.csv) | Nine conditions over three exposed cases, ascending/descending IDs only. |
| Interleaving IDs breaks the universal first-ten account: MySQL follows display order; lrzip/Brotli return 0–9 | [Raw requests](../results/v21_nonmonotone/requests.jsonl), [frozen inputs](../data/nonmonotone_probe_v21.json), [response table](../results/v21_nonmonotone/response_table.csv), [figure](../results/v21_nonmonotone/interleaved_selection.png) | Three new responses; no fresh original repeats; no quality evaluation or unique internal mechanism established. |
| Compression tasks offer little recorded improvement even from their initial reference | [V18 decomposition](checkpoint_opportunity_v18.md), [case data](../results/v18_checkpoint_audit/cases.csv), [V17 physical collection](expanded_grid_v17.md) | Post-hoc recorded-table headroom, not a guarantee about true runtime or other workloads. |
| This is an adaptation, not numerical replication of SNAP2 | [Primary-source audit](source_audit.md), [attribution](../THIRD_PARTY.md), [model manifest](../artifacts/model_manifest.json) | Exact SNAP2 artifact not located in the bounded audit; changed classical implementation and model. |

From the repository root, these commands are safe at the exhausted inference cap:

```sh
PYTHONPATH=src .venv/bin/python -m pytest -q
.venv/bin/python scripts/verify_review_current.py
```

The first runs synthetic correctness tests, kept outside measured aggregates. The second uses only the Python standard library: it verifies every scientific freeze, all 79 entries of the V21 executed evidence index (resolving changed review documents to their exact archived bytes), the V6 policy table, and all twelve V19/V21 request denominators, raw ID-to-configuration mappings, recorded usage totals and approval timing. It checks current limits and local document links. It never imports a provider, queries an objective oracle, resets a ledger or invokes inference.

This is a consistency check. It does not independently reproduce model generation, tokenizer decoding, optimization, controller fitting, physical timing, or all earlier numerical analyses. The saved stage-specific replay checks remain available in the linked reports. A passing checksum does not establish scientific validity or clean-machine reproducibility.

The command prints a fresh JSON receipt; optionally use `--output path/to/new-receipt.json`. Existing receipts are never overwritten. Review-audit wall time is recorded separately from experimental collection/analysis time; the experiment ledger remains byte-identical. Tests and repository maintenance also remain outside the experiment ledger. No costs are interpreted as a deployment saving.

The historical `verify_review_packet.py` expects the old 128-call ledger. Preserve it as historical code; use the current verifier above. Older stage replay scripts can require their recorded ledger snapshots, tokenizer/model files or a runtime allowance. Do not reset live accounting to make them pass. Commands listed under historical preparation/execution headings in [REPRODUCE.md](../REPRODUCE.md) describe past runs, not a request to launch them again.

The single next action is to review this complete evidence with Tim and decide whether a larger, prospectively specified study is justified. The current approval is exhausted (140/140 follow-up attempts, 240 historical attempts including the initial stage; USD 0 external spend). Stronger models, untouched families, repeated conditions, selection-quality effects and live routing benefit remain untested. Nothing has been sent, published or queued.
