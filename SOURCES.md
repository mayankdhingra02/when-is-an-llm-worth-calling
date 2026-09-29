# Sources and provenance

Prepared September 24, 2026. This is a starter index, not a complete or independently re-audited bibliography. The full exported research report is in `reading/deep-research.md`. Verify important claims and links from original sources before implementation; preserve unresolved gaps in the audit.

## Included report

Title: **Cost- and Reliability-Aware Escalation: When Should Software-Configuration Optimization Call an LLM?**

Exported as text from the user's saved Deep Research report, version 1. It is an AI-assisted literature synthesis, not a primary paper or proof of novelty. The export preserves its text/links; ChatGPT-specific citation markers, if any, may not resolve outside ChatGPT.

SHA-256: `59d2decace7ed446f9c274237ea6f088ae68182c027f9c357f2f1a40b0d3070f`

## First three sources: inspect methods and artifacts

1. Srinath Srinivasan and Tim Menzies. **Better Together, in the Right Order: Classical-then-LLM Optimization for SE** (2026).
   - Paper: https://arxiv.org/abs/2607.02583
   - Version used for this handoff: https://arxiv.org/html/2607.02583v1
   - Author page: https://timm.fyi/snap2.html
   - Section VI-B explicitly discusses conditional escalation. The paper describes a 20-label setup with the first 10 assigned to the classical stage. Verify all implementation details before reproducing it.
   - The paper/article were accessible during preparation. A dedicated SNAP2 code artifact has **not** been located/validated for this pack. Do not invent one.

2. **Can AI be Easy? Lessons Learned from the EZR.py Toolkit**.
   - Paper: https://arxiv.org/abs/2606.03640
   - Report's referenced revision: https://arxiv.org/html/2606.03640v2
   - Repository: https://github.com/timm/ezr
   - The repository page was accessible during preparation; its code has **not** been executed for this pack. Check paper-to-code version alignment; do not assume current HEAD matches SNAP2.

3. **MOOT: a Repository of Many Multi-Objective Optimization Tasks**.
   - Paper: https://arxiv.org/abs/2511.16882
   - Repository: https://github.com/timm/moot
   - The repository page was accessible during preparation. Inspect data schema, provenance, licensing, objective directions, aliases, and system families before selection. No data were downloaded or validated for this pack.

## Related Menzies work from the included report

- **Which Optimizer, At What Budget? A Tournament of Optimizers for Search-Based SE**: https://arxiv.org/abs/2607.11705
  - Artifact to verify: https://github.com/KKGanguly/OptimizerTournament
  - Use for task-feature/budget ideas; do not reproduce the whole tournament in the pilot.
- **Is Model Instability just Noise to be Tolerated or a Property that can be Managed?**: https://arxiv.org/abs/2607.10420
  - Artifact to verify: https://github.com/anonymoussepaperauthor/Model-Instability
  - Use for reliability signals, not an assumption that instability implies LLM benefit.
- **Can Large Language Models Improve SE Active Learning via Warm-Starts?**: https://arxiv.org/abs/2501.00125
- **How Low Can You Go? The Data-Light SE Challenge**: https://arxiv.org/abs/2512.13524
- **Minimal Data, Maximum Clarity: A Heuristic for Explaining Optimization**: https://arxiv.org/abs/2509.08667

These entries were extracted from the completed report and were not all independently rechecked during creation of this pack. Confirm their precise authors, dates, versions, and artifact links in the source audit.

## Routing/deferral literature: read ideas, do not clone every implementation

- **FrugalGPT: How to Use Large Language Models While Reducing Cost and Improving Performance**: https://arxiv.org/abs/2305.05176
- **AutoMix: Automatically Mixing Language Models**: https://arxiv.org/abs/2310.12963
  - Report's code link: https://github.com/automix-llm/automix
- **RouteLLM: Learning to Route LLMs with Preference Data**: https://arxiv.org/abs/2406.18665
  - Report's code link: https://github.com/lm-sys/RouteLLM
- **SCOPE: Cost-Efficient Model Selection for Compound AI Systems under Quality Constraints**: https://arxiv.org/abs/2606.00774
  - Report's code link: https://github.com/waetr/SCOPE-LLM-optimizer
- **Consistent Estimators for Learning to Defer to an Expert**: https://arxiv.org/abs/2006.01862
- **Selective Classification for Deep Neural Networks**: https://arxiv.org/abs/1705.08500

These are report-derived reading leads. Read relevant original sections and verify the closest prior work before asserting a gap. Search for newer direct follow-ups too. The report contains additional adjacent papers, but implementing them all is out of scope.

## Codex setup and billing references

- Project instructions (`AGENTS.md`): https://developers.openai.com/codex/guides/agents-md
- Agent-loop description: https://openai.com/index/unrolling-the-codex-agent-loop/
- Separate ChatGPT/API billing: https://help.openai.com/en/articles/9039756

These official pages were retrieved during pack preparation. The USD 0 restriction concerns new external experiment spending, not a promise of unlimited/free Codex usage.

## Audit format

For each load-bearing source, record: exact title/authors/version/date; primary link; sections relevant to the implementation; verified artifact URL/commit/license; supported claim; unresolved ambiguity; and status (`lead`, `metadata_verified`, `methods_read`, `artifact_inspected`, `executed`). A working link is not an executed replication.
