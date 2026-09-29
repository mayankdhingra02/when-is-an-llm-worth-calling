"""Real local model collection with explicit final-answer reserve; no evaluator."""
import time
from runtime_reasoning_v103 import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,now,sha
from reasoning_v102_common import payload,applied_settings,valid_thought,final_prompt,parse_final,END_CONTROL
OUT=ROOT/'results/v119_reasoning'

def main():
    cfg=read(ROOT/'configs/study_v119.json')
    assert cfg['allow_paid_api'] is False and cfg['max_external_spend_usd']==0
    assert cfg['new_generation_request_cap']==5 and cfg['max_allocated_output_tokens']==640
    for n,h in read(ROOT/'reports/protocol_v119.freeze.json')['sha256'].items():
        if sha(ROOT/n)!=h:raise ValueError('Changed frozen input '+n)
    assert read(ROOT/'artifacts/study_v119/classical_verification.json')['verified'] is True
    for n,h in read(ROOT/'artifacts/study_v119/model_inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    model=read(ROOT/'artifacts/study_v91/model_manifest.json')
    assert sha(ROOT/model['path'])==model['sha256']
    assert len(read(ROOT/'artifacts/study_v119/jobs.json'))==5
    rss(-1);OUT.mkdir(exist_ok=False);(OUT/'responses.jsonl').touch();rt=Runtime(OUT,cfg)
    try:
        rt.start();prepared=[]
        for job in read(ROOT/'artifacts/study_v119/jobs.json'):
            p=read(ROOT/job['prefix']);base=rt.api('/apply-template',{'messages':p['messages']})
            assert base['prompt'].endswith('<|im_start|>assistant\n')
            scaffold='<think>\n' if job['mode']=='thinking' else '<think>\n\n</think>\n\n'
            prompt=base['prompt']+scaffold
            ids=rt.api('/tokenize',{'content':prompt,'add_special':False,'parse_special':True})['tokens']
            assert len(ids)+128+128+16<=cfg['context_tokens']
            write(OUT/'preflight'/f"{job['key']}.json",{**job,'messages':p['messages'],
                'rendered':{'base_template':base,'prompt':prompt,'explicit_control_scaffold':scaffold},
                'prompt_tokens':ids,'prefix_sha256':sha(ROOT/job['prefix'])})
            prepared.append((job,prompt))
        write(OUT/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((OUT/'preflight').glob('*.json'))}})
        for job,prompt in prepared:
            start=time.monotonic();key=job['key'];parsed=None
            def generate(phase,text):
                request=payload(text,job['seed'],job['mode'],phase);t=time.monotonic()
                r=rt.generate(request,'scientific',key+'_'+phase)
                append(OUT/'responses.jsonl',{'key':key+'_'+phase,'case':key,'phase':phase,
                    'at':now(),'response':r,'wall_seconds':time.monotonic()-t})
                applied_settings(r,request)
                return r
            try:
                if job['mode']=='thinking':
                    thought=generate('thought',prompt)
                    if not valid_thought(thought):
                        write(OUT/'choices'/f'{key}.json',{**job,'selected_ids':[],'status':'fallback',
                            'reason':'invalid_thought_phase','case_seconds':time.monotonic()-start})
                        print(key,'invalid thought phase',flush=True);continue
                    prompt=final_prompt(prompt,thought)
                    ids=rt.api('/tokenize',{'content':prompt,'add_special':False,'parse_special':True})['tokens']
                    assert len(ids)+128<=cfg['context_tokens']
                    write(OUT/'final_prompts'/f'{key}.json',{'prompt':prompt,'prompt_tokens':ids,
                        'appended_control':END_CONTROL,'control_is_model_output':False,
                        'first_response_key':key+'_thought'})
                result=generate('final',prompt);parsed=parse_final(result)
                write(OUT/'choices'/f'{key}.json',{**job,'parsed':parsed,'selected_ids':parsed['selected_ids'],
                    'status':'completed' if parsed['valid'] else 'fallback','case_seconds':time.monotonic()-start})
                print(key,'valid' if parsed['valid'] else parsed['reasons'],flush=True)
            except Exception as e:
                append(OUT/'errors.jsonl',{'key':key,'at':now(),'error':repr(e)})
                write(OUT/'choices'/f'{key}.json',{**job,'selected_ids':[],'status':'request_failure',
                    'case_seconds':time.monotonic()-start,'error':repr(e)})
                break
    finally:rt.close()

if __name__=='__main__':main()
