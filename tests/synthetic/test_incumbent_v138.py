"""Synthetic-only acquired-label and budget tests."""
import sys,copy
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from incumbent_v138 import choose
def fixture():
 xs=[(i,) for i in range(30)];p={'ids':list(range(10)),'labels':[[float(i+1)] for i in range(10)],'order':list(reversed(range(30)))};s=copy.deepcopy(p);s['ids'].append(29);s['labels'].append([.1]);return xs,p,s
def test_fixed_ignores_new_labels_adaptive_uses_them():
 xs,p,s=fixture();a=choose(xs,p,s,'-','fixed_prefix_neighbor');b=choose(xs,p,s,'-','adaptive_incumbent_neighbor');assert a['anchor_id']==0 and b['anchor_id']==29
 changed=copy.deepcopy(s);changed['labels'][-1]=[100.]
 assert choose(xs,p,changed,'-','fixed_prefix_neighbor')==a
 assert choose(xs,p,changed,'-','adaptive_incumbent_neighbor')['anchor_id']==0
def test_direction_ties_and_novelty():
 xs,p,s=fixture();r=choose(xs,p,s,'+','fixed_prefix_neighbor');assert r['anchor_id']==9 and r['row_id']==28 and r['row_id'] not in s['ids']
 p['labels']=[[1.]]*10;s=copy.deepcopy(p);assert choose(xs,p,s,'-','fixed_prefix_neighbor')['anchor_id']==0
def test_prefix_and_budget_fail_closed():
 xs,p,s=fixture();s['labels'][0]=[99.]
 with pytest.raises(ValueError):choose(xs,p,s,'-','fixed_prefix_neighbor')
 s=copy.deepcopy(p);s['ids']+=list(range(10,20));s['labels']+=[[1.]]*10
 with pytest.raises(ValueError):choose(xs,p,s,'-','adaptive_incumbent_neighbor')
