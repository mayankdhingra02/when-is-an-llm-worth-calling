# V134: where did the apparent improvement occur?

**Retrospective audit, not a new held-out evaluation.** Sixty intended normal-condition cases from twelve families in V127/V129/V130/V131/V133. Older methods and label-rotation probes remain preserved outside this method-defined scope. No new model/native calls.

| Family | Stage | Intended / fallback | Improves B10 prefix | Beats sequential | Beats sequential >1% | Mean paired gain |
|---|---:|---:|---:|---:|---:|---:|
|berkeleydb|127|5 / 0|0|0|0|-1.0387%|
|dune_hsmgp|127|5 / 0|1|0|0|-21.0320%|
|fftw|131|5 / 0|0|1|1|-1.5160%|
|flac|130|5 / 0|2|0|0|-0.1869%|
|hipacc|127|5 / 0|2|1|1|-0.9430%|
|libjpeg|133|5 / 0|0|0|0|-0.0455%|
|llvm|127|5 / 0|1|0|0|-2.5738%|
|mongodb|129|5 / 0|0|0|0|-2.3992%|
|openvpn|127|5 / 0|2|0|0|-3.7863%|
|sac|127|5 / 5|2|0|0|-0.1351%|
|storm|129|5 / 0|1|0|0|-12.7661%|
|wavpack|131|5 / 0|4|2|0|+0.0058%|

Counts are repeated-run descriptions, not independent-system success estimates. Never infer population confidence from sixty seeds. No overall mean across these unlike metrics/contracts is reported.

- all_intended: 60 cases; 15 improve their prefix, 4 beat continued sequential search, 2 exceed 1% paired gain.
- valid_model_only: 55 cases; 13 improve their prefix, 4 beat continued sequential search, 2 exceed 1% paired gain.

FFTW prefix attribution uses original selection times; paired efficacy uses independently remeasured medians. Its one >1% raw win uses identical selected settings and is measurement variability, not a better model choice. Do not erase that raw primary value or combine it with deterministic byte gains without this qualification.

SAC has five fallback cases from the old impossible 512-token representation. Retaining their executed outcomes does not mean five successful LLM proposals. Valid-only counts are a supplementary view, not a replacement denominator. Other historical tasks differ in output capacity, initialization, native versus recorded metrics and prior exposure.

Only WavPack/FFTW/libjpeg have the new frozen V132-controller decisions; the other nine groups include historical development and a failed-contract group. Those three new groups still cannot establish broad generalization. Mean gains in a group may be positive while benefits remain practically tiny. No refit, statistical significance, journal quartile or novelty claim follows from this table.

V133 illustrates attribution directly: +4.5716% relative to a weak left-predictor anchor, zero improvement over its B10 prefixes, and −0.0455% versus continued search. The measurable improvement against that anchor predates escalation. This is a bounded example of why the counterfactual matters, not evidence that all earlier papers made this error.

Reproduce with `.venv/bin/python scripts/attribution_v134.py`; input hashes and exact rational case rows are saved. The preregistration status is explicitly retrospective, including selection of this synthesis after these outcomes were available.
