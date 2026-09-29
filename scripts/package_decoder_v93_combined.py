"""Create a portable saved-response audit bundle; excludes model weights."""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from collect_smollm_v47 import sha

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/study_v93'

def main():
    out = ROOT / 'output/diagnostics_v93_reproduction.zip'
    if out.exists():
        raise ValueError('Preserve existing bundle')
    sources = {
        'reports/protocol_v93b_decoder.md', 'reports/protocol_v93b_decoder.freeze.json',
        'configs/study_v93b.json','artifacts/study_v93/remaining_jobs.json',
        'scripts/replay_decoder_v93_combined.py', 'scripts/package_decoder_v93_combined.py',
        'reports/protocol_v93_decoder.md', 'reports/protocol_v93_decoder.freeze.json',
        'reports/decoder_v93.md', 'configs/study_v93.json', 'artifacts/study_v93/jobs.json',
        'artifacts/study_v93/verification.json', 'artifacts/study_v93/tests_final.log',
        'scripts/replay_sensitivity_v92.py', 'scripts/package_sensitivity_v92.py',
        'reports/protocol_v48_sensitivity.md', 'reports/protocol_v92.md',
        'reports/protocol_v92b.md', 'reports/sensitivity_v92.md',
        'reports/protocol_v92.freeze.json', 'reports/protocol_v92b.freeze.json',
        'configs/study_v92.json', 'configs/study_v92b.json',
        'artifacts/study_v48/jobs.json', 'artifacts/study_v91/model_manifest.json',
        'artifacts/study_v92/verification.json', 'artifacts/study_v92/tests_final.log',
        'results/v92_sensitivity/ledger.json',
    }
    for directory in ['results/v93b_decoder','results/v93_combined','results/v93_combined_analysis','results/v93_decoder','results/v93_analysis','artifacts/study_v48/prompts', 'results/v48_sensitivity', 'results/v92b_sensitivity', 'results/v48_analysis', 'results/v92b_analysis', 'artifacts/sources/v91']:
        sources.update(str(p.relative_to(ROOT)) for p in (ROOT / directory).rglob('*') if p.is_file())
    for stage in ['v48', 'v92', 'v92b']:
        sources.update(str(p.relative_to(ROOT)) for p in (ROOT / 'scripts').glob('*sensitivity_' + stage + '.py'))
    sources.add('scripts/runtime_qwen_v91.py')
    sources.update(str(p.relative_to(ROOT)) for p in (ROOT/'scripts').glob('*decoder_v93*.py'))
    sources.add('scripts/decoder_v49_common.py')
    readme = '''# Portable V92–V93 diagnostic evidence

This archive contains actual saved model responses, prompts, ID mappings, conditions, analysis and a standard-library verifier for two matched development diagnostics: SmolLM3-3B V48 and Qwen3-8B V92b. It contains no model weights and performs no inference or software benchmarking.

From the extracted directory run:

    python3 scripts/replay_sensitivity_v92.py
    python3 scripts/replay_decoder_v93_combined.py

The command checks every bundled file hash, all 2,160 real response records, complete condition denominators, prompt histories, mapped selections, family aggregates and frozen screen decisions. It prints JSON to stdout. Python 3.10 or newer is recommended; no external dependencies are required. File hashes prove consistency with this saved manifest, not external authenticity.

The second command verifies the Qwen3 decoder comparison with a preserved resource failure and a context-only continuation of unattempted cases. It checks original-record provenance, intended denominators and conservative missing-response bounds. This is a two-context amended diagnostic, not a clean single-runtime replication. It explicitly counts absent model/runtime pins that cannot be verified from this archive.

This reproduces saved-response diagnostic results only. Full local inference additionally requires the pinned Qwen3 weights, llama.cpp build and original project environment. Source collection scripts and protocol pins are included as provenance; not every historical dependency or model binary named in those pins is in this portable archive. Do not claim this is an independent experimental replication.

All inputs are previously exposed development cases. Three systems and repeated seeds cannot establish unseen-system generalization, useful escalation or journal readiness. Qwen3's context capacity was amended before any generation from 4,096 to 8,192 tokens after an overlong-prompt preflight failure. The original attempt used zero generation calls and is retained.

See reports/sensitivity_v92.md and reports/decoder_v93.md for results and limitations. Historical model/data code retains its upstream licensing; Qwen3 model-owner Apache-2.0 license and manifest are included, while weights are excluded.
'''
    with tempfile.TemporaryDirectory(prefix='v92_bundle_') as temp:
        base = Path(temp)
        for name in sorted(sources):
            dest = base / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        (base / 'REPRODUCE.md').write_text(readme)
        files = {str(p.relative_to(base)): {'sha256': sha(p), 'bytes': p.stat().st_size} for p in sorted(base.rglob('*')) if p.is_file()}
        (base / 'BUNDLE_MANIFEST.json').write_text(json.dumps({'scope': 'Saved-response replay, not new inference', 'files': files}, indent=2) + '\n')
        result = subprocess.run([sys.executable, str(base / 'scripts/replay_sensitivity_v92.py')], cwd=base, text=True, capture_output=True, check=True)
        (ART / 'bundle_sensitivity_replay.json').write_text(result.stdout)
        decoder = subprocess.run([sys.executable, str(base/'scripts/replay_decoder_v93_combined.py')],cwd=base,text=True,capture_output=True,check=True)
        (ART/'bundle_decoder_replay.json').write_text(decoder.stdout)
        if result.stderr:
            (ART / 'bundle_stderr.log').write_text(result.stderr)
        out.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(out, 'x', zipfile.ZIP_DEFLATED) as z:
            for p in sorted(base.rglob('*')):
                if p.is_file():
                    z.write(p, str(p.relative_to(base)))
    receipt = {'path': str(out.relative_to(ROOT)), 'sha256': sha(out), 'bytes': out.stat().st_size, 'files': len(files) + 1, 'extracted_standard_library_replay_passed': True}
    (ART / 'bundle_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
