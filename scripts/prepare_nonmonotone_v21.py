"""Tokenize exactly three previously specified designs; no model inference."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import digest
from escalation.resources import Resources

def read(p):return json.loads((ROOT/p).read_text())
def write(p,d):(ROOT/p).write_text(json.dumps(d,indent=2)+'\n')
def main():
    if (ROOT/'data/nonmonotone_probe_v21.json').exists():raise RuntimeError('Prepared inputs retained')
    before=read('artifacts/resource_ledger_v2.json');assert before['requests']==137 and before['active_since'] is None
    if 1800-before['experiment_seconds']<24:raise RuntimeError('Insufficient reserve for preparation and proposed probe')
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':137}},ROOT/'artifacts/resource_ledger_v2.json') as resource:
        from transformers import AutoTokenizer
        from escalation.grammar_v8 import CandidateIDGrammar
        base=ROOT/'models/Qwen2.5-0.5B-Instruct'
        for f in read('artifacts/model_manifest.json')['files']:
            if not f['file'].endswith('.safetensors'):assert hashlib.sha256((base/f['file']).read_bytes()).hexdigest()==f['sha256']
        tokenizer=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False);grammar=CandidateIDGrammar(tokenizer)
        assert len(grammar.schedule)==20
        designs=read('artifacts/study_v20/unexecuted_designs.json')['designs'];originals=read('data/order_probe_v19.json')['jobs'];jobs=[]
        for dataset in ['MySQL','lrzip','brotli']:
            design=next(d for d in designs if d['dataset']==dataset)
            old=next(j for j in originals if j['dataset']==dataset and j['condition']=='original')
            body=json.loads(design['messages'][-1]['content'].split('\n',1)[1]);text=tokenizer.apply_chat_template(design['messages'],tokenize=False,add_generation_prompt=True)
            tokens=len(tokenizer(text)['input_ids']);assert tokens+20<=32768
            jobs.append(dict(old,job_id=len(jobs),condition='nonmonotone_ids',messages=design['messages'],mapping=design['mapping'],display_ids=[c['id'] for c in body['candidates']],input_tokens=tokens,prompt_hash=digest(design['messages'])))
        assert len(jobs)==3
        write('data/nonmonotone_probe_v21.json',{'scope':'prepared_only_no_model_responses; frozen nonmonotone extension','jobs':jobs,'intended_requests':3,'new_objective_acquisitions':0})
        write('artifacts/study_v21/tokenizer_preflight.json',{'passed':True,'input_tokens':[j['input_tokens'] for j in jobs],'output_token_cap_each':20,'new_model_calls':0})
        resource.checkpoint()
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==137 and after['active_since'] is None
    write('artifacts/study_v21/preparation_accounting.json',{'before':before['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'remaining_seconds':1800-after['experiment_seconds'],'new_model_calls':0})
    print('Three nonmonotone prompts tokenizer-checked; no inference.')

if __name__=='__main__':main()
