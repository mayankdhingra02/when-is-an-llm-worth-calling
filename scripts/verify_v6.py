"""Independent postcollection audit. Reads hidden labels only retrospectively."""
import sys,collections,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,lines,digest,write
from escalation.data import sha
from escalation.finite_v6 import load_candidates,parse_symbols
from escalation.core import State,initial_state,project
from escalation.finite_domain import recommend,uniform_proposals
from escalation.study_v6 import retrospective_labels,verify_freeze,OUT

def main():
    verify_freeze()
    for old in ['reports/protocol_v4.freeze.json','reports/registry_v5.freeze.json']:
        for p,h in read(old)['sha256'].items():assert sha(p)==h,p
    m=read('data/manifest_v6.json');done=read(OUT/'completed.json');raw=lines(OUT/'acquisitions.jsonl');req=lines(OUT/'requests.jsonl');starts=lines(OUT/'request_starts.jsonl')
    assert len(done['intended'])==30 and len({(r['dataset'],r['seed']) for r in done['intended']})==30
    assert len(starts)<=32 and len(req)==len(starts)
    baseline=read(OUT/'manifest.json')['baseline_ledger'];ledger=read('artifacts/resource_ledger_v2.json')
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained('models/Qwen2.5-0.5B-Instruct',local_files_only=True,trust_remote_code=False)
    assert ledger['requests']-baseline['requests']==len(starts) and ledger['requests']<=100
    assert ledger['experiment_seconds']<=1800 and ledger.get('active_since') is None
    assert done['actual_acquisitions']==len(raw) and all(r['namespace']=='measured_v6' for r in raw)
    for group,es in __import__('itertools').groupby(sorted(raw,key=lambda e:(e['dataset'],e['seed'],e['arm'])),key=lambda e:(e['dataset'],e['seed'],e['arm'])):
        es=list(es);assert len(es)==len({e['row_id'] for e in es}) and len(es)<= (20 if group[2]=='random' else 10)
    for r in req:
        assert r['model_id']=='Qwen/Qwen2.5-0.5B-Instruct' and r['revision']=='7ae557604adf67be50417f59c2c2f167def9a775'
        assert r['parameters']['do_sample'] is False and r['retry']==0
        if r['status']=='response':
            ids=r['generated_token_ids'];schedule=r['grammar_schedule'];assert len(ids)<=1024 and len(ids)==len(schedule)
            assert all(i in options for i,options in zip(ids,schedule))
            assert len(ids)==r['output_tokens'] and r['input_tokens']>0
            assert tokenizer.decode(ids,skip_special_tokens=True)==r['raw_output']
            assert r['raw_output'] is not None and r['rendered_prompt_sha256'] and r['cache_key']
    verified_cases=0
    for d in m['datasets']:
        if not d['selected']:continue
        c=load_candidates(d);ys=retrospective_labels(d,c)
        assert all(__import__('math').isfinite(y[0]) and y[0]>0 for y in ys),'invalid retrospective target table: '+d['id']
        for seed in m['seeds']:
            k=d['id']+'_'+str(seed);cp=OUT/'classical'/f'{k}.json';bp=OUT/'paired'/f'{k}.json'
            if not cp.exists():continue
            a=read(cp);p=read(OUT/'prefixes'/f'{k}.json')
            assert len(p['state']['ids'])==10 and digest(p['state'])==p['prefix_hash']==a['prefix_hash']
            replay=initial_state(c,seed)
            for i,y in zip(p['state']['ids'],p['state']['labels']):
                assert recommend(c,replay)==i;replay.observe(i,y,c.directions)
            assert replay.record()==p['state']
            for name,arm in a['arms'].items():
                s=arm['state'];assert len(s['ids'])==len(set(s['ids']))==20
                assert s['labels']==[ys[i] for i in s['ids']]
                if name!='random':assert s['ids'][:10]==p['state']['ids'] and s['labels'][:10]==p['state']['labels']
                replay=initial_state(c,seed) if name=='random' else State(**p['state']).clone();proposals=uniform_proposals(c,seed+40000,10)
                begin=0 if name=='random' else 10
                for pos in range(begin,20):
                    i=project(c,replay,proposals[pos-10])[0] if name=='uniform_projection' else recommend(c,replay,'random' if name=='random' else 'centroid_nominal')
                    assert i==s['ids'][pos];replay.observe(i,s['labels'][pos],c.directions)
                assert replay.record()==s
            if bp.exists():
                b=read(bp);assert b['prefix_hash']==p['prefix_hash'] and b['state']['ids'][:10]==p['state']['ids']
                assert len(b['state']['ids'])==len(set(b['state']['ids']))==20
                assert b['state']['labels']==[ys[i] for i in b['state']['ids']] and b['actual_new_accesses']==10
                r=next(r for r in req if r['request_id']==b['request_id'])
                if b['status']=='completed':
                    proposals=parse_symbols(r['raw_output'],c);replay=State(**p['state']).clone()
                    for j,proposal in enumerate(proposals):
                        i,event=project(c,replay,proposal);assert i==b['state']['ids'][10+j]
                        assert all(b['events'][j][k]==v for k,v in event.items())
                        replay.observe(i,b['state']['labels'][10+j],c.directions)
                    assert replay.record()==b['state']
                verified_cases+=1
    if done['complete']:
        assert len(raw)==1800 and len(req)==32 and verified_cases==30
        seal=read(OUT/'router_seal.json');assert sha(OUT/'router_seal.json')==read(OUT/'router_seal.sha256.json')['sha256']
        for p,h in seal['development_files'].items():assert sha(p)==h
        test_ids={d['id'] for d in m['datasets'] if d['split']=='test'}
        assert all(e['at']>seal['at'] for e in raw if e['dataset'] in test_ids)
        assert set(seal['benefit']['training_groups'])=={d['system_group'] for d in m['datasets'] if d['split']=='development'}
    report={'verified':True,'complete':done['complete'],'verified_pairs':verified_cases,'acquisitions':len(raw),'new_requests':len(starts),
      'old_freezes_intact':True,'deterministic_prefix_classical_projection_and_llm_replay':True,'tokenizer_decodes_match_raw_responses':True,'logical_budget':20,'checkpoint':10,'test_acquisition_after_router_seal':done['complete'],
      'ledger_requests':ledger['requests'],'ledger_runtime_seconds':ledger['experiment_seconds'],'status_counts':dict(collections.Counter(r['status'] for r in done['intended']))}
    write('artifacts/study_v6/verification.json',report);print(__import__('json').dumps(report,indent=2))
if __name__=='__main__':main()
