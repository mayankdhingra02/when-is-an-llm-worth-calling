"""Python>=3.12 bridge: immutable owner acquire + explicit checkpoint injection.

Only stdin features/prefix labels enter optimization. stdout requests one label
at a time; the parent evaluator, not this module, owns native objective access.
"""
import hashlib,importlib.util,json,math,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'artifacts/sources/ezr_ezr.py'
EXPECTED='d0fdb7ac6242cc7d8eec8ced3abec1c1e89d405326dfe384525c63f0ad92b2ad'
def load_owner():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest()==EXPECTED
    spec=importlib.util.spec_from_file_location('ezr_owner_v169',SOURCE);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def run(body,acquire):
    assert set(body)=={'raw_features','prefix','arm'} and set(body['prefix'])=={'ids','labels','order'}
    ezr=load_owner();raw=body['raw_features'];prefix=body['prefix'];ids=prefix['ids'];ys=[y[0] for y in prefix['labels']];order=prefix['order'];arm=body['arm']
    assert 17<=len(raw)<=128 and raw[0] and all(len(row)==len(raw[0]) for row in raw)
    assert len(ids)==len(set(ids))==len(ys)==10 and set(order)==set(range(len(raw))) and len(order)==len(raw)
    assert all(math.isfinite(y) and y>0 for y in ys) and arm in ['ezr_upstream_centroid','ezr_upstream_bayes']
    known=dict(zip(ids,ys));symbolic=[any(isinstance(row[j],(str,bool)) for row in raw) for j in range(len(raw[0]))]
    headers=[('f' if cat else 'F')+str(j) for j,cat in enumerate(symbolic)]+['RowX','Loss-']
    rows=[[(str(v).lower() if isinstance(v,bool) else v) for v in row]+[i,known.get(i,'?')] for i,row in enumerate(raw)]
    data=ezr.Data([headers]+rows);seeded=ids+[i for i in order if i not in known];rank={i:k for k,i in enumerate(seeded)}
    ezr.shuffle=lambda rs:rs.sort(key=lambda row:rank[row[-2]])
    ezr.the.learn.start=10;ezr.the.learn.budget=7;ezr.the.few=128
    original=ezr.acquireWithCentroid if arm.endswith('centroid') else ezr.acquireWithBayes
    labels=[];cache_hits=[];scores=[];traces=[];start=time.process_time()
    def score(lab,best,rest,row):
        assert len(lab.rows)==10+len(labels)
        assert all(r[-1]!='?' for r in lab.rows) and row[-1]=='?'
        value=original(lab,best,rest,row);assert math.isfinite(value)
        scores.append({'row_id':row[-2],'score':value});return value
    def label(_,row):
        i=row[-2]
        if i in known:
            assert i in ids and row[-1]==known[i];cache_hits.append(i);return row
        assert len(labels)<7 and row[-1]=='?' and i not in ids
        trace={'step':len(labels),'row_id':i,'scores':scores.copy(),'acquired_ids':ids+[r['row_id'] for r in labels]}
        assert scores and i==min(scores,key=lambda r:r['score'])['row_id']
        value=acquire(i,trace);assert math.isfinite(value) and value>0
        row[-1]=value;known[i]=value;labels.append({'row_id':i,'value':value});traces.append(trace);scores.clear();return row
    result=ezr.acquire(data,score=score,label=label)
    assert len(labels)==7 and cache_hits==ids and len(result.rows)==17
    return {'arm':arm,'source_sha256':EXPECTED,'prefix_cache_hits':cache_hits,'new_labels':labels,'headers':headers,'symbolic':symbolic,'source_defaults':{'p':ezr.the.p,'bayes_k':ezr.the.bayes.k,'bayes_m':ezr.the.bayes.m,'few':ezr.the.few,'start':ezr.the.learn.start,'budget':ezr.the.learn.budget},'trace':traces,'optimizer_process_cpu_seconds':time.process_time()-start}
def main():
    body=json.loads(sys.stdin.readline())
    def acquire(i,trace):
        print(json.dumps({'type':'acquire','row_id':i,'trace':trace}),flush=True)
        response=json.loads(sys.stdin.readline());assert response['row_id']==i;return response['value']
    result=run(body,acquire);print(json.dumps({'type':'complete','result':result}),flush=True)
if __name__=='__main__':main()
