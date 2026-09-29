"""Verify an extracted review bundle with Python 3.10+ and no dependencies.

Checks included bytes and selected saved results, not a full experiment replay.
Never imports model, optimizer, network or resource-ledger clients.
"""
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True


def require(ok, message):
    if not ok:
        raise ValueError(message)


def read(path):
    return json.loads((ROOT / path).read_text())


def records(path):
    return [json.loads(s) for s in (ROOT / path).read_text().splitlines() if s.strip()]


def main():
    manifest = read('BUNDLE_MANIFEST.json')
    for name, entry in manifest['files'].items():
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and '..' not in parts.parts, 'Unsafe manifest path')
        path = ROOT / name
        require(path.is_file() and not path.is_symlink(), f'Missing/nonregular file: {name}')
        data = path.read_bytes()
        require(len(data) == entry['bytes'] and hashlib.sha256(data).hexdigest() == entry['sha256'],
                f'Changed file: {name}')
    spec = importlib.util.spec_from_file_location('review', ROOT / 'scripts/verify_review_current.py')
    review = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(review)
    stage_counts = {}
    for directory, data, key, count in [('v19_order_probe', 'order_probe_v19', 'outcomes', 9),
                                       ('v21_nonmonotone', 'nonmonotone_probe_v21', 'cases', 3)]:
        base = f'results/{directory}'
        summary = read(f'{base}/summary.json')
        checked = review.checked_selections(read(f'data/{data}.json')['jobs'],
                   records(f'{base}/requests.jsonl'), records(f'{base}/request_starts.jsonl'), summary[key])
        require(len(checked) == summary['completed'] == summary['intended'] == count, 'Denominator mismatch')
        stage_counts[directory] = len(checked)
    with (ROOT / 'results/v6/policies.csv').open() as f:
        policies = {r['policy']: r for r in csv.DictReader(f)}
    heldout = [r for r in read('results/v6/outcomes.json') if r['split'] == 'test']
    groups = {r['system_group'] for r in heldout}
    require(len(heldout) == 15 and len(groups) == 3, 'Held-out denominator')
    for policy, field in [('never', 'classical_loss'), ('always', 'llm_loss')]:
        means = []
        for group in groups:
            values = [r[field] for r in heldout if r['system_group'] == group]
            require(len(values) == 5, 'Seed count')
            means.append(sum(values) / len(values))
        require(math.isclose(sum(means) / len(means), float(policies[policy]['group_mean_loss']), abs_tol=1e-14),
                'Policy arithmetic mismatch')
    print(json.dumps({'verified': True, 'included_files': len(manifest['files']),
                      'raw_response_mappings_checked': stage_counts, 'heldout_policy_cases_checked': len(heldout),
                      'omitted_frozen_input_paths': len(read('OMITTED_FROZEN_INPUTS.json')['files']),
                      'scope': 'Included-byte integrity, raw selection mappings and never/always summary arithmetic only',
                      'not_checked': ['absent source/model bytes', 'inference replay', 'controller refit', 'fresh experiments'],
                      'new_model_calls': 0, 'new_objective_acquisitions': 0}, indent=2))


if __name__ == '__main__':
    main()
