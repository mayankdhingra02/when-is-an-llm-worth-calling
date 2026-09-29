"""Replay only acquired MongoDB cells, real requests, fixed masks and blinding."""
import csv,json
from table_check_v121 import ROOT,read,sha,write,candidates,MODES
from table_adapter_v121 import audit_case,freeze121
from verify_table_classical_v121 import verify as verify_classical
from prepare_model_v121 import blinded
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain,rank
from escalation.policy_transfer_v41 import predecision_masks

def lines(p):return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def verify():
    freeze121();verify_classical();out=ROOT/'results/v121_analysis';model=ROOT/'results/v121_qwen';s=read(out/'summary.json');spec,c,_=candidates();jobs=read(ROOT/'artifacts/study_v121/model_jobs.json')
    acqs=lines(out/'acquisitions.jsonl');starts=lines(model/'generation_starts.jsonl');responses=lines(model/'responses.jsonl');sm={r['identity']:r for r in starts};rm={r['request_id']:r for r in responses}
    assert s['complete'] and len(s['cases'])==len(jobs)==10 and len(acqs)==100 and s['actual_classical_acquisitions']==300
    assert len(sm)==len(starts)==s['new_model_requests']==s['ledger']['generation_requests']<=100
    assert len(rm)==len(responses)==s['returned_responses']<=len(starts)
    assert s['ledger']['allocated_output_tokens']==len(starts) and s['ledger']['retries']==s['ledger']['external_spend_usd']==0
    assert s['ledger']['server_exit_code'] is not None and s['ledger']['stage_seconds']<=900
    source=__import__('pathlib').Path(spec['path']).read_text().splitlines();header=next(csv.reader([source[0]],delimiter=';'));cases={r['key']:r for r in s['cases']}
    for job in jobs:
        key=job['key'];r=cases[key];p=read(ROOT/job['prefix']);original=read(ROOT/job['original_prefix']);assert p['state']==original['state'] and p['pool']==original['pool']
        assert p['messages']==(original['messages'] if job['condition']=='normal' else blinded(original['messages']))
        state=State(**p['state']).clone();events=[e for e in acqs if e['key']==key];assert len(events)==10 and r['selected_rows']==[e['row_id'] for e in events]
        for e in events:
            assert e['source_line']==c.source_ids[e['row_id']] and e['namespace']=='measured_v121_recorded' and e['seed']==p['seed']
            raw=dict(zip(header,next(csv.reader([source[e['source_line']-1]],delimiter=';'))))['performance'];assert raw==e['raw_target'];state.observe(e['row_id'],[float(raw)],('-',))
        assert state.record()==read(out/'arms'/f'{key}.json')['state'] and len(set(state.ids))==20 and best(state,'-')==r['target']
        for m in MODES:
            ref=State(**read(ROOT/f"results/v121_classical/arms/{job['base_key']}_{m}.json")['state']);assert ref.ids[:10]==p['state']['ids'] and ref.labels[:10]==p['state']['labels'];assert best(ref,'-')==r['references'][m] and relative_gain(best(ref,'-'),r['target'],'-')==r['gains'][m]
        cp=model/'choices'/f'{key}.json';choice=read(cp) if cp.exists() else {'status':'unattempted','selected_ids':[]};pf=model/'preflight'/f'{key}.json'
        if pf.exists():
            pre=read(pf);assert pre['messages']==p['messages'] and pre['prefix_hash']==p['prefix_hash'];parsed=audit_case(job,pre,sm,rm,choice)
            if parsed['valid']:assert r['selected_rows']==[p['pool']['mapping'][i] for i in parsed['selected_ids']]
        assert r['fallback']==(choice['status']!='completed')
        if r['fallback']:assert r['selected_rows']==rank(c,State(**p['state']),p['pool']['ranked'])[:10]
    pc=read(ROOT/'results/v121_classical/policy_precommit.json')
    masks,scores=predecision_masks(pc['rows'],read(ROOT/'results/v121_router/router_first10_seal.json'));assert masks==pc['first10_masks'] and scores==pc['first10_scores']
    for n,h in read(ROOT/'artifacts/study_v121/model_inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h
    return {'verified':True,'groups':1,'normal_cases':5,'loss_blind_cases':5,'source_events_replayed':400,'real_model_requests':len(starts),'returned_responses':len(responses),'new_model_requests':0,'new_acquisitions':0}
if __name__=='__main__':
    r=verify();write(ROOT/'artifacts/study_v121/verification.json',r);print(json.dumps(r))
