"""V92: exact V48 diagnostic prompts, V91 Qwen3 runtime, no target acquisition."""
import json,time
from runtime_sensitivity_v92b import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,now,sha,grammar,IDS
from validate_sensitivity_v92b import validate
from escalation.qwen_v91 import validate_response
OUT=ROOT/'results/v92b_sensitivity';ART=ROOT/'artifacts/study_v92'
def main():
    cfg=read(ROOT/'configs/study_v92b.json');validate(cfg)
    for n,h in read(ROOT/'reports/protocol_v92b.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)
    prior=read(ROOT/'results/v92_sensitivity/ledger.json')
    assert prior['generation_requests']==0 and prior['stage_seconds']<1 and prior['server_exit_code']==0
    rss(-1)
    if OUT.exists():raise ValueError('No implicit restart')
    OUT.mkdir();rt=Runtime(OUT,cfg);rt.ledger.update(completed_cases=0,objective_accesses=0)
    try:
        rt.start()
        tokens={c:rt.api('/tokenize',{'content':c,'add_special':False})['tokens'] for c in IDS+'\n'}
        if any(len(t)!=1 for t in tokens.values()) or len({t[0] for t in tokens.values()})!=21:raise ValueError('Non-single-token ID/delimiter')
        write(OUT/'choice_tokenization.json',tokens)
        prepared=[]; overflows=[]
        for job in read(ROOT/'artifacts/study_v48/jobs.json'):
            p=read(ROOT/job['prefix']);rendered=rt.api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
            ids=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens']
            if len(ids)+20>cfg['context_tokens']:overflows.append({'key':job['key'],'tokens':len(ids)})
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],'rendered':rendered,'prompt_tokens':ids,'prefix_hash':p['prefix_hash']});prepared.append((job,p,rendered['prompt']))
        write(OUT/'context_check.json',{'overflows':overflows,'cases':len(prepared),'context_tokens':cfg['context_tokens']})
        if overflows:raise ValueError('Context overflow: '+str(overflows))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,p,prompt in prepared:
            used=[];failure=None;case_start=time.monotonic();request_ids=[]
            for step in range(10):
                payload={'prompt':prompt+''.join(c+'\n' for c in used),'n_predict':1,'temperature':0,'seed':11,'grammar':grammar(used),'cache_prompt':bool(step),'return_tokens':True,'stream':False,'repeat_penalty':1.0}
                identity=f"{job['key']}_{step}";request_ids.append(identity);request={'request_id':identity,'case':job['key'],'step':step,'at':now(),'payload':payload};append(OUT/'request_starts.jsonl',request);t=time.monotonic()
                try:
                    response=rt.generate(payload,'scientific',identity);append(OUT/'responses.jsonl',{**request,'status':'response','response':response,'wall_seconds':time.monotonic()-t});used.append(validate_response(response,used))
                except Exception as e:
                    failure=f'{type(e).__name__}: {e}';append(OUT/'errors.jsonl',{'request_id':identity,'error':failure,'at':now(),'wall_seconds':time.monotonic()-t})
                    if rt.reason or rt.proc.poll() is not None or isinstance(e,(TimeoutError,OSError,PermissionError)):raise
                    break
            write(OUT/'choices'/f"{job['key']}.json",{**job,'selected_ids':used,'fallback_reason':failure,'request_ids':request_ids,'case_seconds':time.monotonic()-case_start,'prefix_hash':p['prefix_hash'],'status':'completed' if len(used)==10 else 'invalid'})
            rt.ledger['completed_cases']+=1;write(OUT/'ledger.json',rt.ledger);print(job['key'],len(used),'choices',flush=True)
    except Exception as e:rt.ledger['stop_reason']=f'{type(e).__name__}: {e}';raise
    finally:rt.close()
if __name__=='__main__':main()
