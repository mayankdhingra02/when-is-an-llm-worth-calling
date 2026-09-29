"""Private, standard-library replay of V131/V132 saved records; no audio/weights."""
import shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha
def main():
 out=ROOT/'output/v132_replay';out.mkdir(exist_ok=False)
 names=set(read(ROOT/'reports/protocol_v132.freeze.json')['sha256'])
 names.update(['reports/protocol_v132.freeze.json','reports/protocol_v131.md','reports/protocol_v131.freeze.json','reports/native_v131.md','reports/router_v132.md','reports/research_assessment_v132.md','reports/source_audit_v131.md','configs/study_v131.json','scripts/verify_native_v131.py','scripts/verify_router_v132.py','artifacts/study_v131/workloads.json','artifacts/study_v131/inputs.freeze.json','artifacts/study_v131/downloads.json','artifacts/study_v131/binaries.json','artifacts/study_v131/build_wavpack.json','artifacts/study_v131/build_fftw.json','artifacts/study_v132/before_outcomes.json','artifacts/study_v91/model_manifest.json','artifacts/sources/v131/wavpack-5.9.0/license.txt','artifacts/sources/v131/fftw-3.3.11/COPYING','artifacts/sources/v130/LibriSpeech/LICENSE.TXT'])
 for folder in ['results/v131_native','results/v131_proposals','results/v132_router']:
  names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.png'])
 for n in sorted(names):
  p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,p)
 (out/'replay.py').write_text('''"""Local saved-evidence replay; standard library only, no new experiments."""
import hashlib,json,runpy,sys
from pathlib import Path
r=Path(__file__).resolve().parent
for n,m in json.loads((r/'manifest.json').read_text())['files'].items():
 p=r/n;assert p.stat().st_size==m['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],n
sys.argv=[str(r/'scripts/verify_native_v131.py'),'--root',str(r),'--compact']
runpy.run_path(str(r/'scripts/verify_native_v131.py'),run_name='__main__')
sys.argv=[str(r/'scripts/verify_router_v132.py'),'--root',str(r)]
runpy.run_path(str(r/'scripts/verify_router_v132.py'),run_name='__main__')
''')
 (out/'README.md').write_text('# Private V131/V132 saved-evidence replay\n\nRun `python3 -I -S replay.py`. Standard library only; no model, native execution, network or package installation. Independently reconstructs648 trial records/50paired arms, real response provenance, fresh timing validation, historical prefix features, group-exclusion ridge models/calibration and ten decisions saved before new outcomes.\n\nAudio, encoded/numerical outputs, binaries, source archives and model weights are omitted. Compact mode checks saved record semantics and hashes, not full native-output correctness/dependency closure; the full workspace verifier checks physical outputs. Not a second-host execution or Q2-readiness claim. Source and license qualifications remain; this is a local private review bundle, not a publication/redistribution grant.\n')
 write(out/'manifest.json',{'scope':'Compact native receipts plus historical training inputs; excludes physical native outputs/dependency closure','files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}})
 archive=ROOT/'output/v132_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'bytes')
if __name__=='__main__':main()
