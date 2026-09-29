"""Hand-computable, synthetic diagnostic contrasts, never research observations."""
import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from report_headroom_v165 import contrast

def cell(i,median,mad=.01,valid=True):return {'row_id':i,'median':median,'relative_mad':mad,'valid':valid}
def test_actual_gain():assert contrast(cell(1,2),cell(0,1))['headroom']==.5 and contrast(cell(1,2),cell(0,1))['robust_practical_headroom']
def test_negative_not_clipped():assert contrast(cell(1,1),cell(0,2))['headroom']==-1
@pytest.mark.parametrize('target,ref',[(cell(0,1),cell(0,1)),(cell(1,1),cell(0,.95)),(cell(1,1,.06),cell(0,.8)),(cell(1,1),cell(0,.8,.06)),(cell(1,1,valid=False),cell(0,.8)),(cell(1,1),cell(0,.009))])
def test_practical_flags(target,ref):assert not contrast(target,ref)['robust_practical_headroom']
