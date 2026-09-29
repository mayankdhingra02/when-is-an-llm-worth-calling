"""Compact private evidence bundle, excluding runtime binaries and model weights."""
import shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha

def main():
 out=ROOT/'output/v127_replay';out.mkdir(exist_ok=False)
 names={'data/manifest_v41.json','artifacts/study_v91/model_manifest.json','artifacts/study_v127/jobs.json','artifacts/study_v127/cases.json','configs/study_v127.json','reports/protocol_v127.md','reports/protocol_v127.freeze.json','reports/proposals_v127.md','scripts/proposal_v127.py','requirements.lock.txt','reports/capacity_correction_v127.md','reports/verification_correction_v127.md','reports/source_mapping_v127.md','artifacts/study_v127/output_capacity.json','artifacts/study_v127/synthetic_offline_tokenizer.json','artifacts/study_v127/synthetic_tokenizer_diagnostic.json'}
 specs={s['id']:s for s in read(ROOT/'data/manifest_v41.json')['datasets']}
 for j in read(ROOT/'artifacts/study_v127/cases.json'):
  names.add(j['prefix']);names.add(specs[j['dataset']]['path'])
  for m in ['batch_3nn','full_sequential_3nn','random_full']:names.add(f"results/v41_transfer/arms/{j['key']}_{m}.json")
  names.add(f"results/v41_models/0.5/arms/{j['key']}.json")
  p=f"results/v115_portfolio/arms/{j['key']}.json"
  if (ROOT/p).exists():names.add(p)
 for folder in ['artifacts/study_v127/prompts','results/v127_proposals','results/v127_analysis']:
  names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='server.log')
 for n in names:
  p=out/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,p)
 shutil.copyfile(ROOT/'scripts/replay_proposal_v127_standalone.py',out/'replay.py')
 (out/'README.md').write_text('# Private V127 saved-evidence replay\n\nRun `python3 -I -S replay.py`. Python standard library only; no installation, model, network or new objective acquisition. Checks real response provenance, strict failures, prefix-only messages, feature-only projection, independently reconstructed batch3NN ranking,900charged outcomes and all paired comparisons. This compact evidence subset does not include the full project/runtime dependency closure; the full-project verifier checks that separately. No model weights or runtime binaries are included.\n\nAll six families are exposed development data, not a held-out controller test or full source-method replication. Read reports/proposals_v127.md including all failures and controls. Data redistribution qualifications remain in data/manifest_v41.json; local private review only, no public source-table grant. No upload or publication.\n')
 write(out/'manifest.json',{'scope':'Compact V127 private saved-evidence subset,not full protocol dependency closure','files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}})
 archive=ROOT/'output/v127_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
  for p in sorted(out.rglob('*')):
   if p.is_file():z.write(p,str(p.relative_to(out)))
 print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'bytes')
if __name__=='__main__':main()
