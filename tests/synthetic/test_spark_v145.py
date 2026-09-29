import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from spark_v145 import choose,best

def test_missing_never_becomes_training_value_or_repeat():
 c={'x':[[i/30]*30 for i in range(30)]};s={'ids':[0,1,2,3,4],'labels':[[9],[8],[7],[6],[None]],'order':list(range(30))}
 assert choose(c,s,'sequential_3nn') not in s['ids']
 assert choose(c,s,'adaptive_neighbor')==5
 assert best(s)==6

def test_missing_still_spends_arm_budget():
 s={'ids':list(range(20)),'labels':[[1]]+[[None]]*19,'order':list(range(30))}
 with pytest.raises(ValueError):choose({'x':[[0]*30]*30},s,'sequential_3nn')
