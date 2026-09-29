"""Original archive census: configuration features only, no target conversion."""
import csv,hashlib,io,json,math,re,zipfile
from pathlib import Path,PurePosixPath
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'artifacts/sources/v118'
OUT=ROOT/'results/v118_archive'

def feature_census(stream):
    reader=csv.reader(stream);header=next(reader)
    if len(header)<3 or len(set(header))!=len(header) or header[-2:]!=['throughput','latency']:
        raise ValueError('Unexpected original archive schema')
    names=header[:-2];rows=[]
    for row in reader:
        if len(row)!=len(header):raise ValueError('Malformed record')
        f=tuple(float(v) for v in row[:-2])
        if not all(map(math.isfinite,f)):raise ValueError('Nonfinite feature')
        rows.append(f)
    return names,rows

def signature(names,rows):
    norm=[re.sub('[^a-z0-9]','',n.lower()) for n in names]
    if len(set(norm))!=len(norm):raise ValueError('Ambiguous feature normalization')
    order=sorted(range(len(norm)),key=lambda i:norm[i]);keys=[norm[i] for i in order]
    vectors=sorted({tuple(r[i] for i in order) for r in rows})
    return hashlib.sha256(json.dumps([keys,vectors],separators=(',',':')).encode()).hexdigest()

def safe_member(name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts:raise ValueError('Unsafe member path')
    return name.startswith('bo4co_dataset/') and name.endswith('.csv')

def audit():
    for fn in ['reports/protocol_v118.freeze.json','artifacts/study_v118/audit.freeze.json']:
        for n,h in json.loads((ROOT/fn).read_text())['sha256'].items():assert hashlib.sha256((ROOT/n).read_bytes()).hexdigest()==h,n
    record=json.loads((SRC/'record.json').read_text());archive=(SRC/'bo4co_dataset.zip').read_bytes()
    f=record['files'][0];assert len(record['files'])==1 and f['key']=='bo4co_dataset.zip'
    assert len(archive)==f['size'] and 'md5:'+hashlib.md5(archive).hexdigest()==f['checksum']
    sourceledger=json.loads((SRC/'manifest.json').read_text());total=sum(x['bytes'] for x in sourceledger['attempts'])
    assert total<=1024**2
    for a in sourceledger['attempts']:
        assert a['status']=='complete'
        b=(SRC/a['name']).read_bytes();assert len(b)==a['bytes'] and hashlib.sha256(b).hexdigest()==a['sha256']
    import sys
    sys.path.insert(0,str(ROOT/'src'))
    from escalation.admission_v52 import feature_rows,sha256
    registry=json.loads((ROOT/'data/registry_v5.json').read_text())['datasets'];aliases={}
    for d in registry:
        if d['source']=='MOOT' and d['system_group']=='storm':
            p=ROOT/d['path'];assert sha256(p)==d['sha256'];s=d['schema']
            sig=signature(s['feature_names'],feature_rows(p,s['feature_names'],s['objective_names']))
            aliases.setdefault(sig,[]).append(d['dataset_id'])
    inventory=[];tables=[]
    with zipfile.ZipFile(io.BytesIO(archive)) as z:
        assert sum(i.file_size for i in z.infolist())<2*1024**2
        for i in z.infolist():
            accepted=safe_member(i.filename);inventory.append({'name':i.filename,'bytes':i.file_size,'configuration_table':accepted})
            if not accepted:continue
            b=z.read(i);names,rows=feature_census(io.StringIO(b.decode('utf-8-sig')))
            sig=signature(names,rows)
            tables.append({'member':i.filename,'sha256':hashlib.sha256(b).hexdigest(),'features':names,'targets_from_header':['throughput','latency'],
              'rows':len(rows),'unique_configurations':len(set(rows)),'feature_signature':sig,
              'feature_only_moot_matches':aliases.get(sig,[]),'target_cells_converted':0})
    assert len(tables)==10
    return {'scope':'Original BO4CO archived features/schema/license, not original performance outcomes or an admitted optimizer experiment',
      'record_doi':record['metadata']['doi'],'record_license':record['metadata']['license'],
      'zip_sha256':hashlib.sha256(archive).hexdigest(),'zip_md5':hashlib.md5(archive).hexdigest(),'inventory':inventory,'tables':tables,
      'source_bytes':total,'new_model_calls':0,'new_objective_acquisitions':0,'admitted':False,
      'remaining_gaps':['No per-attempt validation/failure log or executed-code manifest present in this deposit; only ten CSV tables plus OS metadata.','Feature equality does not prove objective values or transformations match derivative MOOT tables.','Published description10min versus paper8min and later source metric substitutions remain unresolved.','Cannot certify historical metric type or all successful output semantics from table headers alone.']}

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');a=p.parse_args();r=audit()
    body=json.dumps(r,indent=2,sort_keys=True)+'\n';target=OUT/'summary.json'
    if a.verify_only:assert target.read_text()==body
    else:OUT.mkdir(exist_ok=False);target.write_text(body)
    print(json.dumps({'verified':a.verify_only,'source_bytes':r['source_bytes'],'license':r['record_license'],'tables':[{'member':t['member'],'rows':t['rows'],'unique':t['unique_configurations'],'feature_matches':t['feature_only_moot_matches']} for t in r['tables']],'admitted':r['admitted']}))
