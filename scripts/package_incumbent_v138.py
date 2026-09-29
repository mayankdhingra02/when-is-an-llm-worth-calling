"""Create-once private stdlib replay; full source tables and models excluded."""
import json,shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha
def main():
 dest=ROOT/'output/v138_replay';dest.mkdir(exist_ok=False);jobs=read(ROOT/'artifacts/study_v138/jobs.json');out=ROOT/'results/v138_incumbent'
 names={'scripts/verify_incumbent_v138.py','scripts/analyze_incumbent_v138.py','scripts/collect_smollm_v47.py','reports/incumbent_v138.md','reports/protocol_v138.md','reports/protocol_v138.freeze.json','configs/study_v138.json','artifacts/study_v138/jobs.json'}
 for j in jobs:
  names.update(j[k] for k in ['prefix','model_arm','classical_arm'])
  if j['system_group'] in ['llvm','sac']:names.update(f"results/v136_feedback/arms/{j['key']}_{m}.json" for m in ['feedback','masked'])
 names.update(str(p.relative_to(ROOT)) for p in out.rglob('*') if p.is_file())
 for group in sorted({j['system_group'] for j in jobs}):
  snapshot=f'artifacts/study_v138/candidates/{group}.json';names.add(snapshot);c=read(ROOT/snapshot);spec=c['spec'];p=ROOT/spec['path'];assert sha(p)==spec['sha256'];raw=p.read_text().splitlines();rowids=set()
  for j in [j for j in jobs if j['system_group']==group]:
   paths=[j['prefix'],j['model_arm'],j['classical_arm']]+[f"results/v138_incumbent/arms/{j['key']}_{m}.json" for m in ['fixed_prefix_neighbor','adaptive_incumbent_neighbor']]
   if group in ['llvm','sac']:paths.extend(f"results/v136_feedback/arms/{j['key']}_{m}.json" for m in ['feedback','masked'])
   for path in paths:rowids.update(read(ROOT/path)['state']['ids'])
  lineids={1}|{c['source_ids'][i] for i in rowids};path=f'artifacts/study_v138/source_extracts/{group}.json'
  write(ROOT/path,{'scope':'Header and already acquired rows only; omitted source file cannot be independently authenticated here','source_sha256':spec['sha256'],'lines':{str(n):raw[n-1] for n in sorted(lineids)}});names.add(path)
 for n in sorted(names):
  p=dest/n;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/n,p)
 (dest/'README.md').write_text('''# V138 private recorded-result replay

Run `python3 -I -S replay.py`. Standard library only, no network, model or new outcome acquisition.

Checks all 600 selections/acquisitions, shared prefixes, 60 B20 arms, source-row extracts, historical reference outcomes and contrasts. Full local replay additionally authenticates complete source files. This compact bundle cannot authenticate omitted tables, historic model/runtime execution, or all inherited protocol dependencies. Historical genuine-model provenance remains in the full V127/V135/V136 checkpoints; it is not re-created here. No new model calls were made in V138.

Six exposed systems are development evidence, not a held-out router evaluation. Includes already acquired observations for private review with previous source-license qualifications; no public redistribution right is asserted. Excludes full tables, new admission-source tables, models, binaries and synthetic fixtures. Figure regeneration needs the pinned repository and matplotlib; stdlib replay checks its underlying comparisons only.
''')
 (dest/'replay.py').write_text('''import hashlib,importlib.util,json
from pathlib import Path
root=Path(__file__).resolve().parent
for n,m in json.loads((root/'manifest.json').read_text())['files'].items():
 p=root/n;assert p.stat().st_size==m['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==m['sha256'],n
spec=importlib.util.spec_from_file_location('independent',root/'scripts/verify_incumbent_v138.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
print(json.dumps(m.verify(root,compact=True),indent=2))
''')
 paths=sorted(p for p in dest.rglob('*') if p.is_file());write(dest/'manifest.json',{'scope':'Transport hashes; semantic replay independently reconstructs decisions','files':{str(p.relative_to(dest)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in paths}})
 archive=ROOT/'output/v138_replay.zip';assert not archive.exists()
 with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in sorted(dest.rglob('*')):
   if p.is_file():z.write(p,p.relative_to(dest.parent))
 with zipfile.ZipFile(archive) as z:assert z.testzip() is None
 write(ROOT/'artifacts/study_v138/bundle.json',{'path':str(archive.relative_to(ROOT)),'bytes':archive.stat().st_size,'sha256':sha(archive),'hashed_files':len(paths),'crc_verified':True})
 print(read(ROOT/'artifacts/study_v138/bundle.json'))
if __name__=='__main__':main()
