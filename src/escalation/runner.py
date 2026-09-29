import argparse,sys,time,platform
from pathlib import Path
from .config import load_config
from .data import read_table,Oracle,sha,validate_manifest
from .core import State,initial_state,recommend,features
from .evaluator import evaluate
from .io import read,write,append,now,digest,lines
from .resources import Resources,LimitReached

ROOT=Path(__file__).resolve().parents[2]

def acquire(c,s,o,method,target):
    while len(s.ids)<target:
        i=recommend(c,s,method);s.observe(i,o.acquire(i),c.directions)

def manifest(stage,cfg):
    return {'stage':stage,'started':now(),'python':sys.version,'platform':platform.platform(),'config':cfg,'protocol_sha256':sha('reports/protocol.md'),'data_manifest_sha256':sha('data/manifest.json'),'code_hashes':{str(p.relative_to(ROOT)):sha(p) for p in (ROOT/'src').rglob('*.py')},'requirements_sha256':sha('requirements.lock.txt'),'intended_runs':30 if stage=='classical' else 15,'scope':'descriptive smoke only'}

def classical(cfg):
    out=Path('results/classical');out.mkdir(parents=True,exist_ok=True)
    if (out/'runs.jsonl').exists():raise RuntimeError('refusing overwrite/repeat classical collection')
    datasets=read('data/manifest.json');validate_manifest(datasets);write(out/'manifest.json',manifest('classical',cfg))
    with Resources(cfg) as resources:
        for d in datasets['datasets']:
            c,labels,excluded=read_table(d['path'])
            write(out/f'{d["id"]}_schema.json',{'rows':len(c.x),'excluded_duplicate_source_lines':excluded,'feature_names':c.names,'objective_names':c.objective_names,'system_group':d['system_group']})
            for seed in cfg['seed_list']:
                for method in ['random','ezr_centroid_adapted']:
                    resources.check();t=time.perf_counter();s=initial_state(c,seed);o=Oracle(labels)
                    acquire(c,s,o,method,10);prefix_seconds=time.perf_counter()-t
                    prefix=s.record();z,z_seconds=features(c,s,seed)
                    if method!='random':
                        write(out/f'prefixes/{d["id"]}_{seed}.json',{'dataset':d['id'],'seed':seed,'data_sha256':d['sha256'],'state':prefix,'prefix_hash':digest(prefix),'features':z,'feature_seconds':z_seconds,'prefix_seconds':prefix_seconds})
                    t2=time.perf_counter();acquire(c,s,o,method,20);branch_seconds=time.perf_counter()-t2
                    result={'dataset':d['id'],'system_group':d['system_group'],'split':d['split'],'seed':seed,'method':method,'status':'completed','namespace':'measured','ids':s.ids,'labels':s.labels,'prefix_hash':digest(prefix),'logical_evaluations':len(s.ids),'actual_new_accesses':o.new_accesses,'prefix_seconds':prefix_seconds,'branch_seconds':branch_seconds,'feature_seconds':z_seconds,'requests':0,'input_tokens':0,'output_tokens':0,**evaluate(labels,c.directions,s.ids)}
                    append(out/'runs.jsonl',result);resources.checkpoint()
                    print(d['id'],seed,method,'completed',flush=True)
    write(out/'completed.json',{'completed':now(),'runs':len(lines(out/'runs.jsonl'))})

def paired(cfg):
    from .provider import LocalProvider
    from .llm import continue_llm
    if len(lines('results/classical/runs.jsonl'))!=30:raise RuntimeError('classical gate incomplete')
    gate=read('artifacts/classical_gate.json')
    if not gate['passed']:raise RuntimeError('tests/schema/budget gate missing')
    datasets=read('data/manifest.json');validate_manifest(datasets)
    out=Path('results/paired');out.mkdir(parents=True,exist_ok=True)
    if (out/'runs.jsonl').exists():raise RuntimeError('refusing overwrite paired collection; explicit resume audit required')
    write(out/'manifest.json',manifest('paired',cfg));stop=None
    with Resources(cfg) as resources:
        with LocalProvider(cfg,resources,out/'requests.jsonl') as provider:
            for d in datasets['datasets']:
                c,labels,_=read_table(d['path'])
                for seed in cfg['seed_list']:
                    p=read(f'results/classical/prefixes/{d["id"]}_{seed}.json')
                    if p['data_sha256']!=d['sha256'] or p['prefix_hash']!=digest(p['state']):raise RuntimeError('prefix integrity')
                    s=State(**p['state']);o=Oracle(labels,prefix=p['state']);start=time.perf_counter();events=[]
                    status='blocked' if stop else 'completed'
                    before=resources.d['requests'];req_start=len(lines(out/'requests.jsonl'))
                    if not stop:
                        try:events=continue_llm(c,s,o,provider,{'dataset':d['id'],'seed':seed,'data_hash':d['sha256'],'prefix_hash':p['prefix_hash']},out/f'checkpoints/{d["id"]}_{seed}.json')
                        except LimitReached as e:stop=str(e);status='blocked'
                        except Exception as e:stop=f'{type(e).__name__}: {e}';status='failed'
                    elapsed=time.perf_counter()-start
                    checkpoint=out/f'checkpoints/{d["id"]}_{seed}.json'
                    if not events and checkpoint.exists():
                        saved=read(checkpoint)
                        if saved['context']['prefix_hash']==p['prefix_hash']:events=saved['events']
                    req=lines(out/'requests.jsonl')[req_start:]
                    record={'dataset':d['id'],'system_group':d['system_group'],'split':d['split'],'seed':seed,'method':'local_llm_adapted','namespace':'measured','status':status,'error':stop,'ids':s.ids,'labels':s.labels,'logical_evaluations':len(s.ids),'actual_new_accesses':o.new_accesses,'prefix_hash':p['prefix_hash'],'prefix_seconds':p['prefix_seconds'],'branch_seconds':elapsed,'feature_seconds':p['feature_seconds'],'features':p['features'],'requests':resources.d['requests']-before,'input_tokens':sum(r.get('input_tokens') or 0 for r in req) if all(r.get('input_tokens') is not None for r in req) else None,'output_tokens':sum(r.get('output_tokens') or 0 for r in req) if all(r.get('output_tokens') is not None for r in req) else None,'events':events,**evaluate(labels,c.directions,s.ids)}
                    append(out/'runs.jsonl',record);resources.checkpoint();print(d['id'],seed,status,'requests',record['requests'],flush=True)
    write(out/'completed.json',{'finished':now(),'intended':15,'completed':sum(r['status']=='completed' for r in lines(out/'runs.jsonl')),'stop_reason':stop})

def main():
    import os
    os.chdir(ROOT)
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['classical','paired']);a=parser.parse_args();cfg=load_config()
    expected=Path('reports/protocol.sha256').read_text().strip()
    if sha('reports/protocol.md')!=expected:raise RuntimeError('frozen protocol changed')
    (classical if a.stage=='classical' else paired)(cfg)
if __name__=='__main__':main()
