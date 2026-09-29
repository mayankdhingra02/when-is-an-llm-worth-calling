"""Synthetic checks only. Never imported into measured result generation."""
import copy,json
import numpy as np
import pytest
from escalation.core import Candidates,State,initial_state,recommend,features,losses,project
from escalation.data import Oracle,read_table,validate_manifest
from escalation.evaluator import evaluate
from escalation.config import load_config
from escalation.runner import acquire

def fixture():
    x=tuple(tuple((i>>j)&1 for j in range(5)) for i in range(32))
    return Candidates(tuple('abcde'),x,('Y-',),('-',),tuple(range(32))),tuple((float(i),) for i in range(32))

def test_metric_hand_computable():
    assert np.allclose(losses([[0,10],[10,0]],['-','+']),[0,1])
    assert np.allclose(losses([[5,1],[5,3]],['+','-']),[0,2**-.5])
    assert evaluate([[0],[5],[10]],['-'],[0])['delta_percent']==100
    assert evaluate([[1],[1]],['-'],[0])['delta_percent'] is None

def test_budget_and_duplicates():
    c,y=fixture();o=Oracle(y,budget=20)
    for i in range(20):o.acquire(i)
    with pytest.raises(RuntimeError):o.acquire(20)
    with pytest.raises(ValueError):o.acquire(0)
    assert o.new_accesses==20

def test_pair_isolation_determinism_and_counts():
    c,y=fixture();s=initial_state(c,11);o=Oracle(y);acquire(c,s,o,'ezr_centroid_adapted',10)
    prefix=s.record();a=s.clone();b=s.clone();oa=Oracle(y,prefix=prefix);ob=Oracle(y,prefix=prefix)
    acquire(c,a,oa,'ezr_centroid_adapted',20);acquire(c,b,ob,'ezr_centroid_adapted',20)
    assert a.record()==b.record() and s.record()==prefix
    assert len(set(a.ids))==20 and o.new_accesses+oa.new_accesses+ob.new_accesses==30
    a.labels[0][0]=-999;assert a.labels!=b.labels

def test_hidden_label_perturbation_cannot_change_predecision():
    c,y=fixture();s=initial_state(c,23);o=Oracle(y);acquire(c,s,o,'ezr_centroid_adapted',10)
    altered=tuple(v if i in s.ids else (-99999.,) for i,v in enumerate(y))
    s2=initial_state(c,23);o2=Oracle(altered);acquire(c,s2,o2,'ezr_centroid_adapted',10)
    assert s2.record()==s.record()
    z,_=features(c,s,23);z2,_=features(c,s2,23);assert z==z2
    assert o.new_accesses==10

def test_features_dont_mutate_prefix_or_acquire():
    c,y=fixture();s=initial_state(c,37);o=Oracle(y);acquire(c,s,o,'ezr_centroid_adapted',10)
    old=copy.deepcopy(s.record());features(c,s,37)
    assert old==s.record() and o.new_accesses==10

def test_projection_never_queries_labels():
    c,y=fixture();s=initial_state(c,11);o=Oracle(y);acquire(c,s,o,'random',10)
    i,ev=project(c,s,c.x[s.ids[0]])
    assert i not in s.ids and ev['duplicate'] and o.new_accesses==10

def test_config_paid_rejected(tmp_path):
    import yaml
    c=load_config();c['inference']['allow_paid_api']=True;p=tmp_path/'c.yaml';p.write_text(yaml.safe_dump(c))
    with pytest.raises(ValueError):load_config(p)

def test_split_group_guard(tmp_path):
    from escalation.data import sha
    p=tmp_path/'data';p.write_text('x')
    m={'datasets':[{'system_group':g,'split':s,'path':str(p),'sha256':sha(p)} for g,s in [('a','development'),('a','test'),('b','test')]]}
    with pytest.raises(ValueError,match='crosses'):validate_manifest(m)

def test_real_feature_ending_index_is_never_silently_dropped(tmp_path):
    import csv
    p=tmp_path/'schema.csv'
    with p.open('w') as f:
        writer=csv.writer(f);writer.writerow(['a','b','c','d','sQLITE_OMIT_AUTOMATIC_INDEX','Y-'])
        for i in range(32):writer.writerow([(i>>j)&1 for j in range(5)]+[i])
    c,y,excluded=read_table(p)
    assert len(c.names)==5 and len(c.x)==32 and not excluded
    assert 'sQLITE_OMIT_AUTOMATIC_INDEX' in c.names
