"""Synthetic only; no measured fixture or source outcome loaded."""
import csv,sys,copy
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import spark_v144 as m

def fake_source(tmp_path,target):
 p=tmp_path/'synthetic.csv'
 with p.open('w') as f:
  w=csv.writer(f);w.writerow([f'x{i}' for i in range(30)]+['exec_time','App','App_id','input_size'])
  for i in range(45):w.writerow([str(i+j) if j not in m.CAT else str(i%2) for j in range(30)]+[target,'synthetic','DO_NOT_USE','fixed'])
 return p

def test_target_isolation_context_and_telemetry(tmp_path,monkeypatch):
 monkeypatch.setattr(m,'ROOT',tmp_path);p=fake_source(tmp_path,'DO_NOT_CONVERT_TARGET');a=m.load_features(p,'synthetic','fixed')
 assert len(a['x'])==45 and len(a['names'])==30
 p=fake_source(tmp_path,'A_DIFFERENT_HIDDEN_TARGET');b=m.load_features(p,'synthetic','fixed')
 assert a['x']==b['x'] and a['domains']==b['domains']
 with pytest.raises(ValueError):m.load_features(p,'synthetic','other')

def test_mixed_geometry_and_no_hidden_rank():
 a=[0]*30;b=a.copy();b[0]=.5;b[4]=1
 assert m.distance(a,b)==1.5/30
 c={'x':[[i/40]*30 for i in range(40)]};s={'ids':[0,1,2,3],'labels':[[4],[3],[2],[1]],'order':list(range(40))}
 assert m.choose(c,s,'sequential_3nn')==m.choose(c,copy.deepcopy(s),'sequential_3nn')
 assert m.choose(c,s,'adaptive_neighbor')==4
 assert m.choose(c,s,'fixed_neighbor',anchor=0)==4

def test_projection_unique_and_prefix_excluded(tmp_path,monkeypatch):
 monkeypatch.setattr(m,'ROOT',tmp_path);c=m.load_features(fake_source(tmp_path,'HIDDEN'),'synthetic','fixed');s={'ids':list(range(10)),'labels':[[1]]*10,'order':list(range(45))}
 proposals=[[d[0] for d in c['grid_domains']]]*10;ids,diag=m.project(c,s,proposals)
 assert len(set(ids))==10 and not set(ids)&set(s['ids']) and sum(d['repeated_proposal'] for d in diag)==9
 assert len(s['ids'])==10

def test_oracle_guards_before_source_access():
 o=object.__new__(m.Oracle);o.c={'x':[[0]*30]*30};o.seen=set(range(20))
 for i in [0,20,-1,True]:
  with pytest.raises(ValueError):o.acquire(i)

def test_before_twenty_choice_budget_guard():
 s={'ids':list(range(20)),'labels':[[1]]*20,'order':list(range(40))}
 with pytest.raises(ValueError):m.choose({'x':[[0]*30]*40},s,'random_full')
