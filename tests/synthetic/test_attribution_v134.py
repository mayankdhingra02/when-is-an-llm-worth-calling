"""Hand-computable directional attribution; synthetic only."""
import sys
from pathlib import Path
from fractions import Fraction
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from attribution_v134 import gain
@pytest.mark.parametrize('a,b,d,expected',[(100,90,'minimize',Fraction(1,10)),(100,110,'maximize',Fraction(1,10)),(80,90,'minimize',Fraction(-1,8)),(90,90,'minimize',Fraction(0)),(1.2,1.1,'minimize',Fraction(1,12))])
def test_oriented_gain_exact(a,b,d,expected):assert gain(a,b,d)==expected

def test_prefix_improvement_does_not_establish_incremental_value():
 assert gain(100,90,'minimize')>0
 assert gain(80,90,'minimize')<0
 for a,d in [(0,'minimize'),(-1,'maximize'),(100,'invalid')]:
  with pytest.raises(ValueError):gain(a,1,d)
