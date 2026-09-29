import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'scripts'))
from download_guard import available

def test_model_and_combined_download_caps():
    assert available({'accounted_bytes':5*1024**3,'model_bytes':0})==0
    assert available({'accounted_bytes':4*1024**3,'model_bytes':4*1024**3},True)==0
    assert available({'accounted_bytes':5*1024**3-3,'model_bytes':0},True)==3
