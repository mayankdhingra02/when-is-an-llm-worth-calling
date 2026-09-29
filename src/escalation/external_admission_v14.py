"""Inspect published configuration coverage without parsing optimization outcomes."""
import csv
import re
from collections import Counter, defaultdict

META_FIELDS = ('dataset', 'source', 'codec', 'level', 'container', 'codec_version',
               'chunk_size', 'threads', 'repetition', 'warmup', 'sha256', 'status')
CONTEXT_FIELDS = ('dataset', 'source', 'sha256', 'codec', 'codec_version')
CONFIG_FIELDS = ('level', 'container', 'chunk_size', 'threads')


def metadata_rows(handle):
    reader = csv.DictReader(handle)
    missing = set(META_FIELDS) - set(reader.fieldnames or ())
    if missing:
        raise ValueError(f'Missing configuration/provenance fields: {sorted(missing)}')
    for row in reader:
        # No conversion, comparison or propagation of runtime/size/throughput values.
        selected = {key: row[key] for key in META_FIELDS}
        if any(value is None or value == '' for value in selected.values()):
            raise ValueError('Missing metadata in a published row')
        if selected['warmup'] not in ('True', 'False'):
            raise ValueError('Unknown warmup status')
        yield selected


def coverage_audit(rows, execution_manifest, required_configurations=20):
    if required_configurations < 1:
        raise ValueError('Positive configuration requirement needed')
    cells = defaultdict(lambda: {'configurations': set(), 'measured_configurations': set(),
                                'measured_rows': 0, 'warmup_rows': 0, 'statuses': Counter(),
                                'repetitions': defaultdict(set)})
    count = 0
    for row in rows:
        count += 1
        context = tuple(row[key] for key in CONTEXT_FIELDS)
        config = tuple(row[key] for key in CONFIG_FIELDS)
        cell = cells[context]
        cell['configurations'].add(config)
        cell['statuses'][row['status']] += 1
        if row['warmup'] == 'True':
            cell['warmup_rows'] += 1
        else:
            cell['measured_rows'] += 1
            cell['measured_configurations'].add(config)
            repeat_key = row['repetition']
            if repeat_key in cell['repetitions'][config]:
                raise ValueError('Duplicate measurement identifier within one configuration/context')
            cell['repetitions'][config].add(repeat_key)
    records = []
    for context, cell in sorted(cells.items()):
        measured = len(cell['measured_configurations'])
        records.append({**dict(zip(CONTEXT_FIELDS, context)),
                        'configurations': [dict(zip(CONFIG_FIELDS, c)) for c in sorted(cell['configurations'])],
                        'distinct_measured_configurations': measured,
                        'measured_rows': cell['measured_rows'], 'warmup_rows': cell['warmup_rows'],
                        'status_counts': dict(cell['statuses']),
                        'repetitions_per_measured_configuration': sorted(len(v) for v in cell['repetitions'].values()),
                        'supports_budget_20': measured >= required_configurations})
    commit = execution_manifest.get('git_commit')
    revision_bound = isinstance(commit, str) and bool(re.fullmatch('[0-9a-f]{40}', commit)) and execution_manifest.get('git_dirty') is False
    return {'scope': 'published metadata coverage; not outcome analysis or independently rerun measurements',
            'raw_rows': count, 'contexts': len(records),
            'datasets': len({r['dataset'] for r in records}),
            'codecs': sorted({r['codec'] for r in records}),
            'measured_rows': sum(r['measured_rows'] for r in records),
            'warmup_rows': sum(r['warmup_rows'] for r in records),
            'required_distinct_configurations_per_context': required_configurations,
            'contexts_supporting_budget': sum(r['supports_budget_20'] for r in records),
            'published_execution_git_commit': commit,
            'published_execution_git_dirty': execution_manifest.get('git_dirty'),
            'clean_execution_revision_identified': revision_bound,
            'records': records,
            'admitted_for_collection': False,
            'new_model_requests': 0, 'new_optimizer_acquisitions': 0}
