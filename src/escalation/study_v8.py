"""Development-only candidate-selection comparison; prior data remain immutable."""
import argparse,fcntl,time
from pathlib import Path
from .io import read,write,append,lines,digest,now
from .data import sha
from .core import State
from .finite_domain import recommend
from .finite_v6 import load_candidates,LazyOracle
from .selection_v8 import messages,shortlist,parse_ids,control_rows,VERSION
from .provider_v8 import SelectionProvider
from .resources import Resources,LimitReached
from .config import load_config

OUT=Path('results/v8')

def run_config():
    from .study_v7 import run_config as prior_config
    cfg=prior_config();a=read('configs/authorization_v8.json')
    if a['granted']:
        if a['request_cap']!=128 or not a.get('user_authorization'):raise ValueError('explicit bounded authorization required')
        cfg['inference']['max_new_model_requests']=128
    elif a['request_cap']!=113:raise ValueError('unapproved cap increase')
    return cfg

def manifest():
    m=read('data/manifest_v8.json')
    if len(m['datasets'])!=3 or any(d['split']!='development' for d in m['datasets']):raise ValueError('development only')
    if len({d['system_group'] for d in m['datasets']})!=3:raise ValueError('duplicate family')
    return m

def verify():
    f=read('reports/protocol_v8.freeze.json')
    for p,h in f['sha256'].items():
        if sha(p)!=h:raise ValueError('frozen input changed: '+p)
    return f

def key(d,seed):return d['id']+'_'+str(seed)

def prefix(d,seed):
    p=read(f'results/v6/prefixes/{key(d,seed)}.json')
    if p['prefix_hash']!=digest(p['state']) or p['data_sha256']!=d['sha256']:raise ValueError('prefix mismatch')
    return p

def outcome_path(d,seed,arm):return OUT/arm/(key(d,seed)+'.json')

def preflight():
    m=manifest();cfg=run_config();ledger=read('artifacts/resource_ledger_v2.json')
    remaining=sum(not outcome_path(d,seed,'llm').exists() for d in m['datasets'] for seed in m['seeds'])
    report={'at':now(),'intended':15,'pending_requests':remaining,'allowed_request_cap':cfg['inference']['max_new_model_requests'],
      'used_requests':ledger['requests'],'available_requests':cfg['inference']['max_new_model_requests']-ledger['requests'],
      'remaining_runtime_seconds':1800-ledger['experiment_seconds'],'external_spend_usd':0,'blocked_reasons':[]}
    if report['available_requests']<remaining:report['blocked_reasons'].append('insufficient authorized request allowance for full development arm')
    if ledger.get('active_since'):report['blocked_reasons'].append('unresolved active ledger')
    if report['remaining_runtime_seconds']<=0:report['blocked_reasons'].append('runtime exhausted')
    report['ready']=not report['blocked_reasons'];write('artifacts/study_v8/preflight.json',report);return report

def branch(d,seed,arm,resources,provider=None):
    path=outcome_path(d,seed,arm);marker=OUT/'starts'/f'{key(d,seed)}_{arm}.json'
    if path.exists():return read(path)
    if marker.exists():raise RuntimeError('interrupted transaction needs journal/response audit; no silent repeat')
    c=load_candidates(d);p=prefix(d,seed);s=State(**p['state']).clone();pool=shortlist(c,s,seed);msg=messages(c,s,pool)
    case=next(r for r in manifest()['cases'] if r['dataset']==d['id'] and r['seed']==seed)
    if digest(msg)!=case['prompt_sha256'] or pool!=case['pool']:raise ValueError('frozen prompt/pool mismatch')
    ctx={'dataset':d['id'],'system_group':d['system_group'],'split':'development','seed':seed,'arm':arm,'namespace':'measured_v8',
      'data_hash':d['sha256'],'prefix_hash':p['prefix_hash'],'pool_hash':digest(pool),'scope':'post-v7 exploratory development candidate selection'}
    write(marker,{**ctx,'at':now()});start=time.perf_counter();response=None;error=None;status='completed'
    if arm in ['uniform_selection','static_rank']:
        proposals=control_rows(pool,seed,arm)
    elif arm=='llm':
        response=provider.request(msg,{**ctx,'prompt_version':VERSION,'grammar_mode':VERSION,'grammar_domains':[list(range(20))],'retry':0})
        try:
            if response['status']!='response':raise ValueError(response.get('error','request failed'))
            proposals=parse_ids(response['raw_output'],pool)
        except Exception as exc:proposals=None;status='fallback';error=str(exc)
    else:raise ValueError('unknown arm')
    oracle=LazyOracle(d,c,prefix=p['state'],journal=lambda e:append(OUT/'acquisitions.jsonl',{**ctx,**e,'at':now()}));events=[]
    while len(s.ids)<20:
        resources.check()
        if proposals is None:i=recommend(c,s);event={'fallback':True}
        else:i=proposals[len(s.ids)-10];event={'fallback':False,'direct_selection':True}
        if i in s.ids:raise ValueError('duplicate acquisition')
        s.observe(i,oracle.acquire(i),c.directions);events.append({'row_id':i,**event})
        write(OUT/'checkpoints'/f'{key(d,seed)}_{arm}.json',{'state':s.record(),'events':events,'context':ctx})
    result={**ctx,'state':s.record(),'events':events,'proposals':proposals,'pool':pool,'status':status,'error':error,'actual_new_accesses':oracle.new_accesses,
      'branch_seconds':time.perf_counter()-start,'request_id':response['request_id'] if response else None}
    write(path,result);print(arm,key(d,seed),status,flush=True);return result

