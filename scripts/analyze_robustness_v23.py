"""Run or read-only verify the versioned, post-hoc V23 analysis."""
import argparse
import csv
from decimal import Decimal
import hashlib
import json
import math
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src')); os.chdir(ROOT)
os.environ['MPLCONFIGDIR'] = str(ROOT / '.cache/matplotlib')
from escalation.io import read, write
from escalation.config import load_config
from escalation.larger_v22 import authorization_config, require
from escalation.resources import Resources
from escalation.robustness_v23 import analyze, BASELINES, CONDITIONS
OUT = Path('results/v23_robustness')

def calculate():
    for path, expected in read('reports/protocol_v23_robustness.freeze.json')['sha256'].items():
        require(hashlib.sha256(Path(path).read_bytes()).hexdigest() == expected, 'Changed frozen input: ' + path)
    source = read('results/v22_larger/summary.json')
    require(source['complete'], 'All intended arms required')
    jobs = read('data/larger_probe_v22.json')['jobs']
    expected = {(j['dataset'], j['seed'], j['condition']) for j in jobs if j['condition'] in CONDITIONS}
    require(len(expected) == 45, '45 unique presentations required')
    summary = analyze(source['records'], expected)
    require(summary['case_count'] == 15 and len(summary['families']) == 3, '15 cases / 3 families')
    # Independent decimal arithmetic directly from the previously saved CSV.
    with Path('results/v22_larger/outcomes.csv').open() as stream:
        csv_rows = list(csv.DictReader(stream))
    indexed = {(r['dataset'], int(r['seed']), r['condition']): r for r in csv_rows if r['condition'] in CONDITIONS}
    require(set(indexed) == expected and len(csv_rows) == 60, 'Independent CSV denominator')
    decimal_checks = 0
    for case in summary['cases']:
        for baseline in BASELINES:
            gains = [Decimal(indexed[(case['dataset'], case['seed'], c)][baseline]) - Decimal(indexed[(case['dataset'], case['seed'], c)]['llm_loss']) for c in CONDITIONS]
            values = [min(gains), sum(gains)/3, max(gains)]
            for field, value in zip(('minimum','mean','maximum'), values):
                require(math.isclose(case[baseline][field], float(value), abs_tol=1e-12), 'Independent decimal envelope')
                decimal_checks += 1
    for baseline in BASELINES:
        require(math.isclose(summary['aggregate'][baseline]['mean'], source['primary_family_equal_mean_gain_excluding_repeat'][baseline], abs_tol=1e-12), 'Original mean preserved')
    return summary, {'verified': True, 'independent_decimal_envelope_checks': decimal_checks,
                     'original_aggregate_means_preserved': 4, 'new_model_calls': 0, 'new_objective_acquisitions': 0}

def render(summary):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    cases = summary['cases']; fig, axes = plt.subplots(1, 2, figsize=(11, 6.5), sharey=True)
    for ax, baseline, title in zip(axes, ['classical_loss','first_display_loss'], ['Versus classical continuation', 'Versus first displayed ten']):
        for i, case in enumerate(cases):
            r = case[baseline]
            ax.plot([r['minimum'], r['maximum']], [i,i], color='#637887', linewidth=3)
            ax.scatter([r['mean']], [i], color='#176B93', s=24, zorder=3)
        ax.axvline(0, color='black', linewidth=.8)
        ax.axvline(.02, color='#b55b3d', linestyle='--', linewidth=.8)
        ax.set_title(title); ax.set_xlabel('Gain in normalized loss (positive favors LLM)')
        ax.grid(axis='x', alpha=.15)
    axes[0].set_yticks(range(len(cases)), [f"{c['dataset']} / {c['seed']}" for c in cases])
    axes[0].invert_yaxis()
    fig.suptitle('V23: gain across three observed presentations per saved prefix')
    fig.text(.5,.015,'Lines: observed min–max; dots: mean. Not confidence intervals. Dashed line: prior 0.02 diagnostic margin.\nPost-hoc development analysis: 3 families, 5 seeds. No new model calls.', ha='center', fontsize=9)
    fig.tight_layout(rect=[0,.07,1,.96])
    for ext in ['png','svg']:fig.savefig(OUT / ('gain_envelopes.'+ext),dpi=180)
    plt.close(fig)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--verify-only',action='store_true');args=parser.parse_args()
    if args.verify_only:
        summary, verification=calculate()
        require(summary==read(OUT / 'summary.json'), 'Saved summary differs')
        require(verification==read('artifacts/study_v23/verification.json'), 'Saved verification differs')
        print(json.dumps(verification,indent=2));return
    require(not OUT.exists(), 'Preserve completed V23 analysis')
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>15, 'Analysis runtime reserve required')
        summary,verification=calculate();write(OUT / 'summary.json',summary)
        rows=[]
        for case in summary['cases']:
            for baseline in BASELINES:
                row={k:case[k] for k in ('dataset','system_group','seed','llm_loss_range')}
                row.update(baseline=baseline);row.update({k:v for k,v in case[baseline].items() if k!='gains'})
                row.update(case[baseline]['gains']);rows.append(row)
        with (OUT / 'case_envelopes.csv').open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
        render(summary);resource.check();write('artifacts/study_v23/verification.json',verification)
    after=read('artifacts/resource_ledger_v2.json')
    require(before['requests']==after['requests']==200, 'No model calls permitted')
    write('artifacts/study_v23/accounting.json',{'new_model_calls':0,'new_objective_acquisitions':0,
         'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
         'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],
         'external_spend_usd':0,'active_since':after['active_since']})
    print(json.dumps({'aggregate':summary['aggregate'],'leave_one_family_out':summary['leave_one_family_out'],
                      'verification':verification},indent=2))

if __name__=='__main__':main()
