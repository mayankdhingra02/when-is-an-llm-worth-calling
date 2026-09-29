"""Retokenize recorded prompts and replay output grammar; no model loading."""
import hashlib,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
from escalation.io import read,write,lines,digest
from escalation.resources import Resources
from escalation.transfer_v41 import current_config
from escalation.grammar_v8 import CandidateIDGrammar

def main():
    if not read('results/v41_models/progress.json')['complete']:raise ValueError('Full denominator required')
    before=read('artifacts/resource_ledger_v2.json');records=[]
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        resource.check()
        from transformers import AutoTokenizer
        for size in ('0.5','1.5'):
            tokenizer=AutoTokenizer.from_pretrained(f'models/Qwen2.5-{size}B-Instruct',local_files_only=True,trust_remote_code=False)
            grammar=CandidateIDGrammar(tokenizer);requests=lines(f'results/v41_models/{size}/requests.jsonl')
            if len(requests)!=30:raise ValueError('Request denominator')
            for r in requests:
                resource.check()
                if r['status']!='response':
                    records.append({'request_id':r['request_id'],'token_replay':'unavailable_failed_request'});continue
                text=tokenizer.apply_chat_template(r['messages'],tokenize=False,add_generation_prompt=True)
                if hashlib.sha256(text.encode()).hexdigest()!=r['rendered_prompt_sha256']:raise ValueError('Prompt template changed')
                if len(tokenizer(text)['input_ids'])!=r['input_tokens']:raise ValueError('Input token count')
                generated=r['generated_token_ids']
                if len(generated)!=r['output_tokens'] or len(generated)>20:raise ValueError('Output count/cap')
                if tokenizer.decode(generated,skip_special_tokens=True)!=r['raw_output']:raise ValueError('Raw output/token mismatch')
                if grammar.replay(generated)!=r['selection_trace'] or grammar.sha256!=r['grammar_sha256'] or grammar.schedule!=r['grammar_schedule']:raise ValueError('Grammar choice trace')
                context={k:r[k] for k in ('dataset','system_group','seed','model_size','namespace','prefix_hash','grammar_mode','prompt_version')}
                expected=digest({'messages':r['messages'],'model':r['model_id'],'revision':r['revision'],'parameters':r['parameters'],
                    'context':context,'parser_projection':r['prompt_version'],'grammar_domains':None,'grammar_mode':r['grammar_mode']})
                if expected!=r['cache_key']:raise ValueError('Request provenance/cache key')
                records.append({'request_id':r['request_id'],'token_replay':'verified','input_tokens':r['input_tokens'],'output_tokens':r['output_tokens']})
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/token_replay.json',{'intended_requests':60,'records':records,'seconds':after['experiment_seconds']-before['experiment_seconds'],
        'new_model_requests':0,'new_objective_acquisitions':0,'model_logits_recomputed':False,'scope':'Saved raw output/prompt/grammar provenance, not independent inference replication'})
    print('Replayed',sum(r['token_replay']=='verified' for r in records),'recorded tokenizer/grammar traces')
if __name__=='__main__':main()
