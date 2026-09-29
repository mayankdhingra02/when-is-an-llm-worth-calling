"""Real Qwen3 decoder diagnostic, with the inherited local watchdog."""
import time
from runtime_decoder_v93b import ROOT, Runtime, rss
from collect_smollm_v47 import read, write, append, now, sha, grammar, IDS
from decoder_v93b_common import parse_native, validate
from escalation.qwen_v91 import validate_response
OUT=ROOT/'results/v93b_decoder';ART=ROOT/'artifacts/study_v93'

def main():
    cfg=read(ROOT/'configs/study_v93b.json');validate(cfg)
    for n,h in read(ROOT/'reports/protocol_v93b_decoder.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)
    oldledger=read(ROOT/'results/v92b_sensitivity/ledger.json')
    assert oldledger['completed_cases']==108 and oldledger['server_exit_code']==0
    stopped=read(ROOT/'results/v93_decoder/ledger.json')
    assert stopped['generation_requests']==67 and stopped['resource_stop_reason']=='server_rss_cap' and stopped['stage_seconds']+cfg['max_generation_stage_seconds']<1800
    starts=[__import__('json').loads(x) for x in (ROOT/'results/v93_decoder/request_starts.jsonl').read_text().splitlines()]
    attempted={x['case'] for x in starts}
    remaining=read(ROOT/'artifacts/study_v93/remaining_jobs.json')
    original=read(ROOT/'artifacts/study_v93/jobs.json')
    assert remaining==[j for j in original if j['key'] not in attempted]
    assert sum(1 if j['decoder']=='native' else 10 for j in remaining)==77
    rss(-1)
    if OUT.exists():raise ValueError('No implicit restart')
    OUT.mkdir();rt=Runtime(OUT,cfg);rt.ledger.update(completed_cases=0,valid_cases=0,objective_accesses=0,generated_tokens=0)
    try:
        rt.start();prepared=[]
        for job in read(ROOT/'artifacts/study_v93/remaining_jobs.json'):
            p=read(ROOT/job['prefix']);rendered=rt.api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
            ids=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens']
            old=read(ROOT/'results/v92b_sensitivity/preflight'/f"{job['source_key']}.json")
            assert p['messages']==old['messages'] and rendered['prompt']==old['rendered']['prompt'] and ids==old['prompt_tokens']
            if len(ids)+(128 if job['decoder']=='native' else 20)>cfg['context_tokens']:raise ValueError('Context overflow')
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],'rendered':rendered,'prompt_tokens':ids,'prefix_hash':p['prefix_hash']});prepared.append((job,p,rendered['prompt']))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,p,prompt in prepared:
            used=[];request_ids=[];parsed=None;case_start=time.monotonic()
            for step in range(1 if job['decoder']=='native' else 10):
                payload={'prompt':prompt+''.join(c+'\n' for c in used),'n_predict':128 if job['decoder']=='native' else 1,'temperature':0,'seed':11,'cache_prompt':bool(step),'return_tokens':True,'stream':False,'repeat_penalty':1.0}
                if job['decoder']=='forced':payload['grammar']=grammar(used)
                identity=f"{job['key']}_{step}";request_ids.append(identity)
                request={'request_id':identity,'case':job['key'],'step':step,'at':now(),'payload':payload};append(OUT/'request_starts.jsonl',request);t=time.monotonic()
                try:response=rt.generate(payload,'scientific',identity)
                except Exception as e:
                    append(OUT/'errors.jsonl',{'request_id':identity,'error':repr(e),'at':now(),'wall_seconds':time.monotonic()-t});raise
                append(OUT/'responses.jsonl',{**request,'response':response,'wall_seconds':time.monotonic()-t})
                assert 0<=response['tokens_predicted']<=payload['n_predict']
                rt.ledger['generated_tokens']+=response['tokens_predicted']
                assert rt.ledger['generated_tokens']<=cfg['max_generated_tokens']
                if job['decoder']=='native':
                    parsed=parse_native(response['content'],response.get('truncated',False) or response.get('stopped_limit',False) or response.get('stop_type')=='limit');used=parsed['selected_ids']
                else:
                    try:used.append(validate_response(response,used))
                    except ValueError:
                        parsed={'valid':False,'selected_ids':[],'reasons':['invalid_forced_id']};break
            if parsed is None:parsed={'valid':len(used)==10,'selected_ids':used,'reasons':[]}
            write(OUT/'choices'/f"{job['key']}.json",{**job,**parsed,'request_ids':request_ids,'case_seconds':time.monotonic()-case_start,'prefix_hash':p['prefix_hash'],'status':'valid' if parsed['valid'] else 'invalid'})
            rt.ledger['completed_cases']+=1;rt.ledger['valid_cases']+=parsed['valid'];write(OUT/'ledger.json',rt.ledger)
            print(job['key'],'valid' if parsed['valid'] else parsed['reasons'],flush=True)
    except Exception as e:rt.ledger['stop_reason']=f'{type(e).__name__}: {e}';raise
    finally:rt.close()

if __name__=='__main__':main()
