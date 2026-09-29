"""Metadata/feature-only admission; explicitly avoid parsing objective cells."""
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ROOT/'src'))
from escalation.io import read, write
from escalation.registry_v5 import inspect, feature_model_mismatch
from escalation.admission_v13_1 import exposed_groups
from escalation.transfer_v30 import validate_admission


def sha(p): return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()


def main():
    if (ROOT/'data/manifest_v30.json').exists(): raise ValueError('Preserve admission')
    registry = read(ROOT/'data/registry_v5.json')
    exposed = exposed_groups(read(ROOT/'data/manifest_v3.json'), read(ROOT/'data/manifest_v6.json'))
    aliases = {d['dataset_id'].split('/')[-1].lower(): d['system_group'] for d in registry['datasets'] if d['system_group']}
    logs = []; target_hits = []; observations = 0
    # Inspect existing experiment records, not unacquired data-table targets.
    for path in sorted((ROOT/'results').rglob('*.jsonl')):
        logs.append(str(path.relative_to(ROOT)))
        for line in path.read_text().splitlines():
            row = json.loads(line)
            group = row.get('system_group') or aliases.get(str(row.get('dataset', '')).lower())
            if group:
                exposed.add(group); observations += 1
                if group in ('opus', 'z3'): target_hits.append({'file': str(path.relative_to(ROOT)), 'group': group})
    if target_hits: raise ValueError('Prior outcome/request records found for candidate families')
    paper = read(ROOT/'artifacts/study_v30/source.json')
    if sha(paper['path']) != paper['sha256']: raise ValueError('Changed primary paper')
    sections = (ROOT/'artifacts/study_v30/source_sections.txt').read_text()
    if not all(text in sections for text in ('OPUS', 'Z3', 'Encoding time', 'Solving time')):
        raise ValueError('Missing Table2 metric evidence')
    specs = []
    for name, group, meaning in [('Opus', 'opus', 'recorded audio encoding time; minimize; absolute units not assumed'),
                                  ('z3', 'z3', 'recorded solving time; minimize; absolute units not assumed')]:
        row = next(d for d in registry['datasets'] if d['dataset_id'] == 'ChristianKaltenecker/PerformanceEvolution_Website/'+name)
        s = row['schema']; p = ROOT/row['path']; doc = str((p.parent/'README.md').relative_to(ROOT)); xml = str((p.parent/'FeatureModel.xml').relative_to(ROOT))
        if sha(row['path']) != row['sha256'] or row['finite_domain_feasibility_exclusions']:
            raise ValueError('Source hash or prior quarantine')
        if feature_model_mismatch(ROOT/xml, s['feature_names']): raise ValueError('Feature model mismatch')
        if inspect(p, s['objective_names'], s['metadata_columns'], ';', s['row_filters']) != s:
            raise ValueError('Changed feature-only schema')
        specs.append({'id': name, 'system_group': group, 'path': row['path'], 'sha256': row['sha256'], 'url': row['url'],
            'delimiter': ';', 'feature_names': s['feature_names'], 'objective_columns': s['objective_names'],
            'primary_objective': 'performance', 'direction': '-', 'meaning': meaning,
            'metadata_columns': s['metadata_columns'], 'filters': s['row_filters'], 'rows': s['unique_configurations'],
            'duplicates': s['duplicates'], 'feature_identity_sha256': s['feature_identity_sha256'],
            'evidence': {doc: sha(doc), xml: sha(xml), paper['path']: paper['sha256']},
            'license': 'owner repository GPL-2.0; local use only; original measurement data remain Git ignored',
            'split': 'prospective_transfer', 'selected': True,
            'selection_rule': 'All two unexposed minimization families in this pinned owner collection newly resolved by paper Table2; prior V5 filters unchanged',
            'limitation': 'Single recorded objective; no guarantee of equal output quality or per-row repeat noise estimates'})
    validate_admission(specs, exposed)
    result = {'version': 30, 'datasets': specs, 'seeds': [11,23,37,53,71],
        'objective_values_inspected_before_selection': False, 'historical_exposed_groups': sorted(exposed),
        'scope': 'Prospective classical transfer check on two previously unacquired families; not an LLM/router evaluation',
        'source_paper': paper, 'historical_logs_scanned': {p: sha(p) for p in logs}}
    write(ROOT/'data/manifest_v30.json', result)
    write(ROOT/'artifacts/study_v30/admission.json', {'admitted_families': ['opus', 'z3'], 'historical_log_files': len(logs),
        'records_with_resolved_groups': observations, 'prior_candidate_outcome_records': target_hits,
        'exposed_groups': sorted(exposed), 'objective_values_parsed': 0,
        'qualification': 'No prior acquisitions/model outcomes found in project records; published metadata was consulted. Public benchmark/pretraining exposure remains possible.'})
    print(json.dumps({'admitted': [{'id': d['id'], 'rows': d['rows'], 'filters': d['filters']} for d in specs],
                      'historical_log_files_scanned': len(logs), 'objective_values_parsed': 0}, indent=2))


if __name__ == '__main__': main()
