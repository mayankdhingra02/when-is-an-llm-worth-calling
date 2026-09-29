# V48 — development-only representation, loss and order diagnostic

Freeze before new inference. This is motivated by V47, not a preregistration
of an independent theory. Original development families only: MySQL/mysql_family,
Brotli/brotli, lrzip. Seeds 11,37,71 are the first/middle/last original five seeds,
chosen without inspecting which scores would favor an intervention. Nine saved
V6 ten-label prefixes and V8 twenty-candidate pools. Reuse saved V8 messages;
do not open target tables. No V41 transfer systems or unadmitted future groups.

Full factorial: two representations × loss presence/absence × three presentations
= twelve conditions per prefix, 108 continuations, 1,080 real one-token requests.

Representations: (1) original V8 symbol JSON; (2) a compact table with actual
numeric settings under their feature names, obtained by decoding the supplied
symbol_to_value mapping. Do not invent feature descriptions or parameter units.
Both contain the same observed/candidate configurations and original acquired-only
normalized losses where present. The table is a representation/prompt bundle,
not an isolated measure of one linguistic change. Numeric settings retain their
exact JSON numeric values; no hidden normalization or outcome-derived filtering.

Loss intervention removes all ten observed loss fields/entries, keeps observed
settings, and explicitly says losses are withheld. This does not erase model
pretraining knowledge, so changed/unchanged choices are not proof of reasoning
or its absence. No synthetic replacement losses and no novel target acquisitions.

Presentation intervention: baseline rows/IDs; reverse row display with each ID
attached to its original configuration; or rotate IDs by ten while keeping the
displayed configuration order fixed. The latter two disentangle position-following
from lowest-ID-following. Preserve and compare mapped configuration identities,
not just output strings. All conditions offer the identical twenty configurations.

Runtime/model/greedy decoding are fixed to V47: verified SmolLM3 Q4_K_M,
llama.cpp b11146, thinking off, one-token constrained choice excluding used IDs,
forced newline between choices, ten choices. Tokenize all prompts and single-ID
symbols before the first generation; all must fit 4096 including twenty-token
reserve. Case ordering is shuffled once with Random(48000), before outcomes.
No cross-case cache reuse on first choice; no retries. Retain malformed/timeouts
and intended denominator. Incomplete collection refuses complete-case aggregate.
No classical fallback needed: this study measures output sensitivity, not quality.

New bounded authorization from user's Continue: at most1,080 generation requests,
900 seconds live stage, no new downloads, paid spend or objective accesses.
Local server only, bounded timeouts, process cleanup in finally. Compile and
test collector AND analysis successfully before launch (fix V47 workflow error).
Persist version/hash manifest, raw request/response IDs, rendered prompt/token
records, usage, runtime, and error logs. Freeze analysis before generation.

Primary diagnostic quantities for EACH representation, preserving family groups:
1. Loss removal: set change and overlap/10, matched prefix/presentation.
2. Display reversal and ID rotation: mapped-row overlap/10 against baseline,
   separately for observed and withheld losses. Uniform independent ten-of-twenty
   has expected overlap0.5, as a mathematical reference only, not measured output.
3. Exact lowest-ten-ID set rate and displayed-first-ten selection fraction.
Report all108cases and counts for each family. Three families do not warrant a
generalization claim or confirmatory p-values; seeds are repeated cases.

Predeclared representation screening condition (necessary, not sufficient for
optimization): on the loss-present baseline, removing losses changes the selected
set in at least two of three seeds within at least two of three families; AND
mean mapped-row overlap with the loss-present baseline is >=0.8 for BOTH display
reversal and ID rotation, averaging first within each family. This checks some
responsiveness and stability, not beneficial use of losses. Passing motivates
a separate paired quality test on development groups; it does not validate a
router or authorize test-set tuning. Failure stops this diagnostic, without
trying alternate wording until a favorable result. All conditions reported.

No optimization gains, classical-comparison scores, hidden-target headroom,
learned-controller refit, or newly claimed held-out evidence in V48. Preserve
all prior V46/V47 and historical costs separately; forced newlines are not
generated tokens. Actual request costs include all factorial counterfactuals;
a proposed deployment would use only one condition, not twelve. Do not equate
these acquisition costs or fabricate paid-inference prices.
