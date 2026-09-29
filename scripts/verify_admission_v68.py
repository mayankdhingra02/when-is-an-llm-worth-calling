"""Read-only source/result verification, including metadata pin consistency."""
import json
import time
from pathlib import Path
from audit_admission_v68 import compute, sha, ROOT, SRC, OUT


def main():
    started = time.monotonic()
    freeze = json.loads((ROOT / 'reports/protocol_v68_admission.freeze.json').read_text())
    for name, digest in freeze['sha256'].items():
        assert sha(ROOT / name) == digest, name
    pins = {'knobs': '13290f8dcef965a62820c41b74af097b93dd54a5',
            'ycsb': '4b19340e3bab5e4c88eda75ad56e83dc4d5cc503',
            'benchbase': '33c00473807ebd49304d114a6d769d2d2b2bbb34'}
    for repo, expected in pins.items():
        ref = json.loads((SRC / repo / 'ref.json').read_text())['object']
        if ref['type'] == 'tag':
            ref = json.loads((SRC / repo / 'tag.json').read_text())['object']
        assert ref['type'] == 'commit' and ref['sha'] == expected
        assert json.loads((SRC / repo / 'pin.json').read_text())['commit'] == expected
    saved = json.loads((OUT / 'summary.json').read_text())
    recomputed = compute()
    for item in (saved, recomputed):
        item.pop('seconds', None); item.pop('executed_at_utc', None)
    assert saved == recomputed
    # Independent structural checks, not imports of upstream scripts.
    text = (SRC / 'knobs/source/autotune/dbenv_bench.py').read_text()
    assert 'self.model.predict(' in text and 'joblib.load(model_path)' in text
    xml = (SRC / 'benchbase/source/pom.xml').read_text()
    assert '<maven.compiler.target>23</maven.compiler.target>' in xml
    assert '[0, 1, 5]' == str(saved['decisions']['knobs_measured_replay']['sysbench_interval_columns_used'])
    assert sum(len(x['data_paths_metadata_only']) for x in saved['inventory'].values()) == 15
    print(json.dumps({'verified': True, 'source_files': saved['source_files_verified'],
        'outcome_tables_opened': 0, 'new_model_requests': 0,
        'seconds': time.monotonic() - started}, indent=2))


if __name__ == '__main__': main()
