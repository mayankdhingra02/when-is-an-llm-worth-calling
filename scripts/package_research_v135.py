"""Create-once local stdlib replay subset; excludes weights/images/full tables."""
import hashlib,json,shutil,zipfile
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write

def main():
 out=ROOT/'output/v135_replay';out.mkdir(exist_ok=False);paths=set()
 for folder in ['results/v133_native','results/v133_proposals','results/v134_attribution','results/v135_analysis','results/v135_proposals']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.log','.png'])
 for folder in ['artifacts/study_v133','artifacts/study_v135']:
  paths.update(p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.log'] and not any(x in p.parts for x in ['previous_snapshot','synthetic_mutations']))
 for v in [133,134,135]:
  for folder in ['scripts','reports','configs','tests/synthetic']:paths.update(p for p in (ROOT/folder).glob(f'*v{v}*') if p.is_file())
 for n in ['artifacts/study_v132/model.json','artifacts/study_v91/model_manifest.json','requirements.lock.txt','reports/source_mapping_v127.md','THIRD_PARTY.md']:
  paths.add(ROOT/n)
 for n in read(ROOT/'results/v134_attribution/inputs.json')['sha256']:paths.add(ROOT/n)
 for version in [133,135]:
  for n in read(ROOT/f'artifacts/study_v{version}/inputs.freeze.json')['sha256']:paths.add(ROOT/n)
 for j in read(ROOT/'artifacts/study_v135/jobs.json'):
  paths.add(ROOT/j['old_messages_path']);paths.add(ROOT/f"results/v127_analysis/arms/{j['base_key']}_model.json")
  for m in ['batch_3nn','full_sequential_3nn','random_full']:paths.add(ROOT/f"results/v41_transfer/arms/{j['base_key']}_{m}.json")
  for n in [f"results/v41_models/0.5/arms/{j['base_key']}.json",f"results/v115_portfolio/arms/{j['base_key']}.json"]:
   if (ROOT/n).exists():paths.add(ROOT/n)
 for n in ['LICENSE.md','README.ijg']:paths.add(ROOT/'artifacts/sources/v133/libjpeg-turbo-3.1.2'/n)
 for p in sorted(paths):
  q=out/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
 (out/'README.md').write_text('# Private V133–V135 replay\n\nRun `python3 -I -S replay.py`. Standard-library verification checks saved native receipts,60-case retrospective attribution, five repaired real SAC responses and50charged source rows. It does not invoke models/native engines or reacquire objectives. No network/packages needed.\n\nPhotographs, encoded JPEGs, complete original tables, native sources/binaries and weights are omitted. Full local verifiers additionally validate those source/output hashes. Compact source extracts are only already acquired rows. This is not fresh inference, independent native remeasurement or a license to publicly redistribute historical datasets. Original failures/positive exceptions and their limitations remain in the parent repository.\n')
 (out/'replay.py').write_text('''import hashlib,json,subprocess,sys\nfrom pathlib import Path\nr=Path(__file__).resolve().parent\nm=json.loads((r/'manifest.json').read_text())\nfor n,v in m['files'].items():\n p=r/n\n assert p.stat().st_size==v['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],n\nfor script,flags in [('verify_jpeg_v133.py',['--compact']),('verify_attribution_v134.py',[]),('verify_repair_v135.py',['--compact'])]:\n subprocess.run([sys.executable,'-I','-S',str(r/'scripts'/script),'--root',str(r),*flags],check=True)\nprint(json.dumps({'verified':True,'hashed_files':len(m['files']),'new_collection':0}))\n''')
 files={str(p.relative_to(out)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()};write(out/'manifest.json',{'scope':'Private compact saved-evidence replay','files':files})
 z=ROOT/'output/v135_replay.zip'
 with zipfile.ZipFile(z,'x',zipfile.ZIP_DEFLATED) as f:
  for p in sorted(out.rglob('*')):
   if p.is_file():f.write(p,str(p.relative_to(out.parent)))
 with zipfile.ZipFile(z) as f:assert f.testzip() is None
 print(json.dumps({'files':len(files),'zip_bytes':z.stat().st_size,'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'crc_verified':True}))
if __name__=='__main__':main()
