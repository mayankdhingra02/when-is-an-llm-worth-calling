"""Corruption of isolated saved-evidence copies; no server/workload execution."""
import importlib.util,json,shutil,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
import report_nginx_v105 as r

def test_changed_valid_response_count_rejected(tmp_path):
    out=tmp_path/'copy';shutil.copytree(r.OUT,out)
    p=out/'summary.json';x=json.loads(p.read_text());x['cases'][0]['responses_byte_valid']-=1
    p.write_text(json.dumps(x))
    with pytest.raises(AssertionError):r.verify(out)

def test_modified_same_length_payload_rejected(tmp_path):
    out=tmp_path/'copy';shutil.copytree(r.OUT,out)
    p=out/'00_reference/www/payload.bin';p.write_bytes(b'X'*p.stat().st_size)
    with pytest.raises(AssertionError):r.verify(out)

def test_consistent_summary_and_record_corruption_rejected(tmp_path):
    out=tmp_path/'copy';shutil.copytree(r.OUT,out)
    p=out/'summary.json';x=json.loads(p.read_text());x['cases'][0]['client_counts'][0]['valid']-=1
    p.write_text(json.dumps(x));(out/'00_reference/result.json').write_text(json.dumps(x['cases'][0]))
    with pytest.raises(AssertionError):r.verify(out)
