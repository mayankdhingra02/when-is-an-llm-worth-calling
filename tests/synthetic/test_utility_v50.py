import importlib.util
from pathlib import Path
import pytest,zlib
p=Path(__file__).resolve().parents[2]/'scripts/utility_v50.py'
s=importlib.util.spec_from_file_location('utility_v50',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def test_feature_only_eligibility():
 assert m.eligible({'family':'zstd','checksum':True}) and not m.eligible({'family':'zstd','checksum':False})
 assert m.eligible({'family':'lz4','dependent':False}) and not m.eligible({'family':'lz4','dependent':True})
 assert m.eligible({'family':'zlib'})
def test_zstd_checksum_bit():
 assert m.frame_fields('zstd',bytes.fromhex('28b52ffd0400'))['content_checksum']
 assert not m.frame_fields('zstd',bytes.fromhex('28b52ffd0000'))['content_checksum']
def test_lz4_flags():
 assert m.frame_fields('lz4',bytes.fromhex('04224d18647000'))=={'content_checksum':True,'independent_blocks':True,'block_size_id':7}
 assert not m.frame_fields('lz4',bytes.fromhex('04224d18447000'))['independent_blocks']
def test_bad_magic_rejected_and_real_zlib_wrapper():
 with pytest.raises(ValueError):m.frame_fields('zstd',b'not a frame')
 with pytest.raises(ValueError):m.frame_fields('lz4',b'not a frame')
 assert m.frame_fields('zlib',zlib.compress(b'synthetic fixture'))=={'wrapped':True,'preset_dictionary':False,'window_log':15}
