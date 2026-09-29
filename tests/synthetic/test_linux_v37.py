import importlib.util,json,hashlib
from pathlib import Path
from zipfile import ZipFile,ZipInfo
import pytest
p=Path(__file__).resolve().parents[2]/'scripts/linux_replay_v37.py';spec=importlib.util.spec_from_file_location('linux_v37',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

def test_archive_hash_guard(tmp_path):
    p=tmp_path/'fixture';p.write_bytes(b'synthetic')
    m.archive_ok(p,hashlib.sha256(b'synthetic').hexdigest())
    with pytest.raises(ValueError,match='SHA256'):m.archive_ok(p,'wrong')

@pytest.mark.parametrize('name',['../outside','/outside'])
def test_path_escape_rejected(tmp_path,name):
    p=tmp_path/'fixture.zip'
    with ZipFile(p,'w') as z:z.writestr(name,b'synthetic')
    with pytest.raises(ValueError,match='Unsafe'):m.safe_extract(p,tmp_path/'out')

def test_symlink_rejected(tmp_path):
    p=tmp_path/'fixture.zip';entry=ZipInfo('link');entry.external_attr=0o120777<<16
    with ZipFile(p,'w') as z:z.writestr(entry,b'outside')
    with pytest.raises(ValueError,match='symlink'):m.safe_extract(p,tmp_path/'out')

def test_scientific_comparison_ignores_only_version():
    assert m.scientific({'runtime':'3.10','gain':0})==m.scientific({'runtime':'3.11','gain':0})
    assert m.scientific({'runtime':'3.10','gain':0})!=m.scientific({'runtime':'3.11','gain':1})