def completion(stop=None):
    m=manifest();intended=[]
    for d in m['datasets']:
        for seed in m['seeds']:
            for arm in ['uniform_selection','static_rank','llm']:
                p=outcome_path(d,seed,arm)
                intended.append({'dataset':d['id'],'seed':seed,'arm':arm,'status':read(p)['status'] if p.exists() else 'blocked','reason':None if p.exists() else stop})
    write(OUT/'progress.json',{'at':now(),'intended':intended,'complete':all(r['status'] in ['completed','fallback'] for r in intended),
      'actual_new_accesses':len(lines(OUT/'acquisitions.jsonl')),'actual_request_attempts':len(lines(OUT/'request_starts.jsonl'))})

def run(phase):
    frozen=verify();m=manifest();cfg=run_config();OUT.mkdir(parents=True,exist_ok=True)
    if phase=='llm':
        check=preflight()
        if check['pending_requests']==0:completion();return 0
        if not check['ready']:
            completion('; '.join(check['blocked_reasons']));print('BLOCKED:',check);return 2
        write(OUT/'authorization_at_inference_start.json',{'at':now(),'authorization':read('configs/authorization_v8.json'),'preflight':check})
        if any(not outcome_path(d,seed,arm).exists() for d in m['datasets'] for seed in m['seeds'] for arm in ['uniform_selection','static_rank']):raise ValueError('execute all controls first')
    if not (OUT/'manifest.json').exists():
        write(OUT/'manifest.json',{'at':now(),'baseline_ledger':read('artifacts/resource_ledger_v2.json'),'protocol_freeze':frozen,
          'intended_new_acquisitions':450,'intended_requests':15,'previous_prefixes_and_baselines_reused':True})
        for p in Path('src/escalation').glob('*.py'):
            dst=OUT/'source_snapshot'/p;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(p.read_bytes())
    stop=None
    with Path('artifacts/resource_ledger.lock').open('a') as global_lock:
        fcntl.flock(global_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if read('artifacts/resource_ledger.json').get('active_since'):raise ValueError('prior ledger active')
        with Resources(cfg,'artifacts/resource_ledger_v2.json') as resources:
            try:
                resources.check()
                if phase=='controls':
                    for d in m['datasets']:
                        for seed in m['seeds']:
                            for arm in ['uniform_selection','static_rank']:branch(d,seed,arm,resources)
                else:
                    # Recheck allowance while holding the shared experiment lock.
                    pending=sum(not outcome_path(d,seed,'llm').exists() for d in m['datasets'] for seed in m['seeds'])
                    if cfg['inference']['max_new_model_requests']-resources.d['requests']<pending:raise LimitReached('request reservation preflight changed')
                    with SelectionProvider(cfg,resources,OUT/'requests.jsonl') as provider:
                        for d in m['datasets']:
                            for seed in m['seeds']:branch(d,seed,'llm',resources,provider)
            except Exception as exc:stop=f'{type(exc).__name__}: {exc}';print('STOP',stop,flush=True)
    completion(stop or ('LLM arm not started' if phase=='controls' else None))
    return 0 if stop is None else 1

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['controls','llm','preflight']);args=p.parse_args()
    raise SystemExit((0 if preflight()['ready'] else 2) if args.phase=='preflight' else run(args.phase))
