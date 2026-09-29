"""Corruption checks run only on copies; never solve or call a model."""
import json,shutil,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from analyze_validation_v113 import analyze
from report_validation_v113 import diagnostics
@pytest.fixture
def saved(tmp_path):
 for n in json.loads((ROOT/'reports/protocol_v113.freeze.json').read_text())['sha256']:
  p=tmp_path/n;p.parent.mkdir(parents=True,exist_ok=True);p.symlink_to(ROOT/n)
 shutil.copyfile(ROOT/'reports/protocol_v113.freeze.json',tmp_path/'reports/protocol_v113.freeze.json')
 shutil.copytree(ROOT/'results/v113_validation',tmp_path/'results/v113_validation')
 return tmp_path
@pytest.mark.parametrize('kind',['request','label','count','certificate'])
def test_reject_corrupted_validation(saved,kind):
 out=saved/'results/v113_validation'
 if kind=='request':
  p=next((out/'requests').glob('*.json'));d=json.loads(p.read_text());d['row']+=1
 elif kind=='label':
  p=next((out/'evaluations').glob('*.json'));d=json.loads(p.read_text());d['objective_seconds']+=1
 elif kind=='count':
  p=out/'summary.json';d=json.loads(p.read_text());d['acquisitions']-=1
 else:
  p=next((out/'evaluations').glob('*.json'));d=json.loads(p.read_text());d['measurements'][0]['certificate']['valid']=False
 p.write_text(json.dumps(d))
 with pytest.raises(AssertionError):analyze(saved)

def test_equal_configuration_diagnostic_keeps_all_cases():
 d=json.loads((ROOT/'results/v113_analysis/summary.json').read_text());before=json.dumps(d,sort_keys=True)
 x=diagnostics(d)
 assert x['count_identical']==sum(v for r in d['cases'] for v in r['same_configuration_as_llm'].values())
 assert json.dumps(d,sort_keys=True)==before and len(d['cases'])==10
