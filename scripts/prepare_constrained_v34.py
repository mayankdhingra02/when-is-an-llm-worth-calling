"""Bind already measured runtime-only actions; never parse new size outcomes."""
import hashlib,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,lines,digest,now
from escalation.larger_v22 import MODEL_ID,REVISION,require

def prepare():
    manifest=read('data/manifest_v8.json');jobs=read('data/larger_probe_v22.json')['jobs']
    requests=lines('results/v22_larger/requests.jsonl');cases=[];inputs=set()
    receipt=read('artifacts/study_v33/model_provenance_replay.json')
    require(receipt['verified'] and receipt['request_token_and_provenance_replays']==60,'Provenance replay')
    for case in manifest['cases']:
        if case['dataset'] not in ('brotli','lrzip'):continue
        key=f"{case['dataset']}_{case['seed']}";prefix_path=f'results/v6/prefixes/{key}.json'
        prefix=read(prefix_path);require(digest(prefix['state'])==case['prefix_hash'],'Prefix identity')
        selected={};provenance={};inputs.add(prefix_path)
        for mode,path in [('static_rank',f'results/v8/static_rank/{key}.json'),('runtime_3nn',f'results/v29_neighbors/arms/{key}_sequential_3nn.json')]:
            state=read(path)['state'];require(state['ids'][:10]==prefix['state']['ids'],'Classical prefix')
            selected[mode]=state['ids'][10:];inputs.add(path)
        require(selected['static_rank']==case['pool']['ranked'][:10],'Static order')
        for condition in ('assigned_ids','reverse_display','reassigned_ids'):
            job=next(j for j in jobs if (j['dataset'],j['seed'],j['condition'])==(case['dataset'],case['seed'],condition))
            req=next(r for r in requests if r['job_id']==job['job_id'])
            require((req['model_id'],req['revision'],req['provider'])==(MODEL_ID,REVISION,'local_transformers'),'Real model identity')
            require(req['messages']==job['messages'] and req['status']=='response' and req['retry']==0,'Original successful prompt')
            require(req['prefix_hash']==case['prefix_hash']==job['prefix_hash'],'Response prefix')
            context={k:v for k,v in job.items() if k!='messages'}
            context.update(namespace='measured_v22',prompt_version='larger_v22',grammar_mode='candidate_order_v19',retry=0)
            require(req['cache_key']==digest({'messages':job['messages'],'model':MODEL_ID,'revision':REVISION,'parameters':req['parameters'],
                'context':context,'parser_projection':'larger_v22','grammar_domains':None,'grammar_mode':'candidate_order_v19'}),'Cache binding')
            path=f"results/v22_larger/arms/{job['job_id']:02d}_llm.json";arm=read(path);inputs.add(path)
            ids=[job['mapping'][s] for s in req['raw_output'].strip().splitlines()]
            require(ids==arm['selected_rows']==arm['state']['ids'][10:],'Raw response maps to saved actions')
            mode='cached_llm_'+condition;selected[mode]=ids
            provenance[mode]={k:req[k] for k in ('job_id','request_id','cache_key','prompt_hash','model_id','revision','provider','input_tokens','output_tokens','wall_seconds')}
        for ids in selected.values():
            require(len(ids)==len(set(ids))==10 and set(ids)<=set(case['pool']['ranked']),'Ten shortlist choices')
        inputs.add(f'results/v12_controls/joint_3nn/{key}.json')
        cases.append({'dataset':case['dataset'],'seed':case['seed'],'original_prefix_hash':case['prefix_hash'],
            'prefix_path':prefix_path,'pool':case['pool']['ranked'],'selected':selected,'provenance':provenance})
    specs=[d for d in manifest['datasets'] if d['id'] in ('brotli','lrzip')]
    require(len(cases)==10 and len(specs)==2,'Two fixed families, five seeds')
    for d in specs:
        inputs.add(d['path']);inputs.update(str(p) for p in Path(d['path']).parent.glob('*README*'))
    inputs.update(['data/manifest_v8.json','data/larger_probe_v22.json','results/v22_larger/requests.jsonl','artifacts/study_v33/model_provenance_replay.json'])
    return {'scope':'exploratory evaluation of unchanged runtime-only cached actions under acquired-prefix size cap',
        'datasets':specs,'cases':cases,'new_vector_cap':800,'stage_seconds_cap':120,
        'source_sha256':{p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in sorted(inputs)}}

if __name__=='__main__':
    require(not Path('data/constrained_v34.json').exists(),'Preserve prepared inputs')
    write('data/constrained_v34.json',prepare());print('Bound 10 prefixes and 30 real cached selections; no new labels or inference.')
