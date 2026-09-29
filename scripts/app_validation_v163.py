"""Independent reference construction and raw-output checks, never native execution."""
import hashlib,json,re
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v160'
class Reference:
 def __init__(self,recompute=True):
  self.train=np.loadtxt(A/'optdigits.tra',delimiter=',',dtype=np.int64)[:,:64];self.query=np.loadtxt(A/'optdigits.tes',delimiter=',',dtype=np.int64)[:,:64]
  assert np.array_equal(self.train,np.fromfile(A/'ann_train.f32',dtype='<f4').reshape(3823,64));assert np.array_equal(self.query,np.fromfile(A/'ann_query.f32',dtype='<f4').reshape(1797,64))
  self.kth=np.load(A/'ann_kth_squared.npy');self.bundle=json.loads((ROOT/'artifacts/study_v162/query_references.json').read_text())
  if recompute:
   # Independent norm/dot identity, not the original difference-squared reference.
   ds=(self.query*self.query).sum(1)[:,None]+(self.train*self.train).sum(1)[None,:]-2*self.query@self.train.T
   assert np.array_equal(np.partition(ds,9,axis=1)[:,9],self.kth)
   actual=[{} for _ in self.bundle['patterns']]
   for f in json.loads((A/'corpus_files.json').read_text()):
    path=ROOT/'.native-v160/search_corpus'/f['path'];body=path.read_bytes();assert hashlib.sha256(body).hexdigest()==f['sha256']
    for pattern,counts in zip(self.bundle['patterns'],actual):counts[f['path']]=sum(1 for _ in re.finditer(pattern.encode(),body))
   assert actual==self.bundle['counts']
 def validate(self,v):
  assert v['correct'] is True and v['objective_seconds']>0
  if v['engine']=='ripgrep':
   assert v['native_invocations']==5 and v['individual_query_timings_observed'] is False and len(v['query_results'])==5
   for r,expected in zip(v['query_results'],self.bundle['counts']):
    actual={};raw=r['stdout'].encode()
    for line in raw.split(b'\n'):
     if not line:continue
     key,count=line.rsplit(b'\0',1);key=key.decode().removeprefix('./');assert key not in actual;actual[key]=int(count)
    assert actual==expected and r['correct'] and r['returncode']==0 and hashlib.sha256(raw).hexdigest()==r['raw_output_sha256']
   assert v['quality']==1 and v['value']==v['objective_seconds'];return v['value']
  assert v['engine']=='hnswlib' and v['native_invocations']==1;ids=v['neighbor_ids']
  assert len(ids)==1797 and all(len(row)==10 and len(set(row))==10 and all(type(i)is int and 0<=i<3823 for i in row) for row in ids)
  selected=self.train[np.array(ids)];dist=(selected*selected).sum(2)+(self.query*self.query).sum(1)[:,None]-2*np.einsum('qkd,qd->qk',selected,self.query)
  quality=float(np.sum(dist<=self.kth[:,None]))/(1797*10);assert abs(quality-v['quality'])<1e-15 and v['quality_feasible']==(quality>=.95)
  text=''.join(' '.join(str(i) for i in row)+'\n' for row in ids);assert hashlib.sha256(text.encode()).hexdigest()==v['raw_output_sha256']
  timing=json.loads(v['stdout'])
  for name,value in timing.items():assert v[name]==value
  assert (timing['indexed'],timing['queries'],timing['k'],timing['build_threads'])==(3823,1797,10,1)
  assert abs(v['build_seconds']+v['query_seconds']-v['objective_seconds'])<1e-9
  expected=v['objective_seconds'] if quality>=.95 else 20.;assert v['value']==expected;return expected
