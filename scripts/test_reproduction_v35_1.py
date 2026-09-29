"""Bounded isolated cross-interpreter replay and corruption checks on temporary copies."""
import argparse,hashlib,json,subprocess,sys,tempfile,time
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/reproduction_v35_1'

def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--second-python',type=Path,required=True);a=p.parse_args()
    if (OUT/'validation.json').exists():raise FileExistsError('Preserve completed validation')
    receipts=[];started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='llm-v35_1-validation-') as folder:
        root=Path(folder)
        with ZipFile(a.archive) as z:
            for n in z.namelist():
                if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError('Unsafe extraction')
            z.extractall(root)
        project=root/'llm-escalation-v34-reproduction'
        def run(python):
            start=time.perf_counter();r=subprocess.run([str(python),'-I','-S','scripts/verify_reproduction_v35_1.py'],cwd=project,text=True,capture_output=True,timeout=60)
            return {'interpreter':str(python),'exit_code':r.returncode,'wall_seconds':time.perf_counter()-start,'stdout':r.stdout,'stderr':r.stderr}
        for label,python in [('python310',Path(sys.executable)),('python312',a.second_python)]:
            result=run(python);save(label+'.json',result)
            if result['exit_code']!=0:raise RuntimeError('Clean isolated replay failed: '+label+' '+result['stderr'])
            receipts.append(json.loads(result['stdout']))
        scientific=[{k:v for k,v in r.items() if k!='runtime'} for r in receipts]
        if scientific[0]!=scientific[1]:raise ValueError('Cross-interpreter scientific results differ')
        arm=sorted((project/'results/v34_constrained/arms').glob('*_joint_shortlist.json'))[0]
        cached=sorted((project/'results/v34_constrained/arms').glob('*_cached_llm_assigned_ids.json'))[0]
        prefix=sorted((project/'results/v34_constrained/prefixes').glob('*.json'))[0]
        progress=project/'results/v34_constrained/progress.json';summary=project/'results/v34_constrained/summary.json';journal=project/'results/v34_constrained/acquisitions.jsonl'
        manifest=project/'REPRODUCTION_MANIFEST.json';index_bytes=manifest.read_bytes()
        def json_change(path,fn):
            value=json.loads(path.read_text());fn(value);path.write_text(json.dumps(value,indent=2)+'\n')
        def bad_label():json_change(arm,lambda v:v['labels'][10].__setitem__(0,v['labels'][10][0]+1))
        def bad_budget():json_change(arm,lambda v:v.__setitem__('logical_evaluations',19))
        def duplicate():json_change(arm,lambda v:v['ids'].__setitem__(10,v['ids'][0]))
        def bad_cap():json_change(prefix,lambda v:v['prefix'].__setitem__('size_cap',v['prefix']['size_cap']+1))
        def bad_cache():json_change(cached,lambda v:v['cached_request'].__setitem__('request_id',99999))
        def bad_charge():
            rows=[json.loads(s) for s in journal.read_text().splitlines()];rows[0]['vector_charge']=0
            journal.write_text(''.join(json.dumps(r)+'\n' for r in rows))
        def missing_arm():json_change(progress,lambda v:v['arms'].pop())
        def bad_aggregate():json_change(summary,lambda v:v['summaries'][0].__setitem__('equal_family_constrained_gain',.5))
        cases=[('checksum',arm,lambda:arm.write_bytes(arm.read_bytes()+b' '),False,'Changed bundle file'),
            ('acquired_label',arm,bad_label,True,'Source-bound acquired states'),('inclusive_budget',arm,bad_budget,True,'Inclusive evaluation budget'),
            ('duplicate_acquisition',arm,duplicate,True,'Source-bound acquired states'),('prefix_cap',prefix,bad_cap,True,'Acquired-prefix size cap'),
            ('cached_request',cached,bad_cache,True,'Cached request identity'),('vector_charge',journal,bad_charge,True,'Charged acquisition denominator'),
            ('missing_completed_arm',progress,missing_arm,True,'Completed intended denominator'),('aggregate_score',summary,bad_aggregate,True,'Independent aggregate summary')]
        checks=[]
        for name,path,change,rebind,expected in cases:
            original=path.read_bytes()
            try:
                change()
                if rebind:
                    index=json.loads(index_bytes);b=path.read_bytes();index['files'][path.relative_to(project).as_posix()]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
                    manifest.write_text(json.dumps(index,indent=2)+'\n')
                result=run(Path(sys.executable));entry={'case':name,'index_rebound':rebind,'expected_invariant':expected,**result}
                checks.append(entry);save('corruption_checks.json',checks)
                if result['exit_code']==0 or expected not in result['stderr']:raise ValueError('Corruption failed intended detection: '+name)
            finally:path.write_bytes(original);manifest.write_bytes(index_bytes)
        restored=run(Path(sys.executable));save('restored.json',restored)
        if restored['exit_code']!=0:raise RuntimeError('Restored extraction did not verify')
        # Rebuild from the same frozen project into another temporary output.
        duplicate_zip=root/'determinism.zip';rebuild=subprocess.run([sys.executable,str(ROOT/'scripts/build_reproduction_v35_1.py'),'--output',str(duplicate_zip)],cwd=ROOT,text=True,capture_output=True,timeout=60)
        save('deterministic_rebuild.json',{'exit_code':rebuild.returncode,'stdout':rebuild.stdout,'stderr':rebuild.stderr})
        if rebuild.returncode!=0 or duplicate_zip.read_bytes()!=a.archive.read_bytes():raise ValueError('Deterministic ZIP rebuild mismatch')
    result={'verified':True,'archive_sha256':hashlib.sha256(a.archive.read_bytes()).hexdigest(),'archive_bytes':a.archive.stat().st_size,
        'interpreters':[r['runtime'] for r in receipts],'identical_scientific_outputs':True,'corruptions_rejected':len(checks),
        'semantic_corruptions_after_index_rebinding':8,'restored_clean_replay':True,'byte_identical_rebuild':True,
        'maintenance_wall_seconds':time.perf_counter()-started,'new_inference':0,'new_objective_acquisitions':0,
        'scope':'Temporary extraction outside checkout; same host; standard library only; no fresh inference'}
    save('validation.json',result);print(json.dumps(result,indent=2))

if __name__=='__main__':main()
