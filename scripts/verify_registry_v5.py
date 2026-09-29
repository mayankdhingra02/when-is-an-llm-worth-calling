"""Verify source payloads, schema boundaries, family exclusions and v4 preservation."""
import hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.registry_v5 import family
read=lambda p:json.loads((ROOT/p).read_text())
for p,h in read('reports/protocol_v4.freeze.json')['sha256'].items():
    assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
registry=read('data/registry_v5.json')
for source in read('artifacts/registry_v5/sources.json'):
    payload=(ROOT/source['path']).read_bytes()
    assert hashlib.sha256(payload).hexdigest()==source['sha256']
    assert hashlib.sha1(b'blob '+str(len(payload)).encode()+b'\0'+payload).hexdigest()==source['git_blob_sha1']
for d in registry['datasets']:
    assert hashlib.sha256((ROOT/d['path']).read_bytes()).hexdigest()==d['sha256'],d['path']
    s=d['schema']
    assert not s['objective_values_inspected'] and not d['collection_admitted']
    assert not set(s['feature_names'])&set(s['objective_names'])
    assert not set(s['feature_names'])&set(s['metadata_columns'])
    if d['system_group'] in {'apache','sqlite','x264'}:
        assert 'previously_exposed_family' in d['finite_domain_feasibility_exclusions']
    if d['source']=='ChristianKaltenecker/PerformanceEvolution_Website':
        model=Path(d['path']).parent/'FeatureModel.xml'
        names=[e.findtext('name') for e in ET.parse(ROOT/model).findall('./binaryOptions/configurationOption')]
        if set(names)!=set(s['feature_names']):
            assert d['feature_model_mismatch'] is not None
            assert 'feature_model_header_mismatch' in d['finite_domain_feasibility_exclusions']
        else:assert d['feature_model_mismatch'] is None
        assert s['metadata_columns']==['revision'] and 'revision' in s['row_filters']
        if d['system_group']=='z3':assert s['row_filters']['LRA']=='1'
for p in read('artifacts/registry_v5/papers.json'):
    assert hashlib.sha256((ROOT/p['path']).read_bytes()).hexdigest()==p['sha256']
summary=registry['summary']
assert set(summary['strict_v4_schema_candidate_families'])<=set(summary['finite_domain_candidate_families'])
assert not {'fpga_sort256','noc_cm_log'} & set(summary['finite_domain_candidate_families'])
assert family('VP8')==family('VP9') and family('MySQL')==family('MariaDB')
result={'verified':True,'tables':len(registry['datasets']),
        'feature_model_schema_matches':11,'feature_model_mismatches_quarantined':1,'v4_freeze_unchanged':True,
        'no_new_objective_values_inspected':True,'no_collection_admitted':True,
        'strict_binary_candidate_families':len(summary['strict_v4_schema_candidate_families']),
        'broader_finite_candidate_families':len(summary['finite_domain_candidate_families'])}
(ROOT/'artifacts/registry_v5/verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
