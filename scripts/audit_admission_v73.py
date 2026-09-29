"""Recompute source integrity and feature-only admission facts; no timings read."""
import csv
import hashlib
import json
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.admission_v73 import original_vector,released_vector,FEATURES
SOURCE=ROOT/'artifacts/sources/v73'
def read(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def audit():
    for freeze in ROOT.glob('reports/protocol_v73*.freeze.json'):
        for name,digest in read(freeze)['sha256'].items():assert sha(ROOT/name)==digest,name
    manifest=read(SOURCE/'manifest.json');ranges=read(SOURCE/'range_manifest.json')
    for item in manifest['entries']:assert sha(SOURCE/item['name'])==item['sha256']
    for item in ranges['ranges']:assert sha(SOURCE/item['file'])==item['sha256']
    for proof in SOURCE.glob('*.provenance.json'):
        info=read(proof);assert sha(proof.with_name(proof.name.removesuffix('.provenance.json')))==info['sha256']
    record=read(SOURCE/'zenodo_record.json');latest=read(SOURCE/'zenodo_latest.json')
    for name,filename in [('README.md','README_1_1.md'),('LICENCSE.md','LICENSE_1_1.md'),('accepted_paper.pdf','accepted_paper.pdf')]:
        info=next(f for f in record['files'] if f['key']==name)
        assert 'md5:'+hashlib.md5((SOURCE/filename).read_bytes()).hexdigest()==info['checksum']
    a=list(csv.DictReader((SOURCE/'kanzi_original_configurations.csv').open()))
    b=list(csv.DictReader((SOURCE/'kanzi_configurations.csv').open()))
    av=[original_vector(r) for r in a];bv=[released_vector(r) for r in b]
    assert len(set(av))==len(av) and len(set(bv))==len(bv)
    omitted=set(av)-set(bv); extra=set(bv)-set(av)
    model=ET.parse(SOURCE/'kanzi_features.xml').getroot()
    jobs=next(x for x in model.iter('alt') if x.attrib.get('name')=='jobs')
    model_jobs=[x.attrib['name'] for x in jobs]
    partitions={}
    contracts={'kanzi':['checksum'],'h2':['MVSTORE','IGNORE_CATALOGS','DROP_RESTRICT'],
       'batik':['tiff','jpg','png','pdf','onload','anyScriptOrigin','validate','dpi','resolution','quality','indexed'],
       'z3':['dump_models','model','model_validate','proof','smtlib2_compliant','stats','trace','unsat_core','type_check','well_sorted_check']}
    for system,keys in contracts.items():
        rows=list(csv.DictReader((SOURCE/f'{system}_configurations.csv').open()))
        assert not any(k.lower() in ['time','runtime','performance','throughput','latency'] for k in rows[0])
        fields=[k for k in rows[0] if k!='config_id'];groups=defaultdict(set)
        for row in rows:groups[tuple(row[k] for k in keys)].add(tuple(row[k] for k in fields))
        partitions[system]={'raw_rows':len(rows),'unique_vectors':len({tuple(r[k] for k in fields) for r in rows}),
           'conservative_exploratory_partition_fields':keys,'contracts':len(groups),'largest_partition':max(map(len,groups.values())),
           'semantic_status':'Illustrative conservative partition; not certified utility equivalence or held-out admission'}
    total=sum(x['bytes'] for x in manifest['entries'])+sum(x['bytes'] for x in ranges['ranges'])
    assert total<=10*1024**2
    return {'source_version':latest['metadata']['version'],'source_record':latest['id'],
        'archive_members_declared':327963,'partial_directory_entries_inspected':len(read(SOURCE/'partial_inventory.json')),
        'full_archive_md5_verified':False,'objective_members_opened':0,
        'kanzi':{'original_vectors':len(av),'released_vectors':len(bv),'original_unique_ids':len({r[''] for r in a}),
            'omitted_vectors':len(omitted),'released_vectors_not_in_original':len(extra),'omitted_vector_hashes':sorted(hashlib.sha256(json.dumps(x).encode()).hexdigest() for x in omitted),
            'checksum_enabled_released_vectors':sum(r['checksum']=='True' for r in b),
            'feature_model_jobs':model_jobs,'sample_jobs':sorted({r['jobs'] for r in b}),
            'admission':'not admitted: per-attempt failures/correctness and exact source-to-row mapping unresolved'},
        'configuration_partitions':partitions,
        'license_discrepancy':{'zenodo_metadata':latest['metadata']['license']['id'],'included_license_heading':'CC BY-SA4.0','included_link':'CC BY4.0','status':'record discrepancy; do not assert resolved redistribution terms'},
        'persistent_download_bytes':total,'persistent_total_download_bytes':4800270357+total,
        'remaining_download_bytes':568438763-total,'new_model_calls':0,'new_objective_acquisitions':0,'new_physical_benchmarks':0,'external_spend_usd':0}

if __name__=='__main__':
    out=ROOT/'results/v73_admission';out.mkdir(exist_ok=False)
    result=audit();(out/'summary.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ['kanzi','configuration_partitions']},indent=2))
