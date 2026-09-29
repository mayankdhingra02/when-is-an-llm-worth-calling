"""Serial charged live trials with stage/global deadlines and durable evidence."""
import hashlib,json,sys,time
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.live_compression_v15 import schedule,isolated_trial
from escalation.resources import Resources


def read(path):return json.loads((ROOT/path).read_text())
def write(path,value):
    path=ROOT/path;path.parent.mkdir(parents=True,exist_ok=True)
    temp=path.with_suffix(path.suffix+'.tmp');temp.write_text(json.dumps(value,indent=2)+'\n');temp.replace(path)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def stamp():return datetime.now(timezone.utc).isoformat()
def append(path,value):
    import os
    with (ROOT/path).open('a') as stream:
        stream.write(json.dumps(value)+'\n');stream.flush();os.fsync(stream.fileno())


def main():
    config=read('configs/live_measurement_v15.json');out=Path('results/v15_measurements')
    if (ROOT/out/'complete.json').exists():
        print('Completed dataset retained; no repeat collection.');return
    if (ROOT/out/'started.json').exists():raise RuntimeError('Started run exists; requires explicit audit, no automatic retry')
    for name,expected in read('reports/protocol_v15_live.freeze.json')['sha256'].items():assert sha(ROOT/name)==expected,name
    environment=read('artifacts/study_v15/environment.json')
    for name,expected in environment['sha256'].items():assert sha(name)==expected,name
    workload=read('artifacts/study_v15/workload_manifest.json')
    assert sha(ROOT/workload['workload_path'])==workload['workload_sha256']
    before=read('artifacts/resource_ledger_v2.json')
    if before.get('active_since') is not None:raise RuntimeError('Ledger indicates active experiment')
    if 1800-before['experiment_seconds']<config['stage_wall_seconds']+5:raise RuntimeError('Insufficient remaining allowance for bounded stage')
    assert before['requests']==128 and not config['allow_model_calls']
    trials=schedule(config['repetitions']);assert len(trials)==config['intended_physical_trials']
    (ROOT/out).mkdir(parents=True,exist_ok=True)
    write('artifacts/study_v15/baseline_ledger.json',before)
    write(out/'schedule.json',trials)
    write(out/'started.json',{'at':stamp(),'intended_trials':len(trials),'source_freeze':'reports/protocol_v15_live.freeze.json'})
    resource_config={'resources':{'max_experiment_runtime_minutes':30},'inference':{'max_new_model_requests':128}}
    results=[];stop='completed'
    with Resources(resource_config,ROOT/'artifacts/resource_ledger_v2.json') as resource:
        stage_start=time.monotonic()
        for trial in trials:
            allowed=min(config['trial_timeout_seconds'],config['stage_wall_seconds']-(time.monotonic()-stage_start)-1,resource.remaining()-2)
            if allowed<.1:
                stop='runtime_limit';break
            row={**trial,'started_at':stamp(),'charged_physical_vector':1}
            # Charge/journal every physical attempt before launching the worker.
            append(out/'acquisitions.jsonl',row)
            spec={**trial,'workload_path':workload['workload_path'],'workload_sha256':workload['workload_sha256'],
                  'binary':environment['binary_paths'].get(trial['setting']['family'])}
            started=time.monotonic()
            actual=isolated_trial([sys.executable,'-I',str(ROOT/'scripts/live_worker_v15.py')],json.dumps(spec).encode(),allowed,str(ROOT),{'PATH':'/usr/bin:/bin','LC_ALL':'C'})
            row.update({'finished_at':stamp(),'collection_wall_seconds':time.monotonic()-started,'worker_returncode':actual['returncode'],'stderr':actual['stderr'][:2000]})
            if actual['timed_out']:row['status']='timeout'
            elif actual['returncode']!=0:row['status']='worker_error'
            else:
                try:
                    value=json.loads(actual['stdout'])
                    assert value['roundtrip_equal'] is True and value['decoded_sha256']==workload['workload_sha256']
                    assert value['original_bytes']==workload['workload_bytes'] and value['compression_ns']>0
                    assert sha(ROOT/value['compressed_path'])==value['compressed_sha256']
                    row.update(value);row['status']='ok'
                except (ValueError,KeyError,AssertionError,OSError) as error:
                    row['status']='malformed_result';row['error']=str(error)
            append(out/'trials.jsonl',row);results.append(row)
            write(out/'progress.json',{'intended':len(trials),'attempted':len(results),'ok':sum(r['status']=='ok' for r in results),'failed':sum(r['status']!='ok' for r in results),'unattempted':len(trials)-len(results),'stop_reason':None})
        resource.checkpoint()
        progress={'intended':len(trials),'attempted':len(results),'ok':sum(r['status']=='ok' for r in results),'failed':sum(r['status']!='ok' for r in results),'unattempted':len(trials)-len(results),'stop_reason':stop,'at':stamp()}
        write(out/'progress.json',progress)
        # A terminated stage is retained and never automatically resumed as a new run.
        write(out/'complete.json',progress)
    after=read('artifacts/resource_ledger_v2.json');assert after['requests']==before['requests'] and after['active_since'] is None
    write('artifacts/study_v15/collection_ledger.json',after)
    print(json.dumps(progress,indent=2))


if __name__=='__main__':main()
