"""Fault-injected collector test; exclusively synthetic, never measured evidence."""
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import collect_feedback_v136 as collector
from escalation.finite_domain import FiniteCandidates
from escalation.core import State
def test_transport_failure_preserves_all_arms_and_isolates_labels(tmp_path,monkeypatch):
 root=Path(__file__).resolve().parents[2]
 write=collector.write
 cfg=json.loads((root/'configs/study_v136.json').read_text());write(tmp_path/'configs/study_v136.json',cfg)
 write(tmp_path/'reports/protocol_v136.freeze.json',{'sha256':{}})
 model=tmp_path/'fixture.bin';model.write_bytes(b'synthetic, not model weights')
 write(tmp_path/'artifacts/study_v91/model_manifest.json',{'path':'fixture.bin','sha256':collector.sha(model)})
 c=FiniteCandidates(('a','b'),tuple((float(i%2),float(i//2)) for i in range(24)),('target',),('-',),tuple(range(2,26)))
 prefix=State(list(range(24)))
 for i in range(10):prefix.observe(i,[float(i+1)],c.directions)
 write(tmp_path/'prefix.json',{'state':prefix.record()})
 jobs=[{'key':f'synthetic_{i}','dataset':'synthetic','prefix':'prefix.json','domains':[[0.,1.],list(map(float,range(12)))],'schedule':[{'round':r,'sampling_seed':i*100+r,'arm_order':['feedback','masked']} for r in range(5)]} for i in range(10)]
 write(tmp_path/'artifacts/study_v136/jobs.json',jobs)
 (tmp_path/'results').mkdir()
 oracles=[]
 class Oracle:
  def __init__(self,spec,c,prefix,journal):
   self.ids=set(prefix['ids']);self.new_accesses=0;self.journal=journal;oracles.append(self)
  def acquire(self,i):
   assert i not in self.ids and len(self.ids)<20
   self.ids.add(i);self.new_accesses+=1;self.journal({'row_id':i,'source_line':i+2,'raw_target':str(i+1)})
   return [float(i+1)]
 class Runtime:
  def __init__(self,out,cfg):self.out=out;self.calls=0
  def start(self):pass
  def api(self,path,p):return {'prompt':'synthetic'} if path=='/apply-template' else {'tokens':[1]}
  def authorize(self,*a):return {}
  def generate(self,*a):
   self.calls+=1
   if self.calls==3:raise OSError('injected transport failure')
   return {'truncated':False,'stop_type':'eos','tokens_predicted':8,'content':'["0B","1B"]'}
  def close(self):write(self.out/'synthetic_runtime.json',{'calls':self.calls})
 monkeypatch.setattr(collector,'ROOT',tmp_path);monkeypatch.setattr(collector,'Runtime',Runtime);monkeypatch.setattr(collector,'IndexedOracle',Oracle)
 monkeypatch.setattr(collector,'rss',lambda _:0);monkeypatch.setattr(collector,'vocab',lambda _:[])
 monkeypatch.setattr(collector,'candidates',lambda _:({'meaning':'synthetic loss','direction':'-'},c))
 collector.main()
 out=tmp_path/'results/v136_feedback';s=json.loads((out/'summary.json').read_text())
 assert s['complete'] and s['new_acquisitions']==200 and s['intended_requests']==100 and len(s['completed_arms'])==20
 assert 'injected' in s['generation_stop_reason'] and json.loads((out/'synthetic_runtime.json').read_text())['calls']==3
 assert len(oracles)==20 and all(o.new_accesses==10 and len(o.ids)==20 for o in oracles)
 selections=[json.loads(p.read_text()) for p in (out/'selections').glob('*.json')]
 assert sum(x['fallback'] for x in selections)==98
 for p in (out/'arms').glob('*.json'):
  st=json.loads(p.read_text())['state'];assert st['ids'][:10]==prefix.ids and st['labels'][:10]==prefix.labels
