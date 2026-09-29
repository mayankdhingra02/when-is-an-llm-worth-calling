"""Reproduce V52 without network, target conversion, optimizers or inference."""
import datetime
import json
import sys
import time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.admission_v52 import (GATES, RESERVED, eligible, equivalence_counts,
                                     feature_rows, model_comparison, sha256)


def main():
    started = time.monotonic()
    out = ROOT / 'results/v52_admission'
    out.mkdir(parents=True, exist_ok=True)
    result = out / 'summary.json'
    if result.exists():
        raise FileExistsError('V52 is one-shot; do not overwrite prior evidence')
    freeze = json.loads((ROOT / 'reports/protocol_v52_admission.freeze.json').read_text())
    for path, digest in freeze['files'].items():
        assert sha256(ROOT / path) == digest, path
    for source in json.loads((ROOT / 'artifacts/sources/v52/manifest.json').read_text()):
        assert sha256(ROOT / source['path']) == source['sha256'], source['path']
    registry = json.loads((ROOT / 'data/registry_v5.json').read_text())['datasets']
    by_id = {d['dataset_id']: d for d in registry}
    decisions = json.loads((ROOT / 'data/admission_evidence_v52.json').read_text())
    computed = {}
    d = by_id['MOOT/dconvert']
    assert sha256(ROOT / d['path']) == d['sha256']
    computed['dconvert'] = equivalence_counts(
        feature_rows(ROOT / d['path'], d['schema']['feature_names'], d['schema']['objective_names']),
        {d['schema']['feature_names'].index('threads')})
    computed['dconvert']['contract'] = 'Fix every feature except threads; conservative same-output contract.'
    computed['dconvert']['target_values_converted'] = 0
    gc = by_id['MOOT/javagc']
    computed['javagc'] = {name: model_comparison(ROOT / 'artifacts/sources/v52' / name,
                                              gc['schema']['feature_names'])
                         for name in ('javagc_fse15.xml', 'javagc_features.xml')}
    for record in decisions:
        group = record['group']
        record['split_reservation'] = 'future_evaluation' if group in RESERVED else 'development_candidate'
        tables = [d for d in registry if d['system_group'] == group]
        record['table_inventory'] = [{'dataset_id': d['dataset_id'], 'sha256': d['sha256'],
                                     'unique_configurations': d['schema']['unique_configurations'],
                                     'features': len(d['schema']['feature_names']),
                                     'objective_headers': d['schema']['objective_names'],
                                     'prior_collection_admitted': d.get('collection_admitted', False)}
                                    for d in tables]
        if group == 'dconvert':
            n = computed['dconvert']['largest_contract_configurations']
            record['gates']['feasibility']['status'] = 'verified' if n >= 40 else 'contradicted'
            record['gates']['feasibility']['detail'] = f'Largest fixed-output contract has {n} unique settings; needs 40.'
        record['eligible'] = eligible(record)
        record['blocking_gates'] = [g for g in GATES if record['gates'][g]['status'] != 'verified']
    payload = {'study': 'v52', 'completed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'families': decisions, 'computed_feature_checks': computed,
               'eligible_families': [r['group'] for r in decisions if r['eligible']],
               'families_audited': len(decisions), 'recorded_objective_acquisitions': 0,
               'physical_trials': 0, 'model_requests': 0, 'external_spend_usd': 0,
               'runtime_seconds': time.monotonic() - started,
               'scope': 'Outcome-blind admission only. Historical values remain unscored; no classical screen authorized by failed gates.'}
    result.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps({k: v for k, v in payload.items() if k not in ('families', 'computed_feature_checks')}, indent=2))
    print(json.dumps(computed, indent=2))


if __name__ == '__main__':
    main()
