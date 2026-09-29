"""Versioned follow-up: real format gate, then conditional paired continuations."""
import fcntl,json,random,time,sys
from pathlib import Path
from .config import load_config
from .data import sha,read_table,validate_manifest,Oracle
from .core import Candidates,State,losses,project,recommend
from .io import now,read,write,append,lines,digest
from .resources import Resources,LimitReached
from .provider import LocalProvider,WorkerUnavailable
from .llm import parse
from .evaluator import evaluate

OUT=Path('results/v2');VERSION='compact_binary_v2'

def compact_messages(c,s,collisions):
    scores=losses(s.labels,c.directions)
    history=[{'x':[int(v) for v in c.x[s.ids[j]]],'loss':round(float(scores[j]),5)} for j in sorted(range(len(s.ids)),key=lambda j:-scores[j])]
    body={'feature_order':c.names,'allowed_values':[[int(v) for v in d] for d in c.domains],'observations':history,'avoid':collisions}
    return [{'role':'system','content':'You optimize configurations. Infer useful settings from observed losses. Lower loss is better.'},{'role':'user','content':'Choose two new binary feature arrays in feature_order. Prefer lower predicted loss and avoid observed arrays. Output {"candidates":[[...],[...]]}.\n'+json.dumps(body,separators=(',',':'))}]

def synthetic_fixture(dim):
    rng=random.Random(20260924+dim);xs=[]
    while len(xs)<32:
        row=tuple(rng.randint(0,1) for _ in range(dim))
        if row not in xs:xs.append(row)
    c=Candidates(tuple(f'f{i}' for i in range(dim)),tuple(xs),('synthetic_loss-',),('-',),tuple(range(32)))
    s=State(list(range(32)))
    for i in range(10):s.observe(i,[sum(xs[i])/dim],c.directions)
    return c,s

def feasibility(provider):
    good=True;records=[]
    for dim in [9,16,39]:
        record={'namespace':'synthetic_feasibility_real_inference','dimensions':dim,'status':'blocked' if not good else 'pending','valid':False}
        if good:
            c,s=synthetic_fixture(dim)
            write(OUT/f'feasibility/fixture_{dim}.json',{'namespace':record['namespace'],'candidates':c.__dict__,'observations':s.record()})
            try:
                response=provider.request(compact_messages(c,s,[]),{'namespace':record['namespace'],'dimensions':dim,'stage':'format_gate','prompt_version':VERSION,'grammar_domains':c.domains,'fixture_hash':digest({'x':c.x,'s':s.record()}),'retry':0})
                record['request_id']=response['request_id']
                if response['status']!='response':raise RuntimeError(response.get('error','provider failure'))
                choices=parse(response['raw_output'],c)
                record.update({'status':'completed','valid':True,'proposals':choices,'wall_seconds':response['wall_seconds']})
            except Exception as e:good=False;record.update({'status':'failed','error':f'{type(e).__name__}: {e}'})
        append(OUT/'feasibility/runs.jsonl',record);records.append(record)
        print('format',dim,record['status'],flush=True)
    write(OUT/'feasibility/gate.json',{'passed':good,'intended':3,'valid':sum(r['valid'] for r in records),'at':now()})
    return good

def continuation(c,s,o,provider,context,checkpoint):
    events=[];collisions=[]
    for batch in range(1,6):
        response=provider.request(compact_messages(c,s,collisions),{**context,'batch':batch,'stage':'paired','namespace':'measured','prompt_version':VERSION,'grammar_domains':c.domains,'retry':0})
        if response['status']!='response':raise WorkerUnavailable(response.get('error','provider failed'))
        error=None
        try:proposals=parse(response['raw_output'],c)
        except (ValueError,TypeError) as e:proposals=None;error=str(e)
        append(OUT/'validation.jsonl',{**context,'batch':batch,'request_id':response['request_id'],'valid':proposals is not None,'error':error})
        next_collisions=[]
        for j in range(2):
            if proposals is None:i=recommend(c,s);event={'fallback':True,'distance':None,'projected':False,'duplicate':False,'collision':False}
            else:
                i,event=project(c,s,proposals[j]);event['fallback']=False
                if event['collision']:next_collisions.append([int(v) for v in c.x[event['nearest_seen']]])
            s.observe(i,o.acquire(i),c.directions)
            event.update({'row_id':i,'batch':batch,'request_id':response['request_id']});events.append(event)
            write(checkpoint,{'context':context,'state':s.record(),'events':events})
        collisions=next_collisions
    return events

