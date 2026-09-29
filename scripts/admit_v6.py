"""Outcome-blind semantic admission from pinned case READMEs; no objective reads."""
import sys, json, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import write,read,digest
from escalation.data import sha
from escalation.registry_v5 import inspect,feature_model_mismatch

# Explicit primary documentation, not inference from a generic column name.
CASES={
 'brotli':('brotli','-','compression runtime in seconds','uiq-generated compression workload; per-case README preferred over inconsistent global size summary'),
 'HSQLDB':('hsqldb','-','runtime; source does not state unit here','PolePosition 0.6.0 custom configuration'),
 'MySQL':('mysql_family','-','runtime; source does not state unit here','sysbench 1.0.17 oltp_read_write, 10000 events; specific case README takes precedence over global PolePosition description'),
 'OpenVPN':('openvpn','+','throughput in Mbit/s','iperf 3.6 client-to-server TCP, uiq2 payload'),
 'PostgreSQL':('postgresql','-','runtime; source does not state unit here','PolePosition 0.6.0 custom configuration'),
 'VP8':('libvpx','-','encoding runtime; source does not state unit here','lossless Sintel trailer y4m 480p to VP8 webm; v0.9.1 predates >=v1.4.0 alias warning'),
 'lrzip':('lrzip','-','compression runtime; source does not state unit here','621 MB uiq2 file in case README; global summary says about 100 MB, unresolved payload-size discrepancy retained'),
}

def build():
 registry=read(ROOT/'data/registry_v5.json'); admitted=[]
 for name,(group,direction,meaning,workload) in CASES.items():
  row=next(r for r in registry['datasets'] if r['dataset_id']=='ChristianKaltenecker/PerformanceEvolution_Website/'+name)
  s=row['schema'];p=ROOT/row['path'];doc=p.parent/'README.md';xml=p.parent/'FeatureModel.xml'
  assert sha(p)==row['sha256'] and not feature_model_mismatch(xml,s['feature_names'])
  assert not row['finite_domain_feasibility_exclusions']
  assert inspect(p,s['objective_names'],s['metadata_columns'],';',s['row_filters'])==s
  admitted.append({'id':name,'system_group':group,'path':row['path'],'sha256':row['sha256'],'url':row['url'],
    'delimiter':';','feature_names':s['feature_names'],'objective_columns':s['objective_names'],'primary_objective':'performance',
    'direction':direction,'meaning':meaning,'workload':workload,'metadata_columns':s['metadata_columns'],'filters':s['row_filters'],
    'rows':s['unique_configurations'],'duplicates':s['duplicates'],'feature_identity_sha256':s['feature_identity_sha256'],
    'evidence':{str(doc.relative_to(ROOT)):sha(doc),str(xml.relative_to(ROOT)):sha(xml)},
    'license':'owner repository GPL-2.0; raw data kept outside shareable Git history; no third-party algorithm code reused',
    'revision_rule':'lexicographically first recorded revision, not chronologically earliest; no outcome-based selection',
    'admission':'local offline single-target adaptation; no guarantee of matched output quality across configurations'})
 ranked=sorted(admitted,key=lambda d:hashlib.sha256(('v6-bounded:'+d['system_group']).encode()).hexdigest())
 for i,d in enumerate(ranked):
  d['selected']=i<6;d['split']=('development' if i<3 else 'test') if i<6 else 'unused'
 report={'version':6,'basis_registry_sha256':sha(ROOT/'data/registry_v5.json'),'datasets':ranked,
 'rule':'seven README-supported families; first six by SHA256(v6-bounded:family), first three development, next three test; five fixed seeds',
 'seeds':[11,23,37,53,71],'new_families':6,'scope':'exploratory expanded binary-data smoke with a finite-domain-capable interface; insufficient generalization evidence',
 'deferred':{g:'not admitted: original target/transformation, workload/revision evidence remains incomplete' for g in registry['summary']['finite_domain_candidate_families'] if g not in {r['system_group'] for r in ranked}},
 'specific_exclusions':{'MariaDB':'same family represented by MySQL; conflicting crash-gap revision metadata not resolved',
 'VP9':'same family represented by earlier VP8; no independent group', 'FastDownward':'CSV/feature-model mismatch',
 'Opus':'README specifies workload but does not explicitly establish performance unit/direction',
 'z3':'README specifies fixed LRA workload but not explicit performance unit/direction'},
 'objective_values_inspected':False}
 write(ROOT/'data/manifest_v6.json',report)
 print(json.dumps([{'id':d['id'],'group':d['system_group'],'split':d['split'],'direction':d['direction'],'revision':d['filters']['revision']} for d in ranked],indent=2))
if __name__=='__main__':build()
