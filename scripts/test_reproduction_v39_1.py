"""Bounded cross-interpreter and negative-control validation on temporary copies."""
import argparse,hashlib,json,subprocess,sys,tempfile,time
from pathlib import Path
from zipfile import ZipFile
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'artifacts/reproduction_v39_1'
def save(name,value):(OUT/name).write_text(json.dumps(value,indent=2)+'\n')
def main():
    p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True);p.add_argument('--second-python',type=Path,required=True);a=p.parse_args()
    if (OUT/'validation.json').exists():raise FileExistsError('Preserve completed validation')
    started=time.perf_counter()
    with tempfile.TemporaryDirectory(prefix='llm-v39-validation-') as folder:
        root=Path(folder)
        with ZipFile(a.archive) as z:
            for n in z.namelist():
                if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError('Unsafe extraction')
            z.extractall(root)
        project=root/'llm-escalation-v38-reproduction'
        def run(python):
            t=time.perf_counter();r=subprocess.run([str(python),'-I','-S','scripts/verify_reproduction_v39.py'],cwd=project,text=True,capture_output=True,timeout=120)
            return {'interpreter':str(python),'exit_code':r.returncode,'wall_seconds':time.perf_counter()-t,'stdout':r.stdout,'stderr':r.stderr}
        outputs=[]
        for label,python in [('python310',sys.executable),('python312',a.second_python)]:
            result=run(python);save(label+'.json',result)
            if result['exit_code']!=0:raise RuntimeError('Isolated replay failed: '+label+' '+result['stderr'])
            outputs.append(json.loads(result['stdout']))
        if [{k:v for k,v in r.items() if k!='runtime'} for r in outputs][0]!={k:v for k,v in outputs[1].items() if k!='runtime'}:raise ValueError('Cross-version mismatch')
        index=project/'REPRODUCTION_MANIFEST.json';index_original=index.read_bytes()
        freezes={p:p.read_bytes() for p in project.glob('reports/*.freeze.json')}
        def rebind(path):
            changed={path.relative_to(project).as_posix():hashlib.sha256(path.read_bytes()).hexdigest()}
            for _ in range(len(freezes)+1):
                altered=False
                for p in freezes:
                    data=json.loads(p.read_text());before=p.read_bytes()
                    for n,h in changed.items():
                        if n in data['sha256']:data['sha256'][n]=h
                    # Avoid modifying unchanged files merely to reformat them.
                    if data!=json.loads(before):
                        p.write_text(json.dumps(data,indent=2)+'\n');changed[p.relative_to(project).as_posix()]=hashlib.sha256(p.read_bytes()).hexdigest();altered=True
                if not altered:break
            data=json.loads(index_original)
            for name in changed:
                b=(project/name).read_bytes();data['files'][name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
            index.write_text(json.dumps(data,indent=2)+'\n')
        def json_change(path,fn):
            value=json.loads(path.read_text());fn(value);path.write_text(json.dumps(value,indent=2)+'\n')
        def jsonl_change(path,fn):
            value=[json.loads(s) for s in path.read_text().splitlines()];fn(value);path.write_text(''.join(json.dumps(r)+'\n' for r in value))
        arm=project/'results/v38_size_prompt/arms/00.json';req=project/'results/v38_size_prompt/requests.jsonl';summary=project/'results/v38_size_prompt/summary.json'
        progress=project/'results/v38_size_prompt/progress.json';journal=project/'results/v38_size_prompt/acquisitions.jsonl'
        cases=[('checksum',arm,lambda:arm.write_bytes(arm.read_bytes()+b' '),False,'Bundle checksum'),
               ('raw_response',req,lambda:jsonl_change(req,lambda v:v[0].__setitem__('raw_output','X\n')),True,'Output token decoding'),
               ('cache_identity',req,lambda:jsonl_change(req,lambda v:v[0].__setitem__('cache_key','bad')),True,'Cache identity'),
               ('acquired_label',arm,lambda:json_change(arm,lambda v:v['labels'][10].__setitem__(0,'999')),True,'Source-bound response selection'),
               ('duplicate_row',arm,lambda:json_change(arm,lambda v:v['ids'].__setitem__(10,v['ids'][0])),True,'Source-bound response selection'),
               ('inclusive_budget',arm,lambda:json_change(arm,lambda v:v.__setitem__('logical_evaluations',19)),True,'Inclusive budget'),
               ('missing_arm',progress,lambda:json_change(progress,lambda v:v['arms'].pop()),True,'Completed denominator'),
               ('free_acquisition',journal,lambda:jsonl_change(journal,lambda v:v[0].__setitem__('vector_charge',0)),True,'Acquisition charges'),
               ('aggregate',summary,lambda:json_change(summary,lambda v:v['summaries'][0].__setitem__('equal_family_mean_gain',.9)),True,'Independent aggregate'),
               ('family_mean',summary,lambda:json_change(summary,lambda v:v['summaries'][0]['families'][0].__setitem__('mean_gain',.9)),True,'Family mean')]
        receipts=[]
        for name,path,change,rebound,expected in cases:
            original=path.read_bytes()
            try:
                change()
                if rebound:rebind(path)
                result=run(sys.executable);receipts.append({'case':name,'checksums_rebound':rebound,'expected_invariant':expected,**result});save('corruption_checks.json',receipts)
                if result['exit_code']==0 or expected not in result['stderr']:raise ValueError('Wrong corruption outcome: '+name+' '+result['stderr'])
            finally:
                path.write_bytes(original)
                for p,b in freezes.items():p.write_bytes(b)
                index.write_bytes(index_original)
        restored=run(sys.executable);save('restored.json',restored)
        if restored['exit_code']!=0:raise RuntimeError('Restored replay failed')
        duplicate=root/'repeat.zip';rebuild=subprocess.run([sys.executable,str(ROOT/'scripts/build_reproduction_v39_1.py'),'--output',str(duplicate)],cwd=ROOT,text=True,capture_output=True,timeout=120)
        save('deterministic_rebuild.json',{'exit_code':rebuild.returncode,'stdout':rebuild.stdout,'stderr':rebuild.stderr})
        if rebuild.returncode or duplicate.read_bytes()!=a.archive.read_bytes():raise ValueError('Deterministic rebuild failed')
    result={'verified':True,'archive_sha256':hashlib.sha256(a.archive.read_bytes()).hexdigest(),'archive_bytes':a.archive.stat().st_size,
            'interpreters':[r['runtime'] for r in outputs],'identical_scientific_outputs':True,'corruptions_rejected':len(receipts),
            'semantic_corruptions_with_rebound_hashes':len(receipts)-1,'restored_clean_replay':True,'byte_identical_rebuild':True,
            'maintenance_wall_seconds':time.perf_counter()-started,'new_inference':0,'new_objective_acquisitions':0,
            'scope':'Temporary extraction outside checkout; same host; Python standard library only; saved evidence'}
    save('validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
