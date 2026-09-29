"""Corrupt copies only; saved real outputs are immutable and never test fixtures in aggregates."""
import importlib.util,json,shutil,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from verify_classical_nginx_v111 import verify
@pytest.fixture
def saved(tmp_path):
 # Avoid copying gigabytes or executing a new objective. Copy small receipts,
 # symlink immutable code/binaries so their original freeze still verifies.
 for n in json.loads((ROOT/'reports/protocol_v111.freeze.json').read_text())['sha256']:
  target=tmp_path/n;target.parent.mkdir(parents=True,exist_ok=True);target.symlink_to(ROOT/n)
 p=tmp_path/'reports/protocol_v111.freeze.json';shutil.copyfile(ROOT/'reports/protocol_v111.freeze.json',p)
 shutil.copytree(ROOT/'results/v111_classical',tmp_path/'results/v111_classical')
 return tmp_path
@pytest.mark.parametrize('kind',['budget','branch','native_count','schedule'])
def test_reject_corrupt_saved_evidence(saved,kind):
 out=saved/'results/v111_classical'
 if kind=='budget':
  p=out/'summary.json';d=json.loads(p.read_text());d['charged_native_configuration_attempts']=10;p.write_text(json.dumps(d))
 elif kind=='branch':
  p=out/'prefix.json';d=json.loads(p.read_text());d['state']['labels'][0][0]+=1;p.write_text(json.dumps(d))
 elif kind=='native_count':
  p=next((out/'trials').glob('*/client_0.stdout'));d=json.loads(p.read_text());d['responses_byte_valid']-=1;p.write_text(json.dumps(d))
 else:
  p=out/'starts.jsonl';lines=p.read_text().splitlines();lines[0],lines[1]=lines[1],lines[0];p.write_text('\n'.join(lines)+'\n')
 with pytest.raises(AssertionError):verify(saved)
