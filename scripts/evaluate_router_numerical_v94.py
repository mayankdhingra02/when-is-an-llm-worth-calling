"""Evaluate immutable precontinuation masks; no fitting or threshold choice."""
import json,statistics
from collect_smollm_v47 import ROOT,read,write,sha

def main():
    pin=read(ROOT/'artifacts/study_v94/precontinuation_analysis_pin.json')
    for n,h in pin['sha256'].items():assert sha(ROOT/n)==h,n
    p=read(ROOT/'artifacts/study_v94/router_precommit.json')
    for n,h in p['sha256'].items():assert sha(ROOT/n)==h,n
    summary=read(ROOT/'results/v94_analysis/summary.json')
    cases={f"{r['family']}_{r['seed']}":r for r in summary['cases']}
    rows=[cases[r['key']] for r in p['rows']]
    # Show that decisions were fixed before the first continuation was charged.
    acquisitions=[json.loads(s) for s in (ROOT/'results/v94_native/acquisitions.jsonl').read_text().splitlines()]
    assert p['at']<min(r['at'] for r in acquisitions if r['arm']!='prefix')
    gains=[r['relative_gains']['full_sequential_3nn'] for r in rows]
    masks={**p['masks'],'hindsight_oracle_diagnostic':[g>0 for g in gains]}
    outputs={}
    for name,mask in masks.items():
        assert len(mask)==len(rows)==10 and all(type(v) is bool for v in mask)
        outputs[name]={'calls':sum(mask),'intended_cases':10,'estimated_deployment_objective_labels':200,
            'estimated_deployment_physical_solves':600,'model_requests_selected':10*sum(mask),
            'measured_model_case_seconds_selected':sum(r['model_seconds'] for r,m in zip(rows,mask) if m),
            'runtime_exclusions':'startup, controller execution, native objective acquisition; not full deployment latency',
            'useful_cases_missed_at_5pct':sum(g>=.05 and not m for g,m in zip(gains,mask)),
            'harmful_escalations_at_5pct':sum(g<=-.05 and m for g,m in zip(gains,mask)),
            'family_mean_relative_gain':{f:statistics.mean(g if m else 0. for g,m,r in zip(gains,mask,rows) if r['family']==f) for f in ['superlu','highs']},
            'nondeployable_diagnostic':name.endswith('_diagnostic')}
    write(ROOT/'results/v94_analysis/policies.json',{'scope':p['scope'],'precommitted_at':p['at'],
        'thresholds':{'benefit':p['benefit'],'uncertainty':p['uncertainty']},'policies':outputs,
        'conclusion':'Both development-selected thresholds are never-call. There is no learned selection advantage over never, uncertainty or matched-rate random; all fitted and random masks coincide.'})
    lines=['# V94 secondary frozen router transfer','',
        'Decisions were sealed after prefix collection but before the first continuation outcome. '
        'Ridge coefficients and both thresholds used only 30 older Qwen3 paired cases grouped into six development systems. '
        'No new-family outcome was used to choose a threshold. The addition was exploratory and its timing is disclosed.', '',
        '| Policy | Calls / 10 | SuperLU gain | HiGHS gain | Useful cases missed | Harmful calls |',
        '|---|---:|---:|---:|---:|---:|']
    for name,r in outputs.items():
        g=r['family_mean_relative_gain'];lines.append(f"| {name} | {r['calls']} | {g['superlu']:+.2%} | {g['highs']:+.2%} | {r['useful_cases_missed_at_5pct']} | {r['harmful_escalations_at_5pct']} |")
    lines += ['', 'The benefit and uncertainty thresholds both selected never-call on development data. '
        'This saves every model request, but does not demonstrate benefit prediction or superiority over random routing. '
        'All matched-rate random decisions also call zero times. A positive hindsight value is available headroom, not an achieved policy.', '',
        'Only two fresh test groups were evaluated. No confidence interval or population claim is made. '
        'Quality gains above use measured final incumbents; failures stay in the paired arms. '
        'The 0.05 development penalty was a quality-preference scenario, not a monetary price or calibrated reliability guarantee.', '',
        'Saved evidence: `artifacts/study_v94/router_precommit.json`, `results/v94_analysis/policies.json`. '
        'Reproduce: `.venv/bin/python scripts/evaluate_router_numerical_v94.py`.']
    (ROOT/'reports/router_numerical_v94.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps(outputs,indent=2))
if __name__=='__main__':main()
