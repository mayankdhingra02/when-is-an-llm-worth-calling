"""Replay saved feasibility evidence without model calls or objective access."""
import json
from collect_smollm_v47 import ROOT,read,write,sha
from reasoning_v98_common import check_payload,audit_case
RAW=ROOT/'results/v101_reasoning'
def rows(name):
    p=RAW/name
    return [json.loads(x) for x in p.read_text().splitlines()] if p.exists() else []
def main():
    for n,h in read(ROOT/'reports/protocol_v101.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    cfg=read(ROOT/'configs/study_v101.json');jobs=read(ROOT/'artifacts/study_v101/jobs.json')
    starts=rows('generation_starts.jsonl');responses=rows('responses.jsonl')
    sm={r['identity']:r for r in starts};rm={r['key']:r for r in responses};ledger=read(RAW/'ledger.json')
    assert len(sm)==len(starts)==ledger['generation_requests']<=3
    assert len(rm)==len(responses) and set(rm)<=set(sm)
    allowed={j['key']+'_'+phase for j in jobs for phase in (['thought','final'] if j['mode']=='thinking' else ['final'])}
    assert set(sm)<=allowed
    for r in starts:check_payload(r['payload'])
    assert sum(r['payload']['n_predict'] for r in starts)==ledger['allocated_output_tokens']<=768
    assert ledger['server_exit_code'] is not None and ledger['stage_seconds']<=600
    assert ledger['retries']==0 and ledger['external_spend_usd']==0
    runtime=read(RAW/'runtime.json');assert runtime['config']==cfg
    cmd=runtime['command'];assert cmd[cmd.index('-c')+1]=='4096' and cmd[cmd.index('--load-mode')+1]=='none'
    cases=[]
    for job in jobs:
        key=job['key'];path=RAW/'choices'/f'{key}.json';pre=RAW/'preflight'/f'{key}.json'
        choice=read(path) if path.exists() else {'status':'unattempted','selected_ids':[]}
        parsed=None
        if pre.exists():
            p=read(pre);assert p['prefix_sha256']==sha(ROOT/job['prefix'])
            assert len(p['prompt_tokens'])+512+128+16<=4096
            parsed=audit_case(job,p,sm,rm,choice)
        else:assert not any(k.startswith(key+'_') for k in sm)
        fp=RAW/'final_prompts'/f'{key}.json'
        if fp.exists():
            f=read(fp);assert len(f['prompt_tokens'])+128<=4096
            assert f['prompt']==sm[key+'_final']['payload']['prompt']
            assert f['control_is_model_output'] is False
        cases.append({'key':key,'mode':job['mode'],'status':choice['status'],'valid':bool(parsed and parsed['valid'])})
    missing=sorted(set(sm)-set(rm));generated=sum(r['response']['tokens_predicted'] for r in responses)
    prefill=[r['response'].get('timings',{}).get('prompt_n') for r in responses]
    summary={'scope':'resource feasibility only; no objective outcomes acquired/scored','conditions':cases,
        'feasibility_passed':all(c['valid'] for c in cases),'ledger':ledger,'responses_returned':len(responses),
        'missing_response_ids':missing,'returned_generated_tokens':generated,
        'total_generated_tokens':None if missing else generated,
        'returned_observed_prefill_tokens':sum(v for v in prefill if v is not None),
        'total_actual_prefill_tokens':None if missing or any(v is None for v in prefill) else sum(prefill),
        'new_objective_acquisitions':0,'replay_new_model_calls':0,'replay_new_objective_acquisitions':0}
    write(ROOT/'artifacts/study_v101/feasibility.json',summary)
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
