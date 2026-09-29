"""Prepare reviewable prompts from actual V8 provenance; tokenizer only, no model."""
import hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,lines,digest
from escalation.order_probe_v19 import transform,CONDITIONS
from escalation.resources import Resources

def main():
    if Path('data/order_probe_v19.json').exists():raise RuntimeError('Prepared inputs retained; no overwrite')
    baseline=read('artifacts/resource_ledger_v2.json');assert baseline['active_since'] is None and baseline['requests']==128
    with Resources({'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}},'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        from transformers import AutoTokenizer
        from escalation.grammar_v8 import CandidateIDGrammar
        model=read('artifacts/model_manifest.json');base=Path('models/Qwen2.5-0.5B-Instruct')
        # Verify tokenizer/config provenance. Weight provenance is checked by the real provider at launch.
        for f in model['files']:
            if not f['file'].endswith('.safetensors'):assert hashlib.sha256((base/f['file']).read_bytes()).hexdigest()==f['sha256']
        tok=AutoTokenizer.from_pretrained(base,local_files_only=True,trust_remote_code=False)
        manifest=read('data/manifest_v8.json');requests=lines('results/v8/requests.jsonl');families=manifest['datasets']
        assert len(families)==3 and all(d['split']=='development' for d in families)
        cases=[]
        for d in families:
            case=next(c for c in manifest['cases'] if c['dataset']==d['id'] and c['seed']==11)
            request=next(q for q in requests if q['dataset']==d['id'] and q['seed']==11)
            assert digest(request['messages'])==case['prompt_sha256'] and request['prefix_hash']==case['prefix_hash']
            cases.append((d,case,request))
        jobs=[];grammar=CandidateIDGrammar(tok)
        assert len(grammar.schedule)==20 and len(grammar.choice_positions)==10
        for round_id in range(3):
            for index,(d,case,request) in enumerate(cases):
                condition=CONDITIONS[(round_id+index)%3];treatment=transform(request['messages'],case['pool'],condition)
                prompt=tok.apply_chat_template(treatment['messages'],tokenize=False,add_generation_prompt=True)
                n=len(tok(prompt)['input_ids']);assert n+20<=32768
                jobs.append(dict(job_id=len(jobs),dataset=d['id'],system_group=d['system_group'],seed=11,condition=condition,split='development',prefix_hash=case['prefix_hash'],original_pool=case['pool'],source_request_id=request['request_id'],input_tokens=n,prompt_hash=digest(treatment['messages']),**treatment))
        write('data/order_probe_v19.json',{'scope':'prepared_only_no_model_outputs; post-v8 exploratory mechanism probe','jobs':jobs,'intended_requests':9,'expected_output_tokens_each':20,'new_objective_acquisitions':0})
        write('artifacts/study_v19/tokenizer_preflight.json',{'passed':True,'prepared_prompts':9,'input_tokens':[j['input_tokens'] for j in jobs],'grammar_choices':10,'allowed_choices_per_position':[20-i for i in range(10)],'new_model_calls':0})
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==baseline['requests']==128
    write('artifacts/study_v19/preparation_accounting.json',{'before':baseline['experiment_seconds'],'after':after['experiment_seconds'],'charged_seconds':after['experiment_seconds']-baseline['experiment_seconds'],'remaining_seconds':1800-after['experiment_seconds'],'new_requests':0})
    print('Prepared nine provenance-checked prompts; tokenizer validation only; no model inference.')

if __name__=='__main__':main()
