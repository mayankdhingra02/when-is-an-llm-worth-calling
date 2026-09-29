"""Private compact saved-evidence replay. No weights, binaries or audio."""
import shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha

def main():
 out=ROOT/'output/v130_replay';out.mkdir(exist_ok=False)
 names={'scripts/verify_flac_v130.py','reports/protocol_v130.md','reports/protocol_v130.freeze.json','reports/flac_v130.md','reports/research_assessment_v130.md','configs/study_v130.json','artifacts/study_v91/model_manifest.json','artifacts/study_v130/workloads.json','artifacts/study_v130/build_xcode.json','artifacts/study_v130/corpus_selection.json','artifacts/study_v130/downloads.json','artifacts/study_v130/inputs.freeze.json','artifacts/study_v130/jobs.json','artifacts/sources/v130/LibriSpeech/LICENSE.TXT'}
 for folder in ['artifacts/study_v130/prompts','results/v130_native','results/v130_proposals']:
  names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ['.json','.jsonl','.png'])
 for n in sorted(names):
  p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,p)
 (out/'replay.py').write_text('''"""Verify bundle byte identity and replay saved evidence without new experiments."""
import hashlib,json,runpy,sys
from pathlib import Path
r=Path(__file__).resolve().parent
manifest=json.loads((r/'manifest.json').read_text())
for n,m in manifest['files'].items():
 p=r/n
 assert p.stat().st_size==m['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],n
sys.argv=[str(r/'scripts/verify_flac_v130.py'),'--root',str(r),'--compact']
runpy.run_path(str(r/'scripts/verify_flac_v130.py'),run_name='__main__')
''')
 (out/'README.md').write_text('# V130 private saved-evidence replay\n\nRun `python3 -I -S replay.py`. Python standard library only; no package installation, network, model or encoder calls. Independently reconstructs all paired selections, prefix-only model observations, real responses, budgets and comparisons. Checks303 native trial receipts/909 encoder and909 decoder records, but excludes encoded audio and binaries: full source-byte and decoded-sample verification requires the main repository. This is saved-record replay, not a second-host experiment. One software family; no Q2-readiness claim. No model weights, source archive, audio or runtime binaries included. Kept locally; no publication/upload.\n')
 write(out/'manifest.json',{'scope':'Compact receipts; no physical FLAC outputs/full dependency closure','files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}})
 archive=ROOT/'output/v130_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'bytes')
if __name__=='__main__':main()
