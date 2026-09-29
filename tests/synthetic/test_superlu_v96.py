import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from superlu_v96_common import jobs, classify

def test_fixed_diagnostic_denominator_and_single_factor():
    rows = jobs()
    assert rows == jobs() and len(rows) == len({r['key'] for r in rows}) == 40
    for panel in [16, 20, 21, 32]:
        assert sum(r['configuration'][3] == panel for r in rows) == 10
    for source in {r['source'] for r in rows}:
        group = [r for r in rows if r['source'] == source]
        assert len({tuple(r['configuration'][:3]) for r in group}) == 1
        assert len(group) == 20

def test_crash_after_valid_vectors_stays_failure():
    record = {'measurements':[{'certificate':{'valid':True}}] * 3}
    assert classify(0, None, record) == 'valid'
    assert classify(-10, None, record) == 'worker_failure'
    assert classify(0, 'rss_guard', record) == 'rss_guard'
    assert classify(0, None, None) == 'missing_output'
    assert classify(0, None, {'measurements':[]}) == 'invalid_certificate'
