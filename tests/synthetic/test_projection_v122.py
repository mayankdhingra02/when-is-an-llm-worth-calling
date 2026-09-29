import sys
from pathlib import Path
from types import SimpleNamespace
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from project_cached_v122 import project

def fixture():
 c=SimpleNamespace(names=('a','b'),domains=((0.,1.,2.,3.,4.),(0.,1.,2.,3.)),x=tuple((float(i//4),float(i%4)) for i in range(20)))
 p={'pool':{'ranked':list(range(20))},'state':{'order':list(range(20)),'ids':[]}}
 return c,p

def test_exact_strings_map_without_labels():
 c,p=fixture();raw='\n'.join(f'{i//4}{i%4}' for i in range(10));ids,trace=project(raw,c,p);assert ids==list(range(10)) and all(t['distance']==0 for t in trace)
def test_invalid_domain_rejected():
 c,p=fixture();raw='\n'.join(['99']+[f'{i//4}{i%4}' for i in range(9)])
 with pytest.raises(ValueError):project(raw,c,p)
def test_duplicate_strings_rejected():
 c,p=fixture()
 with pytest.raises(ValueError):project('\n'.join(['00']*10),c,p)
def test_projected_collisions_use_distinct_rows():
 c,p=fixture();c.domains=(tuple(float(i) for i in range(10)),c.domains[1]);c.x=tuple((float(2*(i//4)),float(i%4)) for i in range(20));p['state']['labels']='POISON: projection must not read labels'
 ids,trace=project('\n'.join(str(i)+'0' for i in range(10)),c,p)
 assert len(set(ids))==10 and any(t['closest_already_used'] for t in trace) and any(t['projected'] for t in trace)
