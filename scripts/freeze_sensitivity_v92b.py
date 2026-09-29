"""Freeze exact inherited diagnostic inputs and the new model adaptation."""
from collect_smollm_v47 import ROOT, read, write, sha, now
from validate_sensitivity_v92b import validate

def main():
    out = ROOT / 'reports/protocol_v92b.freeze.json'
    assert not out.exists()
    validate(read(ROOT / 'configs/study_v92b.json'))
    pins = read(ROOT / 'reports/protocol_v48_sensitivity.freeze.json')['sha256']
    for n, digest in pins.items():
        assert sha(ROOT / n) == digest, n
    names = [
        'reports/protocol_v92b.md', 'configs/study_v92b.json',
        'reports/protocol_v92.freeze.json', 'reports/protocol_v92.md', 'results/v92_sensitivity/ledger.json',
        'scripts/runtime_sensitivity_v92b.py', 'scripts/collect_smollm_v47.py',
        'scripts/run_planning_v55.py', 'src/escalation/receipts_v70.py',
        'src/escalation/qwen_v91.py', 'artifacts/study_v91/model_manifest.json',
        'artifacts/study_v91/evidence_manifest.json',
        'models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf',
        '.local-runtime/llama-b11146/llama-server',
        'reports/protocol_v48_sensitivity.freeze.json',
        'results/v48_analysis/summary.json', 'results/v48_analysis/cases.json',
        'tests/synthetic/test_qwen_v91.py', 'tests/synthetic/test_sensitivity_v92b.py',
    ]
    names += [str(p.relative_to(ROOT)) for p in (ROOT / 'scripts').glob('*sensitivity_v92b.py')]
    pins.update({n: sha(ROOT / n) for n in names})
    assert pins['models/Qwen3-8B-Q4_K_M/Qwen3-8B-Q4_K_M.gguf'] == 'd98cdcbd03e17ce47681435b5150e34c1417f50b5c0019dd560e4882c5745785'
    write(out, {'at': now(), 'scope': 'V92 development-only Qwen3 loss/order diagnostic; no new objective outcomes', 'sha256': pins})
    print('Frozen', len(pins), 'files before generation')

if __name__ == '__main__':
    main()
