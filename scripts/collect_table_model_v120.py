"""Real Qwen3 outputs; isolated from objective acquisition/evaluation code."""
import json,time
from runtime_qwen_v91 import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,now,sha,grammar,IDS
from escalation.qwen_v91 import validate_response
OUT=ROOT/'results/v120_qwen';ART=ROOT/'artifacts/study_v120'
def main():
    cfg=read(ROOT/'configs/study_v120.json')
    assert cfg['allow_paid_api'] is False and cfg['allow_cloud'] is False and cfg['max_external_spend_usd']==0
    assert cfg['new_generation_request_cap']==cfg['scientific_request_cap']==cfg['max_allocated_output_tokens']==50
    assert cfg['compatibility_request_cap']==cfg['retries']==cfg['stage_download_cap_bytes']==0
    model=read(ROOT/'artifacts/study_v91/model_manifest.json');assert sha(ROOT/model['path'])==model['sha256']
    for n,h in read(ROOT/'reports/protocol_v120.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)
    rss(-1)
    if OUT.exists():raise ValueError('No implicit restart')
    OUT.mkdir();rt=Runtime(OUT,cfg);rt.ledger['completed_cases']=0
    try:
        rt.start()
        tokens={c:rt.api('/tokenize',{'content':c,'add_special':False})['tokens'] for c in IDS+'\n'}
        if any(len(t)!=1 for t in tokens.values()) or len({t[0] for t in tokens.values()})!=21:raise ValueError('Non-single-token ID/delimiter')
        write(OUT/'choice_tokenization.json',tokens)
        prepared=[]
        for job in read(ROOT/'artifacts/study_v119/jobs.json'):
            p=read(ROOT/job['prefix']);rendered=rt.api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
            ids=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens']
            if len(ids)+20>cfg['context_tokens']:raise ValueError('Context overflow')
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],'rendered':rendered,'prompt_tokens':ids,'prefix_hash':p['prefix_hash']});prepared.append((job,p,rendered['prompt']))
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
            write(OUT/'choices'/f"{job['key']}.json",{**job,'selected_ids':used,'fallback_reason':failure,'request_ids':request_ids,'case_seconds':time.monotonic()-case_start,'prefix_hash':p['prefix_hash'],'status':'completed' if len(used)==10 else 'fallback'})
            rt.ledger['completed_cases']+=1;write(OUT/'ledger.json',rt.ledger);print(job['key'],len(used),'choices',flush=True)
    except Exception as e:rt.ledger['stop_reason']=f'{type(e).__name__}: {e}';raise
    finally:
        rt.ledger['allocated_output_tokens']=rt.ledger['generation_requests']
        rt.close()
if __name__=='__main__':main()
