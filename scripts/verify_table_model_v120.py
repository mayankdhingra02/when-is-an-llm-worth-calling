"""Independent request/source replay of the actual V120 model continuations."""
import csv,json
from table_check_v119 import ROOT,read,sha,write,frozen,candidates,MODES
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain,rank
from table_adapter_v120 import audit_case,freeze120
from verify_table_classical_v119 import verify as verify_classical

def lines(p):return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def verify(root=ROOT,check_freeze=True):
    verify_classical(root,check_freeze)
    if check_freeze:freeze120()
    model=root/'results/v120_qwen';out=root/'results/v120_analysis';s=read(out/'summary.json');spec,c,_=candidates(root)
    assert s['complete'] and s['intended_cases']==s['completed_cases']==5
    jobs=read(root/'artifacts/study_v119/jobs.json');acqs=lines(out/'acquisitions.jsonl');starts=lines(model/'generation_starts.jsonl');responses=lines(model/'responses.jsonl')
    assert len(jobs)==len(s['cases'])==5 and len(acqs)==50 and s['actual_classical_acquisitions']==0 and s['historical_shared_classical_acquisitions']==250 and s['actual_new_llm_acquisitions']==50
    sm={r['identity']:r for r in starts};rm={r['request_id']:r for r in responses};cases={r['key']:r for r in s['cases']}
    assert len(sm)==len(starts)==s['ledger']['generation_requests']==s['new_model_requests']<=50
    assert len(rm)==len(responses)==s['returned_responses']<=len(starts)
    assert s['ledger']['allocated_output_tokens']==len(starts)<=50 and s['ledger']['retries']==0 and s['ledger']['external_spend_usd']==0
    assert s['ledger']['server_exit_code'] is not None and s['ledger']['stage_seconds']<=900
    source=__import__('pathlib').Path(spec['path']).read_text().splitlines();header=next(csv.reader([source[0]]))
    for job in jobs:
        key=job['key'];r=cases[key];p=read(root/job['prefix']);state=State(**p['state']).clone();arm=read(out/'arms'/f'{key}.json')
        assert p['seed']==job['optimization_seed']==r['optimization_seed'] and r['decoding_seed']==11
        events=[e for e in acqs if e['key']==key];assert len(events)==10
        assert r['selected_rows']==[e['row_id'] for e in events]
        for e in events:
            assert e['source_line']==c.source_ids[e['row_id']] and e['seed']==p['seed'] and e['namespace']=='measured_v120_recorded'
            row=dict(zip(header,next(csv.reader([source[e['source_line']-1]]))));assert row['latency']==e['raw_target']
            state.observe(e['row_id'],[float(e['raw_target'])],('-',))
        assert len(set(state.ids))==20 and state.record()==arm['state'] and arm['prefix_sha256']==sha(root/job['prefix'])
        assert best(state,'-')==r['target']
        for mode in MODES:
            ref=State(**read(root/f'results/v119_classical/arms/{key}_{mode}.json')['state'])
            assert ref.ids[:10]==p['state']['ids'] and ref.labels[:10]==p['state']['labels']
            assert best(ref,'-')==r['references'][mode]
            assert relative_gain(best(ref,'-'),r['target'],'-')==r['gains'][mode]
        cp=model/'choices'/f'{key}.json';choice=read(cp) if cp.exists() else {'status':'unattempted','selected_ids':[]};pf=model/'preflight'/f'{key}.json'
        if pf.exists():
            pre=read(pf);assert pre['messages']==p['messages'] and pre['prefix_hash']==p['prefix_hash']
            parsed=audit_case(job,pre,sm,rm,choice)
            if parsed and parsed['valid']:assert [p['pool']['mapping'][i] for i in parsed['selected_ids']]==r['selected_rows']
        assert r['fallback']==(choice['status']!='completed') and r['status']==choice['status']
        if r['fallback']:assert r['selected_rows']==rank(c,State(**p['state']),p['pool']['ranked'])[:10]
        assert r['charged_requests']==sum(k.startswith(key+'_') for k in sm) and r['returned_responses']==sum(k.startswith(key+'_') for k in rm)
    for n,h in read(root/'artifacts/study_v119/model_inputs.freeze.json')['sha256'].items():assert sha(root/n)==h,n
    return {'verified':True,'groups':1,'prefixes':5,'acquired_source_events_replayed':300,'separate_v119_fallback_events':50,'model_requests':len(starts),'real_responses':len(responses),'fallbacks':sum(r['fallback'] for r in cases.values()),'new_objective_acquisitions':0,'new_model_requests':0}

if __name__=='__main__':
    r=verify();write(ROOT/'artifacts/study_v120/model_verification.json',r);print(json.dumps(r))
