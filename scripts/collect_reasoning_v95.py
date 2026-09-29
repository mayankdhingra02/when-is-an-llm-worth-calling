"""Real native Qwen outputs, both modes; no objective/evaluator imports."""
import time
from runtime_reasoning_v95 import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,now,sha
from reasoning_v95_common import parse,applied_settings
OUT=ROOT/'results/v95_reasoning'

def main():
    cfg=read(ROOT/'configs/study_v95.json')
    assert cfg['allow_paid_api'] is False and cfg['max_external_spend_usd']==0 and cfg['new_generation_request_cap']==36
    for n,h in read(ROOT/'reports/protocol_v95.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)
    rss(-1)
    if OUT.exists():raise ValueError('No implicit restart')
    OUT.mkdir();rt=Runtime(OUT,cfg)
    try:
        rt.start();prepared=[]
        for job in read(ROOT/'artifacts/study_v95/jobs.json'):
            p=read(ROOT/job['prefix']);thinking=job['mode']=='thinking'
            rendered=rt.api('/apply-template',{'messages':p['messages'],'add_generation_prompt':True,
                        'chat_template_kwargs':{'enable_thinking':thinking}})
            prompt=rendered['prompt'];expected='<think>' if thinking else '</think>'
            assert prompt.rstrip().endswith(expected),repr(prompt[-150:])
            tokens=rt.api('/tokenize',{'content':prompt,'add_special':False,'parse_special':True})['tokens']
            reserve=2048 if thinking else 128
            assert len(tokens)+reserve<=cfg['context_tokens']
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],'rendered':rendered,
                'prompt_tokens':tokens,'prefix_sha256':sha(ROOT/job['prefix']),'output_reserve':reserve})
            prepared.append((job,prompt))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,prompt in prepared:
            thinking=job['mode']=='thinking';start=time.monotonic()
            payload={'prompt':prompt,'n_predict':2048 if thinking else 128,'temperature':.6 if thinking else .7,
                'top_p':.95 if thinking else .8,'top_k':20,'min_p':0.,'presence_penalty':1.5,'repeat_penalty':1.,
                'seed':job['seed'],'stream':False,'cache_prompt':False,'return_tokens':True}
            try:
                response=rt.generate(payload,'scientific',job['key'])
                append(OUT/'responses.jsonl',{'key':job['key'],'at':now(),'response':response,'wall_seconds':time.monotonic()-start})
                applied_settings(response,payload);parsed=parse(response,job['mode'])
                write(OUT/'choices'/f"{job['key']}.json",{**job,'parsed':parsed,'selected_ids':parsed['selected_ids'],
                    'status':'completed' if parsed['valid'] else 'fallback','case_seconds':time.monotonic()-start})
                print(job['key'], 'valid' if parsed['valid'] else parsed['reasons'],response['tokens_predicted'],'tokens',flush=True)
            except Exception as e:
                append(OUT/'errors.jsonl',{'key':job['key'],'at':now(),'error':repr(e),'wall_seconds':time.monotonic()-start})
                write(OUT/'choices'/f"{job['key']}.json",{**job,'selected_ids':[],'status':'request_failure','case_seconds':time.monotonic()-start,'error':repr(e)})
                break
    finally:rt.close()
if __name__=='__main__':main()
