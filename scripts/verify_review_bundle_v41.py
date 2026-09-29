"""Standard-library local bundle integrity plus exact measured-result replay."""
import hashlib,json,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def main():
    manifest=json.loads((ROOT/'bundle_manifest_v41.json').read_text())
    for relative,expected in manifest['sha256'].items():
        path=ROOT/relative
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:raise ValueError('Changed/missing bundle evidence: '+relative)
    result=subprocess.run([sys.executable,'-I','-S',str(ROOT/'scripts/verify_model_results_v41.py')],capture_output=True,text=True,timeout=45)
    if result.returncode:raise RuntimeError(result.stderr)
    print(json.dumps({'files_verified':len(manifest['sha256']),'arithmetic':json.loads(result.stdout),
        'scope':'Local results replay; no inference, full-source download, or live measurement'},indent=2))
if __name__=='__main__':main()
