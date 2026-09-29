"""Bounded fresh physical validation; every attempt journaled before launch."""
import hashlib,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write,now,lines
from escalation.live_compression_v17 import isolated_trial
from escalation.resources import Resources
from escalation.config import load_config
from escalation.larger_v22 import authorization_config,require
OUT=Path('results/v32_reliability')

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def append(p,row):
    with p.open('a') as f:f.write(json.dumps(row)+'\n');f.flush();os.fsync(f.fileno())

def main():
    require(not OUT.exists(),'Refuse restart/overwrite of started campaign')
    for p,h in read('reports/protocol_v32_reliability.freeze.json')['sha256'].items():require(sha(p)==h,'Changed input: '+p)
    m=read('data/reliability_v32.json');env=read('artifacts/study_v15/environment.json');w=read('artifacts/study_v15/workload_manifest.json')
    for p,h in env['sha256'].items():require(sha(p)==h,'Changed executable/library')
    require(sha(w['workload_path'])==w['workload_sha256'],'Workload identity')
    schedule=read('artifacts/study_v32/schedule.json');require(len(schedule)==m['intended_trials'],'Intended trial count')
    expected={s['setting']['config_id']:s for s in m['selected']}
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'))
    before=read('artifacts/resource_ledger_v2.json');require(before['active_since'] is None,'Active ledger')
    results=[];stop='completed'
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        require(resource.remaining()>65,'65-second stage reserve')
        write(OUT/'started.json',{'at':now(),'intended_trials':len(schedule),'baseline_ledger':before})
        started=time.monotonic()
        try:
            for trial in schedule:
                allowed=min(2.,60-(time.monotonic()-started)-1,resource.remaining()-2)
                if allowed<.1:stop='runtime_limit';break
                row={**trial,'started_at':now(),'charged_physical_vector':1,'namespace':'measured_reliability_v32'}
                append(OUT/'acquisitions.jsonl',row)
                spec={**trial,'workload_path':w['workload_path'],'workload_sha256':w['workload_sha256'],
                    'binary':env['binary_paths'].get(trial['setting']['family'])}
                clock=time.monotonic()
                actual=isolated_trial([sys.executable,'-I',str(ROOT/'scripts/live_worker_v32.py')],json.dumps(spec).encode(),allowed,str(ROOT),{'PATH':'/usr/bin:/bin','LC_ALL':'C'})
                row.update(finished_at=now(),collection_wall_seconds=time.monotonic()-clock,worker_returncode=actual['returncode'],stderr=actual['stderr'][:2000])
                if actual['timed_out']:row['status']='timeout'
                elif actual['returncode']!=0:row['status']='worker_error'
                else:
                    try:
                        value=json.loads(actual['stdout']);e=expected[trial['setting']['config_id']]
                        require(value['roundtrip_equal'] and value['decoded_sha256']==w['workload_sha256'],'Roundtrip')
                        require(value['original_bytes']==w['workload_bytes'] and value['compression_ns']>0,'Valid measurement')
                        require(value['compressed_bytes']==e['expected_compressed_bytes'],'Historical size identity')
                        require(value['compressed_sha256']==e['expected_compressed_sha256']==sha(value['compressed_path']),'Historical payload identity')
                        row.update(value);row['status']='ok'
                    except (ValueError,KeyError,AssertionError,OSError,RuntimeError) as exc:
                        row['status']='malformed_or_changed_result';row['error']=str(exc)
                append(OUT/'trials.jsonl',row);results.append(row)
                write(OUT/'progress.json',{'intended':len(schedule),'attempted':len(results),
                    'ok':sum(r['status']=='ok' for r in results),'unattempted':len(schedule)-len(results),'stop_reason':None})
                if row['status']!='ok':stop='trial_failure';break
        except Exception as exc:stop=f'{type(exc).__name__}: {exc}'
        finally:
            acquired=lines(OUT/'acquisitions.jsonl')
            progress={'complete':len(results)==len(schedule) and all(r['status']=='ok' for r in results),
                'intended':len(schedule),'charged_attempts':len(acquired),'results_recorded':len(results),
                'ok':sum(r['status']=='ok' for r in results),'failed':sum(r['status']!='ok' for r in results),
                'missing_results':len(acquired)-len(results),'unattempted':len(schedule)-len(acquired),'stop_reason':stop}
            write(OUT/'progress.json',progress)
    after=read('artifacts/resource_ledger_v2.json');require(after['requests']==before['requests']==200,'No inference')
    write('artifacts/study_v32/collection_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],
        'cumulative_seconds':after['experiment_seconds'],'new_physical_trials':progress['charged_attempts'],
        'new_recorded_optimizer_acquisitions':0,'new_model_calls':0,'active_since':after['active_since']})
    print(json.dumps(progress,indent=2))
    require(progress['complete'],'Incomplete campaign; do not drop failures or retry')

if __name__=='__main__':main()
