"""Validate pinned inputs and frozen source snapshots without running inference."""
from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root/'reports/protocol.md')==(root/'reports/protocol.sha256').read_text().strip()
for stage in ['classical','paired']:
 m=json.loads((root/f'results/{stage}/manifest.json').read_text())
 for path,expected in m['code_hashes'].items():assert sha(root/f'artifacts/code_snapshots/{stage}'/path)==expected
 assert sha(root/f'artifacts/code_snapshots/{stage}/requirements.lock.txt')==m['requirements_sha256']
 assert sha(root/'reports/protocol.md')==m['protocol_sha256']
print('Frozen inputs and executed source snapshots verified')
