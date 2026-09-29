"""Independent budget, policy, solution-vector audit and descriptive V97 report."""
import json, random, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from scipy.io import mmread
from collect_smollm_v47 import read,write,sha,grammar
from escalation.numerical_v97 import candidates,linear_certificate,lp_certificate
from escalation.core import initial_state,State
from escalation.finite_domain import recommend
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import rank,messages
from escalation.qwen_v91 import validate_response
NATIVE=ROOT/'results/v97_native';MODEL=ROOT/'results/v97_qwen';OUT=ROOT/'results/v97_analysis'

def lines(path):
    return [json.loads(s) for s in path.read_text().splitlines()] if path.exists() else []

def audit():
    freeze=read(ROOT/'reports/protocol_v97.freeze.json')
    for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
    assert read(NATIVE/'completed.json')['intended_pairs']==5
    records=lines(NATIVE/'acquisitions.jsonl');assert len(records)==250
    assert len({r['key'] for r in records})==250
    acquired={r['key']:r for r in records}
    failures={r['key']:r for r in lines(NATIVE/'failures.jsonl')}
    exits={r['key']:r for r in lines(NATIVE/'worker_exits.jsonl')}
    a=mmread(ROOT/'data/native_v94/orsreg_1.mtx').tocsc()
    truth=1.+(np.arange(a.shape[0])%17)/17.;b=a@truth
    physical_starts=physical_returns=certificates_checked=0
    valid_acquisitions=0;max_rss=0
    for r in records:
        key=r['key'];events=lines(NATIVE/'evaluations'/f'{key}.attempts.jsonl')
        physical_starts+=sum(e['status']=='started' for e in events)
        physical_returns+=sum(e['status']=='returned' for e in events)
        request=read(NATIVE/'requests'/f'{key}.json')
        assert request['row']==r['row'] and request['configuration']==list(candidates(r['family']).x[r['row']])
        max_rss=max(max_rss,exits[key]['peak_sampled_rss_bytes'])
        if key in failures:
            assert r['label']==[30.];continue
        result=read(NATIVE/'evaluations'/f'{key}.json');vectors=np.load(NATIVE/'evaluations'/f'{key}.npz')
        certs=[]
        for rep in range(3):
            cert=linear_certificate(a,b,vectors[f'x{rep}'],truth)
            certs.append(cert);certificates_checked+=1
            assert cert['valid']==result['measurements'][rep]['certificate']['valid']
        expected=float(np.median([m['seconds'] for m in result['measurements']])) if all(c['valid'] for c in certs) else 30.
        assert expected==r['label'][0]==result['objective_seconds']
        valid_acquisitions+=int(result['valid'])
    responses=lines(MODEL/'responses.jsonl');starts=lines(MODEL/'generation_starts.jsonl')
    byid={r['request_id']:r for r in responses};assert len(byid)==len(responses)
    rows=[]
    for job in read(ROOT/'artifacts/study_v97/jobs.json'):
        p=read(ROOT/job['prefix']);c=candidates(p['family']);seed=p['seed'];key=job['key']
        assert sha(ROOT/job['prefix'])==job['prefix_sha256']
        state=initial_state(c,seed)
        for j in range(10):
            record=acquired[f'{key}_prefix_{j:02d}'];assert record['row']==recommend(c,state)
            state.observe(record['row'],record['label'],c.directions)
        assert state.record()==p['state'] and shortlist(c,state,seed)==p['pool']
        assert messages(c,state,p['pool'])==p['messages']
        choice=read(MODEL/'choices'/f'{key}.json') if (MODEL/'choices'/f'{key}.json').exists() else {'selected_ids':[],'status':'unattempted','case_seconds':None}
        used=[];preflight=read(MODEL/'preflight'/f'{key}.json')
        for request in [s for s in starts if s['identity'].startswith(key+'_')]:
            payload=request['payload']
            assert payload['prompt']==preflight['rendered']['prompt']+''.join(k+'\n' for k in used)
            assert payload['grammar']==grammar(used) and payload['n_predict']==1 and payload['temperature']==0
            if request['identity'] in byid:used.append(validate_response(byid[request['identity']]['response'],used))
        assert used==choice['selected_ids']
        modes=['batch_3nn','full_sequential_3nn','random_full','llm'];random.Random(seed+97000).shuffle(modes)
        case={'family':p['family'],'seed':seed,'prefix_best_seconds':min(y[0] for y in state.labels),
              'model_status':choice['status'],'model_seconds':choice['case_seconds'],'arms':{}}
        for mode in modes:
            s=state.clone();available=[i for i in s.order if i not in s.ids]
            if mode=='batch_3nn':batch=rank(c,s,p['pool']['ranked'])[:10]
            elif mode=='random_full':batch=random.Random(seed+41000).sample(available,10)
            elif mode=='llm':
                batch=[p['pool']['mapping'][k] for k in used]
                batch += [i for i in rank(c,state,p['pool']['ranked']) if i not in batch][:10-len(batch)]
            else:batch=None
            for j in range(10):
                record=acquired[f'{key}_{mode}_{j+10:02d}'];expected=batch[j] if batch is not None else rank(c,s,available)[0]
                assert record['row']==expected and record['row'] not in s.ids
                s.observe(record['row'],record['label'],c.directions)
            saved=read(NATIVE/'branches'/f'{key}_{mode}.json')
            assert len(s.ids)==20 and saved['state']==s.record() and saved['branch_order']==modes
            assert saved['prefix_sha256']==job['prefix_sha256']
            case['arms'][mode]=min(y[0] for y in s.labels)
        llm=case['arms']['llm']
        case['relative_gains']={mode:(value-llm)/value for mode,value in case['arms'].items() if mode!='llm'}
        case['inference_only_amortization_reuses_vs_sequential']=(case['model_seconds']/(case['arms']['full_sequential_3nn']-llm)
            if case['model_seconds'] is not None and case['arms']['full_sequential_3nn']>llm else None)
        case['hindsight_best_seconds']=min(llm,case['arms']['full_sequential_3nn'])
        rows.append(case)
    groups={}
    for family in ['superlu']:
        rs=[r for r in rows if r['family']==family]
        groups[family]={mode:{'mean_relative_gain':statistics.mean(r['relative_gains'][mode] for r in rs),
            'useful_at_5pct':sum(r['relative_gains'][mode]>=.05 for r in rs),
            'harmful_at_5pct':sum(r['relative_gains'][mode]<=-.05 for r in rs)} for mode in ['batch_3nn','full_sequential_3nn','random_full']}
    total_tokens=sum(r['response']['tokens_predicted'] for r in responses)
    known_context=sum(r['response']['tokens_evaluated'] for r in responses)
    ledger=read(NATIVE/'ledger.json');ml=read(MODEL/'ledger.json')
    assert ledger['acquisitions']==250 and ml['generation_requests']==len(starts)<=50
    summary={'scope':'one exposed engine; exploratory restricted-domain follow-up; no router confirmation',
        'cases':rows,'groups':groups,'failures_by_family':{f:sum(r['key'] in failures for r in records if r['family']==f) for f in ['superlu']},
        'audit':{'acquisitions':len(records),'valid_acquisitions':valid_acquisitions,'physical_starts':physical_starts,
            'physical_return_events':physical_returns,'certificates_recomputed':certificates_checked,
            'failed_worker_acquisitions':len(failures),'generation_requests':len(starts),'responses':len(responses),
            'returned_generated_tokens':total_tokens,'full_context_tokens_summed':known_context,
            'native_stage_seconds':ledger['worker_wall_seconds'],'model_stage_seconds':ml['stage_seconds'],
            'peak_native_sampled_rss_bytes':max_rss,'peak_model_rss_bytes':ml['peak_server_rss_bytes'],
            'external_spend_usd':0,'unobserved_request_usage_unknown':len(starts)-len(responses)},
        'download_bytes':freeze['download_bytes']}
    write(OUT/'summary.json',summary)
    return summary

if __name__=='__main__':
    summary=audit();print(json.dumps({'groups':summary['groups'],'audit':summary['audit']},indent=2))
