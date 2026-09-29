import json
import pytest
from escalation.record_json_v69 import bytes_default

def test_live_file_boundary_bytes_roundtrip():
    value={'live_sst_files':[{'start_key':b'user0','end_key':b'\x00\xff','size':100}]}
    output=json.loads(json.dumps(value,default=bytes_default))
    assert bytes.fromhex(output['live_sst_files'][0]['end_key']['bytes_hex'])==b'\x00\xff'
    assert output['live_sst_files'][0]['size']==100

def test_unknown_metadata_fails():
    with pytest.raises(TypeError):json.dumps({'x':object()},default=bytes_default)
