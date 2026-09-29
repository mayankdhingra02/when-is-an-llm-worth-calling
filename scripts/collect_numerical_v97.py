"""V97 model collection; no native solver/objective evaluator imports."""
import time
from runtime_qwen_v91 import ROOT, Runtime, rss
from collect_smollm_v47 import read,write,append,now,sha,grammar,IDS
from escalation.qwen_v91 import validate_response
OUT=ROOT/'results/v97_qwen'

def main():
    cfg=read(ROOT/'configs/study_v97.json')
    assert cfg['allow_paid_api'] is False and cfg['max_external_spend_usd']==0 and cfg['new_generation_request_cap']==50
    for n,h in read(ROOT/'reports/protocol_v97.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)
    jobs=read(ROOT/'artifacts/study_v97/jobs.json')
    assert len(jobs)==5 and len({j['key'] for j in jobs})==5
    for job in jobs:assert sha(ROOT/job['prefix'])==job['prefix_sha256']
    rss(-1)
    if OUT.exists():raise ValueError('No implicit restart')
    OUT.mkdir();rt=Runtime(OUT,cfg)
    try:
        rt.start()
        tokens={c:rt.api('/tokenize',{'content':c,'add_special':False})['tokens'] for c in IDS+'\n'}
        assert all(len(t)==1 for t in tokens.values()) and len({t[0] for t in tokens.values()})==21
        write(OUT/'choice_tokenization.json',tokens)
        prepared=[]
        for job in jobs:
            p=read(ROOT/job['prefix'])
            rendered=rt.api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}})
            ids=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens']
            assert len(ids)+20<=4096
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],'rendered':rendered,'prompt_tokens':ids})
            prepared.append((job,rendered['prompt']))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,prompt in prepared:
            used=[];started=time.monotonic();failure=None
            for step in range(10):
                payload={'prompt':prompt+''.join(c+'\n' for c in used),'n_predict':1,'temperature':0,'seed':11,
                         'grammar':grammar(used),'cache_prompt':bool(step),'return_tokens':True,'stream':False,'repeat_penalty':1.0}
                identity=f"{job['key']}_{step}";start=time.monotonic()
                try:
                    response=rt.generate(payload,'scientific',identity)
                    append(OUT/'responses.jsonl',{'request_id':identity,'case':job['key'],'step':step,'at':now(),
                        'response':response,'wall_seconds':time.monotonic()-start})
                    used.append(validate_response(response,used))
                except Exception as e:
                    failure=repr(e);append(OUT/'errors.jsonl',{'request_id':identity,'error':failure,'at':now()});break
            write(OUT/'choices'/f"{job['key']}.json",{**job,'selected_ids':used,'failure':failure,
                'status':'completed' if len(used)==10 else 'fallback','case_seconds':time.monotonic()-started})
            print(job['key'],len(used),'choices',flush=True)
            if rt.reason or rt.proc.poll() is not None or failure:break
    finally:rt.close()
if __name__=='__main__':main()
