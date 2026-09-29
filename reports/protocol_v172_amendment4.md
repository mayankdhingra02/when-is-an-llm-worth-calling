# V172 amendment 4: report wording (presentation only)

Written 2026-09-28, after the verified analysis. This changes only `scripts/report_v172.py`, which formats `results/v172_analysis/analysis.json`. No data, selection, analysis value or decision changes.

The first generated report is preserved as `artifacts/study_v172/model_scale_v172_initial_generated.md`. It had three omissions:

1. **Fallback attribution.** The lower-bound note attributed all 25 re-draw fallbacks to stage B1. Nineteen came from B1's RSS-cap stop and six from B2's server loss (cause unconfirmed; see amendment 2).
2. **Reliability table.** It had no column for requests attempted without a response, so one charged request per B stage was invisible in the row arithmetic.
3. **Re-draw mean.** The re-draw's secondary mean did not say that it includes the fallback cases.

The regenerated `reports/model_scale_v172.md` corrects all three.

**Procedural note.** This amendment also makes `scripts/common_v172.py` discover amendment freeze files by name in numeric order, and updates the matching test, so the overlay list no longer has to be edited for each amendment. The first `freeze_amendment4.json` omitted these two files. It was regenerated once, immediately and before it was used for any verification, to cover all changed files.
