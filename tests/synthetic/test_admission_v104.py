"""Synthetic isolated admission-integrity tests; never research measurements."""
import importlib.util
import json
from pathlib import Path
import shutil
import pytest

ROOT=Path(__file__).resolve().parents[2]
def module(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
A=module('audit_admission_v104');F=module('fetch_admission_v104')

@pytest.mark.parametrize('url',[
    'http://api.github.com/repos/ideas-labo/dhda/commits/main',
    'https://raw.githubusercontent.com/other/thing/main/README.md',
    'https://raw.githubusercontent.com/ideas-labo/dhda/main/drift_data/data6/nginx1.csv',
    'https://www.se.cs.uni-saarland.de/projects/splconqueror/expDesign/CaseStudies/measurements_gemm.xml',
    'https://username:secret@api.github.com/repos/ideas-labo/dhda/commits/main',
    'https://api.github.com.evil.example/repos/ideas-labo/dhda/commits/main',
])
def test_rejects_unapproved_or_objective_sources(url):
    with pytest.raises(ValueError):F.check_url(url)


def test_features_have_no_objective_cells():
    m=A.feature_metadata(A.SRC/'nginx_FeatureModel.xml')
    assert 'tls' in m['binary']
    assert not {'performance','energy','cpu'} & set(m['binary'])


def test_tampered_source_rejected(tmp_path):
    dest=tmp_path/'sources';shutil.copytree(A.SRC,dest)
    with (dest/'nginx_README.md').open('a') as f:f.write('synthetic corruption')
    with pytest.raises(AssertionError):A.verify_sources(dest)


def test_updated_checksum_cannot_bypass_pinned_blob(tmp_path):
    dest=tmp_path/'sources';shutil.copytree(A.SRC,dest)
    p=dest/'nginx_README.md';p.write_text('synthetic replacement')
    lp=dest/'manifest.json';ledger=json.loads(lp.read_text())
    for e in ledger['attempts']:
        if e['name']==p.name:e.update(sha256=A.sha(p),bytes=p.stat().st_size)
    lp.write_text(json.dumps(ledger))
    with pytest.raises(AssertionError):A.verify_sources(dest)


def test_identity_scan_keeps_compiler_alias_and_excludes_synthetic(tmp_path):
    (tmp_path/'results/old').mkdir(parents=True)
    (tmp_path/'results/old/run.json').write_text('{"system_group":"llvm","value":999}')
    (tmp_path/'results/old/other.json').write_text('{"system":"OpenResty"}')
    (tmp_path/'tests/synthetic').mkdir(parents=True)
    (tmp_path/'tests/synthetic/fake.json').write_text('{"system":"TriMesh"}')
    out=A.exposure_inventory(tmp_path)
    assert out['hits']['gemm_llvm']==['results/old/run.json']
    assert out['hits']['nginx']==['results/old/other.json']
    assert not out['hits']['trimesh']
    assert '999' not in json.dumps(out)
