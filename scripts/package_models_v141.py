"""Create-once private standard-library replay of the matched-model experiment."""
import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def main():
 out=ROOT/'output/v141_replay';out.mkdir(exist_ok=False);paths=set();a=ROOT/'artifacts/study_v141'
 for folder in ['results/v141_models','results/v142_smollm','results/v141_analysis']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.log','.png','.svg'])
 for folder in ['prompts','candidates','source_extracts']:paths.update((a/folder).glob('*.json'))
 paths.update((ROOT/'artifacts/study_v142').glob('*.json'))
 for n in ['jobs.json','models.json','inputs.freeze.json']:paths.add(a/n)
 for j in read(a/'jobs.json'):paths.update(ROOT/j[n] for n in ['prefix','old_messages_path'])
 for key in read(ROOT/'results/v141_analysis/summary.json')['arms']:
  r=read(ROOT/f'results/v141_analysis/arms/{key}.json');paths.update(ROOT/v['path'] for v in r['references'].values())
 for n in ['scripts/verify_models_v141.py','scripts/report_models_v141.py','scripts/collect_smollm_v47.py','reports/protocol_v141.md','reports/protocol_v141.freeze.json','reports/models_v141.md','configs/study_v141.json','configs/study_v142.json','reports/protocol_v142.md','reports/protocol_v142.freeze.json','artifacts/study_v46/model_card.md','artifacts/study_v46/model_metadata.json','artifacts/study_v91/model_manifest.json','requirements.lock.txt','THIRD_PARTY.md']:paths.add(ROOT/n)
 for p in paths:
  q=out/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
 (out/'README.md').write_text('''# V141 private matched-model saved-evidence replay

Run `python3 -I -S replay.py`. Standard library only. Verifies raw recorded responses and preflight/payload identity, identical acquired prefixes, independent projection, 600 charged source-row acquisitions, 60 B20 arms, historical controls and descriptive comparisons. No inference, network or new objective acquisition.

Contains only already acquired source-row extracts. Full tables, model/runtime binaries and synthetic fixtures are omitted. Compact replay cannot authenticate omitted files or reproduce original model behavior; full local verifier checks the pinned files. Inherited freeze dependencies are partly omitted. This is not fresh-host replication, an independent-system holdout, or a public redistribution grant. One failed SmolLM server startup and its bounded pre-outcome repair are preserved; generation retries remained zero. Both model pipelines differ in training/tokenization/templates; no isolated parameter-count causal claim. All original rights and failure qualifications remain.
''')
 (out/'replay.py').write_text('''import hashlib,json,subprocess,sys
from pathlib import Path
r=Path(__file__).resolve().parent
for n,v in json.loads((r/'manifest.json').read_text())['files'].items():
 p=r/n;assert p.stat().st_size==v['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],n
subprocess.run([sys.executable,'-I','-S',str(r/'scripts/verify_models_v141.py'),'--root',str(r),'--compact'],check=True)
''')
 files={str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()};(out/'manifest.json').write_text(json.dumps({'files':files},indent=2)+'\n')
 archive=ROOT/'output/v141_replay.zip'
 with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(out.parent))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 receipt={'path':str(archive.relative_to(ROOT)),'bytes':archive.stat().st_size,'sha256':sha(archive),'hashed_files':len(files),'crc_verified':True};(a/'bundle.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt)
if __name__=='__main__':main()
