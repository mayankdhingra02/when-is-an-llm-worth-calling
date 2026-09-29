"""Finite native evaluator supervising the isolated owner-source optimizer."""
import copy,json,os,random,selectors,signal,subprocess,time
from collect_smollm_v47 import ROOT,read,write,sha,now,append
from native_evaluator_v170 import ENGINES,stage,candidate,command,validate
A=ROOT/'artifacts/study_v170';O=ROOT/'results/v170_ezr'
def prepare():
    assert not (A/'freeze.json').exists()
    cfg=read(ROOT/'configs/study_v170.json');jobs=[j for v in [159,163] for j in read(ROOT/f'artifacts/study_v{v}/jobs.json')];tasks=[{'case':j['key'],'engine':j['engine'],'seed':j['seed'],'arm':arm,'prefix':j['prefix'],'prefix_sha256':j['prefix_sha256']} for j in jobs for arm in cfg['new_arms']]
    random.Random(cfg['schedule_seed']).shuffle(tasks);write(A/'plan.json',tasks)
    prior=[s for v in [159,163] for s in read(ROOT/f'results/v{v}_native/selections.json')];assert len(prior)==140;write(A/'prior_selections.json',prior)
    files=['reports/protocol_v170.md','configs/study_v170.json','scripts/ezr_bridge_v169.py','scripts/native_evaluator_v170.py','scripts/collect_ezr_v170.py','scripts/prepare_ezr_v170.py','scripts/app_validation_v163.py','scripts/solver_worker_v157.py','scripts/app_worker_v162.py','tests/synthetic/test_ezr_v170.py','artifacts/study_v170/runtime.json','artifacts/study_v170/plan.json','artifacts/study_v170/prior_selections.json','artifacts/study_v170/preflight_tests.log','artifacts/sources/ezr_ezr.py','artifacts/sources/ezr_LICENSE.md','artifacts/source_manifest.json','results/v159_native/selections.json','results/v163_native/selections.json']
    hashes=read(ROOT/'artifacts/study_v169/freeze.json')['sha256'].copy()
    for v in [159,163]:
        for name in ['freeze.json','inputs.freeze.json']:hashes.update(read(ROOT/f'artifacts/study_v{v}/{name}')['sha256'])
    for f in read(ROOT/'artifacts/study_v160/corpus_files.json'):hashes['.native-v160/search_corpus/'+f['path']]=f['sha256']
    hashes.update({n:sha(ROOT/n) for n in files});rt=read(A/'runtime.json');hashes[rt['path']]=rt['sha256']
    write(A/'freeze.json',{'at':now(),'at_unix':time.time(),'sha256':hashes})
