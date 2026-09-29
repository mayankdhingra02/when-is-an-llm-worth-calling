"""Compact private evidence bundle, excluding runtime binaries and model weights."""
import shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha

def main():
 out=ROOT/'output/v128_replay';out.mkdir(exist_ok=False)
 names={'data/manifest_v119.json','data/manifest_v121.json','artifacts/study_v91/model_manifest.json','artifacts/study_v128/jobs.json','artifacts/study_v128/cases.json','configs/study_v128.json','reports/protocol_v128.md','reports/protocol_v128.freeze.json','reports/proposals_v128.md','scripts/proposal_v127.py','scripts/proposal_v128.py','requirements.lock.txt','artifacts/study_v128/synthetic_offline_tokenizer.json','artifacts/study_v128/structural_preflight.json'}
 for j in read(ROOT/'artifacts/study_v128/cases.json'):
  names.add(j['prefix']);v=j['classical_version'];spec=read(ROOT/f'data/manifest_v{v}.json')['datasets'][0];names.add(spec['path'])
  for m in ['batch_3nn','full_sequential_3nn','random_full','single_portfolio']:names.add(f"results/v{v}_classical/arms/{j['key']}_{m}.json")
  names.add(f"results/v120_analysis/arms/{j['key']}.json" if v==119 else f"results/v121_classical/arms/{j['key']}_presentation_first10.json")
 for folder in ['artifacts/study_v128/prompts','results/v128_proposals','results/v128_analysis']:
  names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='server.log')
 for n in names:
  p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,p)
 shutil.copyfile(ROOT/'scripts/replay_proposal_v128_interrupted_standalone.py',out/'replay.py')
 (out/'README.md').write_text('# Private V128 saved-evidence replay\n\nRun `python3 -I -S replay.py`. Python standard library only; no installation, model, network or new objective acquisition. Checks real response provenance, strict failures, prefix-only messages, feature-only projection, independently reconstructed batch3NN ranking,300 charged outcomes and all paired comparisons. This compact evidence subset does not include the full project/runtime dependency closure; the full-project verifier checks that separately. No model weights or runtime binaries are included.\n\nBoth families are exposed development data, not a held-out controller test or full source-method replication. Read reports/proposals_v128.md including all failures and controls. Data redistribution qualifications remain in data/manifest_v119.json and data/manifest_v121.json; local private review only, no public source-table grant. No upload or publication.\n')
 write(out/'manifest.json',{'scope':'Compact V128 private saved-evidence subset,not full protocol dependency closure','files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}})
 archive=ROOT/'output/v128_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'bytes')
if __name__=='__main__':main()
