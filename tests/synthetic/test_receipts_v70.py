import json
import pytest
from escalation.receipts_v70 import atomic_json

def test_failed_serialization_preserves_timing(tmp_path):
    path=tmp_path/'progress.json';atomic_json(path,{'phase':'timed','seconds':1.25})
    with pytest.raises(TypeError):atomic_json(path,{'metadata':object()})
    assert json.loads(path.read_text())=={'phase':'timed','seconds':1.25}
    assert not list(tmp_path.glob('*.pending'))

def test_replace_failure_preserves_receipt(tmp_path,monkeypatch):
    path=tmp_path/'progress.json';atomic_json(path,{'phase':'loaded'})
    def fail(*args):raise OSError('injected replacement failure')
    monkeypatch.setattr('escalation.receipts_v70.os.replace',fail)
    with pytest.raises(OSError):atomic_json(path,{'phase':'timed'})
    assert json.loads(path.read_text())=={'phase':'loaded'}
    assert not list(tmp_path.glob('*.pending'))

def test_metadata_bytes(tmp_path):
    path=tmp_path/'receipt.json';atomic_json(path,{'key':b'\xff'})
    assert json.loads(path.read_text())=={'key':{'bytes_hex':'ff'}}
