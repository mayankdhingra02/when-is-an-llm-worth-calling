import sys,copy
from pathlib import Path
import numpy as np
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
import gp_continuations_v155 as g

def fixture():return [[float(i)] for i in range(25)],list(range(10)),[float(20-i) for i in range(10)],list(range(25))

def test_ei_independent_formula():
 from statistics import NormalDist
 raw,ids,y,order=fixture();i,d=g.choose(raw,ids,y,order,'minimize',1.);z=(np.array(y)-np.mean(y))/np.std(y);delta=min(z)-d['mean'];v=delta*NormalDist().cdf(delta/d['sd'])+d['sd']*NormalDist().pdf(delta/d['sd']);assert d['ei']==pytest.approx(v);assert i not in ids and d['ei']>=0

def test_units_and_direction_equivariance():
 raw,ids,y,order=fixture();i,d=g.choose(raw,ids,y,order,'minimize',1.)
 assert g.choose(raw,ids,[v*1000 for v in y],order,'minimize',1.)[0]==i
 assert g.choose(raw,ids,[100-v for v in y],order,'maximize',1.)[0]==i

def test_no_hidden_targets_passed():
 raw,ids,y,order=fixture();i,d=g.choose(raw,ids,y,order,'minimize',.2);assert i not in ids and len(y)==10

@pytest.mark.parametrize('n',[9,20,21])
def test_budget(n):
 with pytest.raises(ValueError):g.choose([[float(i)] for i in range(30)],list(range(n)),[10.]*n,list(range(30)),'minimize',1.)

def test_duplicate_rejected():
 raw,ids,y,order=fixture();ids[1]=ids[0]
 with pytest.raises(ValueError):g.choose(raw,ids,y,order,'minimize',1.)

def test_oracle_charges_invalid_source_and_blocks_repeat(tmp_path,monkeypatch):
 monkeypatch.setattr(g,'O',tmp_path);ledger={'attempts':0,'started_monotonic':g.time.monotonic()};o=g.Oracle({'x':[[0]]*30},list(range(10)),'synthetic',ledger)
 def bad(c,i):raise ValueError('synthetic missing target')
 monkeypatch.setattr(g,'target',bad)
 with pytest.raises(ValueError):o.acquire(10)
 assert ledger['attempts']==1 and 10 in o.seen
 with pytest.raises(ValueError):o.acquire(10)
 assert ledger['attempts']==1 and 'invalid_source' in (tmp_path/'acquisitions.jsonl').read_text()

def test_global_cap_before_source_read(monkeypatch):
 o=g.Oracle({'x':[[0]]*30},list(range(10)),'synthetic',{'attempts':1400,'started_monotonic':g.time.monotonic()})
 with pytest.raises(PermissionError):o.acquire(10)
