"""Record reproducible analysis inputs/code and current outputs; no inference."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]

def hashes(paths):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths)) if p.is_file()}

paths = list((root / 'src/escalation').glob('*.py'))
paths += [root / p for p in [
    'scripts/report_v3.py', 'scripts/verify_v3.py',
    'scripts/verify_results_v3.py', 'scripts/record_analysis_manifest.py',
    'requirements.lock.txt', 'data/manifest_v3.json', 'configs/followup_v3.yaml',
    'reports/protocol_v3.md', 'artifacts/resource_ledger_v2.json',
]]
paths += list((root / 'results/v3').glob('*.json*'))
paths += list((root / 'results/v3/classical').glob('*.json*'))
paths += list((root / 'results/v3/classical/prefixes').glob('*.json'))
paths += list((root / 'results/v3/checkpoints').glob('*.json'))
outputs = list((root / 'results/v3/analysis').glob('*'))
outputs += [root / 'reports/pilot_report_v3.md']
record = {
    'recorded_at': datetime.now(timezone.utc).isoformat(),
    'scope': 'Post-run v3 analysis/input/output integrity manifest; collection snapshots remain separate.',
    'note': 'Timing fields and rendering bytes may vary on regeneration. No inference or label acquisition here.',
    'inputs_and_code_sha256': hashes(paths),
    'outputs_sha256': hashes(outputs),
}
target = root / 'artifacts/analysis_manifest_v3.json'
target.write_text(json.dumps(record, indent=2) + '\n')
print(f'Recorded {len(record["inputs_and_code_sha256"])} inputs/code files and {len(record["outputs_sha256"])} outputs')
