"""Bounded expanded smoke: durable acquisitions, paired prefixes and sealed policies."""
import argparse,fcntl,json,random,sys,time
from pathlib import Path
import numpy as np
from .io import read,write,append,lines,digest,now
from .data import sha
from .core import State,initial_state,project
from .finite_domain import FiniteCandidates,recommend,uniform_proposals
from .finite_v6 import load_candidates,LazyOracle,features,messages,parse_symbols,VERSION
from .provider_v6 import FiniteProvider
from .resources import Resources,LimitReached
from .config import load_config
from .router import GainRouter,UncertaintyRouter
from .evaluator import evaluate

OUT=Path('results/v6')

def key(d,seed):return d['id']+'_'+str(seed)

def verify_freeze():
    frozen=read('reports/protocol_v6.freeze.json')
    for p,h in frozen['sha256'].items():
        if sha(p)!=h:raise ValueError('freeze mismatch: '+p)
    return frozen

def journal(context):
    return lambda event:append(OUT/'acquisitions.jsonl',{**context,**event,'at':now()})

def advance(c,s,oracle,resources,n=20,method='centroid_nominal',proposals=None):
    events=[]
    while len(s.ids)<n:
        resources.check()
        if proposals is None:i=recommend(c,s,method);event={}
        else:i,event=project(c,s,proposals[len(s.ids)-10])
        s.observe(i,oracle.acquire(i),c.directions);events.append({'row_id':i,**event})
    return events

def classical(d,seed,resources):
    k=key(d,seed);target=OUT/'classical'/f'{k}.json';marker=OUT/'starts'/f'{k}_classical.json'
    if target.exists():return read(target)
    if marker.exists():raise RuntimeError('interrupted classical transaction; audit journal before recovery: '+k)
    write(marker,{'at':now()});start=time.perf_counter();c=load_candidates(d)
    ctx={'dataset':d['id'],'seed':seed,'namespace':'measured_v6'}
    s=initial_state(c,seed);o=LazyOracle(d,c,journal=journal({**ctx,'arm':'prefix'}))
    advance(c,s,o,resources,10);f,ft=features(c,s,seed)
    p={'state':s.record(),'prefix_hash':digest(s.record()),'data_sha256':d['sha256'],'features':f,'feature_seconds':ft,'prefix_seconds':time.perf_counter()-start}
    write(OUT/'prefixes'/f'{k}.json',p)
    arms={}
    for method in ['centroid_nominal','uniform_projection','random']:
        branch=initial_state(c,seed) if method=='random' else s.clone()
        oracle=LazyOracle(d,c,prefix=None if method=='random' else p['state'],journal=journal({**ctx,'arm':method}));t=time.perf_counter()
        proposals=uniform_proposals(c,seed+40000,10) if method=='uniform_projection' else None
        events=advance(c,branch,oracle,resources,method='random' if method=='random' else 'centroid_nominal',proposals=proposals)
        arms[method]={'state':branch.record(),'actual_new_accesses':oracle.new_accesses,'branch_seconds':time.perf_counter()-t,'events':events}
    r={**ctx,'system_group':d['system_group'],'split':d['split'],'prefix_hash':p['prefix_hash'],'features':f,'arms':arms,'status':'completed','actual_new_accesses':50}
    write(target,r);print('classical',k,'completed',flush=True);return r

def gate(provider):
    records=[]
    for dim,mixed in [(4,True),(30,False)]:
        rng=random.Random(606+dim);xs=[]
        while len(xs)<32:
            x=tuple(rng.randrange(3 if mixed else 2) for _ in range(dim))
            if x not in xs:xs.append(x)
        c=FiniteCandidates(tuple('f'+str(i) for i in range(dim)),tuple(xs),('synthetic',),('-',),tuple(range(32)))
        s=initial_state(c,11)
        for i in s.order[:10]:s.observe(i,[1+sum(c.x[i])],c.directions)
        fixture={'namespace':'synthetic_real_inference_v6','candidates':c.__dict__,'state':s.record()}
        write(OUT/'feasibility'/f'{dim}.json',fixture)
        response=provider.request(messages(c,s),{'namespace':'synthetic_real_inference_v6','stage':'format_gate','fixture_hash':digest(fixture),'dimensions':dim,'prompt_version':VERSION,'grammar_mode':VERSION,'grammar_domains':c.domains,'retry':0})
        error=None
        try:
            if response['status']!='response':raise ValueError(response.get('error','failed'))
            parse_symbols(response['raw_output'],c)
        except Exception as exc:error=str(exc)
        records.append({'dimensions':dim,'passed':error is None,'error':error,'request_id':response['request_id']})
        write(OUT/'feasibility/gate.json',{'records':records,'passed':len(records)==2 and all(r['passed'] for r in records)})
        print('format gate',dim,'passed' if error is None else error,flush=True)
        if error:return False
    return True

