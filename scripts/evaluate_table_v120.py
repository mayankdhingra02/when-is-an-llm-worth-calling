"""After model shutdown, charge saved selections and compare frozen controls."""
import json,time
from table_check_v119 import ROOT,read,write,append,sha,frozen,candidates,MODES
from escalation.core import State
from escalation.transfer_v41 import IndexedOracle,rank,best,relative_gain
from table_adapter_v120 import audit_case,freeze120
MODEL=ROOT/'results/v120_qwen';OUT=ROOT/'results/v120_analysis'

def lines(p):return [json.loads(s) for s in p.read_text().splitlines()] if p.exists() else []
def known_sum(xs):return None if any(x is None for x in xs) else sum(xs)

def main():
    frozen();freeze120();assert not OUT.exists();ledger=read(MODEL/'ledger.json');assert ledger['server_exit_code'] is not None
    assert ledger['generation_requests']<=50 and ledger['allocated_output_tokens']<=50 and ledger['retries']==0
    assert ledger['stage_seconds']<=900 and ledger['external_spend_usd']==0
    for n,h in read(ROOT/'artifacts/study_v119/model_inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h
    jobs=read(ROOT/'artifacts/study_v119/jobs.json');starts=lines(MODEL/'generation_starts.jsonl');responses=lines(MODEL/'responses.jsonl')
    sm={r['identity']:r for r in starts};rm={r['request_id']:r for r in responses}
    assert len(sm)==len(starts)==ledger['generation_requests'] and len(rm)==len(responses)
    spec,c,_=candidates();OUT.mkdir();count=0;rows=[];stop=None;t=time.monotonic()
    try:
        for job in jobs:
            p=read(ROOT/job['prefix']);state=State(**p['state']).clone();key=job['key'];cp=MODEL/'choices'/f'{key}.json'
            choice=read(cp) if cp.exists() else {'status':'unattempted','selected_ids':[],'case_seconds':None}
            pf=MODEL/'preflight'/f'{key}.json';parsed=None
            if pf.exists():
                pre=read(pf);assert pre['messages']==p['messages'] and pre['prefix_hash']==p['prefix_hash']
                parsed=audit_case(job,pre,sm,rm,choice)
            chosen=[p['pool']['mapping'][i] for i in choice['selected_ids']] if choice['status']=='completed' else rank(c,state,p['pool']['ranked'])[:10]
            assert len(chosen)==len(set(chosen))==10 and not set(chosen)&set(state.ids)
            oracle=IndexedOracle(spec,c,p['state'],lambda e:append(OUT/'acquisitions.jsonl',{'namespace':'measured_v120_recorded','key':key,'seed':job['optimization_seed'],'arm':'llm',**e}))
            for row in chosen:
                if count>=50 or time.monotonic()-t>180:raise RuntimeError('Evaluator cap')
                count+=1;state.observe(row,oracle.acquire(row),c.directions)
            refs={};classical_seconds={}
            for mode in MODES:
                r=read(ROOT/'results/v119_classical/arms'/f'{key}_{mode}.json');s=State(**r['state'])
                assert s.ids[:10]==p['state']['ids'] and s.labels[:10]==p['state']['labels']
                refs[mode]=best(s,spec['direction']);classical_seconds[mode]=r['branch_seconds']
            target=best(state,spec['direction']);responses_case=[v for v in responses if v['case']==key];charged=sum(k.startswith(key+'_') for k in sm)
            def observed(field):return known_sum([field(v) for v in responses_case]) if len(responses_case)==charged else None
            r={'key':key,'family':'storm','optimization_seed':job['optimization_seed'],'decoding_seed':11,
              'status':choice['status'],'fallback':choice['status']!='completed','selected_rows':chosen,'target':target,
              'references':refs,'gains':{k:relative_gain(v,target,spec['direction']) for k,v in refs.items()},
              'charged_requests':sum(k.startswith(key+'_') for k in sm),'returned_responses':len(responses_case),
              'model_seconds':observed(lambda v:v['wall_seconds']),
              'case_seconds':choice['case_seconds'],'generated_tokens':observed(lambda v:v['response'].get('tokens_predicted')),
              'prefill_tokens':observed(lambda v:v['response'].get('timings',{}).get('prompt_n')),
              'full_context_tokens':observed(lambda v:v['response'].get('tokens_evaluated')),
              'prefix_seconds':p['prefix_seconds'],'classical_seconds':classical_seconds,'failure_reasons':None if parsed is None else parsed['reasons']}
            write(OUT/'arms'/f'{key}.json',{**r,'state':state.record(),'prefix_sha256':sha(ROOT/job['prefix'])});rows.append(r)
    except Exception as e:stop=repr(e)
    finally:
        summary={'scope':'Exploratory adapter follow-up after V119 format failures on the same exposed Storm table; original published labels only; one family, five seeds; stronger V52 admission remains closed.',
          'complete':stop is None and len(rows)==5,'stop_reason':stop,'intended_cases':5,'completed_cases':len(rows),'cases':rows,
          'actual_new_llm_acquisitions':count,'actual_classical_acquisitions':0,'historical_shared_classical_acquisitions':250,'historical_v119_fallback_acquisitions':50,
          'new_model_requests':len(starts),'returned_responses':len(responses),'ledger':ledger,'evaluation_seconds':time.monotonic()-t,
          'actual_generated_tokens':known_sum([r.get('response',{}).get('tokens_predicted') for r in responses]) if len(responses)==len(starts) else None,
          'actual_prefill_tokens':known_sum([r.get('response',{}).get('timings',{}).get('prompt_n') for r in responses]) if len(responses)==len(starts) else None,
          'missing_response_usage':len(starts)-len(responses),'external_spend_usd':0}
        write(OUT/'summary.json',summary)
    if stop:raise RuntimeError(stop)
    assert count==50;print(json.dumps({'completed':5,'new_llm_acquisitions':count,'new_requests':len(starts),'fallbacks':sum(r['fallback'] for r in rows)}))

if __name__=='__main__':main()
