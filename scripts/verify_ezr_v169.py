"""Raw-objective validation and zero-acquisition replay of owner-source decisions."""
import copy,json,random,selectors,subprocess,time
from collect_smollm_v47 import ROOT,read,write,sha
from verify_apps_v168 import objective
from report_ezr_v169 import analyze
A=ROOT/'artifacts/study_v169';O=ROOT/'results/v169_ezr';OLD=ROOT/'artifacts/study_v168'
def lines(p):return [json.loads(x) for x in p.read_text().splitlines()]
def main():
    for n,h in read(A/'freeze.json')['sha256'].items():assert sha(ROOT/n)==h,n
    acq=[read(p) for p in sorted((O/'acquisitions').glob('*.json'))];assert len(acq)==410 and [r['charge'] for r in acq]==list(range(1,411))
    assert sum(r['measurement']['native_invocations'] for r in acq)==820
    cs={e:read(OLD/'candidates'/f'{e}.json') for e in ['polars','xgboost']}
    for r in acq:objective(r,cs[r['engine']])
    tasks=read(A/'plan.json');assert len(tasks)==20;total_cached=total_new=0
    for task in tasks:
        key=task['case']+'__'+task['arm'];record=read(O/'search'/f'{key}.json');p=read(ROOT/task['prefix']);assert sha(ROOT/task['prefix'])==task['prefix_sha256']
        body=read(O/'optimizer_inputs'/f'{key}.json');assert body=={'raw_features':cs[task['engine']]['raw_features'],'prefix':p,'arm':task['arm']}
        events=lines(O/'optimizer_events'/f'{key}.jsonl');rr=[r for r in acq if r['case']==task['case'] and r['arm']==task['arm'] and r['phase']=='search'];assert len(rr)==7
        state=copy.deepcopy(p)
        for e,r in zip(events[:7],rr):
            assert e['type']=='acquire' and e['row_id']==r['row_id'] and e['trace']['acquired_ids']==state['ids']
            scores=e['trace']['scores'];assert {x['row_id'] for x in scores}==set(p['order'])-set(state['ids'])
            assert e['row_id']==min(scores,key=lambda x:x['score'])['row_id']
            assert r['row_id'] not in state['ids'];state['ids'].append(r['row_id']);state['labels'].append([r['value']])
        assert record['state']==state and len(events)==8 and events[-1]['type']=='complete' and events[-1]['result']==record['source_result']
        # Real owner source runs again against acquired saved labels only. No native workers.
        cmd=[read(A/'runtime.json')['path'],str(ROOT/'scripts/ezr_bridge_v169.py')]
        proc=subprocess.Popen(cmd,cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1);selector=selectors.DefaultSelector();selector.register(proc.stdout,selectors.EVENT_READ);seen=0
        try:
            proc.stdin.write(json.dumps(body)+'\n');proc.stdin.flush()
            while True:
                assert selector.select(timeout=10),'Replay stalled'
                line=proc.stdout.readline();assert line,'Replay EOF';m=json.loads(line)
                if m['type']=='complete':
                    a=m['result'];b=copy.deepcopy(record['source_result']);a.pop('optimizer_process_cpu_seconds');b.pop('optimizer_process_cpu_seconds');assert a==b;break
                assert m==events[seen];r=rr[seen];proc.stdin.write(json.dumps({'row_id':r['row_id'],'value':r['value']})+'\n');proc.stdin.flush();seen+=1
            proc.stdin.close();proc.wait(timeout=5);assert proc.returncode==0 and seen==7
        finally:
            selector.close()
            if proc.poll() is None:proc.kill();proc.wait()
        total_cached+=10;total_new+=seen
    selections=read(O/'selections.json');prior=read(A/'prior_selections.json');assert selections[20:]==prior==read(ROOT/'results/v168_native/selections.json')
    assert sha(O/'selections.json')==read(O/'selection.freeze.json')['sha256']
    for s in selections[:20]:
        file=O/'search'/f"{s['case']}__{s['arm']}.json";state=read(file)['state'];k=min(range(17),key=lambda i:state['labels'][i][0]);assert s['row_id']==state['ids'][k] and s['search_best']==state['labels'][k][0] and sha(file)==s['search_sha256']
    plan=[]
    for block in range(3):
        order=list(range(90));random.Random(16910+block).shuffle(order);plan.extend({'block':block,**selections[i]} for i in order)
    assert plan==read(O/'validation_plan.json');validation=[r for r in acq if r['phase']=='validation'];stored=lines(O/'validation.jsonl');assert len(validation)==270
    assert read(O/'selection.freeze.json')['at_unix']<min(r['at_unix'] for r in validation)
    for expected,r,row in zip(plan,validation,stored):
        assert all(row[k]==v for k,v in expected.items()) and row['value']==r['value']
        assert (r['case'],r['arm'],r['row_id'])==(expected['case'],expected['arm'],expected['row_id'])
    arms,cases=analyze(selections,acq);comp=read(O/'comparison.json');assert comp['arms']==arms and comp['cases']==cases
    # Independent gain arithmetic and denominator check, distinct from report helper.
    for c in cases:
        model=next(a for a in arms if a['case']==c['case'] and a['arm']==c['model'])
        for name,g in c['gains'].items():
            b=next(a for a in arms if a['case']==c['case'] and a['arm']==name);assert g==1-model['median']/b['median'] or abs(g-(1-model['median']/b['median']))<1e-14
    rejected=[]
    for kind in ['value','native_output','configuration']:
        r=copy.deepcopy(acq[0]);c=cs[r['engine']]
        if kind=='value':r['value']+=1
        elif kind=='native_output':r['measurement']['quality']=0
        else:r['row_id']=(r['row_id']+1)%len(c['configs'])
        try:objective(r,c)
        except (AssertionError,KeyError):rejected.append(kind)
        else:raise AssertionError('Accepted mutation '+kind)
    assert read(O/'completion.json')['status']=='completed' and all(r['return_code']==0 for r in read(O/'bridge_exits.json'))
    write(A/'replay.json',{'verified':True,'acquisitions':410,'query_training_executions':820,'source_continuations_replayed':20,'cached_prefix_callback_hits':total_cached,'new_acquired_labels_replayed':total_new,'validation_outcomes':270,'historical_selections_preserved':70,'mutations_rejected':rejected,'new_objective_or_model_calls':0,'limitation':'Deterministic replay executes the same pinned upstream implementation; objective checks use separate evaluator code. It is not independent reimplementation or independent-host replication.'})
    print('Verified410outcomes/20sourcecontinuations/270validations;zeroacquisitionreplay')
if __name__=='__main__':main()