def paired(provider,manifest):
    stopped=None
    for d in manifest['datasets']:
        c,labels,_=read_table(d['path'])
        for seed in provider.cfg['seed_list']:
            p=read(f'results/classical/prefixes/{d["id"]}_{seed}.json')
            assert p['prefix_hash']==digest(p['state']) and p['data_sha256']==d['sha256']
            s=State(**p['state']);o=Oracle(labels,prefix=p['state']);before=provider.resources.d['requests'];start=time.perf_counter();events=[];status='blocked' if stopped else 'completed'
            context={'dataset':d['id'],'seed':seed,'data_hash':d['sha256'],'prefix_hash':p['prefix_hash']}
            checkpoint=OUT/f'checkpoints/{d["id"]}_{seed}.json'
            if not stopped:
                try:events=continuation(c,s,o,provider,context,checkpoint)
                except Exception as e:stopped=f'{type(e).__name__}: {e}';status='blocked' if isinstance(e,LimitReached) else 'failed'
            if checkpoint.exists():events=read(checkpoint)['events']
            req=[r for r in lines(OUT/'requests.jsonl') if r.get('dataset')==d['id'] and r.get('seed')==seed]
            r={'dataset':d['id'],'system_group':d['system_group'],'split':d['split'],'seed':seed,'method':'local_llm_constrained_v2','namespace':'measured','scope':'exploratory_smoke_v2','status':status,'error':stopped,'ids':s.ids,'labels':s.labels,'logical_evaluations':len(s.ids),'actual_new_accesses':o.new_accesses,'prefix_hash':p['prefix_hash'],'prefix_seconds':p['prefix_seconds'],'feature_seconds':p['feature_seconds'],'features':p['features'],'branch_seconds':time.perf_counter()-start,'requests':provider.resources.d['requests']-before,'input_tokens':sum(v['input_tokens'] for v in req) if all(v['input_tokens'] is not None for v in req) else None,'output_tokens':sum(v['output_tokens'] for v in req) if all(v['output_tokens'] is not None for v in req) else None,'events':events,**evaluate(labels,c.directions,s.ids)}
            append(OUT/'runs.jsonl',r);provider.resources.checkpoint();print(d['id'],seed,status,'requests',r['requests'],flush=True)
    write(OUT/'completed.json',{'intended':15,'completed':sum(r['status']=='completed' for r in lines(OUT/'runs.jsonl')),'stop_reason':stopped,'finished':now()})

def main():
    import os
    os.chdir(Path(__file__).resolve().parents[2]);cfg=load_config('configs/followup_v2.yaml');OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'requests.jsonl').exists():raise RuntimeError('v2 already started; no automatic overwrite or repeat')
    assert sha('reports/protocol_v2.md')==Path('reports/protocol_v2.sha256').read_text().strip()
    manifest=read('data/manifest.json');validate_manifest(manifest)
    write(OUT/'manifest.json',{'started':now(),'protocol_sha256':sha('reports/protocol_v2.md'),'config':cfg,'python':sys.version,'data_manifest_sha256':sha('data/manifest.json'),'code_hashes':{str(p):sha(p) for p in Path('src').rglob('*.py')},'requirements_sha256':sha('requirements.lock.txt'),'prior_collection':'v1 unchanged; reused prefixes/classical labels; all v2 results exploratory','intended_feasibility_calls':3,'conditional_intended_paired_runs':15})
    for p in Path('src').rglob('*.py'):
        target=OUT/'source_snapshot'/p;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(p.read_bytes())
    # Hold the original experiment lock too: v1 analysis/collection cannot overlap v2.
    with Path('artifacts/resource_ledger.lock').open('a') as global_lock:
        fcntl.flock(global_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        prior=read('artifacts/resource_ledger.json')
        if prior['active_since'] is not None:raise RuntimeError('prior session unresolved')
        ledger=Path(cfg['followup']['ledger'])
        if not ledger.exists():write(ledger,{'requests':0,'experiment_seconds':prior['experiment_seconds'],'carried_v1_seconds':prior['experiment_seconds'],'external_spend_usd':0,'sessions':[],'authorization':cfg['followup']['authorization']})
        with Resources(cfg,ledger) as resources:
            with LocalProvider(cfg,resources,OUT/'requests.jsonl') as provider:
                if feasibility(provider):paired(provider,manifest)
                else:write(OUT/'completed.json',{'completed':0,'paired_gate':'failed; paired experiment not started','finished':now()})
if __name__=='__main__':main()
