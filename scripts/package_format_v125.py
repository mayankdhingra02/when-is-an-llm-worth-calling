"""Private compact format-only replay with genuine original response references."""
import shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha

def main():
 out=ROOT/'output/v125_replay';out.mkdir(exist_ok=False);names={'data/manifest_v41.json','artifacts/study_v91/model_manifest.json','artifacts/study_v125/jobs.json','configs/study_v125.json','reports/protocol_v125.md','reports/protocol_v125.freeze.json','reports/format_probe_v125.md','results/v124_surrogate/responses.jsonl'}
 for j in read(ROOT/'artifacts/study_v125/jobs.json'):names.add(j['prefix']);names.add(f"results/v124_surrogate/preflight/{j['original_request_key']}.json")
 for folder in ['artifacts/study_v125/prompts','results/v125_format','results/v125_analysis']:
  names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='server.log')
 for n in sorted(names):dest=out/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dest)
 shutil.copyfile(ROOT/'scripts/replay_format_v125_standalone.py',out/'replay.py')
 (out/'README.md').write_text('# V125 private format-feasibility replay\n\nRun `python3 -I replay.py`. Standard library only, no network or inference. Checks18new scheduled calls, deterministic prompt transformations and9corresponding original real V124responses. This is a saved-evidence subset, not complete protocol dependency closure or fresh inference. Zero new objective labels; no optimization/generalization claim. Prior V124failures remain unchanged. Full original response journal included for provenance; only9specified originals enter this diagnostic. No weights or runtime binary.\n')
 write(out/'manifest.json',{'files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}});archive=ROOT/'output/v125_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'compressed bytes')
if __name__=='__main__':main()
