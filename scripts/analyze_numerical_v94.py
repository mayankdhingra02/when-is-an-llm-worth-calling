"""Independent budget, policy, solution-vector audit and descriptive V94 report."""
import json, random, statistics, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
from scipy.io import mmread
from collect_smollm_v47 import read,write,sha,grammar
from escalation.numerical_v94 import candidates,linear_certificate,lp_certificate
from escalation.core import initial_state,State
from escalation.finite_domain import recommend
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import rank,messages
from escalation.qwen_v91 import validate_response
NATIVE=ROOT/'results/v94_native';MODEL=ROOT/'results/v94_qwen';OUT=ROOT/'results/v94_analysis'

def lines(path):
    return [json.loads(s) for s in path.read_text().splitlines()] if path.exists() else []

def audit():
    freeze=read(ROOT/'reports/protocol_v94.freeze.json')
    for n,h in freeze['sha256'].items():assert sha(ROOT/n)==h,n
    assert read(NATIVE/'completed.json')['intended_pairs']==10
    records=lines(NATIVE/'acquisitions.jsonl');assert len(records)==500
    assert len({r['key'] for r in records})==500
    acquired={r['key']:r for r in records}
    failures={r['key']:r for r in lines(NATIVE/'failures.jsonl')}
    exits={r['key']:r for r in lines(NATIVE/'worker_exits.jsonl')}
    a=mmread(ROOT/'data/native_v94/orsreg_1.mtx').tocsc()
    truth=1.+(np.arange(a.shape[0])%17)/17.;b=a@truth
    import highspy
    h=highspy.Highs();h.setOptionValue('output_flag',False)
    assert h.readModel(str(ROOT/'artifacts/sources/v94/25fv47.mps'))==highspy.HighsStatus.kOk
    lp=h.getLp();assert lp.a_matrix_.format_==highspy.MatrixFormat.kColwise
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
            cert=(linear_certificate(a,b,vectors[f'x{rep}'],truth) if r['family']=='superlu'
                  else lp_certificate(lp,vectors[f'x{rep}'],vectors[f'y{rep}'],vectors[f'z{rep}']))
            certs.append(cert);certificates_checked+=1
            assert cert['valid']==result['measurements'][rep]['certificate']['valid']
        expected=float(np.median([m['seconds'] for m in result['measurements']])) if all(c['valid'] for c in certs) else 30.
        assert expected==r['label'][0]==result['objective_seconds']
        valid_acquisitions+=int(result['valid'])
    responses=lines(MODEL/'responses.jsonl');starts=lines(MODEL/'generation_starts.jsonl')
    byid={r['request_id']:r for r in responses};assert len(byid)==len(responses)
    rows=[]
    for job in read(ROOT/'artifacts/study_v94/jobs.json'):
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
        modes=['batch_3nn','full_sequential_3nn','random_full','llm'];random.Random(seed+94000).shuffle(modes)
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
    for family in ['superlu','highs']:
        rs=[r for r in rows if r['family']==family]
        groups[family]={mode:{'mean_relative_gain':statistics.mean(r['relative_gains'][mode] for r in rs),
            'useful_at_5pct':sum(r['relative_gains'][mode]>=.05 for r in rs),
            'harmful_at_5pct':sum(r['relative_gains'][mode]<=-.05 for r in rs)} for mode in ['batch_3nn','full_sequential_3nn','random_full']}
    total_tokens=sum(r['response']['tokens_predicted'] for r in responses)
    known_context=sum(r['response']['tokens_evaluated'] for r in responses)
    ledger=read(NATIVE/'ledger.json');ml=read(MODEL/'ledger.json')
    assert ledger['acquisitions']==500 and ml['generation_requests']==len(starts)<=100
    summary={'scope':'two-group fixed-policy extension; descriptive, no learned-router confirmation',
        'cases':rows,'groups':groups,'failures_by_family':{f:sum(r['key'] in failures for r in records if r['family']==f) for f in ['superlu','highs']},
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

def report(s):
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axs=plt.subplots(1,2,figsize=(10,4),sharey=True)
    controls=['batch_3nn','full_sequential_3nn','random_full']
    for ax,family in zip(axs,['superlu','highs']):
        for x,control in enumerate(controls):
            gains=[100*r['relative_gains'][control] for r in s['cases'] if r['family']==family]
            ax.scatter(x+np.linspace(-.12,.12,len(gains)),gains,color='#286DA8',s=28)
            ax.plot([x-.2,x+.2],[np.mean(gains)]*2,color='black',linewidth=2)
        ax.axhline(0,color='gray',lw=1);ax.axhline(5,color='green',ls='--',lw=.8);ax.axhline(-5,color='red',ls='--',lw=.8)
        ax.set_xticks(range(3),['Batch 3NN','Sequential 3NN','Random']);ax.set_title(family)
    axs[0].set_ylabel('LLM relative incumbent runtime gain (%)')
    fig.suptitle('V94: five seeds per engine; black bars are within-engine means')
    fig.tight_layout();fig.savefig(OUT/'paired_gains.png',dpi=180);fig.savefig(OUT/'paired_gains.svg');plt.close(fig)
    a=s['audit'];out=['# V94: fresh numerical-engine results','',
        'The fixed Qwen3 policy was evaluated prospectively on two new native engine groups. '
        'This is not a learned-router validation or evidence of journal acceptance.','',
        '| Engine | vs batch 3NN mean | vs sequential 3NN mean | vs random mean |',
        '|---|---:|---:|---:|']
    for family,g in s['groups'].items():out.append('| '+family+' | '+' | '.join(f"{100*g[c]['mean_relative_gain']:+.2f}%" for c in controls)+' |')
    out += ['', 'Positive gain means a faster validated incumbent. Every seed is retained in `results/v94_analysis/summary.json`; '
        'the 5% practical threshold was fixed before measurements. No group confidence interval is warranted with two engines.', '',
        '## What actually ran','',json.dumps(a,indent=2),'',
        'Each of 10 shared prefixes acquired ten labels. Four continuations acquired ten labels each: '
        '500 actual configuration acquisitions, versus 20 logical labels for deployment of any one branch. '
        'Each acquisition planned three physical solves. Native failures remain charged and penalized; '
        'physical starts/returns are reported separately, and missing executions are unknown. '
        'The verification recomputes solution certificates from saved vectors and reconstructs every classical/LLM selection.', '',
        '## Costs and interpretation','',
        'Actual collection includes all four continuations, all real model requests and native/model lifecycle time. '
        'A deployed policy would use its shared prefix plus one branch and pay model cost only on escalation. '
        'External spending is zero; electricity and hardware costs are unknown. '
        'The per-case inference-only break-even reuse count divides measured model case time by positive incumbent runtime savings. '
        'It excludes startup and different search costs, so it is a scenario, not demonstrated deployment savings.', '',
        '## Limitations','',
        'Two engine groups, one input per engine, one machine, three timing repetitions per acquired configuration, '
        'and selection on noisy measured minima. Repeated seeds are not independent systems. '
        'Public benchmarks may be in model pretraining. Native and wrapper versions are pinned, but a clean-machine '
        'replication has not run. SuperLU worker crashes are actual runtime failures, not filtered observations; '
        'the cause is not yet established by a native debugger. The freeze remains unchanged. '
        'The constructed RHS is disclosed. Historical dataset redistribution terms remain unresolved. '
        'New router thresholds were not fit or assessed on these held-out outcomes.', '',
        'Reproduce analysis: `.venv/bin/python scripts/analyze_numerical_v94.py`. '
        'Raw records: `results/v94_native/`, `results/v94_qwen/`. Freeze: `reports/protocol_v94.freeze.json`.']
    (ROOT/'reports/numerical_v94.md').write_text('\n'.join(out)+'\n')

if __name__=='__main__':
    summary=audit();report(summary);print(json.dumps({'groups':summary['groups'],'audit':summary['audit']},indent=2))
