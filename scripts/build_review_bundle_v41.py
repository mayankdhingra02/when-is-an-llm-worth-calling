"""Build and test a deterministic local review kit, excluding weights/full tables."""
import hashlib,json,os,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.chdir(ROOT)
from escalation.io import read,write
from escalation.resources import Resources
from escalation.transfer_v41 import current_config

def main():
    target=Path('output/llm_escalation_v41_review.zip')
    if target.exists():raise ValueError('Preserve published local artifact identity')
    paths=[Path('data/manifest_v41.json'),Path('reports/models_v41.md'),Path('reports/source_audit_v41.md'),
        Path('reports/protocol_v41_transfer.md'),Path('reports/protocol_v41_transfer.freeze.json'),Path('reports/analysis_addendum_v41.md'),
        Path('reports/policy_transfer_v41.md'),Path('scripts/verify_model_results_v41.py'),Path('scripts/verify_review_bundle_v41.py'),
        Path('artifacts/model_manifest.json'),Path('artifacts/model_manifest_v22.json'),Path('requirements.lock.txt')]
    for folder in ('results/v41_transfer','results/v41_models','results/v41_model_analysis','results/v41_policy_precommit','artifacts/study_v41'):
        paths += [p for p in Path(folder).rglob('*') if p.is_file() and p.suffix in ('.json','.jsonl','.csv','.png','.svg','.log')]
    paths=sorted(set(paths));content={str(p):p.read_bytes() for p in paths}
    content['REVIEW_V41.md']=b'''# V41 local results review kit\n\nStart with reports/models_v41.md. Run:\n\n    python3 -I -S scripts/verify_review_bundle_v41.py\n\nThis uses only the Python standard library, verifies every bundled evidence hash, and independently replays420exact comparisons and108policy means from acquired records. It makes no model call or new objective acquisition.\n\nThis is a results-replay subset of the local repository, not the full inference environment. Full source tables, model weights and third-party papers are deliberately omitted. Manifest URLs/hashes and model identities preserve provenance. Reproducing fresh inference and source-row authenticity checks needs those original inputs and the full project. Bundled source-check receipts document what ran locally; they do not make omitted source files independently verifiable inside this kit.\n\nAll60model cases are retained, including original infrastructure-failure logs and recovery metadata. Synthetic fixtures are not research outputs. No new-model generalization, application-utility validation, or journal acceptance is established. This local artifact has not been uploaded or published. Review dataset licensing before external redistribution.\n'''
    content['bundle_manifest_v41.json']=json.dumps({'scope':'Local measured-results replay only','sha256':{p:hashlib.sha256(data).hexdigest() for p,data in sorted(content.items())}},indent=2).encode()
    before=read('artifacts/resource_ledger_v2.json');receipts=[]
    with Resources(current_config(),'artifacts/resource_ledger_v2.json') as resource:
        resource.check();target.parent.mkdir(exist_ok=True)
        with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name,data in sorted(content.items()):
                info=zipfile.ZipInfo(name,(2026,9,25,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16
                z.writestr(info,data)
        dest=Path('artifacts/study_v41/bundle_validation/clean');dest.mkdir(parents=True,exist_ok=False)
        with zipfile.ZipFile(target) as z:z.extractall(dest)
        for interpreter in [str(ROOT/'.venv/bin/python'),'/Users/mayankdhingra/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3']:
            result=subprocess.run([interpreter,'-I','-S',str((dest/'scripts/verify_review_bundle_v41.py').resolve())],capture_output=True,text=True,timeout=45)
            receipts.append({'interpreter':interpreter,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
            if result.returncode:raise RuntimeError(result.stderr)
        if json.loads(receipts[0]['stdout'])!=json.loads(receipts[1]['stdout']):raise ValueError('Interpreter discrepancy')
        # Synthetic corruption of extracted copy only. Original measured evidence
        # and the finalized archive are never modified by this negative test.
        victim=dest/'results/v41_models/acquisitions.jsonl';original=victim.read_bytes();victim.write_bytes(original+b'\n')
        failure=subprocess.run([str(ROOT/'.venv/bin/python'),'-I','-S',str((dest/'scripts/verify_review_bundle_v41.py').resolve())],capture_output=True,text=True,timeout=45)
        victim.write_bytes(original)
        if failure.returncode==0 or 'Changed/missing bundle evidence' not in failure.stderr:raise ValueError('Corruption was not detected')
    after=read('artifacts/resource_ledger_v2.json')
    write('artifacts/study_v41/review_bundle.json',{'path':str(target),'bytes':target.stat().st_size,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),
        'files':len(content),'validation':receipts,'synthetic_corruption_rejected':True,'seconds':after['experiment_seconds']-before['experiment_seconds'],
        'new_model_calls':0,'new_objective_acquisitions':0,'uploaded_or_published':False})
    print('Validated',target,target.stat().st_size,'bytes;',len(content),'files; two interpreters; corruption rejected')
if __name__=='__main__':main()
