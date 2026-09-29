"""Fail-closed V38 execution; preflight does not import or load the model."""
import argparse,hashlib,sys,time
from fractions import Fraction
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines,append,digest,now
from escalation.config import load_config
from escalation.size_prompt_v38 import authorization_config
from escalation.resources import Resources
from escalation.order_probe_v19 import StageResources,inspect_response
OUT=Path('results/v38_size_prompt');FREEZE=Path('reports/protocol_v38_size_prompt.freeze.json')

def preflight():
    reasons=[];ledger=read('artifacts/resource_ledger_v2.json');cfg=None
    if not FREEZE.exists():reasons.append('Protocol not frozen')
    else:
        for p,h in read(FREEZE)['sha256'].items():
            if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:reasons.append('Frozen input changed: '+p)
        approval=read('configs/authorization_v38.json') if Path('configs/authorization_v38.json').exists() else None
        try:cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'),approval,hashlib.sha256(FREEZE.read_bytes()).hexdigest())
        except PermissionError as e:reasons.append(str(e))
    if ledger['requests']!=200 or ledger['active_since'] is not None:reasons.append('Expected inactive ledger at200calls')
    if 3600-ledger['experiment_seconds']<700:reasons.append('700-second reserve required')
    if OUT.exists():reasons.append('Prior transaction preserved; no restart')
    prompt=read('artifacts/study_v38/prompt_preflight.json')
    if not prompt['validated'] or prompt['prepared_prompts']!=30 or prompt['input_token_max']>4096:reasons.append('Prompt preflight invalid')
    result={'ready':not reasons,'blocked_reasons':reasons,'current_requests':ledger['requests'],'requested_cap':230,'additional_requests':30,
        'runtime_cap_seconds':3600,'remaining_seconds':3600-ledger['experiment_seconds'],'stage_seconds':600,'maximum_new_vectors':300,
        'new_model_calls':0,'new_objective_acquisitions':0}
    write('artifacts/study_v38/execution_preflight.json',result);return cfg,result

def run():
    cfg,pre=preflight()
    if not pre['ready']:print(pre);return 2
    m=read('data/size_prompt_v38.json');prefixes=read('data/arithmetic_v36.json');jobs=m['jobs'];stop=None;count=0
    from escalation.finite_v6 import load_candidates
    from escalation.arithmetic_v36 import Oracle
    before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as base:
        if base.d['requests']!=200 or base.remaining()<700:raise RuntimeError('Reservation changed')
        write(OUT/'started.json',{'at':now(),'approval':read('configs/authorization_v38.json'),'baseline_ledger':before,'intended_requests':30,'intended_vectors':300})
        resource=StageResources(base,600)
        try:
            from escalation.provider_v22 import LargerProvider
            with LargerProvider(cfg,resource,OUT/'requests.jsonl') as provider:
                for job in jobs:
                    ctx=job['context'];resource.check();response=provider.request(job['messages'],ctx)
                    if response['status']!='response':raise RuntimeError(response.get('error','Model failure'))
                    if response['cache_key']!=job['expected_cache_key'] or response['input_tokens']!=job['expected_input_tokens'] or response['rendered_prompt_sha256']!=job['rendered_prompt_sha256']:raise ValueError('Measured prompt/cache mismatch')
                    selected=inspect_response(response['raw_output'],ctx)['selected_rows']
                    case=next(c for c in prefixes['cases'] if (c['dataset'],c['seed'])==(ctx['dataset'],ctx['seed']));p=case['prefix']
                    spec=next(s for s in prefixes['datasets'] if s['id']==ctx['dataset']);candidates=load_candidates(spec)
                    if set(selected)&set(p['ids']) or not set(selected)<=set(case['pool']):raise ValueError('Candidate isolation')
                    oracle=Oracle(spec,candidates,p,lambda e:append(OUT/'acquisitions.jsonl',{**ctx,**e,'at':now()}))
                    ids=p['ids'][:];labels=[y[:] for y in p['labels']];t=time.perf_counter()
                    for i in selected:
                        resource.check()
                        if count>=300:raise RuntimeError('300-vector limit')
                        count+=1;labels.append(oracle.acquire(i));ids.append(i)
                        write(OUT/'checkpoints'/f"{ctx['job_id']:02d}.json",{'ids':ids,'labels':labels})
                    best=min((j for j,y in enumerate(labels) if Fraction(y[1])<=Fraction(p['size_cap'])),key=lambda j:Fraction(labels[j][0]))
                    write(OUT/'arms'/f"{ctx['job_id']:02d}.json",{**ctx,'status':'completed','ids':ids,'labels':labels,'selected_rows':selected,
                        'size_cap':p['size_cap'],'best_row':ids[best],'best_runtime':labels[best][0],'best_size':labels[best][1],
                        'infeasible_new_acquisitions':sum(Fraction(y[1])>Fraction(p['size_cap']) for y in labels[10:]),
                        'actual_new_accesses':oracle.new_accesses,'logical_evaluations':20,'branch_seconds':time.perf_counter()-t})
                    print(ctx['job_id'],ctx['dataset'],ctx['seed'],ctx['condition'],'completed',flush=True)
        except Exception as e:stop=f'{type(e).__name__}: {e}'
        finally:
            statuses=[{'job_id':j['context']['job_id'],'status':'completed' if (OUT/'arms'/f"{j['context']['job_id']:02d}.json").exists() else 'incomplete_or_unattempted'} for j in jobs]
            write(OUT/'progress.json',{'complete':all(r['status']=='completed' for r in statuses),'intended_model_requests':30,'intended_arms':30,'arms':statuses,
                'actual_attempts':len(lines(OUT/'request_starts.jsonl')),'actual_new_vectors':len(lines(OUT/'acquisitions.jsonl')),'stop_reason':stop})
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v38/collection_accounting.json',{'new_requests':after['requests']-before['requests'],'new_vectors':len(lines(OUT/'acquisitions.jsonl')),
        'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'active_since':after['active_since']})
    if stop:raise RuntimeError(stop)
    return 0
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--preflight',action='store_true');args=parser.parse_args()
    if args.preflight:
        _,r=preflight();print(r);raise SystemExit(0 if r['ready'] else 2)
    raise SystemExit(run())
