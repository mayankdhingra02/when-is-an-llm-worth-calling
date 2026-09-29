"""Create a local review bundle without model/runtime binaries or corpus payloads."""
import hashlib,json,shutil,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    assert json.loads((ROOT/'artifacts/study_v80_execution/supplementary_verification.json').read_text())['verified']
    dest=ROOT/'output/v80_portable';dest.mkdir(exist_ok=False)
    paths=[]
    for directory in ['results/v80_kanzi_paired','results/v80_kanzi_analysis']:
        paths.extend(p for p in (ROOT/directory).rglob('*') if p.is_file())
    paths.extend((ROOT/'results/v79_kanzi_classical').glob('prefix_*.json'))
    paths.extend(ROOT/n for n in ['artifacts/study_v79/workloads.json','artifacts/study_v80_execution/user_approval.json','artifacts/study_v80_execution/resource_ledger.json','artifacts/study_v80_execution/supplementary_verification.json','reports/protocol_v80.md','reports/protocol_v80.freeze.json','reports/kanzi_v80.md','reports/workload_audit_v79.md','scripts/replay_kanzi_v80_portable.py','requirements.lock.txt'])
    for p in paths:
        q=dest/p.relative_to(ROOT);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    readme='''# V80 local outcome-reconstruction bundle\n\nRun `python3 -I -S scripts/replay_kanzi_v80_portable.py` from an extracted copy. Python3.10+; standard library only. The verifier checks file hashes, all450charge/validation receipts,45arm budgets/shared prefixes, selected incumbents, real response/request denominators and published means/win counts/token totals.\n\nThis reconstructs saved outcomes. It does not rerun RF training/selection, native compression, the local model, or prove clean-machine runtime replication. Full acquired-only RF/grammar decision replay was performed separately with the pinned project environment. Original freeze references files intentionally absent here (model, runtime, corpus and older history); this bundle's manifest describes only its included files.\n\nNo model weights, executable runtimes or raw corpus bytes are included. Owner corpus URLs/hashes are retained for provenance; no corpus redistribution license is asserted. Raw local process commands contain host paths. No credentials are intentionally included. This archive is a local review artifact, not published or pushed anywhere.\n\nChecksums detect accidental changes; this is not a signed authenticity guarantee. See the report for the single-family/development scope, failed-run denominators and cost limits.\n'''
    (dest/'README.md').write_text(readme)
    files={str(p.relative_to(dest)):{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(dest.rglob('*')) if p.is_file()}
    (dest/'portable_manifest.json').write_text(json.dumps({'scope':'V80 saved outcome reconstruction only','files':files},indent=2)+'\n')
    archive=ROOT/'output/kanzi_v80_outcome_reconstruction.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(dest.rglob('*')):
            if p.is_file():
                info=zipfile.ZipInfo(str(p.relative_to(dest)),date_time=(2026,9,26,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,p.read_bytes())
    print(json.dumps({'included_files':len(files),'archive_bytes':archive.stat().st_size,'archive_sha256':hashlib.sha256(archive.read_bytes()).hexdigest()}))
if __name__=='__main__':main()
