"""Report strict native results and a labeled outcome-free formatting diagnostic."""
import itertools
import json
import os
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'artifacts/.mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
def read(p): return json.loads(p.read_text())


def main():
    raw = ROOT / 'results/v65_sat_llm'
    out = ROOT / 'results/v65_sat_llm_analysis'
    assert read(ROOT / 'artifacts/study_v65/verification.json')['verified']
    summary = read(out / 'summary.json')
    choices = read(raw / 'all_cases.json')
    jobs = read(ROOT / 'artifacts/study_v65/jobs.json')
    responses = [json.loads(line) for line in (raw / 'responses.jsonl').read_text().splitlines()]
    domain = list(itertools.product([.8, .95], [.9, .999], [25, 100, 400], [1.2, 2], [0, 2]))
    diagnostics = []
    for r, job in zip(responses, jobs):
        assert r['seed'] == job['seed']
        text = r['response']['content'].strip()
        wrapped = text.startswith('```json\n') and text.endswith('\n```')
        d = {'seed': r['seed'], 'single_json_fence': wrapped, 'diagnostic_only_no_acquisitions': True}
        try:
            proposal = json.loads(text[len('```json\n'):-len('\n```')] if wrapped else text)
            ids = [domain.index(tuple(row)) for row in proposal]
            overlap = sorted(set(ids) & {o['config_id'] for o in job['prefix']})
            d.update(proposals=len(ids), unique_proposals=len(set(ids)), repeated_proposal_occurrences=len(ids) - len(set(ids)), already_acquired_ids=overlap, format_only_repair_would_satisfy_contract=len(ids) == len(set(ids)) == 10 and not overlap)
        except (ValueError, TypeError): d['diagnostic_parse_failed'] = True
        diagnostics.append(d)
    (out / 'posthoc_format_diagnostic.json').write_text(json.dumps({'scope': 'post-hoc outcome-free diagnosis; no repaired arm or objective access', 'cases': diagnostics}, indent=2) + '\n')
    fig, ax = plt.subplots(figsize=(8, 4.3))
    ax.bar([str(c['seed']) for c in choices], [c.get('wall_seconds', 0) for c in choices], color='#9a5a45')
    ax.set(xlabel='Prefix seed (one generated development task)', ylabel='Observed request wall seconds', title=f"Native SAT proposals: {summary['valid_cases']}/5 accepted, {summary['operational_fallbacks']}/5 RF fallbacks")
    fig.text(.5, .01, 'Actual local SmolLM3-3B requests; startup and physical table collection excluded from bar heights.', ha='center', fontsize=8)
    fig.tight_layout(rect=(0, .035, 1, 1))
    fig.savefig(out / 'reliability.png', dpi=160)
    fig.savefig(out / 'reliability.svg')
    plt.close(fig)
    table = '\n'.join(f"| {c['seed']} | {c['status']}: {c.get('reason')} | {c.get('wall_seconds', 0):.3f} | {c.get('usage', {}).get('tokens_predicted')} | {d.get('repeated_proposal_occurrences')} | {len(d.get('already_acquired_ids', []))} |" for c, d in zip(choices, diagnostics))
    repaired = sum(d.get('format_only_repair_would_satisfy_contract', False) for d in diagnostics)
    report = f'''# V65 — real native SAT proposals fail the frozen reliability contract

Five real local SmolLM3-3B requests ran on all five saved prefixes of the task
admitted by V64. **{summary['valid_cases']}/5 outputs satisfied the frozen contract;
{summary['operational_fallbacks']}/5 used the paired RF fallback.** No valid LLM proposal arm
was measured and no LLM-attributable quality gain was observed. Equal terminal
scores are operational fallback ties, not evidence of model/classical equivalence.

| Seed | Strict result | Request seconds | Generated tokens | Duplicate occurrences after fence removal | Already acquired distinct IDs |
|---|---|---:|---:|---:|---:|
{table}

![Actual request latency and reliability](../results/v65_sat_llm_analysis/reliability.png)

## Actual execution and bounded costs

The approved protocol allowed five generations, at most1,024 output tokens each,
900seconds collection,50new recorded acquisitions,0retries/downloads/spending.
Actual: five requests, {summary['usage']['tokens_predicted']['observed_total']} generated
tokens and {summary['usage']['tokens_evaluated']['observed_total']} evaluated input tokens,
{summary['collection_seconds']:.3f}seconds total collection including
{summary['startup_seconds']:.3f}seconds startup, and **{summary['new_recorded_accesses']} new
recorded acquisitions**. The server shut down with exit0. All five requests have
observed token counts; no failed transport or missing intended case. Physical SAT
table construction (288V64 trials plus9admission trials) remains actual research
cost, distinct from inference and a modeled deployment's evaluation cost.

Existing owner-pinned SmolLM3-3B Q4_K_M weights, revision
4965cb60b150737b68a0408c36aeefb65078f894, were used with local llama.cpp b11146.
This is the same3B model already available, not a new model/reasoning-enabled test.
Thinking was off, temperature0, seed11 requested, native unconstrained decoding,
no retries, projection or repair. Exact executable/model hashes, commands,
rendered prompts, token IDs, request starts, native response metadata and raw
outputs are preserved. Fixed seed does not establish cross-device determinism.

## What failed, and what cannot be inferred

All five responses included Markdown code fences despite the explicit JSON-only
instruction. The predeclared parser rejects these. This is partly an interface
contract result; it does not demonstrate that the model cannot optimize SAT.
A separately labeled **post-hoc, outcome-free diagnostic** removes exactly one
outer JSON fence and checks proposal identities, without reading additional
objectives or constructing a repaired optimization arm. Only {repaired}/5 then satisfy
the remaining ten-unique-unobserved contract. See the table for duplicate and
already-acquired proposals. This diagnostic neither overrides the frozen result
nor counts repaired choices as real measured model arms.

All operational arms reuse their corresponding saved RF branch. The primary
always-escalate-versus-never comparison has five ties and pays additional inference
cost; the hindsight best-of-two diagnostic also cannot improve on RF here. No
finite inference break-even is observed. Because terminal improvement is zero,
counting startup or additional overhead cannot turn this implementation into a
net-benefit result. Positive terminal differences against other classical controls
would be RF fallback behavior, not model credit.

The broader opportunity result remains: on planted_512, preselected RF left
47.13% headroom in two of five cases, about43.55ms absolute. Thus lack of opportunity
alone does not explain this failure; reliable novel proposals are an additional
requirement. This is one generated task in one development solver family, after
adaptive feasibility and opportunity admission. It is not an independent held-out
replication, learned-router evaluation, significance result or Q2-readiness proof.
Five seeds cannot substitute for independent software systems.

## Verification and stop decision

Independent verification checks frozen sources/model/runtime and approval hash,
all five request starts and complete raw responses, rendered prompt identity,
context reserve, strict domain/uniqueness/exclusion rules, fallback provenance,
shared ten-prefix/twenty-inclusive budgets, all five pair effects and observed
token counts. The verifier does not use the production parser. All415 Python tests
pass, with ten new synthetic parser/prompt tests isolated from measured outcomes.
The diagnostic above is a report addition made after observing output formatting.

```sh
.venv/bin/python scripts/verify_sat_llm_v65.py
.venv/bin/python scripts/report_sat_llm_v65.py
```

Stop prompt/decoder/grid tuning on these exposed cases as frozen. A future test
would need a separately frozen reliability-preserving interface (for example,
constrained legal unobserved proposals) and fresh eligible software-system groups,
not another prompt chosen until these five cases pass. Such a test remains
unexecuted. No further model allowance, background job, cloud spend or publication
is implied. Raw results: results/v65_sat_llm/; paired fallbacks, cost summaries and
the labeled diagnostic: results/v65_sat_llm_analysis/.
'''
    (ROOT / 'reports/sat_llm_v65.md').write_text(report)
    print(json.dumps({'valid': summary['valid_cases'], 'format_only_repair_valid': repaired, 'new_recorded_accesses': summary['new_recorded_accesses']}))


if __name__ == '__main__': main()
