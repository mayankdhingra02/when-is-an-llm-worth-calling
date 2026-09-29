"""Pre-generation freeze of the whole new proposal contract."""
from collect_smollm_v47 import ROOT,read,write,sha,now

def main():
 dest=ROOT/'reports/protocol_v127.freeze.json';assert not dest.exists();assert not (ROOT/'results/v127_proposals').exists()
 paths={ROOT/n for n in read(ROOT/'reports/protocol_v126.freeze.json')['sha256']}
 paths.update(ROOT/n for n in ['reports/protocol_v127.md','configs/study_v127.json','artifacts/study_v127/inputs.freeze.json','artifacts/study_v127/tests_precollection.log','artifacts/study_v127/tests_full_precollection.log','artifacts/study_v91/model_manifest.json'])
 paths.update(ROOT/n for n in read(ROOT/'artifacts/study_v127/inputs.freeze.json')['sha256'])
 for folder in ['scripts','tests/synthetic']:paths.update((ROOT/folder).glob('*v127.py'))
 for j in read(ROOT/'artifacts/study_v127/cases.json'):paths.add(ROOT/f"results/v41_models/0.5/arms/{j['key']}.json")
 write(dest,{'at':now(),'scope':'V127exposed development full-domain proposals;36requests,900recordedacquisitions,zero spend/downloads','sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(paths)}});print('Frozen',len(paths),'inputs',sha(dest))
if __name__=='__main__':main()
