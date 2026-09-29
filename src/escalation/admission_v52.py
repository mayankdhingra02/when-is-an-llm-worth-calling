"""Outcome-blind utility admission. This module does not parse target cells."""
import csv
import hashlib
import re
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

GATES = ('identity', 'utility', 'validation', 'feasibility', 'reproducibility')
RESERVED = frozenset(('mongodb', 'redis', 'storm'))


def eligible(record):
    if set(record['gates']) != set(GATES):
        raise ValueError('all five gates required')
    for gate in record['gates'].values():
        if gate['status'] not in ('verified', 'unresolved', 'contradicted'):
            raise ValueError('invalid gate status')
        if not gate.get('evidence'):
            raise ValueError('gate requires inspectable evidence')
    return all(g['status'] == 'verified' for g in record['gates'].values())


def feature_rows(path, names, targets):
    if set(names) & set(targets):
        raise ValueError('objective column requested as feature')
    with Path(path).open(newline='') as stream:
        reader = csv.reader(stream)
        header = next(reader)
        if len(set(header)) != len(header):
            raise ValueError('duplicate header')
        indices = [header.index(n) for n in names]
        if not set(targets).issubset(header):
            raise ValueError('missing target schema')
        for row in reader:
            if len(row) != len(header):
                raise ValueError('malformed row')
            # Only declared features are indexed/converted; targets can be poison.
            yield tuple(float(row[i]) for i in indices)


def equivalence_counts(rows, free_indices):
    unique = set(rows)
    counts = Counter(tuple(v for i, v in enumerate(row) if i not in free_indices)
                     for row in unique)
    return {'unique_configurations': len(unique), 'utility_contracts': len(counts),
            'largest_contract_configurations': max(counts.values(), default=0),
            'contracts_with_at_least_40_configurations': sum(n >= 40 for n in counts.values()),
            'contract_size_histogram': dict(sorted(Counter(counts.values()).items()))}


def sha256(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def normalized_feature(name):
    return re.sub('[^a-z0-9]', '', name.lower()).removeprefix('xx')


def model_comparison(path, names):
    model = {normalized_feature(e.text) for e in ET.parse(path).findall('.//name')}
    table = {normalized_feature(n) for n in names}
    return {'model_names': len(model), 'table_names': len(table),
            'table_only': sorted(table - model), 'model_only': sorted(model - table),
            'exact_normalized_name_match': model == table,
            'caveat': 'Name-set agreement alone does not establish domain, outcome or workload equivalence.'}
