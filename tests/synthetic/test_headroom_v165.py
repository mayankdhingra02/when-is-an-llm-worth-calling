"""Synthetic plan and reference-selection tests; no native or LLM execution."""
import copy,sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from headroom_v165 import plan,select_reference

def test_plan_budget():
 p=plan();assert len(p)==768 and sum(5 if r['engine']=='ripgrep' else 1 for r in p)==2304
 for phase in ['selection','validation']:
  for block in range(3):
   cells=[r for r in p if r['phase']==phase and r['block']==block];assert len(cells)==128 and len({(r['engine'],r['row_id']) for r in cells})==128
 assert all(r['phase']=='selection' for r in p[:384]) and all(r['phase']=='validation' for r in p[384:])
def cells():return [{'engine':e,'row_id':i,'median':float(i+1),'valid':True} for e in ['ripgrep','hnswlib'] for i in range(4)]
def test_feasibility_not_fast_penalty():
 c=cells();c[0]['valid']=False;c[0]['median']=.01;assert select_reference(c)[0]['row_id']==1
def test_tie_and_purity():
 c=cells();c[1]['median']=1.;old=copy.deepcopy(c);assert select_reference(c)[0]['row_id']==0 and c==old
def test_missing_feasible_group():
 c=cells()
 for r in c:
  if r['engine']=='ripgrep':r['valid']=False
 with pytest.raises(ValueError):select_reference(c)
