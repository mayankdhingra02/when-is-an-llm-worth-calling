"""Synthetic boundary checks only; no encoder/model or measured aggregates."""
import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import flac_v130 as f

def prefix():
 s=f.state(11)
 for row in s['order'][:10]:f.observe(s,row,1000+row)
 return s

def test_domain_and_effective_partition_legality():
 assert len(f.XS)==len(set(f.XS))==96
 assert f.XS[f.PRESET]==(4096,12,6)
 assert all(b%2**r==0 and b//2**r>l and l<=12 and b<=4608 and r<=8 for b,l,r in f.XS)

def test_budget_and_duplicate_fail_closed():
 s=prefix();before=copy.deepcopy(s)
 with pytest.raises(ValueError):f.observe(s,s['ids'][0],12)
 assert s==before
 for row in [r for r in s['order'] if r not in s['ids']][:10]:f.observe(s,row,50)
 with pytest.raises(ValueError):f.observe(s,next(r for r in s['order'] if r not in s['ids']),1)
 assert len(s['ids'])==20

def test_branch_independence_and_only_acquired_targets():
 p=prefix();old=copy.deepcopy(p)
 class Fake:
  def __init__(self):self.rows=[]
  def acquire(self,key,row):self.rows.append(row);return 500+row
 a=Fake();r=f.continue_arm(a,p,'sequential_3nn',11)
 assert p==old and len(a.rows)==len(set(a.rows))==10 and len(r['state']['ids'])==20
 assert not set(a.rows)&set(p['ids'])
 b=Fake();assert f.continue_arm(b,p,'sequential_3nn',11)==r

def test_bad_labels_and_empty_prefix_rejected():
 for value in [0,-1,float('nan'),3.5,True]:
  with pytest.raises(ValueError):f.observe(f.state(11),0,value)
 with pytest.raises(ValueError):f.branch_choices(f.state(11),'batch_3nn',11)

def test_projection_duplicate_repair_and_tie_order():
 p=prefix();proposals=[f.XS[p['ids'][0]]]*10
 ids,diag=f.branch_choices(p,'llm',11,proposals)
 assert len(set(ids))==10 and not set(ids)&set(p['ids'])
 assert sum(d['repeated_proposal'] for d in diag)==9
 assert all(d['matches_initial_observation'] for d in diag)
 s=prefix();s['labels']=[[100] for _ in s['ids']]
 assert f.rank(s)==[r for r in s['order'] if r not in s['ids']]

def test_provider_has_no_cloud_route():
 from runtime_proposal_v129 import Runtime
 from collect_smollm_v47 import read,ROOT
 c=read(ROOT/'configs/study_v130.json');c['allow_paid_api']=True
 with pytest.raises(AssertionError):Runtime(Path('/unused'),c)
