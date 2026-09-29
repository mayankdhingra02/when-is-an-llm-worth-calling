"""Execute a pinned source-only admission audit; never open outcome tables."""
import ast
import hashlib
import json
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'artifacts/sources/v68'
OUT = ROOT / 'results/v68_admission'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compute():
    started = time.monotonic()
    manifest = json.loads((SRC / 'manifest.json').read_text())
    for name, meta in manifest['files'].items():
        path = SRC / name
        assert path.stat().st_size == meta['bytes'] and sha(path) == meta['sha256'], name
        assert '/data/' not in name and not name.endswith(('.res', '.joblib', '.csv', '.pkl')), name
    inventory = {}
    for repo in ('knobs', 'ycsb', 'benchbase'):
        tree = json.loads((SRC / repo / 'tree.json').read_text())
        assert not tree['truncated']
        blobs = [x for x in tree['tree'] if x['type'] == 'blob']
        inventory[repo] = {
            **json.loads((SRC / repo / 'pin.json').read_text()),
            'blobs': len(blobs),
            'license_paths': [x['path'] for x in blobs if Path(x['path']).name.lower().startswith(('license', 'copying'))],
            'data_paths_metadata_only': [{'path': x['path'], 'bytes': x['size']} for x in blobs
                if x['path'].startswith('tuning_benchmark/data/')],
        }
    domains = json.loads((SRC / 'knobs/source/scripts/experiment/gen_knobs/mysql_all_197.json').read_text())
    # Unranked declared domains only; never load outcome-derived SHAP rankings.
    semantic_keys = ['innodb_doublewrite', 'innodb_flush_log_at_trx_commit', 'sync_binlog']
    varying_semantics = {k: domains[k] for k in semantic_keys}
    parser_source = (SRC / 'knobs/source/autotune/utils/parser.py').read_text()
    parser_tree = ast.parse(parser_source)
    function = next(n for n in parser_tree.body if isinstance(n, ast.FunctionDef) and n.name == 'parse_sysbench')
    used_interval_columns = sorted({n.slice.value for n in ast.walk(function)
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == 'i'
        and isinstance(n.slice, ast.Constant)})
    assert used_interval_columns == [0, 1, 5]
    assert 'err/s:' in parser_source and 'reconn/s:' in parser_source
    y = (SRC / 'ycsb/source/core/src/main/java/site/ycsb/workloads/CoreWorkload.java').read_text()
    verifier = y.split('protected void verifyRow(', 1)[1].split('long nextKeynum()', 1)[0]
    assert 'cells.entrySet()' in verifier and '!cells.isEmpty()' in verifier
    assert 'cells.size()' not in verifier and 'fieldnames' not in verifier
    assert 'DATA_INTEGRITY_PROPERTY_DEFAULT = "false"' in y
    decisions = {
        'knobs_measured_replay': {
            'admitted': False, 'group': 'mysql', 'declared_knobs': len(domains),
            'independent_workloads_are_not_independent_systems': True,
            'varying_utility_sensitive_domains': varying_semantics,
            'sysbench_interval_columns_used': used_interval_columns,
            'sysbench_error_and_reconnect_columns_used': False,
            'reasons': ['No reuse license found in complete pinned tree or setup metadata.',
                'Fixed durability/integrity contract not established across the published knob domain.',
                'Measurement parser does not retain sysbench error/reconnect columns in returned metric vector.',
                'No verified raw-attempt to released-training-row mapping; failure denominator unresolved.',
                'The surrogate execution path predicts outcomes; it is not new physical measurement.'],
            'configuration_count_at_fixed_utility': None,
            'minimum_400_configuration_gate': 'not_evaluated_prerequisites_failed',
        },
        'ycsb_harness': {
            'admitted_as_measured_dataset': False, 'usable_as_workload_source': True,
            'release': '0.17.0', 'license': 'Apache-2.0',
            'integrity_default': False, 'all_requested_fields_verified': False,
            'reasons': ['A workload harness is not a recorded configuration-response table.',
                'Integrity mode checks returned fields, not requested-field completeness.',
                'Fresh backend/domain/build and complete response checks are still needed.'],
            'selected_followup': 'read-only workload C with explicit integrity and complete-field validation',
        },
        'benchbase_harness': {
            'admitted_as_measured_dataset': False, 'usable_as_workload_source': True,
            'license': 'Apache-2.0', 'pinned_java_target': 23,
            'reasons': ['A workload harness is not a recorded configuration-response table.',
                'Inspected ReadRecord procedure copies result fields but has no expected-value comparison.',
                'Pinned Java 23 target differs from project-local JDK 17; no compatibility build attempted.'],
        },
    }
    assert len(domains) == 197 and not inventory['knobs']['license_paths']
    assert time.monotonic() - started < 120
    return {'inventory': inventory, 'decisions': decisions,
        'source_files_verified': len(manifest['files']),
        'persisted_source_bytes': sum(v['bytes'] for v in manifest['files'].values()),
        'retrieval_failures': manifest['failures'],
        'new_objective_accesses': 0, 'new_model_requests': 0, 'new_physical_trials': 0,
        'scope_limit': 'Source inspection, not proof of absent artifacts elsewhere or an invalid original paper.',
        'seconds': time.monotonic() - started}


if __name__ == '__main__':
    assert not OUT.exists(), 'one-shot audit; use verifier for replay'
    freeze = json.loads((ROOT / 'reports/protocol_v68_admission.freeze.json').read_text())
    for name, expected in freeze['sha256'].items():
        assert sha(ROOT / name) == expected, name
    result = compute()
    OUT.mkdir(parents=True)
    result['executed_at_utc'] = datetime.now(timezone.utc).isoformat()
    (OUT / 'summary.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
