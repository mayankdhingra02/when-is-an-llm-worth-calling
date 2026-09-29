"""Reproduce V104 metadata provenance and historical identity audit; no oracles."""
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT/'artifacts/sources/v104'
OUT = ROOT/'results/v104_admission'
ALIASES = {
    'nginx': ['nginx', 'openresty'],
    'gemm_llvm': ['gemm', 'polly', 'llvm'],
    'trimesh': ['trimesh', 'triangular'],
}


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1024*1024), b''): h.update(b)
    return h.hexdigest()


def verify_sources(source_dir=SRC):
    ledger = json.loads((source_dir/'manifest.json').read_text())
    total = 0
    for a in ledger['attempts']:
        total += a['bytes']
        p = source_dir/a['name']
        if 'sha256' in a:
            assert p.stat().st_size == a['bytes'] and sha(p) == a['sha256'], a['name']
        else:
            assert a['bytes'] == 0 and not p.exists(), a['name']
        assert a['status'] in ['complete', 'failed']
    assert total <= 10*1024**2
    comparisons = []
    for tag, names in {'dhda': {'README.md':'dhda_README.md', 'LICENSE':'dhda_LICENSE.txt',
            'paper/ICSE_DHDA.pdf':'dhda.pdf', 'drift_data/readme.md':'dhda_data_readme.md'},
            'twins': {'README.md':'twins_README.md', 'LICENSE':'twins_LICENSE.txt',
            'data/nginx/README.md':'nginx_README.md', 'data/nginx/FeatureModel.xml':'nginx_FeatureModel.xml'}}.items():
        rev = json.loads((source_dir/f'{tag}_revision.json').read_text())
        tree = json.loads((source_dir/f'{tag}_tree.json').read_text())
        assert tree['truncated'] is False
        # GitHub echoes the requested commit-ish in this recursive tree response.
        assert tree['sha'] == rev['sha']
        entries = {e['path']: e for e in tree['tree']}
        for remote, local in names.items():
            body = (source_dir/local).read_bytes()
            blob = hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
            assert blob == entries[remote]['sha'], local
            comparisons.append({'source':local,'revision':rev['sha'],'git_blob_sha1':blob})
    return {'persisted_http_body_bytes': total, 'attempts': len(ledger['attempts']),
            'failed_requests': sum(a['status']=='failed' for a in ledger['attempts']),
            'pinned_blob_checks':comparisons}


def feature_metadata(path):
    root=ET.parse(path).getroot()
    assert root.tag=='vm'
    return {'name':root.attrib['name'], 'binary':[n.findtext('name') for n in root.findall('./binaryOptions/configurationOption')],
            'numeric':[{'name':n.findtext('name'),'min':n.findtext('minValue'),'max':n.findtext('maxValue'),
                        'values':n.findtext('values'),'step':n.findtext('stepFunction')}
                       for n in root.findall('./numericOptions/configurationOption')],
            'boolean_constraints':[n.text for n in root.findall('./booleanConstraints/constraint')],
            'mixed_constraints':[{'text':n.text,**n.attrib} for n in root.findall('./mixedConstraints/constraint')]}


def exposure_inventory(root=ROOT):
    patterns={k:re.compile(r'(?i)(?<![a-z0-9])(?:'+ '|'.join(map(re.escape,v))+r')(?![a-z0-9])') for k,v in ALIASES.items()}
    entries=[];hits={k:[] for k in ALIASES}
    paths=set()
    for folder in ['results','reports','configs']:
        paths.update(p for p in (root/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.csv','.md','.yaml','.yml'])
    paths.update(p for p in (root/'data').glob('*') if p.is_file() and p.suffix in ['.json','.yaml'])
    scope_path=root/'configs/exposure_scope_v104.json'
    frozen_scope=json.loads(scope_path.read_text()) if scope_path.exists() else None
    if frozen_scope is not None: paths={root/n for n in frozen_scope}
    for p in sorted(paths):
        rel=str(p.relative_to(root))
        if 'v104' in rel:continue
        snapshot=root/'artifacts/study_v104/previous_snapshot'/rel
        if snapshot.exists():p=snapshot
        entry={'path':rel,'bytes':p.stat().st_size,'sha256':sha(p)}
        if frozen_scope is not None:
            assert {k:entry[k] for k in ['bytes','sha256']}==frozen_scope[rel],rel
        # Existing saved results only: emit identities/hashes, never objective cells.
        text=p.read_text(errors='replace')
        matched=[k for k,pattern in patterns.items() if pattern.search(text) or pattern.search(rel)]
        entry['matched_groups']=matched;entries.append(entry)
        for k in matched:hits[k].append(rel)
    return {'scope':'all pre-V104 results/reports/configs text metadata and top-level data manifests; synthetic tests, raw source tables and arbitrary personal files excluded',
            'limitations':'Text identity audit is not proof of code independence; group GEMM with LLVM using original paper. Reviewed TriMesh aliases can match generic numerical terminology.',
            'aliases':ALIASES,'files':entries,'hits':hits}


def audit():
    freeze=json.loads((ROOT/'reports/protocol_v104.freeze.json').read_text())
    for n,h in freeze['sha256'].items(): assert sha(ROOT/n)==h
    sources=verify_sources();exposure=exposure_inventory()
    metadata={n:feature_metadata(SRC/f) for n,f in [('gemm','gemm_VarModel.xml'),('trimesh','TriMesh_VarModel.xml'),('nginx','nginx_FeatureModel.xml')]}
    assert {'tls','basicAuth','compression','keepalive'} <= set(metadata['nginx']['binary'])
    assert {'preSmoothing','postSmoothing'} <= {n['name'] for n in metadata['trimesh']['numeric']}
    decisions=json.loads((ROOT/'configs/admission_v104.json').read_text())
    assert all(d['admitted_recorded_table'] is False for d in decisions['candidates'])
    tree=json.loads((SRC/'dhda_tree.json').read_text())
    inventory=[{k:e[k] for k in ['path','sha','size']} for e in tree['tree'] if e['path'].startswith('drift_data/data6/nginx') and e['type']=='blob']
    return {'stage':'v104_objective_blind_admission','new_model_requests':0,'new_objective_acquisitions':0,
            'new_native_workloads':0,'source_integrity':sources,'feature_metadata':metadata,
            'dhda_nginx_table_inventory_only':inventory,'exposure':exposure,'decisions':decisions,
            'cumulative_download_bytes':9870221104+sources['persisted_http_body_bytes'],
            'remaining_download_bytes':867197136-sources['persisted_http_body_bytes']}


if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    result=audit();target=OUT/'summary.json'
    body=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.verify_only:assert target.read_text()==body
    else:
        OUT.mkdir(parents=True,exist_ok=True)
        with target.open('x') as f:f.write(body)
    print(json.dumps({'verified':args.verify_only,'scanned_files':len(result['exposure']['files']),
        'identity_matches':{k:len(v) for k,v in result['exposure']['hits'].items()},
        'source_integrity':result['source_integrity'],'new_objectives':0,'new_model_requests':0}))
