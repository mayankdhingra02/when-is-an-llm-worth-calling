"""Render verified V64 measurements, including all physical resource failures."""
import csv
import json
import os
import statistics
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault('MPLCONFIGDIR', str(ROOT / 'artifacts/.mpl_cache'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def read(path):
    return json.loads(path.read_text())


def main():
    out = ROOT / 'results/v64_sat_screen'
    summary = read(out / 'summary.json')
    physical = read(ROOT / 'results/v64_sat_physical/summary.json')
    verified = read(ROOT / 'artifacts/study_v64/verification.json')
    assert verified['verified'] and physical['complete_table']
    rows = read(ROOT / 'results/v64_sat_physical/all_cases.json')
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.8))
    descriptions = []
    for ax, w in zip(axes, summary['workloads']):
        folder = out / ('minisat_' + w['workload'])
        table = read(folder / 'table.json')
        with (folder / 'settings.csv').open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['id', 'configuration', 'median_penalized_ms', 'valid_repetitions', 'cv'])
            for row in table:
                writer.writerow([row['config_id'], json.dumps(row['configuration']), row['median_ms'], row['valid_repetitions'], row['cv']])
        for method, label, marker in [('random', 'Random', 'o'), ('nn', '3NN', 's'), ('rf_lcb', 'RF-LCB (primary)', '^')]:
            values = [100 * (c['best_ms'][method] - w['minimum_ms']) / c['best_ms'][method] for c in w['cases']]
            ax.plot(range(5), values, marker=marker, label=label)
        if w['threshold_percent'] is not None:
            ax.axhline(w['threshold_percent'], color='brown', ls=':', label='Frozen threshold')
        ax.set(title=w['workload'], xticks=range(5), xticklabels=[c['seed'] for c in w['cases']], xlabel='Seed (one solver family)', ylabel='Remaining recorded headroom (%)')
        ax.legend(fontsize=8)
        selected = [r for r in rows if r['workload'] == w['workload']]
        cvs = [t['cv'] for t in table if t['valid_repetitions'] == 3]
        descriptions.append({**w, 'valid_trials': sum(r['status'] == 'valid' for r in selected), 'resource_failures': sum(r['status'] == 'resource_noncompletion' for r in selected), 'median_valid_cv_percent': 100 * statistics.median(cvs) if cvs else None})
    fig.suptitle('MiniSat: opportunity remaining after 20 classical evaluations')
    fig.text(.5, .01, 'Generated development tasks; recorded medians of three; failures score 40,000 ms. Not an LLM result.', ha='center', fontsize=9)
    fig.tight_layout(rect=(0, .045, 1, .94))
    fig.savefig(out / 'headroom.png', dpi=160)
    fig.savefig(out / 'headroom.svg')
    plt.close(fig)
    (out / 'descriptive_summary.json').write_text(json.dumps(descriptions, indent=2) + '\n')
    def number(value):
        return 'undefined' if value is None else f'{value:.3f}'
    table_text = '\n'.join(f"| {w['workload']} | {w['valid_trials']}/144 | {w['resource_failures']} | {w['minimum_ms']:.3f} | {number(w['median_valid_cv_percent'])} | {number(w['threshold_percent'])} | {w['gate_case_count']}/5 | {'pass' if w['gate_passed'] else 'stop'} |" for w in descriptions)
    passes = [w['workload'] for w in descriptions if w['gate_passed']]
    conclusion = ('The frozen opportunity gate passes for ' + ', '.join(passes) + '. This justifies preparing a bounded real-model comparison; it does not establish that an LLM improves anything.') if passes else 'Neither task passes the frozen opportunity gate. Stop LLM collection on this grid under this protocol; do not retune it to obtain a positive result.'
    report = f'''# V64 — measured SAT configuration opportunity screen

**{conclusion}**

All 288 intended physical trials ran: {verified['valid_models']} valid solutions and
{verified['resource_noncompletion']} resource noncompletions. Every valid solution
was independently checked against every clause of its original CNF. No retries or
dropped failures. Collection took {physical['stage_seconds']:.3f} seconds under the
explicitly approved 7,200-second envelope. No model calls, downloads or spending.

| Task | Valid trials | Resource failures | Best median ms | Median valid CV % | Threshold % | Gate cases | Decision |
|---|---:|---:|---:|---:|---:|---:|---|
{table_text}

![Remaining recorded headroom](../results/v64_sat_screen/headroom.png)

The primary comparator was RF-LCB before full-grid outcomes. Random and 3NN are
controls, not candidates for post-hoc selection of a favorable primary method.
Each of five fixed seeds has the same saved ten-evaluation prefix across three
arms, each ending at twenty inclusive evaluations. Thirty arms consumed 400
charged recorded-table acquisitions in {summary['runtime_seconds']:.3f} seconds.
Full-table scoring occurred only after decisions. Headroom is the improvement
available relative to that arm's best score, not an achieved LLM improvement.
The hindsight portfolio remains diagnostic only.

Forty-eight configurations vary decay, restart and phase-saving options. Each row
is the median of three fresh physical runs. An 18-second CPU / 20-second wall /
sampled 512 MiB RSS limit applies per trial; resource noncompletion receives a
40,000-ms PAR2-style objective score. This penalty is not reported as measured
runtime. The gate requires RF-LCB headroom at least max(5%, twice the median CV
percentage among fully valid settings) for at least two of five seeds. Undefined
noise thresholds cannot pass. The threshold is a screening heuristic, not a test
of statistical significance or equivalence.

## Scope and limitations

Both admitted generated tasks (256 and 512 variables) were retained. The three
1,024-variable CPU-limit noncompletions from V62 remain in the admission report.
The 512-variable task followed one disclosed adaptive size calibration. There
will be no further size calibration in this series. These are planted random
3-CNF tasks with known witnesses saved for validation only, not production or
SAT-competition samples. Seeds, tasks and parameter settings do not create
independent software systems. MiniSat is conservatively grouped with historical
Z3. The current evidence supplies one development solver family, no fresh held-out
router validation and no basis for a journal acceptance claim.

The owner MiniSat commit and compatibility patch are pinned in the V62 source
manifest and V64 freeze. Search code was not changed. CPU noncompletions are part
of the denominator; three repetitions and one host leave uncertainty about noise,
machine dependence and stable minima. Outcomes are now exposed development data.
No threshold or configuration-grid change may be described as confirmatory.

## Costs and verification

Actual research collection cost: 288 physical solver invocations plus the nine
earlier admission invocations, and 400 recorded aggregate acquisitions for this
screen. A modeled deployment of one 20-outcome arm using the same median-of-three
recipe would require 60 physical trials, including failures and initialization.
That is an estimate from the recipe, not measured deployment time or evidence
that full-grid data would be free. All resource-failure wall times remain logged.
External experiment spend is zero; hardware, electricity and researcher costs
are unknown. Model request/token/runtime costs are absent because this stage
contains no inference.

Independent verification reconstructed all 288 physical receipts and schedule,
all returned models, table medians, noise thresholds, 400 charged acquisitions,
360 optimizer choices, shared prefixes, inclusive budgets and gate decisions.
Verification took {verified['runtime_seconds']:.3f} seconds. Synthetic tests are
separate from these measurements. Raw evidence: results/v64_sat_physical/;
tables, acquisition journals, arms, CSV and figures: results/v64_sat_screen/.

```sh
.venv/bin/python scripts/verify_sat_v64.py
.venv/bin/python scripts/report_sat_v64.py
```

Collection and primary analysis are one-shot and refuse existing output trees.
The exact approval receipt is artifacts/study_v64/approval_receipt.json; the
pre-outcome protocol and input hashes are reports/protocol_v64_sat_screen.md and
its freeze JSON. No additional inference allowance follows from the runtime
approval. The next step must respect the decision above.
'''
    (ROOT / 'reports/sat_screen_v64.md').write_text(report)
    print(conclusion)


if __name__ == '__main__':
    main()
