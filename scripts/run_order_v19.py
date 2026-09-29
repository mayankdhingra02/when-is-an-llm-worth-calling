"""Fail-closed actual local-model probe. Authorization checked before model loading."""
import argparse,hashlib,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.config import load_config
from escalation.io import read,write,lines,now,digest
from escalation.order_probe_v19 import authorization_config,StageResources,inspect_response
from escalation.resources import Resources
OUT=Path('results/v19_order_probe')

def preflight():
    auth=read('configs/authorization_v19.json');ledger=read('artifacts/resource_ledger_v2.json');reasons=[]
    try:cfg=authorization_config(load_config('configs/followup_v3.yaml'),auth)
    except (ValueError,PermissionError) as error:cfg=None;reasons.append(str(error))
    if ledger['active_since'] is not None:reasons.append('Ledger active')
    if 1800-ledger['experiment_seconds']<45:reasons.append('Need45 seconds remaining for40-second stage plus reserve')
    if cfg and cfg['inference']['max_new_model_requests']-ledger['requests']<9:reasons.append('Need full nine-request reservation')
    if (OUT/'started.json').exists():reasons.append('Started/completed probe retained; no automatic rerun')
    result={'ready':not reasons,'blocked_reasons':reasons,'intended_requests':9,'requests_used':ledger['requests'],'authorized_cap':137 if cfg else 128,'remaining_runtime_seconds':1800-ledger['experiment_seconds'],'new_model_calls':0}
    write('artifacts/study_v19/preflight.json',result);return cfg,result

def run():
    cfg,check=preflight()
    if not check['ready']:print(check);return 2
    for p,h in read('reports/protocol_v19_order.freeze.json')['sha256'].items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input changed:'+p)
    jobs=read('data/order_probe_v19.json')['jobs'];assert len(jobs)==9
    for job in jobs:assert digest(job['messages'])==job['prompt_hash']
    write(OUT/'started.json',{'at':now(),'authorization':read('configs/authorization_v19.json'),'baseline_ledger':read('artifacts/resource_ledger_v2.json'),'intended':9})
    stop=None;completed={}
    try:
        with Resources(cfg,'artifacts/resource_ledger_v2.json') as base:
            bounded=StageResources(base,40)
            from escalation.provider_v19 import OrderProbeProvider
            provider=OrderProbeProvider(cfg,bounded,OUT/'requests.jsonl')
            try:
                with provider:
                    for job in jobs:
                        bounded.check()
                        response=provider.request(job['messages'],{k:v for k,v in dict(job,namespace='measured_order_probe_v19',prompt_version='order_probe_v19',grammar_mode='candidate_order_v19',retry=0).items() if k not in ['messages']})
                        result={'job_id':job['job_id'],'dataset':job['dataset'],'condition':job['condition'],'request_id':response['request_id'],'status':'failed','new_objective_acquisitions':0}
                        try:
                            if response['status']!='response':raise ValueError(response.get('error','No valid response'))
                            result.update(inspect_response(response['raw_output'],job));result['status']='completed'
                        except ValueError as error:result['error']=str(error)
                        completed[job['job_id']]=result;write(OUT/'outcomes'/f"{job['job_id']:02d}.json",result)
                        if result['status']!='completed':raise RuntimeError('Stop after failed response; no retries or replacement outputs')
            finally:provider.close()
    except Exception as error:stop=f'{type(error).__name__}: {error}'
    finally:
        write(OUT/'progress.json',{'intended':9,'completed':sum(r['status']=='completed' for r in completed.values()),'cases':[completed.get(j['job_id'],{'job_id':j['job_id'],'dataset':j['dataset'],'condition':j['condition'],'status':'unattempted','reason':stop}) for j in jobs],'request_attempts':len(lines(OUT/'request_starts.jsonl')),'stop_reason':stop,'new_objective_acquisitions':0})
    print(read(OUT/'progress.json'));return 1 if stop else 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');args=p.parse_args()
    if args.preflight:
        _,check=preflight();print(check);raise SystemExit(0 if check['ready'] else 2)
    raise SystemExit(run())
