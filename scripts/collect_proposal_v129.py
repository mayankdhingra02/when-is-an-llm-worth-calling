"""Bounded real local numeric predictions; never imports objective evaluation."""
import time
from runtime_proposal_v129 import ROOT,Runtime,rss
from collect_smollm_v47 import read,write,append,sha,now
from proposal_v128 import payload,parse,MAX_OUTPUT
from audit_output_capacity_v127 import vocab

def main():
    cfg=read(ROOT/'configs/study_v129.json');assert cfg['new_generation_request_cap']==11 and cfg['max_allocated_output_tokens']==11264 and cfg['allow_paid_api'] is False and cfg['allow_cloud'] is False and cfg['max_external_spend_usd']==cfg['retries']==0
    for path in ['reports/protocol_v129.freeze.json','artifacts/study_v128/inputs.freeze.json']:
        for n,h in read(ROOT/path)['sha256'].items():assert sha(ROOT/n)==h,n
    model=read(ROOT/'artifacts/study_v91/model_manifest.json');assert sha(ROOT/model['path'])==model['sha256'];vocabulary=vocab(ROOT/model['path']);rss(-1);out=ROOT/'results/v129_proposals';out.mkdir(exist_ok=False);(out/'responses.jsonl').touch();rt=Runtime(out,cfg)
    try:
        rt.start();prepared=[]
        for job in read(ROOT/'artifacts/study_v129/jobs.json'):
            msgs=read(ROOT/job['messages_path']);rendered=rt.api('/apply-template',{'messages':msgs,'add_generation_prompt':True,'chat_template_kwargs':{'enable_thinking':False}});tokens=rt.api('/tokenize',{'content':rendered['prompt'],'add_special':False,'parse_special':True})['tokens'];assert len(tokens)+MAX_OUTPUT<=4096
            proof=rt.authorize(payload(rendered['prompt'],job['sampling_seed'],job['domains']),job['domains'],vocabulary,len(tokens))
            write(out/'preflight'/f"{job['key']}.json",{**job,'messages':msgs,'rendered':rendered,'prompt_tokens':tokens,'output_capacity':proof});prepared.append((job,rendered['prompt']))
        write(out/'preflight_seal.json',{'at':now(),'sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted((out/'preflight').glob('*.json'))}})
        for j,prompt in prepared:
            t=time.monotonic()
            try:
                response=rt.generate(payload(prompt,j['sampling_seed'],j['domains']),'scientific',j['key']);append(out/'responses.jsonl',{'key':j['key'],'at':now(),'response':response,'wall_seconds':time.monotonic()-t})
                try:score=parse(response,j['domains']);status='valid';error=None
                except ValueError as e:score=None;status='invalid';error=str(e)
                write(out/'scores'/f"{j['key']}.json",{**j,'score':score,'status':status,'error':error});print(j['key'],status,score,flush=True)
            except Exception as e:
                append(out/'errors.jsonl',{'key':j['key'],'at':now(),'error':repr(e),'seconds':time.monotonic()-t});rt.ledger['stop_reason']=repr(e);break
    finally:rt.close()
if __name__=='__main__':main()