def paired(d,seed,provider):
    k=key(d,seed);target=OUT/'paired'/f'{k}.json';marker=OUT/'starts'/f'{k}_paired.json'
    if target.exists():return read(target)
    if marker.exists():raise RuntimeError('interrupted paired transaction; audit journal/response before recovery: '+k)
    c=load_candidates(d);p=read(OUT/'prefixes'/f'{k}.json')
    if p['prefix_hash']!=digest(p['state']) or p['data_sha256']!=d['sha256']:raise ValueError('prefix integrity')
    write(marker,{'at':now(),'prefix_hash':p['prefix_hash']});s=State(**p['state']);start=time.perf_counter()
    context={'dataset':d['id'],'seed':seed,'namespace':'measured_v6','split':d['split'],'system_group':d['system_group'],'data_hash':d['sha256'],'prefix_hash':p['prefix_hash'],
      'prompt_version':VERSION,'grammar_mode':VERSION,'grammar_domains':c.domains,'stage':'paired','retry':0}
    o=LazyOracle(d,c,prefix=p['state'],journal=journal({**context,'arm':'local_llm'}));response=provider.request(messages(c,s),context)
    error=None;proposals=None;events=[];status='completed'
    try:
        if response['status']!='response':raise ValueError(response.get('error','request failed'))
        proposals=parse_symbols(response['raw_output'],c)
    except Exception as exc:error=str(exc);status='fallback'
    while len(s.ids)<20:
        provider.resources.check()
        if proposals is None:i=recommend(c,s);event={'fallback':True}
        else:i,event=project(c,s,proposals[len(s.ids)-10]);event['fallback']=False
        s.observe(i,o.acquire(i),c.directions);events.append({'row_id':i,**event})
        write(OUT/'checkpoints'/f'{k}.json',{'state':s.record(),'events':events,'prefix_hash':p['prefix_hash'],'request_id':response['request_id']})
    result={**context,'state':s.record(),'events':events,'request_id':response['request_id'],'status':status,'error':error,'actual_new_accesses':o.new_accesses,
      'branch_seconds':time.perf_counter()-start,'input_tokens':response['input_tokens'],'output_tokens':response['output_tokens'],'request_wall_seconds':response['wall_seconds']}
    write(target,result);print('paired',k,status,flush=True);return result

def retrospective_labels(d,c):
    """Evaluator boundary ONLY; never called by search, prompt or feature functions."""
    import csv
    wanted=set(c.source_ids);ys={}
    with Path(d['path']).open(newline='') as f:
        for line,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
            if line in wanted:ys[line]=[float(row[d['primary_objective']])]
    return [ys[i] for i in c.source_ids]

def outcome_rows(manifest,split):
    result=[]
    for d in manifest['datasets']:
        if not d['selected'] or d['split']!=split:continue
        c=load_candidates(d);ys=retrospective_labels(d,c)
        for seed in manifest['seeds']:
            k=key(d,seed);a=read(OUT/'classical'/f'{k}.json');b=read(OUT/'paired'/f'{k}.json')
            classic=evaluate(ys,c.directions,a['arms']['centroid_nominal']['state']['ids'])['loss'];llm=evaluate(ys,c.directions,b['state']['ids'])['loss']
            result.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'split':split,'features':a['features'],
              'classical_loss':classic,'llm_loss':llm,'gain':classic-llm,'projection_loss':evaluate(ys,c.directions,a['arms']['uniform_projection']['state']['ids'])['loss'],
              'random_loss':evaluate(ys,c.directions,a['arms']['random']['state']['ids'])['loss'],'status':b['status'],'input_tokens':b['input_tokens'],'output_tokens':b['output_tokens'],'request_wall_seconds':b['request_wall_seconds']})
    return result

