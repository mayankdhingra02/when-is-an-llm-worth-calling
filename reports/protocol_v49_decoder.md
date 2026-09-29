# V49 — frozen native decoder diagnostic on development prefixes

Motivated by V48's display-order dependence. This is an exploratory mechanism
study, not a new held-out test, optimization-quality result or router refit.
Freeze scripts, config, saved inputs and analysis before generation.

Reuse EXACT V48 symbol messages, mappings and acquired losses for nine prefixes:
MySQL, Brotli, lrzip; seeds 11, 37, 71. All are original development families.
Two loss modes (observed/withheld), three presentations (base/reverse/relabel),
54 native cases. Only symbol representation: these prompts fit the unchanged
4096 context with 128 output tokens, while some value prompts do not. This
choice uses prompt lengths, not unseen V49 output. No new target-table access.

Native arm uses one /completion call, at most 128 generated tokens, with no
grammar and no externally forced delimiter. The complete assistant continuation
is generated autoregressively. Messages, chat template, thinking off, greedy
sampling, seed, repeat penalty, weights, runtime and context stay as in V48.
Thinking remains off: this is not a reasoning-enabled model test. Do not append
format hints or repair outputs. Strict parser accepts only ten distinct IDs
from 0..9,A..J, one per nonempty line, with whitespace stripped. Empty lines
are ignored. Explanations, bullets, commas, missing/duplicate/unknown IDs fail.
A truncated response fails even if parseable. Preserve all failures, no retry
or fallback. Failure is a reliability result, not a loss of a data point.

Repeat the nine observed/base forced-ID cases using the EXACT V48 ten-request
protocol as a temporal control. Jointly shuffle the 63 cases with Random(49000).
Cache is off for the first request of every case; within-case reuse only for
forced controls. Before inference, require each rendered prompt and token list
to equal its V48 preflight and to fit its output reserve. Model and runtime hashes
must agree. The repeats check reproducibility on one machine, not cross-device
nondeterminism. Comparisons to all 54 historical V48 forced cases are descriptive;
only nine forced cases are concurrently repeated. Decoder mode includes grammar,
forced delimiters and request chunking; these components are not isolated.

New bound: 144 generation requests maximum (54 native + 90 forced), 900 seconds
for live stage including startup/preflight/cleanup, 30 seconds per request,
zero downloads/objective acquisitions/external spending, no retries. Maximum
new predicted tokens 7002 (54*128+90); runtime-observed counts are reported.
A transport failure or resource limit terminates the stage; remaining intended
cases are recorded missing by analysis. Local loopback only; finally stop server.
No indefinite background process or automatic second collection.

Primary analysis, using mapped configuration sets:
- All 54 native intended cases: valid/invalid/missing/truncated, parse reason,
  duplicate rate, generated tokens, input tokens and latency, by family/condition.
- All 63 within-native sensitivity pairs: 27 loss-removal pairs, 36 base-vs-order
  pairs. Invalid/missing endpoints stay in denominator; overlap is unknown with
  [0,1] bounds. Report valid-only means explicitly as conditional. Pairing a
  failure with success is not evidence of meaningful label responsiveness.
- Native versus historical forced overlap for all 54 matched cases, and nine
  concurrently repeated forced controls versus their original choices.
- Order-following rates for valid outputs, with valid/intended denominators.

Screen fixed before output: >=95% valid native responses; baseline loss removal
changes valid selections in at least two seeds within each of two families;
and lower-bound family-mean overlap >=0.8 for BOTH observed-loss display reversal
and ID rotation. Missing overlap contributes zero to the stability lower bound.
Also require all nine forced repeats to reproduce original mapped sets before
attributing a change to the intervention rather than temporal variability.
Report each criterion even if another fails. Three families are the independent
units; no confirmatory p-values. This is necessary, not sufficient for quality.

If screen passes, a SEPARATE frozen development quality comparison against
strong classical controls is the next step, not an automatic positive claim.
If it fails, stop decoder/prompt tuning on these cases and consolidate this
bounded negative result and its unresolved novelty. Do not keep enabling new
prompt/decoding settings until one passes. No new held-out group is exposed.

Actual research cost includes both modes and all counterfactual conditions.
A native deployment uses one request; forced uses ten, but token use and quality
may differ. No claimed quality-preserving savings or paid-price estimates.
