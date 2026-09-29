# V92: Qwen3 responds to some losses but fails the stability screen

**Actual result:** all 108 conditions completed, 1,080 real requests, no invalid responses or retries. Neither representation passed the prospectively inherited loss-responsiveness and row-stability criteria. These are development diagnostics on three families and nine prefixes, not optimization gains or independent held-out trials.

Removing acquired losses changed four of nine symbol-format selections and three of nine numeric-format selections. Qwen3 is not wholly insensitive to losses. However, only one family per representation reached two changed seeds, below the two-family requirement. Reversing candidate order preserved only 68.9% of selected configurations for symbols and 33.3% for numeric values. Relabeling arbitrary IDs preserved 55.6% and 82.2%, respectively. Both stability conditions needed at least 80% overlap. Numeric relabeling alone passed that threshold; neither complete representation screen passed.

| Representation | Intervention | Qwen3 overlap | SmolLM3 overlap | Qwen3 changed sets / 9 |
|---|---|---:|---:|---:|
| symbols | loss_removal | 55.6% | 100.0% | 4 |
| symbols | reverse | 68.9% | 22.2% | 4 |
| symbols | relabel | 55.6% | 100.0% | 6 |
| values | loss_removal | 93.3% | 88.9% | 3 |
| values | reverse | 33.3% | 22.2% | 8 |
| values | relabel | 82.2% | 75.6% | 6 |

The table compares exact matched conditions from V48 and V92. Higher overlap after loss removal means less response to removing evidence; higher overlap after irrelevant presentation changes means greater stability. Neither measures choice quality. Different model families and context capacities prevent attributing differences solely to model size. These results qualify the V91 paired result, where Qwen3 remained below both primary classical controls; they do not replace it.

## Executed protocol and compatibility amendment

Reused all V48 messages and configuration mappings for MySQL, Brotli and lrzip, seeds 11/37/71: two representations × observed/withheld losses × base/reverse/relabel presentation. All related seeds remain development data. No objective table was opened by the diagnostic and no new labels were acquired. Inputs were frozen before generation; independent verification checked 108 prompts, 1,080 requests and 126 mapped contrasts. All nine symbol baselines equal the historical source messages.

The first 4,096-context attempt stopped in preflight with zero generations, exit 0, after 0.938369 seconds. The preserved context-only amendment used 8,192 tokens, unchanged prompts and limits otherwise; its lifecycle cap was reduced to 1,799 seconds to keep the combined ceiling under 1,800. Nine prompts would exceed the original context including selection reserve; maximum prompt length was 4,147 tokens. No prompt shortening or favorable subset was used. The original sandbox process-monitor failure also happened before inference and is preserved.

Same owner-pinned Qwen3-8B Q4_K_M weights and llama.cpp b11146 as V91. Non-thinking greedy decoding, one token under grammar per request, manually inserted newlines, single local slot. Full GPU offload was requested; actual device residency is not enumerated by the saved log. The larger context is a disclosed compatibility change from V48/V91, and the forced decoder remains a potential confound to check in V93.

## Actual collection cost

- Scientific lifecycle: 1330.322889 seconds; combined with the failed preflight: 1331.261258 seconds.
- Request wall-time sum: 1327.602263 seconds. Startup: 1.033650 seconds.
- Peak sampled server RSS: 8,166,637,568 bytes (7.606 GiB), below 8 GiB.
- 1,080 generated tokens; 2,740,380 summed full-context input tokens; 275,010 actual prefill tokens reported by the runtime. Context counts are not additional separately billed tokens.
- 1,322 HTTP calls in the successful stage plus 55 in the zero-generation attempt; no retry of a generation request. Both servers exited 0.
- Zero new objective acquisitions, downloads, paid spending or cloud access. Electricity and hardware cost remain unknown. These costs are diagnostic research collection, not modeled deployment savings.

Cumulative real requests: 3,574. Recorded acquisitions remain 26,658; native counts and download totals are unchanged. Both V92 generation allowances are now closed; V92b used all 1,080 shared requests.

## Reproduction and limitations

731 tests passed in 22.17 seconds after collection. This includes synthetic guard checks and prepared V93 code; no synthetic outputs enter research aggregates. Independent arithmetic replay passed. The scientific figure `results/v92b_analysis/sensitivity.png` was rendered and visually inspected; SVG and full tables are alongside it. Raw requests/responses, preflight seals, choices, runtime, model identity and all charges are under `results/v92b_sensitivity/`. Original failed-attempt logs remain under `results/v92_sensitivity/` and `artifacts/study_v92/`.

Run `.venv/bin/python scripts/replay_sensitivity_v92.py` for a saved-response check of both models. The portable `output/sensitivity_v92_reproduction.zip` provides the same standard-library replay without weights. This checks recorded evidence and arithmetic, not a fresh model or hardware replication. Full collection refuses existing output directories. Earlier evidence is preserved via exact snapshots and historical manifest resolution.

No quality outcomes, useful-escalation predictor, new independent systems, native clean-machine replication, stochastic-decoding robustness or Q2 readiness were established. Raw selected-set changes alone cannot show that the model understood losses beneficially. Next: execute the already specified V93 native-versus-forced diagnostic without selecting cases or tuning prompts, then decide the scope of the supported negative claim. The broader original routing hypothesis remains unestablished.
