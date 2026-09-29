# V131 native WavPack and FFTW extension

Two newly executed implementation families, five paired seeds each. Shared speech source is acknowledged; seeds/windows are not independent systems. Method/domain/validation protocol frozen before outcomes.

| Family | Evaluation | Mean model gain | Wins/ties/losses |
|---|---|---:|---:|
|wavpack|Selection vs sequential_3nn|+0.0058%|2/2/1|
|wavpack|Selection vs batch_3nn|+0.0240%|4/1/0|
|wavpack|Selection vs random_projection|+0.0202%|3/2/0|
|wavpack|Selection vs random_full|+0.0260%|3/2/0|
|wavpack|Selection vs expert|+0.0497%|5/0/0|
|wavpack|Selection vs default|+3.0098%|5/0/0|
|fftw|Selection vs sequential_3nn|-1.4095%|0/3/2|
|fftw|Selection vs batch_3nn|-1.6933%|0/3/2|
|fftw|Selection vs random_projection|-0.5923%|0/4/1|
|fftw|Selection vs random_full|+0.0000%|0/5/0|
|fftw|Selection vs expert|+8.7226%|5/0/0|
|fftw|Selection vs default|+3.1120%|3/2/0|
|fftw|**Fresh validation vs sequential (primary)**|-1.5160%|1/0/4|

| FFTW seed | Fresh sequential median ns | Fresh model median ns | Relative gain | Three block gains | Same configuration? |
|---:|---:|---:|---:|---|---|
|11|18246000|19172000|-5.0751%|-1.044%, -5.260%, -5.535%|False|
|23|18694000|18488000|+1.1020%|+0.556%, +0.527%, +2.092%|True|
|37|18666000|18733000|-0.3589%|-0.434%, +0.994%, -0.578%|True|
|53|18247000|18338000|-0.4987%|+0.351%, -0.300%, -1.607%|True|
|71|18622000|19134000|-2.7494%|-2.749%, -1.985%, -4.896%|False|

Fresh validation runs each frozen FFTW incumbent three more times in mixed order alongside the expert reference. Its45trials are charged separately and never fed into B20search. Different measured times for the same configuration are measurement variability, not a policy/configuration improvement. WavPack byte outcomes are deterministic checks; FFTW selection-time diagnostics should not replace the fresh primary comparison.

Actual collection: 648 configuration attempts, 909 WavPack encodes/909 decodes and 345 FFTW workers. Native stage time total 145.914s. Each numerical result checked against independent NumPy pocketfft reference; full sample equality for codec outputs. Raw results retain all correctness errors/timings/commands.

Model: 10 actual requests, 10 returns, 10/10 valid responses, 0 fallbacks, 0 retries; observable generated/prefill tokens 473/5050, missing-usage attempts 0. Allocated output tokens 10240. Lifecycle 44.723s, startup 3.053s, peak sampled server RSS 6025412608bytes; server exit0, resource stopNone.

Deployment estimate: one selected B20path plus one model call on escalation. Paired controls, three codec repeats,45timing-validation trials, build/startup/decoding and reference computation are actual collection overhead. FFT planning cost is reported separately and would require an explicit deployment amortization assumption. No dollar/energy guarantee.

Limitations: small finite domains, short correlated speech workloads, one host/model, sampled machine-load noise, approximate FFT planner time limit and possible pretraining familiarity. Only two family groups: no learned-router fit, group confidence interval, significance, journal-readiness or novelty claim. Keep prior adaptive stages and unlike task metrics separate.

Reproduce `.venv/bin/python scripts/analyze_native_v131.py`; raw native data `results/v131_native/`; real model provenance `results/v131_proposals/`; frozen protocol `reports/protocol_v131.md`.
