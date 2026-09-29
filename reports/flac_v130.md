# V130: native FLAC result

One newly executed implementation family, three fixed speech clips (26.655 seconds), five paired B10/B20 seeds. This is a descriptive pilot, not a held-out router study. Every prefix includes the strongest documented preset.

| Seed | Preset bytes | Sequential bytes | Model bytes | Model gain vs sequential |
|---:|---:|---:|---:|---:|
|11|455080|441983|442705|-0.1634%|
|23|455080|441983|445167|-0.7204%|
|37|455080|441740|441740|+0.0000%|
|53|455080|441740|441740|+0.0000%|
|71|455080|442705|442930|-0.0508%|

| Comparator | Mean model gain | Wins/ties/losses |
|---|---:|---:|
|sequential_3nn|-0.1869%|0/2/3|
|batch_3nn|-0.2090%|0/3/2|
|random_projection|+0.0479%|2/2/1|
|random_full|-0.1980%|0/3/2|
|preset|+2.6860%|5/0/0|

Model: 5 charged requests, 5 returned responses, 5/5 valid; 0 fallback cases. Observable usage: 211 generated and 2395 prefill tokens; 0 attempts lack complete usage. Allocated output capacity 5120; lifecycle 20.244s; startup 2.791s; sampled peak RSS 5943099392 bytes; resource stop None; server exit 0.
Projection: 2/50 proposals needed nonzero Hamming projection, 0 repeated a proposal and 1 matched acquired settings.

Actual native collection: 303 configuration attempts, 909 encoder and 909 external decoder calls, plus three corpus-preparation decodes. All completed encodings passed exact sample hash/length checks and internal encoder verification. Native collection lifecycle total 14.441s; encoder/decoder timings are raw costs, not latency-optimization evidence.
Separately charged post-selection preset repeats: [455080, 455080, 455080] bytes; excluded from arm budgets/selection. Actual trials comprise50 shared prefixes+250 continuations+3 repeats. Logical25 arms each useB20. No native trial was made free by overlap with another arm.

Estimated deployment:20 configuration trials and one model request when escalating, versus20 classical trials or one preset-only trial. Model loading, paired controls and reliability repeats are collection overhead. No dollar/energy savings estimated.

The 96 argument vectors can produce identical bytes; different maxima are not necessarily different effective codec decisions. Only acquired values are analyzed, without full-domain normalization or hidden-label headroom. The three clips are correlated speech workloads of one encoder, and seeds do not add independent systems. Same-implementation decoding is a correctness limitation. No second host, music workload, extra model, routing fit, statistical generalization, novelty or journal readiness is established.

Reproduce: `.venv/bin/python scripts/analyze_flac_v130.py`. Native trial records/encoded files: `results/v130_native/{classical,continuations}/`; model requests/raw outputs: `results/v130_proposals/`; frozen protocol: `reports/protocol_v130.md`.
