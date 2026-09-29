import json,sys
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from decoder_v93b_common import validate
@pytest.mark.parametrize('key,value',[('scientific_request_cap',78),('new_generation_request_cap',78),('max_generation_stage_seconds',1579),('max_server_rss_bytes',8589934593),('context_tokens',8192),('retries',1)])
def test_remaining_allowance_cannot_expand(key,value):
    cfg=json.loads((ROOT/'configs/study_v93b.json').read_text());cfg[key]=value
    with pytest.raises(ValueError):validate(cfg)
def test_remaining_config():validate(json.loads((ROOT/'configs/study_v93b.json').read_text()))
