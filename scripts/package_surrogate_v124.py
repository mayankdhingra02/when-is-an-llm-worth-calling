"""Private compact evidence package, including retained owner license."""
import shutil,zipfile,sys
from collect_smollm_v47 import ROOT,read,write,sha
from analyze_pointwise_v123 import refpaths

def main():
 bundle='v124_replay_corrected' if '--corrected' in sys.argv else 'v124_replay';out=ROOT/'output'/bundle;out.mkdir(exist_ok=False);names={'data/manifest_v41.json','artifacts/study_v91/model_manifest.json','artifacts/study_v124/jobs.json','artifacts/study_v124/cases.json','configs/study_v124.json','reports/protocol_v124.md','reports/protocol_v124.freeze.json','reports/surrogate_v124.md','requirements.lock.txt'};specs={s['id']:s for s in read(ROOT/'data/manifest_v41.json')['datasets']}
 if '--corrected' in sys.argv:names.update(['reports/attainability_v125.md','results/v125_design_audit/attainability.json','results/v42_selection_reference/summary.json'])
 for j in read(ROOT/'artifacts/study_v124/cases.json'):names.add(j['prefix']);names.add(specs[j['dataset']]['path']);names.update(refpaths(j['key']).values())
 for folder in ['artifacts/study_v124/prompts','artifacts/sources/v124','results/v124_surrogate','results/v124_analysis']:
  names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='server.log')
 for n in sorted(names):dest=out/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dest)
 shutil.copyfile(ROOT/'scripts/replay_surrogate_v124_standalone.py',out/'replay.py')
 (out/'README.md').write_text('# Private V124 saved-evidence replay\n\nRead reports/attainability_v125.md when present: the fixed pools make the original joint5% quality screen impossible. Format/reliability measurements remain valid; this is not evidence against unrestricted LLM optimization.\n\nRun `python3 -I replay.py`. Standard library only; no installation, network, model or new objective acquisition. Checks requests, numeric sample handling, raw acquired prompts, EI/mean selections, same-prefix controls and60charged source cells. Full-project verifier additionally reconstructs candidate restrictions and checks all protocol dependencies; this compact subset is not a fresh inference replication or full dependency closure.\n\nThree exposed development families, one prefix each. Not held-out validation, complete LLAMBO replication or journal-readiness evidence. Owner source files are included for read-only method audit with their MIT license; the replay never imports them. Data source redistribution qualifications remain in data/manifest_v41.json: local private review only, no grant to publish the source tables. No weights or runtime binary included.\n')
 write(out/'manifest.json',{'scope':'Private saved-evidence subset','files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}})
 archive=ROOT/'output'/(bundle+'.zip');assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'compressed bytes')
if __name__=='__main__':main()
