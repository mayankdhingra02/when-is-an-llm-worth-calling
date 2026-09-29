"""Fail-closed actual local-model probe. Authorization checked before model loading."""
import argparse,hashlib,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.config import load_config
from escalation.io import read,write,lines,now,digest
from escalation.nonmonotone_v21 import authorization_config
from escalation.order_probe_v19 import StageResources,inspect_response
from escalation.resources import Resources
OUT=Path('results/v21_nonmonotone')

def preflight():
    auth=read('configs/authorization_v21.json');ledger=read('artifacts/resource_ledger_v2.json');reasons=[]
    try:cfg=authorization_config(load_config('configs/followup_v3.yaml'),auth)
    except (ValueError,PermissionError) as error:cfg=None;reasons.append(str(error))
    if ledger['active_since'] is not None:reasons.append('Ledger active')
    if 1800-ledger['experiment_seconds']<22:reasons.append('Need22 seconds remaining for14-second work stage plus cleanup/analysis reserve')
    if cfg and cfg['inference']['max_new_model_requests']-ledger['requests']<3:reasons.append('Need full three-request reservation')
    if (OUT/'started.json').exists():reasons.append('Started/completed probe retained; no automatic rerun')
    result={'ready':not reasons,'blocked_reasons':reasons,'intended_requests':3,'requests_used':ledger['requests'],'authorized_cap':140 if cfg else 137,'remaining_runtime_seconds':1800-ledger['experiment_seconds'],'new_model_calls':0}
    write('artifacts/study_v21/preflight.json',result);return cfg,result

def run():
    cfg,check=preflight()
    if not check['ready']:print(check);return 2
    for p,h in read('reports/protocol_v21_nonmonotone.freeze.json')['sha256'].items():
        if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise ValueError('Frozen input changed:'+p)
    jobs=read('data/nonmonotone_probe_v21.json')['jobs'];assert len(jobs)==3
    for job in jobs:assert digest(job['messages'])==job['prompt_hash']
    write(OUT/'started.json',{'at':now(),'authorization':read('configs/authorization_v21.json'),'baseline_ledger':read('artifacts/resource_ledger_v2.json'),'intended':3})
    stop=None;completed={}
    try:
        with Resources(cfg,'artifacts/resource_ledger_v2.json') as base:
            bounded=StageResources(base,14)
            from escalation.provider_v19 import OrderProbeProvider
            provider=OrderProbeProvider(cfg,bounded,OUT/'requests.jsonl')
            try:
                with provider:
                    for job in jobs:
                        bounded.check()
                        response=provider.request(job['messages'],{k:v for k,v in dict(job,namespace='measured_nonmonotone_v21',prompt_version='nonmonotone_v21',grammar_mode='candidate_order_v19',retry=0).items() if k not in ['messages']})
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
        write(OUT/'progress.json',{'intended':3,'completed':sum(r['status']=='completed' for r in completed.values()),'cases':[completed.get(j['job_id'],{'job_id':j['job_id'],'dataset':j['dataset'],'condition':j['condition'],'status':'unattempted','reason':stop}) for j in jobs],'request_attempts':len(lines(OUT/'request_starts.jsonl')),'stop_reason':stop,'new_objective_acquisitions':0})
    print(read(OUT/'progress.json'));return 1 if stop else 0

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preflight',action='store_true');args=p.parse_args()
    if args.preflight:
        _,check=preflight();print(check);raise SystemExit(0 if check['ready'] else 2)
    raise SystemExit(run())
