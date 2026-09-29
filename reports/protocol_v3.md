# Frozen corrected exploratory protocol v3 — 2026-09-24

This is a corrected follow-up within the user-authorized 100-additional-attempt allowance announced for continuation. No new allowance is added. At freeze, v2 consumed 33 attempts and cumulative recorded runtime was 831.99 seconds; at most 67 attempts and 968 seconds remain before the 100-attempt / cumulative 1,800-second caps. USD 0 spending, no downloads, one local model process. v1 and v2 evidence remain unchanged except explicit errata/disposition records.

## Why v2 stopped

An audit identified a schema defect: the loader's generic trailing-X ignore rule removed SQLite's real sQLITE_OMIT_AUTOMATIC_INDEX configuration option. The original code actually used 38 features and 4,132 unique projected configurations, despite reports describing 39 features and 4,652 configurations. v2 was interrupted immediately. Completed/partial/blocked records and request 33's interrupted state are preserved. Those SQLite results and controllers trained from them cannot support full-schema claims. This is an implementation mistake, not a finding about SQLite or LLMs.

## Corrected data and baselines

Use explicit feature names from data/manifest_v3.json; no implicitly ignored columns. Expect Apache 9 features/192 rows/0 duplicates, SQLite 39 features/4,652 rows/1 duplicate, x264 16 features/1,152 rows/0 duplicates. Duplicates keep their first source row, independent of objectives. Assert schema dimensions/names and duplicate counts against the manifest before any experiment. Same original files/commits/objectives/groups.

Rerun all 30 classical arms at B=20, t=10, four random initialization labels and fixed seeds 11,23,37,53,71, saving corrected prefixes. These are 600 newly charged offline label accesses; repeated accesses are not hidden. The algorithm, acquired-only scaling, features, bootstrap procedure, projection distance, retrospective d2h scoring and delta=0.02 from v1 remain fixed. Apache/SQLite development; x264 one held-out smoke group. Results are exploratory after previous inspection; no generalization claim.

## More compact real-model interface

Same pinned local Qwen 0.5B model, greedy logits, no remote code or API. Instead of spending generation on JSON punctuation, request five binary strings separated by newlines, each exactly the feature count. A token schedule constrains each coordinate to its legal 0/1 domain; only newline/EOS syntax is fixed. Every nonconstant configuration choice is selected by the model logits. Record raw binary text, generated IDs, constraint schedule and choice positions; parsing maps each character to its corresponding coordinate with no heuristic repair or completion. This is a deterministic serialization of real model choices, never fabricated proposals.

Each continuation makes two calls, with five proposals/call and exactly ten new charged objective acquisitions. The second call sees the five outcomes from the first. Batch size differs from SNAP2/v1/v2 and is explicitly an adaptation selected for bounded runtime before inspecting v3 outcomes. Numeric option values remain binary categorical; parse requires exact arity, coordinate length and domains. Feature-only nearest-unevaluated projection, ties by seeded order and collision feedback stay fixed. Invalid response => classical fallback for that batch; provider failure/timeout => stop all new requests and preserve incomplete run denominator. No retries or automatic worker restarts; dead worker detected before reservation.

## Gate and limits

After corrected classical tests/gate, execute three real-model synthetic feasibility fixtures (dimensions 9,16,39; same independent fixture generator; now five proposals). These remain in a separate synthetic namespace and count toward real inference costs, never software quality. Exactly three calls; all must parse within 60 seconds to open the paired gate. If passed, 15 software continuations × 2 calls = 30 paired calls. Expected additional calls for v3: 33; combined follow-up total: 66 <=100. Per-request timeout 60 seconds; total remaining runtime stays enforced by the same persistent v2/follow-up ledger, which includes v1 runtime. No cap resets.

Freeze this protocol, compact prompt, grammar, schemas and code before the first corrected classical outcome. No v3 outcome-driven changes. All three groups/five seeds retained in denominator. Do not pool v2 JSON treatment outcomes with v3 binary-string outcomes. Capture code snapshots and integrity hashes.

## Analysis

Apply the originally frozen v1 analysis unchanged to v3 paired gains: never/always, random development-selected rate, random realized-rate diagnostic, uncertainty threshold and ridge benefit/ablations fitted on development groups only, plus non-deployable hindsight. Fixed threshold grid and material margin remain. Report actual marginal v3 and cumulative collection costs, separate deployment trace estimates, reliability and projected/duplicate/fallback rates. A format gate success says nothing about optimization skill. Two development groups and one held-out smoke group provide insufficient evidence for a learned router's generalization. Corrected v3 is the primary usable smoke result; earlier versions remain disclosed debugging history.
