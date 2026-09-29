"""Inspect all pinned configuration/system tables without reading objective values."""
import json,sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.registry import inspect_features,SYSTEMS,eligibility,split_groups
sources=json.loads((ROOT/'artifacts/registry_v4/sources.json').read_text());rows=[]
for item in sources['files']:
    if not item['path'].endswith('.csv'):continue
    if hashlib.sha256((ROOT/item['path']).read_bytes()).hexdigest()!=item['sha256']:
        raise ValueError('registry source hash mismatch')
    name=Path(item['path']).stem;group=SYSTEMS.get(name)
    row={**item,'dataset_id':name,'system_group':group,
         'identity_status':'source_named' if group else 'quarantined_unresolved',
         'identity_evidence':'MOOT pinned systems/config README and explicit option names; see registry audit',
         'aliases':sorted(k for k,v in SYSTEMS.items() if v==group) if group else [name],
         'original_workload_version':'unresolved','hardware':'unresolved',
         'license':'MIT repository-level; upstream lineage not assumed',
         'schema':inspect_features(ROOT/item['path'])}
    row['exclusion_reasons']=eligibility(row);rows.append(row)
registry={'version':4,'moot_commit':sources['commit'],'selection_uses_objective_values':False,
          'criteria':'source-named untouched systems; binary 1-39 features; one objective; 20-5000 unique rows',
          'target_groups':20,'test_groups':8,'datasets':rows,'split':split_groups(rows)}
(ROOT/'data/registry_v4.json').write_text(json.dumps(registry,indent=2)+'\n')
summary={'tables':len(rows),'source_named_groups':len({r['system_group'] for r in rows if r['system_group']}),
         'eligible_untouched_groups':sorted({r['system_group'] for r in rows if not r['exclusion_reasons']}),
         'quarantined_tables':sum(r['system_group'] is None for r in rows),'split':registry['split'],
         'objective_values_inspected':False}
(ROOT/'artifacts/registry_v4/summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary,indent=2))
for r in rows:print(r['dataset_id'],len(r['schema']['feature_names']),r['schema']['unique_configurations'],','.join(r['exclusion_reasons']) or 'ELIGIBLE')
