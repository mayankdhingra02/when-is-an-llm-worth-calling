# V133 lossless JPEG: strong cheap controls and frozen-router transfer

Three real photographs, one software family, five seeds. Every arm shares B10 and has B20. Correctness requires identical complete RGB pixels. Public photo familiarity, one family, a 70-vector domain and same-library decoder limit generalization.

| Comparator | Mean model gain | Wins/ties/losses |
|---|---:|---:|
|sequential_3nn|-0.0455%|0/3/2|
|batch_3nn|-0.0115%|0/4/1|
|random_projection|+0.0000%|0/5/0|
|random_full|-0.0115%|0/4/1|
|predictor_sweep|+0.0000%|0/5/0|
|reference|+0.0567%|3/2/0|
|default_anchor|+4.5716%|5/0/0|
|prefix_best|+0.0000%|0/5/0|

Incremental attribution: the model improved 0/5 prefixes; sequential search improved 2/5. A gain against the left-predictor anchor is not automatically a gain caused by escalation. The saved B10 outcomes identify how much was already achieved before the call.

The predictor-sweep arm uses documented domain knowledge and charges every acquisition. The predictor-7 reference is not advertised as an expert optimum; the left-predictor anchor is not the ordinary lossy JPEG default. Primary comparison remains sequential 3NN, with predictor sweep a mandatory strong control.

| Seed | Prefix bytes | Sequential bytes | Predictor sweep bytes | Model bytes | Paired model gain |
|---:|---:|---:|---:|---:|---:|
|11|1298214|1298214|1298214|1298214|+0.0000%|
|23|1297466|1297466|1297466|1297466|+0.0000%|
|37|1298942|1297466|1298942|1298942|-0.1138%|
|53|1298942|1297466|1298942|1298942|-0.1138%|
|71|1297466|1297466|1297466|1297466|+0.0000%|

| Policy | Modeled calls | Mean gain vs never | Missed >1% | Harmful >1% |
|---|---:|---:|---:|---:|
|never|0/5|+0.0000%|0|0|
|always|5/5|-0.0455%|0|0|
|benefit|0/5|+0.0000%|0|0|
|uncertainty|0/5|+0.0000%|0|0|
|random_development_rate|0/5|+0.0000%|0|0|
|random_matched_realized_rate|0/5|+0.0000%|0|0|
|hindsight_oracle_diagnostic|0/5|+0.0000%|0|0|

Benefit/uncertainty parameters are unchanged from V132 historical training (40 pairs/eight groups); each decision was saved before its classical continuation and before all new model calls. Random development rate is fixed from that calibration. Matched-realized-rate random is a batch diagnostic; hindsight is non-deployable. These now-exposed outcomes may not tune the frozen controller. Zero-rate policies matching never do not demonstrate selective routing advantage.

Actual collection: 353 native configurations, 1059 encodes and 1059 decodes; native wall time 23.252 s. All alternatives and three reference repeats are charged. Thirty logical B20 arms share fifty physical prefix trials. Model calls 5, retries 0, valid 5/5, fallbacks 0; tokens generated/prefill 215/2730, missing usage 0. Allocated output tokens 5120. Model lifecycle 21.772 s, startup 2.837 s, peak sampled RSS 5989859328 bytes, server exit 0.

Feature/prediction time total 0.002431 s; historical original fit time remains unknown. A deployment uses one B20 arm and a model call only if selected, plus decision overhead and explicit model-loading assumptions. This counterfactual cannot erase actual research collection cost. No cloud-dollar/energy savings inferred.

Images are full-resolution scikit-image v0.20.0 astronaut/coffee/rocket photographs with owner-verified hashes and documented public-domain/CC0 attribution. Rocket starts as JPEG; its decoded pixels are the fixed input. This is native software-configuration research, not a new codec, a test of broad medical-image suitability, or exact SNAP2 replication. No significance from repeated seeds; no journal-acceptance guarantee.

Reproduce: `.venv/bin/python scripts/analyze_jpeg_v133.py`; verify: `.venv/bin/python scripts/verify_jpeg_v133.py`. Protocol/source audit and raw logs are preserved.
