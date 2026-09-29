"""Generate/validate frozen size-aware prompts using acquired labels and local tokenizer only."""
import copy,hashlib,json,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false')
from escalation.io import read,write,lines,digest
from escalation.larger_v22 import MODEL_ID,REVISION
from escalation.size_prompt_v38 import transform
from escalation.finite_v6 import load_candidates,symbols

def main():
    if Path('data/size_prompt_v38.json').exists():raise FileExistsError('Preserve prepared prompts')
    before=Path('artifacts/resource_ledger_v2.json').read_bytes();manifest=read('data/arithmetic_v36.json');old_jobs=read('data/larger_probe_v22.json')['jobs']
    from transformers import AutoTokenizer
    tok=AutoTokenizer.from_pretrained('models/Qwen2.5-1.5B-Instruct',local_files_only=True,trust_remote_code=False)
    model=read('artifacts/model_manifest_v22.json')
    for f in model['files']:
        if f['file'] in ('tokenizer.json','tokenizer_config.json','config.json'):
            assert hashlib.sha256(Path('models/Qwen2.5-1.5B-Instruct',f['file']).read_bytes()).hexdigest()==f['sha256']
    jobs=[];tokens=[]
    for old in old_jobs:
        if old['dataset'] not in ('brotli','lrzip') or old['condition']=='assigned_ids_repeat':continue
        case=next(c for c in manifest['cases'] if (c['dataset'],c['seed'])==(old['dataset'],old['seed']));p=case['prefix']
        spec=next(s for s in manifest['datasets'] if s['id']==old['dataset']);c=load_candidates(spec)
        body=json.loads(old['messages'][-1]['content'].split('\n',1)[1]);assert [o['x'] for o in body['observations']]==[symbols(c,c.x[i]) for i in p['ids']]
        messages=transform(old,p);newbody=json.loads(messages[-1]['content'].split('\n',1)[1])
        assert newbody['candidates']==body['candidates'] and len({r['id'] for r in body['candidates']})==20
        assert [{k:v for k,v in row.items() if k!='output_size'} for row in newbody['observations']]==body['observations']
        assert set(old['mapping'].values())==set(case['pool']) and not set(case['pool'])&set(p['ids'])
        rendered=tok.apply_chat_template(messages,tokenize=False,add_generation_prompt=True);count=len(tok(rendered)['input_ids'])
        assert count<=4096 and digest(messages)!=old['prompt_hash']
        context={'job_id':len(jobs),'source_v22_job_id':old['job_id'],'dataset':old['dataset'],'seed':old['seed'],'system_group':old['system_group'],
            'split':'exposed_development','condition':old['condition'],'prefix_hash':case['prefix_hash'],'v34_prefix_hash':case['v34_prefix_hash'],
            'prompt_hash':digest(messages),'mapping':old['mapping'],'display_ids':old['display_ids']}
        context.update(namespace='measured_v38',prompt_version='size_prompt_v38',grammar_mode='candidate_order_v19',retry=0)
        key=digest({'messages':messages,'model':MODEL_ID,'revision':REVISION,'parameters':{'do_sample':False,'max_new_tokens':20},
            'context':context,'parser_projection':'size_prompt_v38','grammar_domains':None,'grammar_mode':'candidate_order_v19'})
        assert key not in {r['cache_key'] for r in lines('results/v22_larger/requests.jsonl')}
        jobs.append({'context':context,'messages':messages,'expected_cache_key':key,'expected_input_tokens':count,'rendered_prompt_sha256':hashlib.sha256(rendered.encode()).hexdigest()})
        tokens.append({'job_id':context['job_id'],'dataset':old['dataset'],'seed':old['seed'],'condition':old['condition'],'input_tokens':count})
    assert len(jobs)==30 and len({j['context']['prompt_hash'] for j in jobs})==30
    write('data/size_prompt_v38.json',{'scope':'prepared size-aware prompts only; no model responses or experiment result','model_id':MODEL_ID,'revision':REVISION,'jobs':jobs})
    write('artifacts/study_v38/prompt_preflight.json',{'validated':True,'prepared_prompts':30,'cases':10,'systems':2,'local_tokenizer_only':True,
        'input_token_min':min(r['input_tokens'] for r in tokens),'input_token_max':max(r['input_tokens'] for r in tokens),'input_tokens_sum':sum(r['input_tokens'] for r in tokens),
        'input_token_cap':4096,'all_candidate_mappings_unchanged':True,'all_source_runtime_observations_unchanged':True,
        'added_objectives_from_prefix_only':True,'compatible_v22_cache_hits':0,'new_inference':0,'new_objective_acquisitions':0,'records':tokens})
    assert Path('artifacts/resource_ledger_v2.json').read_bytes()==before
    print('Validated30new size-aware prompts with local tokenizer; no inference.')
if __name__=='__main__':main()
