"""Independent replay of uniform-coordinate draws, projection, labels and scores."""
import hashlib,json,random,sys
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.data import read_table,sha
from escalation.io import read,lines,write,now,digest
out=ROOT/'results/v4_projection_diagnostic'
frozen=read(ROOT/'reports/protocol_v4.freeze.json')
for path,expected in frozen['sha256'].items():assert sha(ROOT/path)==expected,path
records=lines(out/'runs.jsonl');manifest=read(out/'manifest.json')
assert len(records)==15 and len({(r['dataset'],r['seed']) for r in records})==15
for path,expected in manifest['comparison_input_sha256'].items():assert sha(ROOT/path)==expected
lookup={d['id']:d for d in read(ROOT/'data/manifest_v3.json')['datasets']}
for r in records:
    assert r['namespace']=='measured_non_llm_projection_diagnostic'
    assert r['requests']==r['input_tokens']==r['output_tokens']==0
    d=lookup[r['dataset']];assert sha(ROOT/d['path'])==r['data_sha256']
    c,y,_=read_table(ROOT/d['path'])
    p=read(ROOT/f'results/v3/classical/prefixes/{r["dataset"]}_{r["seed"]}.json')
    assert digest(p['state'])==r['prefix_hash'] and r['ids'][:10]==p['state']['ids']
    key=f'uniform_domains_projection_v1:{d["sha256"]}:{r["seed"]}'.encode()
    seed=int.from_bytes(hashlib.sha256(key).digest()[:8],'big')
    assert seed==r['derived_proposal_seed'];rng=random.Random(seed)
    acquired=list(p['state']['ids']);order=p['state']['order'];domains=c.domains
    for event in r['events']:
        proposal=[rng.choice(domain) for domain in domains]
        assert event['proposal']==proposal
        available=[i for i in order if i not in acquired]
        distance=lambda i:sum(a!=b for a,b in zip(c.x[i],proposal))/len(proposal)
        chosen=min(available,key=distance);seen=min(acquired,key=distance)
        assert chosen==event['row_id']
        assert np.isclose(event['distance'],distance(chosen)**.5)
        assert event['projected']==(distance(chosen)>0)
        assert event['duplicate']==(distance(seen)==0)
        assert event['collision']==(distance(seen)<distance(chosen))
        acquired.append(chosen)
    assert acquired==r['ids'] and len(acquired)==len(set(acquired))
    assert r['labels']==[list(y[i]) for i in acquired]
    assert r['actual_new_accesses']==len(acquired)-10<=10
    assert r['logical_evaluations']==len(acquired)
    if r['status']=='completed':assert len(acquired)==20
    a=np.asarray(y);span=np.ptp(a,axis=0)
    z=np.divide(a-a.min(axis=0),span,out=np.zeros_like(a),where=span!=0)
    z=np.where(np.asarray(c.directions)=='+',1-z,z);z[:,span==0]=0
    expected=float(np.min(np.sqrt(np.mean(z[acquired]**2,axis=1))))
    assert np.isclose(expected,r['loss'])
write(ROOT/'artifacts/registry_v4/projection_verification.json',{'verified':True,'at':now(),
    'records':len(records),'completed':sum(r['status']=='completed' for r in records),
    'new_labels':sum(r['actual_new_accesses'] for r in records),
    'checks':['frozen code/inputs','deterministic independent coordinate sampling','nearest-unevaluated projection and tie order',
              'prefix equality','20 logical / 10 new labels','actual outcomes and metrics','no model calls','separate namespace']})
print('Projection evidence verified:',len(records),'records')