def main():
    cfg=read(ROOT/'configs/study_v170.json');assert cfg['new_model_request_cap']==cfg['new_download_bytes_cap']==cfg['retries']==cfg['external_spend_usd_cap']==0 and not cfg['allow_paid_api'] and not cfg['allow_cloud']
    assert not O.exists()
    for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    O.mkdir();(O/'optimizer_events').mkdir();start=time.monotonic();ledger={'at':now(),'acquisitions':0,'query_training_executions':0,'intended':820,'model_requests':0,'retries':0,'status':'running'};write(O/'ledger.json',ledger)
    cs={e:candidate(e) for e in cfg['engines']};selections=[];bridges=[]
    def budget():
        if time.monotonic()-start>cfg['stage_seconds_cap']-cfg['worker_seconds_cap']-5:raise TimeoutError('Global reserve reached')
    def measure(task,i,phase):
        budget();assert type(i)==int and 0<=i<len(cs[task['engine']]['configs'])
        q=5 if task['engine']=='ripgrep' else 1
        assert ledger['acquisitions']<cfg['new_outcome_cap'] and ledger['query_training_executions']+q<=cfg['query_training_execution_cap']
        ledger['acquisitions']+=1;ledger['query_training_executions']+=q;write(O/'ledger.json',ledger)
        record={'charge':ledger['acquisitions'],'case':task['case'],'engine':task['engine'],'arm':task['arm'],'phase':phase,'row_id':i,'at_unix':time.time(),'status':'started','value':None};path=O/'acquisitions'/f"{record['charge']:03d}.json";write(path,record);t=time.monotonic()
        cmd=command(task['engine'],i,cs[task['engine']])
        try:
            env={k:v for k,v in os.environ.items() if not k.startswith(('POLARS_','XGBOOST_','OMP_'))};env['PYTHONHASHSEED']='16901'
            worker=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=True)
            try:stdout,stderr=worker.communicate(timeout=cfg['worker_seconds_cap'])
            finally:
                if worker.poll() is None:os.killpg(worker.pid,signal.SIGKILL);worker.wait()
            p=subprocess.CompletedProcess(cmd,worker.returncode,stdout,stderr);record.update(command=cmd,returncode=p.returncode,stderr=p.stderr,raw_stdout=p.stdout)
            if p.returncode:raise RuntimeError('Native worker failed')
            raw=json.loads(p.stdout)
            v,status=validate(raw,task['engine'],cs[task['engine']],i);record.update(measurement=v,status=status,value=v['value'])
        except Exception as exc:record.update(status='failed',error=repr(exc));raise
        finally:record['collection_seconds']=time.monotonic()-t;write(path,record)
        return record['value']
    try:
        for task in read(A/'plan.json'):
            budget();p=read(ROOT/task['prefix']);assert sha(ROOT/task['prefix'])==task['prefix_sha256'];body={'raw_features':cs[task['engine']]['raw_features'],'prefix':p,'arm':task['arm']};state=copy.deepcopy(p)
            key=task['case']+'__'+task['arm'];write(O/'optimizer_inputs'/f'{key}.json',body)
            cmd=[read(A/'runtime.json')['path'],str(ROOT/'scripts/ezr_bridge_v169.py')];proc=None;selector=selectors.DefaultSelector();done=None
            with (O/(key+'.stderr.txt')).open('w') as errorlog:
                try:
                    proc=subprocess.Popen(cmd,cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=errorlog,text=True,bufsize=1,start_new_session=True);selector.register(proc.stdout,selectors.EVENT_READ)
                    proc.stdin.write(json.dumps(body)+'\n');proc.stdin.flush()
                    while True:
                        budget()
                        if not selector.select(timeout=60):raise TimeoutError('Optimizer bridge stalled')
                        line=proc.stdout.readline()
                        if not line:raise RuntimeError('Optimizer bridge EOF')
                        message=json.loads(line);append(O/'optimizer_events'/f'{key}.jsonl',message)
                        if message['type']=='complete':done=message['result'];break
                        assert message['type']=='acquire' and len(state['ids'])<17
                        i=message['row_id'];assert i not in state['ids'] and message['trace']['acquired_ids']==state['ids']
                        y=measure(task,i,'search');state['ids'].append(i);state['labels'].append([y]);proc.stdin.write(json.dumps({'row_id':i,'value':y})+'\n');proc.stdin.flush()
                    proc.stdin.close();proc.wait(timeout=5);assert proc.returncode==0 and len(state['ids'])==17 and done['prefix_cache_hits']==p['ids']
                finally:
                    selector.close()
                    if proc is not None and proc.poll() is None:os.killpg(proc.pid,signal.SIGKILL);proc.wait()
                    if proc is not None:bridges.append({'case':task['case'],'arm':task['arm'],'return_code':proc.returncode});write(O/'bridge_exits.json',bridges)
            write(O/'search'/f'{key}.json',{'case':task['case'],'engine':task['engine'],'arm':task['arm'],'state':state,'source_result':done,'source':'unmodified owner acquire with documented checkpoint wrapper'})
            best=min(range(17),key=lambda k:state['labels'][k][0]);selections.append({'case':task['case'],'engine':task['engine'],'arm':task['arm'],'row_id':state['ids'][best],'search_best':state['labels'][best][0],'search_sha256':sha(O/'search'/f'{key}.json')})
            print(key,'17 search labels',flush=True)
        assert ledger['acquisitions']==280
        selections+=read(A/'prior_selections.json');assert len(selections)==180
        write(O/'selections.json',selections);write(O/'selection.freeze.json',{'at_unix':time.time(),'sha256':sha(O/'selections.json')})
        plan=[]
        for block in range(3):
            ids=list(range(180));random.Random(17010+block).shuffle(ids);plan.extend({'block':block,**selections[i]} for i in ids)
        write(O/'validation_plan.json',plan)
        for row in plan:append(O/'validation.jsonl',{**row,'value':measure(row,row['row_id'],'validation')})
        assert ledger['acquisitions']==820 and ledger['query_training_executions']==1640;ledger['status']='completed'
    except Exception as exc:ledger['status']='failed';ledger['error']=repr(exc);raise
    finally:
        ledger.update(finished_at=now(),seconds=time.monotonic()-start);write(O/'ledger.json',ledger)
    write(O/'completion.json',ledger);print('820 new outcomes /1640 query-training executions complete',flush=True)
if __name__=='__main__':main()
