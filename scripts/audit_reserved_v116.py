"""Outcome-blind reserved-family feasibility and reproducible exposure inventory."""
import argparse, hashlib, json, math, re, time
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from escalation.admission_v52 import feature_rows, equivalence_counts, sha256
SRC=ROOT/'artifacts/sources/v116'
OUT=ROOT/'results/v116_admission'
CONTRACTS={
 'MOOT/SS-V':['journal','nojournal','ssl','wireObjectCheck','journalCommitInterval'],
 'MOOT/storm':['Message.size','Topology.acker.executors','topology.level'],
 'MOOT/SS-K':[], 'MOOT/SS-I':[],
 'MOOT/SS-J':['Message_size','Chunk_size','Emit_freq'],
 'MOOT/redis':[],
}
# Feature partitions are illustrative necessary coverage checks, never proof of utility.

def partition(path,names,targets,fixed):
    if not set(fixed)<=set(names):raise ValueError('Unknown contract column')
    rows=list(feature_rows(path,names,targets))
    if any(not math.isfinite(v) for r in rows for v in r):raise ValueError('Nonfinite feature')
    free={i for i,n in enumerate(names) if n not in fixed}
    return {'fixed_columns':fixed,**equivalence_counts(rows,free),
      'certifies_utility_equivalence':False,'objective_values_converted':0}

def verify_sources():
    m=json.loads((SRC/'manifest.json').read_text());total=0;checks=[]
    rev=json.loads((SRC/'bo_ref_retry.json').read_text())['object']['sha']
    tree=json.loads((SRC/'bo_tree.json').read_text());assert tree['sha']==rev and not tree['truncated']
    blobs={e['path']:e for e in tree['tree'] if e['type']=='blob'}
    for a in m['attempts']:
        total+=a['bytes'];p=SRC/a['name']
        assert a['status'] in ['complete','failed']
        if a['bytes']:
            assert sha256(p)==a['sha256'] and p.stat().st_size==a['bytes']
        else:assert not p.exists()
        if a['status']=='complete' and 'raw.githubusercontent.com/' in a['url']:
            remote=a['url'].split('/'+rev+'/')[1];b=p.read_bytes()
            actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            assert actual==blobs[remote]['sha'];checks.append({'path':remote,'local':a['name'],'git_blob_sha1':actual})
    assert total<=10*1024**2 and total<861515123
    return {'revision':rev,'inventory_entries':len(tree['tree']),'blob_checks':checks,
      'persisted_body_bytes':total,'attempts':len(m['attempts']),'failures':sum(a['status']=='failed' for a in m['attempts'])}

def exposure(registry,scope):
    tokens={}
    for d in registry:
        if d['system_group'] in ['mongodb','redis','storm']:
            for t in [d['system_group'],d['dataset_id'],Path(d['path']).stem]:tokens.setdefault(t.lower(),set()).add(d['system_group'])
    # One regex pass per document; exact token boundaries avoid names embedded in unrelated identifiers.
    pat=re.compile(rb'(?<![a-z0-9])(?:'+b'|'.join(re.escape(t.encode()) for t in sorted(tokens,key=len,reverse=True))+rb')(?![a-z0-9])',re.I)
    hits=[];start=time.monotonic();total=0
    for n,meta in sorted(scope.items()):
        if time.monotonic()-start>180:raise TimeoutError('Exposure scan180s cap')
        p=ROOT/n;b=p.read_bytes();assert len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256'],n
        total+=len(b);found=sorted({m.group().decode().lower() for m in pat.finditer(b)})
        if found:
            hits.append({'path':n,'sha256':meta['sha256'],'tokens':found,'possible_groups':sorted(set().union(*(tokens[t] for t in found)))})
    return {'files':len(scope),'bytes':total,'hits':hits,'certified_untouched':False,
      'limitations':['Only saved structured result files and top-level manifests inventoried; absent names are not proof of no exposure.','External/deleted/unnamed outcomes not discoverable; variants remain one family.','Redis has native V60 measurements and cannot be declared an untouched family.']}

def audit():
    for f in ['reports/protocol_v116.freeze.json','artifacts/study_v116/audit.freeze.json']:
        for n,h in json.loads((ROOT/f).read_text())['sha256'].items():assert sha256(ROOT/n)==h,n
    registry=json.loads((ROOT/'data/registry_v5.json').read_text())['datasets'];byid={d['dataset_id']:d for d in registry}
    partitions={}
    for key,fixed in CONTRACTS.items():
        d=byid[key];assert sha256(ROOT/d['path'])==d['sha256']
        partitions[key]=partition(ROOT/d['path'],d['schema']['feature_names'],d['schema']['objective_names'],fixed)
    scope=json.loads((ROOT/'artifacts/study_v116/exposure_scope.json').read_text())
    return {'stage':'v116_reserved_family_admission','new_model_requests':0,'new_objective_acquisitions':0,'new_native_workloads':0,
      'sources':verify_sources(),'feature_partitions':partitions,'exposure':exposure(registry,scope),
      'decisions':json.loads((ROOT/'configs/admission_v116.json').read_text()),'admitted_groups':[]}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--verify-only',action='store_true');args=ap.parse_args()
    d=audit();body=json.dumps(d,sort_keys=True,indent=2)+'\n';out=OUT/'summary.json'
    if args.verify_only:assert out.read_text()==body
    else:
        OUT.mkdir(exist_ok=False)
        out.write_text(body)
    print(json.dumps({'verified':args.verify_only,'source_bytes':d['sources']['persisted_body_bytes'],
      'feature_partitions':d['feature_partitions'],'scanned_files':d['exposure']['files'],'hit_files':len(d['exposure']['hits']),'admitted_groups':[]}))
