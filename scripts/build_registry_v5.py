"""Build a versioned, outcome-blind registry and exact feature-only alias matches."""
import csv,hashlib,json,sys,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.registry_v5 import inspect,metadata_values,family,schema_reasons,feature_model_mismatch
read=lambda p:json.loads((ROOT/p).read_text())
VEER={'SS-A':'hsqldb','SS-B':'mariadb','SS-C':None,'SS-D':'vp8','SS-E':'vp9',
      'SS-F':'storm','SS-G':'lrzip','SS-H':'x264','SS-I':'mongodb','SS-J':'llvm','SS-K':'exastencils'}
# SS-C has anonymized headers that contradict the paper's five-feature description.
# Keep it unresolved rather than propagating the paper's label to an incompatible file.
rows=[]
for d in read('data/registry_v4.json')['datasets']:
    s=inspect(ROOT/d['path'],d['schema']['objective_names'])
    rows.append({k:d[k] for k in ['path','upstream_path','sha256','url']}|{
        'source':'MOOT','dataset_id':'MOOT/'+d['dataset_id'],'system_group':family(d['system_group']) if d['system_group'] else None,
        'identity_basis':'MOOT named catalogue' if d['system_group'] else 'unresolved',
        'schema':s,'objective_semantics':'MOOT direction header; original transformation not independently verified',
        'admission':'candidate_only'})
for d in read('artifacts/registry_v5/sources.json'):
    if not d['path'].endswith('.csv'):continue
    path=ROOT/d['path'];assert hashlib.sha256(path.read_bytes()).hexdigest()==d['sha256']
    repo=d['repo'];metadata=[];filters={};delim=',';revisions=[]
    if repo=='DeepPerf/DeepPerf':
        system=path.stem.removesuffix('_AllNumeric');header=next(csv.reader(path.open()))
        objectives=[header[-1]];basis='DeepPerf owner README named system; explicit last-column performance schema'
    elif repo=='anonymous12138/multiobj':
        system=VEER[path.stem];header=next(csv.reader(path.open()))
        objectives=[h for h in header if h.startswith(('<$','>$'))]
        basis='VEER v3 Table 2 and linked artifact; SS-C quarantined due schema mismatch'
    else:
        system=path.parent.name;delim=';';header=next(csv.reader(path.open(),delimiter=delim))
        # Explicit nonfunctional-property names from table/model documentation.
        objectives=[h for h in header if h in ['performance','cpu','size','memory','energy','benchmark-energy','fixed-energy','benchmark-power','fixed-power']]
        metadata=['revision'];revisions=metadata_values(path,'revision',delim);filters={'revision':revisions[0]}
        if system=='z3':filters.update({'LRA':'1','QF_FP':'0','QF_LRA':'0','QF_UFLRA':'0'})
        basis='owner directory/README and feature model; lexicographically first revision; z3 fixed LRA workload'
    s=inspect(path,objectives,metadata,delim,filters)
    rows.append({k:d[k] for k in ['path','upstream_path','sha256','url']}|{
        'source':repo,'dataset_id':repo+'/'+(path.parent.name if 'Evolution' in repo else path.stem),
        'system_group':family(system) if system else None,'identity_basis':basis,
        'schema':s,'all_revisions':revisions,
        'objective_semantics':'explicit primary metadata review required before collection',
        'admission':'candidate_only'})
# Exact names + full distinct feature matrix, ignoring case/punctuation only.
# Identity matches do not assert objective equality or provenance equivalence.
matched=[]
for row in rows:
    if row['source']!='MOOT' or row['system_group']:continue
    peers=[p for p in rows if (p['source']!='MOOT' or p['identity_basis']=='MOOT named catalogue') and p['system_group'] and
           p['schema']['feature_identity_sha256']==row['schema']['feature_identity_sha256']]
    groups={p['system_group'] for p in peers}
    if len(groups)==1:
        row['system_group']=groups.pop();row['identity_basis']='exact normalized names and distinct feature matrix match to named original artifact'
        row['feature_matches']=[p['dataset_id'] for p in peers];matched.append({'dataset':row['dataset_id'],'group':row['system_group'],'matches':row['feature_matches']})
