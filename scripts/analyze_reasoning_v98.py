"""Charge V98 selected cells, retain all 36 cases, and analyze fixed comparisons."""
import json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read,write,append,sha
from escalation.core import State
from escalation.finite_v6 import load_candidates
from escalation.transfer_v41 import restrict,IndexedOracle,best,relative_gain,rank
from reasoning_v98_common import audit_case
MODEL=ROOT/'results/v98_reasoning';OUT=ROOT/'results/v98_analysis'

def main():
    if OUT.exists():raise ValueError('No implicit reacquisition')
    for n,h in read(ROOT/'reports/protocol_v98.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    ledger=read(MODEL/'ledger.json');assert ledger.get('server_exit_code') is not None
    assert ledger['generation_requests']<=54 and ledger['allocated_output_tokens']<=13824
    assert ledger['stage_seconds']<=1800
    starts=[json.loads(s) for s in (MODEL/'generation_starts.jsonl').read_text().splitlines()] if (MODEL/'generation_starts.jsonl').exists() else []
    responses=[json.loads(s) for s in (MODEL/'responses.jsonl').read_text().splitlines()] if (MODEL/'responses.jsonl').exists() else []
    sm={r['identity']:r for r in starts};rm={r['key']:r for r in responses}
    assert len(sm)==len(starts)==ledger['generation_requests'] and len(rm)==len(responses)
    manifest=read(ROOT/'data/manifest_v41.json');specs={d['id']:d for d in manifest['datasets']}
    # Paths in existing source manifests are relative to the original repository.
    import os;os.chdir(ROOT)
    candidates={k:restrict(load_candidates(s),s['fixed_features'])[0] for k,s in specs.items()}
    old={r['key']:r for r in read(ROOT/'results/v91_analysis/cases.json')}
    OUT.mkdir();rows=[];accesses=0
    for job in read(ROOT/'artifacts/study_v98/jobs.json'):
        p=read(ROOT/job['prefix']);state=State(**p['state']);c=candidates[job['dataset']];spec=specs[job['dataset']]
        choicepath=MODEL/'choices'/f"{job['key']}.json"
        choice=read(choicepath) if choicepath.exists() else {'status':'unattempted','selected_ids':[],'case_seconds':None}
        pfpath=MODEL/'preflight'/f"{job['key']}.json"
        parsed=None
        if pfpath.exists():
            pf=read(pfpath)
            assert pf['messages']==p['messages'] and pf['prefix_sha256']==sha(ROOT/job['prefix'])
            parsed=audit_case(job,pf,sm,rm,choice)
        selected=[p['pool']['mapping'][k] for k in choice['selected_ids']] if choice['status']=='completed' else rank(c,state,p['pool']['ranked'])[:10]
        assert len(selected)==len(set(selected))==10 and not set(selected)&set(state.ids)
        oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'case':job['key'],**e}))
        for row in selected:
            if accesses>=360:raise RuntimeError('Recorded-acquisition cap')
            accesses+=1;state.observe(row,oracle.acquire(row),c.directions)
        assert len(state.ids)==20 and oracle.new_accesses==10
        target=best(state,spec['direction']);base=old[job['base_key']]
        refs={k:base['references'][k] for k in ['full_sequential_3nn','batch_3nn','random_full']}
        refs['greedy_forced_qwen']=base['target']
        case_responses=[v for k,v in rm.items() if k in [job['key']+'_thought',job['key']+'_final']]
        case_starts=[v for k,v in sm.items() if k in [job['key']+'_thought',job['key']+'_final']]
        r={'key':job['key'],'base_key':job['base_key'],'family':job['system_group'],
            'seed':job['seed'],'mode':job['mode'],'status':choice['status'],'selected_rows':selected,
            'fallback':choice['status']!='completed','failure_reasons':None if parsed is None else parsed['reasons'],
            'target':target,'references':refs,'gains':{k:relative_gain(v,target,spec['direction']) for k,v in refs.items()},
            'model_seconds':choice['case_seconds'],
            'generated_tokens':sum(v['response']['tokens_predicted'] for v in case_responses) if case_responses else None,
            'charged_requests':len(case_starts),'returned_responses':len(case_responses),
            'missing_request_usage':len(case_starts)-len(case_responses)}
        write(OUT/'arms'/f"{job['key']}.json",{**r,'state':state.record(),'prefix_sha256':sha(ROOT/job['prefix'])})
        rows.append(r)
    assert len(rows)==36 and accesses==360
    groups={};modes={}
    for mode in ['thinking','nonthinking']:
        rs=[r for r in rows if r['mode']==mode]
        groups[mode]={f:{k:statistics.mean(r['gains'][k] for r in rs if r['family']==f) for k in rs[0]['gains']} for f in sorted({r['family'] for r in rs})}
        modes[mode]={'intended':18,'valid':sum(r['status']=='completed' for r in rs),'fallbacks':sum(r['fallback'] for r in rs),
            'generated_tokens_returned':sum(r['generated_tokens'] or 0 for r in rs),'missing_token_usage_cases':sum(r['generated_tokens'] is None for r in rs),
            'mean_gain_vs_sequential':statistics.mean(v['full_sequential_3nn'] for v in groups[mode].values()),
            'useful_at_5pct_vs_sequential':sum(r['gains']['full_sequential_3nn']>=.05 for r in rs),
            'harmful_at_5pct_vs_sequential':sum(r['gains']['full_sequential_3nn']<=-.05 for r in rs)}
    summary={'scope':'development-only two-stage final-answer reserve; not unrestricted reasoning or held-out evaluation',
        'cases':rows,'family_means':groups,'modes':modes,'actual_new_recorded_acquisitions':accesses,
        'requests':len(starts),'responses':len(responses),'ledger':ledger,
        'reported_actual_prefill_tokens':sum(r['response']['timings']['prompt_n'] for r in responses),
        'summed_full_context_tokens':sum(r['response']['tokens_evaluated'] for r in responses),'external_spend_usd':0}
    write(OUT/'summary.json',summary);print(json.dumps({'modes':modes,'family_means':groups},indent=2))
if __name__=='__main__':main()
