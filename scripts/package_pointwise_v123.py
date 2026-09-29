"""Private compact saved-evidence bundle; no model weights/binary or publication."""
import shutil,zipfile
from collect_smollm_v47 import ROOT,read,write,sha
from analyze_pointwise_v123 import refpaths

def main():
    out=ROOT/'output/v123_replay';out.mkdir(exist_ok=False)
    names={'data/manifest_v41.json','artifacts/study_v91/model_manifest.json','artifacts/study_v123/jobs.json','artifacts/study_v123/cases.json','configs/study_v123.json','reports/protocol_v123.md','reports/protocol_v123.freeze.json','reports/pointwise_v123.md','requirements.lock.txt'}
    specs={s['id']:s for s in read(ROOT/'data/manifest_v41.json')['datasets']}
    for j in read(ROOT/'artifacts/study_v123/cases.json'):names.add(j['prefix']);names.add(specs[j['dataset']]['path']);names.update(refpaths(j['key']).values())
    for folder in ['artifacts/study_v123/prompts','results/v123_pointwise','results/v123_analysis']:
        names.update(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file() and p.name!='server.log')
    for name in sorted(names):dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
    shutil.copyfile(ROOT/'scripts/replay_pointwise_v123_standalone.py',out/'replay.py')
    (out/'README.md').write_text('# Private V123 saved-evidence replay\n\nRun `python3 -I replay.py`. Standard library only; no network, install, model weights or fresh inference. Verifies request settings, transformed observed-only prompts, scalar selections, paired states and30charged source cells, plus intervention diagnostic counts. Full-project verifier additionally checks original feature restriction and all protocol dependencies; this compact package does not reproduce model generation or execute the full study.\n\nThree exposed development families, one prefix each. Results are not held-out validation or Q2 acceptance evidence. Sources retain manifest owners, pinned revisions and unresolved data-specific redistribution limitations. Local private review only; no grant to publish the bundled source tables. Qwen3-8B Q4_K_M revision/blob are recorded in the owner model manifest; weights must be independently obtained under their license for fresh inference.\n')
    write(out/'manifest.json',{'scope':'Private standard-library replay subset, not complete protocol dependency closure','files':{str(p.relative_to(out)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}})
    archive=ROOT/'output/v123_replay.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(out.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(out)))
    print('Packaged',len(read(out/'manifest.json')['files']),'files;',archive.stat().st_size,'compressed bytes')
if __name__=='__main__':main()