# Family-level metadata mapping from FLASH's original Table 1. This does not
# claim equality of objective payloads or exact source-table hashes.
flash_storm={'SS-A','SS-C','SS-D','SS-E','SS-F','SS-G','SS-I','SS-K',
             'sol-6d-c2-obj1','wc+rs-3d-c4-obj1','wc+sol-3d-c4-obj1',
             'wc+wc-3d-c4-obj1','wc-6d-c1-obj1'}
for row in rows:
    row['task_kind']='software_configuration'
    row['feature_model_mismatch']=None
    if row['source']=='ChristianKaltenecker/PerformanceEvolution_Website':
        row['feature_model_mismatch']=feature_model_mismatch(ROOT/Path(row['path']).parent/'FeatureModel.xml',row['schema']['feature_names'])
    if row['source']=='MOOT' and not row['system_group']:
        name=row['dataset_id'].split('/')[-1]
        if name in flash_storm:
            row['system_group']='storm'
            row['identity_basis']='FLASH Table 1 / MoConfig Table I workload-family metadata; not exact file equivalence'
        elif name=='HSMGP_num':
            row['system_group']='dune_hsmgp'
            row['identity_basis']='DeepPerf named HSMGP and matching option names; original multigrid study, conservatively grouped with DUNE'
        elif name in {'SS-B','SS-H'}:
            row['system_group']={'SS-B':'fpga_sort256','SS-H':'noc_cm_log'}[name]
            row['task_kind']='hardware_design'
            row['identity_basis']='FLASH Table 1 hardware-design identity and dimensions; excluded from software scope'
for row in rows:
    reasons=[]
    if row['task_kind']!='software_configuration':reasons.append('outside_software_configuration_scope')
    if row['feature_model_mismatch']:reasons.append('feature_model_header_mismatch')
    if row['system_group'] is None:reasons.append('unresolved_identity')
    if row['system_group'] in {'apache','sqlite','x264'}:reasons.append('previously_exposed_family')
    row['binary_with_target_selection_exclusions']=reasons+schema_reasons(row['schema'])
    row['v4_binary_schema_exclusions']=row['binary_with_target_selection_exclusions']+([] if len(row['schema']['objective_names'])==1 else ['requires_single_objective'])
    row['finite_domain_feasibility_exclusions']=reasons+schema_reasons(row['schema'],64,200000,False)
    # Multiple objective columns are never silently converted to feature inputs.
    # A future amended protocol must select its target by semantics, not scores.
    row['selected_primary_objective']=None
    row['collection_admitted']=False
summary={'tables_audited':len(rows),'feature_verified_alias_matches':matched,
         'binary_with_target_selection_candidate_families':sorted({r['system_group'] for r in rows if not r['binary_with_target_selection_exclusions']}),
         'strict_v4_schema_candidate_families':sorted({r['system_group'] for r in rows if not r['v4_binary_schema_exclusions']}),
         'finite_domain_candidate_families':sorted({r['system_group'] for r in rows if not r['finite_domain_feasibility_exclusions']}),
         'objective_values_inspected':False,'collection_admitted':False,
         'caveat':'Schema candidates only. Multi-objective files require a frozen semantic target selection; licenses/lineage and representation require review. No split is issued.'}
(ROOT/'data/registry_v5.json').write_text(json.dumps({'version':5,'previous_registry_sha256':hashlib.sha256((ROOT/'data/registry_v4.json').read_bytes()).hexdigest(),'datasets':rows,'summary':summary},indent=2)+'\n')
(ROOT/'artifacts/registry_v5/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
for r in rows:
 if r['source']=='ChristianKaltenecker/PerformanceEvolution_Website':print(r['dataset_id'],r['schema']['row_filters'],r['schema']['unique_configurations'],r['schema']['binary'])
