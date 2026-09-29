"""Synthetic guard fixtures; no measured outcomes."""
import pytest
from escalation.admission_v52 import GATES, eligible, equivalence_counts, feature_rows


def test_fail_closed():
    r = {'gates': {g: {'status': 'verified', 'evidence': ['synthetic']} for g in GATES}}
    assert eligible(r)
    r['gates']['validation']['status'] = 'unresolved'
    assert not eligible(r)
    del r['gates']['identity']
    with pytest.raises(ValueError):
        eligible(r)


def test_evidence_required():
    r = {'gates': {g: {'status': 'verified', 'evidence': []} for g in GATES}}
    with pytest.raises(ValueError):
        eligible(r)


def test_poison_objective_never_converted(tmp_path):
    p = tmp_path / 'synthetic.csv'
    p.write_text('quality,threads,Time-\n0,1,DO_NOT_PARSE\n0,2,SECRET\n1,1,NAN\n')
    rows = list(feature_rows(p, ['quality', 'threads'], ['Time-']))
    assert rows == [(0, 1), (0, 2), (1, 1)]
    with pytest.raises(ValueError):
        list(feature_rows(p, ['Time-'], ['Time-']))


def test_distinct_configurations_and_contracts():
    rows = [(0, 1), (0, 1), (0, 2), (1, 1)]
    x = equivalence_counts(rows, {1})
    assert x['unique_configurations'] == 3
    assert x['utility_contracts'] == 2
    assert x['largest_contract_configurations'] == 2
    assert x['contracts_with_at_least_40_configurations'] == 0
