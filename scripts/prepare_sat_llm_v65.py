"""Freeze the bounded five-prefix assay before any new generation."""
import hashlib
import json
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from escalation.sat_llm_v65 import messages
def read(p): return json.loads(p.read_text())
def write(p, x): p.write_text(json.dumps(x, indent=2) + '\n')
def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()


def main():
    art = ROOT / 'artifacts/study_v65'
    art.mkdir(exist_ok=False)
    assert read(ROOT / 'artifacts/study_v64/verification.json')['verified']
    eligible = [w['workload'] for w in read(ROOT / 'results/v64_sat_screen/summary.json')['workloads'] if w['gate_passed']]
    assert eligible == ['planted_512']
    folder = ROOT / 'results/v64_sat_screen/minisat_planted_512'
    jobs = []
    for seed in [11, 23, 37, 53, 71]:
        p = folder / f'prefix_{seed}.json'
        prefix = read(p)
        jobs.append({'seed': seed, 'prefix_path': str(p.relative_to(ROOT)), 'prefix_sha256': sha(p), 'prefix': prefix, 'messages': messages(prefix)})
    write(art / 'jobs.json', jobs)
    cmd = list(read(ROOT / 'results/v48_sensitivity/runtime.json')['command'])
    cmd[cmd.index('--port') + 1] = '18485'
    write(art / 'runtime_plan.json', {'command': cmd, 'model_revision': read(ROOT / 'configs/study_v65.json')['model_revision'], 'existing_weights_no_download': True})
    paths = [ROOT / p for p in ['reports/protocol_v65_sat_llm.md', 'configs/study_v65.json', 'scripts/prepare_sat_llm_v65.py', 'scripts/collect_sat_llm_v65.py', 'scripts/analyze_sat_llm_v65.py', 'src/escalation/sat_llm_v65.py', 'src/escalation/sat_v64.py', 'src/escalation/classical_java_v54.py', 'tests/synthetic/test_sat_llm_v65.py', 'requirements.lock.txt', 'artifacts/study_v65/jobs.json', 'artifacts/study_v65/runtime_plan.json', 'artifacts/study_v64/verification.json', 'results/v64_sat_screen/summary.json', 'reports/protocol_v64_sat_screen.freeze.json']]
    paths += list(folder.glob('*.json')) + [Path(cmd[0]), Path(cmd[cmd.index('-m') + 1])]
    freeze = ROOT / 'reports/protocol_v65_sat_llm.freeze.json'
    assert not freeze.exists()
    write(freeze, {'stage': 'v65', 'before_new_model_output': True, 'sha256': {str(p.relative_to(ROOT)): sha(p) for p in sorted(set(paths))}})
    print(sha(freeze))


if __name__ == '__main__': main()