def fit_and_seal(manifest):
    path=OUT/'router_seal.json'
    if path.exists():return read(path)
    rows=outcome_rows(manifest,'development');r=GainRouter().fit(rows);u=UncertaintyRouter().fit(rows);export=r.export()
    export['evidence']='insufficient for generalization: three development and three held-out families'
    seal={'at':now(),'benefit':export,'uncertainty':{'threshold':None if np.isinf(u.threshold) else float(u.threshold),'rate':u.rate,'curve':u.curve},
      'development_rows_sha256':digest(rows),'development_files':{str(p):sha(p) for folder in ['classical','paired'] for p in (OUT/folder).glob('*.json')},
      'test_outcomes_used':False}
    write(OUT/'development_outcomes.json',rows);write(path,seal);write(OUT/'router_seal.sha256.json',{'sha256':sha(path)});print('router fitted on development and sealed',flush=True);return seal

def run():
    manifest=read('data/manifest_v6.json');frozen=verify_freeze();cfg=load_config('configs/followup_v3.yaml')
    OUT.mkdir(parents=True,exist_ok=True)
    if (OUT/'completed.json').exists():raise RuntimeError('completed run is immutable; use analysis command')
    if not (OUT/'manifest.json').exists():
        write(OUT/'manifest.json',{'started':now(),'protocol_freeze':frozen,'dataset_manifest_sha256':sha('data/manifest_v6.json'),'baseline_ledger':read('artifacts/resource_ledger_v2.json'),
          'intended_pairs':30,'intended_model_requests':32,'scope':manifest['scope'],'python':sys.version})
        for p in Path('src/escalation').glob('*.py'):
            dst=OUT/'source_snapshot'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
    stop=None
    with Path('artifacts/resource_ledger.lock').open('a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if read('artifacts/resource_ledger.json').get('active_since'):raise RuntimeError('prior ledger active')
        with Resources(cfg,'artifacts/resource_ledger_v2.json') as resources:
            try:
                # Classical smoke on all development groups is mandatory before new inference.
                for d in manifest['datasets']:
                    if d['selected'] and d['split']=='development':
                        for seed in manifest['seeds']:classical(d,seed,resources)
                with FiniteProvider(cfg,resources,OUT/'requests.jsonl') as provider:
                    gp=OUT/'feasibility/gate.json'
                    if gp.exists():
                        if not read(gp)['passed']:raise RuntimeError('failed/incomplete gate: no automatic retry')
                    elif not gate(provider):raise RuntimeError('real format gate failed')
                    for split in ['development','test']:
                        if split=='test':
                            fit_and_seal(manifest)
                            if sha(OUT/'router_seal.json')!=read(OUT/'router_seal.sha256.json')['sha256']:raise ValueError('router seal changed')
                        for d in manifest['datasets']:
                            if d['selected'] and d['split']==split:
                                for seed in manifest['seeds']:
                                    classical(d,seed,resources);paired(d,seed,provider)
            except Exception as exc:stop=f'{type(exc).__name__}: {exc}';print('STOP',stop,flush=True)
    intended=[]
    for d in manifest['datasets']:
        if not d['selected']:continue
        for seed in manifest['seeds']:
            p=OUT/'paired'/f'{key(d,seed)}.json'
            intended.append({'dataset':d['id'],'seed':seed,'split':d['split'],'status':read(p)['status'] if p.exists() else 'blocked','reason':None if p.exists() else stop})
    write(OUT/'completed.json',{'at':now(),'intended':intended,'stop_reason':stop,'complete':all(r['status'] in ['completed','fallback'] for r in intended),
      'actual_acquisitions':len(lines(OUT/'acquisitions.jsonl')),'new_model_attempts':len(lines(OUT/'request_starts.jsonl'))})

if __name__=='__main__':run()
