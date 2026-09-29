"""Private replay bundle, excluding full tables and model/native artifacts."""
import json,shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha
def main():
 dest=ROOT/'output/v136_replay';dest.mkdir(exist_ok=False);jobs=read(ROOT/'artifacts/study_v136/jobs.json');out=ROOT/'results/v136_feedback';acq=[json.loads(x) for x in (out/'acquisitions.jsonl').read_text().splitlines()]
 names={'reports/research_assessment_v136.md','scripts/verify_feedback_v136.py','scripts/analyze_feedback_v136.py','scripts/collect_smollm_v47.py','reports/feedback_v136.md','reports/protocol_v136.md','reports/protocol_v136.freeze.json','configs/study_v136.json','artifacts/study_v91/model_manifest.json','artifacts/study_v136/jobs.json','artifacts/study_v136/admission.json','artifacts/study_v136/prior_metadata_erratum.json'}
 for j in jobs:names.update(j[k] for k in ['prefix','historical_batch','historical_sequential'])
 names.update(str(p.relative_to(ROOT)) for p in out.rglob('*') if p.is_file())
 for group in sorted({j['system_group'] for j in jobs}):
  snap=ROOT/f'artifacts/study_v136/candidates/{group}.json';s=read(snap);names.add(str(snap.relative_to(ROOT)));spec=s['spec'];source=ROOT/spec['path'];assert sha(source)==spec['sha256'];raw=source.read_text().splitlines()
  keys={j['key'] for j in jobs if j['system_group']==group};lineids={1}|{a['source_line'] for a in acq if a['key'] in keys}
  path=ROOT/f'artifacts/study_v136/source_extracts/{group}.json';write(path,{'scope':'Header and already charged rows only; compact replay does not verify the omitted full source file','source_sha256':spec['sha256'],'lines':{str(n):raw[n-1] for n in sorted(lineids)}});names.add(str(path.relative_to(ROOT)))
 for n in sorted(names):
  target=dest/n;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/n,target)
 (dest/'README.md').write_text('''# V136 private recorded-result replay

Run `python3 -I -S replay.py`. Python standard library only; no network, model calls, objective collection or third-party packages.

Reconstructs 100 intended two-proposal rounds, 20 B20 arms, masking, saved response parsing, projection, 200 charged source-row extracts and summary contrasts. Full local verifier additionally checks full original table hashes. This compact bundle cannot independently authenticate omitted full tables, model weights, runtime binaries or historic native executions. The full protocol freeze includes dependencies omitted here and is provenance, not a claim that this bundle contains them all.

Includes measured raw local responses, prompts/configuration, recorded acquired outcomes, original prefixes and historical reference arms. Excludes full tables, weights, binaries, images and unrelated earlier studies. For private review; inclusion is not a new claim of public redistribution rights. Two exposed systems are not a confirmatory population study or journal-readiness certification.

The descriptive figure/report can be regenerated in the full pinned repository using scripts/analyze_feedback_v136.py (matplotlib required). This standard-library replay verifies measured summaries without regenerating plots. Synthetic tests are excluded.
''')
 (dest/'replay.py').write_text('''import hashlib,importlib.util,json
from pathlib import Path
root=Path(__file__).resolve().parent
for n,m in json.loads((root/'manifest.json').read_text())['files'].items():
 p=root/n;assert p.stat().st_size==m['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],n
spec=importlib.util.spec_from_file_location('independent',root/'scripts/verify_feedback_v136.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
print(json.dumps(m.verify(root,compact=True),indent=2))
''')
 paths=sorted(p for p in dest.rglob('*') if p.is_file());write(dest/'manifest.json',{'scope':'Transport hashes; semantic replay is separate','files':{str(p.relative_to(dest)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}})
 archive=ROOT/'output/v136_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(dest.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(dest.parent))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 write(ROOT/'artifacts/study_v136/bundle.json',{'path':str(archive.relative_to(ROOT)),'sha256':sha(archive),'bytes':archive.stat().st_size,'hashed_files':len(paths),'crc_verified':True})
 print(read(ROOT/'artifacts/study_v136/bundle.json'))
if __name__=='__main__':main()
