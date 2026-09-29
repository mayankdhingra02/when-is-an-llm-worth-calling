"""Copy-based raw-receipt tamper tests; no acquisitions or inference."""
import json,shutil,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from analyze_portfolio_v115 import verify
@pytest.fixture
def saved(tmp_path):
 freeze=json.loads((ROOT/'reports/protocol_v115.freeze.json').read_text())
 for n in freeze['sha256']:
  p=tmp_path/n;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(ROOT/n)
 shutil.copytree(ROOT/'results/v115_portfolio',tmp_path/'results/v115_portfolio')
 return tmp_path
@pytest.mark.parametrize('change',['step','budget','label'])
def test_tampered_portfolio_rejected(saved,change):
 out=saved/'results/v115_portfolio'
 if change=='label':
  p=out/'acquisitions.jsonl';rows=[json.loads(s) for s in p.read_text().splitlines()];rows[0]['raw_target']=str(float(rows[0]['raw_target'])+100);p.write_text(''.join(json.dumps(r)+'\n' for r in rows))
 else:
  p=next((out/'arms').glob('*.json'));d=json.loads(p.read_text())
  if change=='step':d['trace'][0]['mode']='sequential'
  else:d['logical_evaluations']=19
  p.write_text(json.dumps(d))
 with pytest.raises(AssertionError):verify(saved,check_freeze=False)
