"""Replay acquired-source values, prefix decisions and isolated B20 controls."""
import csv,json
from collections import Counter
from table_check_v119 import ROOT,read,sha,write,frozen,candidates,MODES,SEEDS
from escalation.core import initial_state
from escalation.finite_domain import recommend
from escalation.finite_v6 import features
from escalation.selection_v8 import shortlist
from escalation.transfer_v41 import branch,messages
from escalation.policy_transfer_v41 import predecision_masks
from portfolio_v115 import portfolio

def verify(root=ROOT,check_freeze=True):
    if check_freeze:frozen()
    out=root/'results/v119_classical';spec,c,_=candidates(root);progress=read(out/'progress.json')
    assert progress['complete'] and progress['actual_new_acquisitions']==250 and progress['stage_seconds']<180
    events=[json.loads(s) for s in (out/'acquisitions.jsonl').read_text().splitlines()]
    assert len(events)==250
    counts=Counter((e['seed'],e['arm']) for e in events)
    assert counts==Counter({(s,m):10 for s in SEEDS for m in ('prefix',)+MODES})
    source=__import__('pathlib').Path(spec['path']).read_text().splitlines();header=next(csv.reader([source[0]]));records={}
    for e in events:
        assert e['namespace']=='measured_v119_recorded' and e['dataset']==spec['id'] and e['system_group']=='storm'
        assert e['source_line']==c.source_ids[e['row_id']]
        row=dict(zip(header,next(csv.reader([source[e['source_line']-1]]))))
        assert row['latency']==e['raw_target'] and float(e['raw_target'])>0
        k=(e['seed'],e['arm'],e['row_id']);assert k not in records;records[k]=float(e['raw_target'])
    rows=[]
    for seed in SEEDS:
        key=f"{spec['id']}_{seed}";state=initial_state(c,seed);pp=out/'prefixes'/f'{key}.json';p=read(pp)
        def acquire_for(mode):
            es=[e for e in events if e['seed']==seed and e['arm']==mode];at=0
            def f(row):
                nonlocal at
                assert at<len(es) and row==es[at]['row_id'];at+=1
                return [records[(seed,mode,row)]]
            return f
        acq=acquire_for('prefix')
        for _ in range(10):state.observe(recommend(c,state),acq(recommend(c,state)),c.directions)
        assert state.record()==p['state'];pool=shortlist(c,state,seed);fs,_=features(c,state,seed)
        assert pool==p['pool'] and fs==p['features'] and messages(c,state,pool)==p['messages']
        rows.append({k:p[k] for k in ('dataset','seed','system_group','features')})
        for mode in MODES:
            r=read(out/'arms'/f'{key}_{mode}.json');acq=acquire_for(mode)
            if mode=='single_portfolio':got,trace=portfolio(c,state,pool['ranked'],acq);assert trace==r['trace']
            else:got=branch(c,state,pool['ranked'],seed,mode,acq)
            assert got.record()==r['state'] and len(set(got.ids))==20 and r['prefix_sha256']==sha(pp)
    pc=read(out/'policy_precommit.json');masks,scores=predecision_masks(rows,read(root/'results/v6/router_seal.json'))
    assert rows==pc['rows'] and masks==pc['masks'] and scores==pc['scores'] and pc['continuation_outcomes_used'] is False
    assert pc['fitted_on_new_data'] is False and 'storm' not in pc['training_groups']
    return {'verified':True,'source_acquisitions_replayed':250,'prefixes':5,'B20_controls':20,'groups':1,'new_objective_acquisitions':0,'new_model_requests':0}

if __name__=='__main__':
    r=verify();write(ROOT/'artifacts/study_v119/classical_verification.json',r);print(json.dumps(r))
