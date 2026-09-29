"""Create-once private native/model receipt replay, excluding binary artifacts."""
import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 out=ROOT/'output/v140_replay';out.mkdir(exist_ok=False);paths=set()
 for folder in ['results/v140_native','results/v140_proposals']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.log','.png','.svg'])
 for name in ['jobs.json','decisions.json','domain.json','workloads.json','build.json','downloads.json','exposure.json','inputs.freeze.json','command_root.json','preparation_plan.json']:
  paths.add(ROOT/'artifacts/study_v140'/name)
 paths.update((ROOT/'artifacts/study_v140/prompts').glob('*.json'))
 for n in ['scripts/verify_xz_v140.py','scripts/analyze_xz_v140.py','scripts/collect_smollm_v47.py','reports/protocol_v140.md','reports/protocol_v140.freeze.json','reports/xz_v140.md','reports/source_audit_v139_v140.md','configs/study_v140.json','artifacts/study_v132/model.json','artifacts/study_v91/model_manifest.json','requirements.lock.txt','artifacts/sources/v140/xz-5.8.4/COPYING']:
  paths.add(ROOT/n)
 for p in paths:
  dest=out/p.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
 (out/'README.md').write_text('''# V140 private native XZ receipt replay

Run `python3 -I -S replay.py`. Python standard library only. Verifies 353 native configuration receipts, 30 B20 arms, five real model response records, prefix-only decisions, source-byte equality receipts, projection, budgets and comparisons. No network, inference, objective acquisition or native execution.

Photographs, compressed outputs, full native sources, runtime binaries and weights are excluded. Compact replay cannot independently decode outputs or authenticate those omitted files; full local verification checks their hashes. Inherited protocol dependencies are partly omitted. This is saved-evidence replay, not fresh model or second-host reproduction. One new software family on already exposed photographs is not a multi-system held-out router evaluation. No public redistribution rights are asserted beyond original source licenses. Synthetic tests are not measured records and are excluded.
''')
 (out/'replay.py').write_text('''import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
for n,v in json.loads((r/'manifest.json').read_text())['files'].items():
 p=r/n;assert p.stat().st_size==v['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],n
subprocess.run([sys.executable,'-I','-S',str(r/'scripts/verify_xz_v140.py'),'--root',str(r),'--compact'],check=True)
''')
 files={str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()};(out/'manifest.json').write_text(json.dumps({'files':files},indent=2)+'\n')
 archive=ROOT/'output/v140_replay.zip'
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(out.parent))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 receipt={'path':str(archive.relative_to(ROOT)),'bytes':archive.stat().st_size,'sha256':sha(archive),'hashed_files':len(files),'crc_verified':True};(ROOT/'artifacts/study_v140/bundle.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
if __name__=='__main__':main()
