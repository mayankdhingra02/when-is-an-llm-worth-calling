# V124 implementation-to-owner mapping

Owner source: LLAMBO, revision196fe237f60a3d3a2fa53cbf8f474ec20a01dd57. Three captured owner files total19,537bytes; hashes in artifacts/sources/v124/manifest.json. License MIT, copyright2024Tennison Liu. Source fetched from owner URLs; no upstream imports/installers/provider access executed. This file records the already frozen adaptation, not a protocol change.

| Component | Owner artifact | V124 |
|---|---|---|
| Observed performance | Supplied acquired values formatted to6decimals | Same precision; raw prefix values, no global normalization |
| Example order | Template seed0permutes examples | Local RandomState0; no global RNG mutation |
| Serialization | Named hyperparameter sentences; demonstrated marked performance answers | Compact feature-order/setting arrays in JSON; observed scalar strings; requested marked numeric response |
| Context | Classification/regression HPO description | Software-configuration task and source-audited performance meaning |
| Model/backend | GPT-3.5-era provider interface | Existing local Qwen3-8B Q4_K_M/llama.cpp b11146 |
| Sampling | At least3completions, temperature0.7/top_p0.95 | Three explicit requests/seeds per candidate; same temperature/top_p; no grammar |
| Output limit |8tokens |32tokens; explicit local-tokenizer adaptation |
| Parsing | Extract marked decimal; missing predictions become NaN | Strict complete marked decimal with whitespace tolerance; invalid sample retained |
| Missing values | NaN-aware moments plus cross-candidate imputation | Require≥2valid samples for every candidate; no imputation; family fallback otherwise |
| Uncertainty | Population standard deviation, floor1e-5 | Same moments/floor, independently tested against SciPy EI formula |
| Acquisition | Expected improvement; one next configuration | Batch top10EI from fixed20shortlist; mean-only ablation from identical predictions |
| Sequential updates | Main optimization loop can update after acquisition | All predictions use the same prefix10; all10choices sealed before labels |
| Cost | Provider usage and historical price constants; retries | Precharged local requests/allocated tokens, raw usage/runtime;0retries and no paid calls |

Thus this measures a constrained local adaptation of a published surrogate component, not a faithful full-method replication. In particular, observed examples do not reproduce the owner's marked-answer few-shot text. The compact format can itself affect output validity. Neither a parsing failure nor an optimization failure here refutes the owner method. The EI-versus-mean comparison is paired within this representation; cross-version comparisons with V123 change several factors simultaneously.

During collection, some HIPAcc responses repeated the literal requested placeholder before their number. This is a post-start observation; it does not authorize editing the parser or prompt. Full raw outputs and strict failures remain recorded. Any future test of the owner's demonstration format must be separately frozen, with its own bounded cost, and labeled development work.
