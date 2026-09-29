"""Build and actually check a compact, isolated saved-outcome archive."""
import hashlib,json,shutil,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    art=ROOT/'artifacts/reproduction_v84';art.mkdir(exist_ok=False);bundle=art/'bundle';bundle.mkdir()
    names=['scripts/replay_h2_v84_portable.py','src/native_v83/H2Probe.java','src/escalation/h2_v84.py','reports/protocol_v83.md','reports/protocol_v84.md','reports/h2_v84.md','reports/novelty_boundary_v84.md','requirements.lock.txt']
    for d in ['results/v84_h2_classical','results/v84_h2_analysis']:
        names += [str(p.relative_to(ROOT)) for p in (ROOT/d).rglob('*') if p.is_file()]
    for n in names:
        dest=bundle/n;dest.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(ROOT/n,dest)
    (bundle/'README.md').write_text('''# H2 V84 saved-outcome reconstruction

Run `python3 -I -S scripts/replay_h2_v84_portable.py` with Python3.10+.
No installation, network or model required. Verifies retained native answers,
settings, indexes, budgets and reported confirmation results. Does not rerun
H2, RF selection, or inference. Java source is included for inspection; native
JAR/runtime and older evidence are omitted. Full original repository contains
pinned-dependency RF replay and source retrieval/build instructions. All seeds
belong to one exposed H2 family. No LLM treatment was run in V84.
''')
    files={str(p.relative_to(bundle)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(bundle.rglob('*')) if p.is_file()}
    (bundle/'manifest.json').write_text(json.dumps({'scope':'H2 V84 outcome reconstruction','files':files},indent=2)+'\n')
    archive=ROOT/'output/h2_v84_outcome_reconstruction.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(bundle.rglob('*')):
            if p.is_file():z.write(p,str(p.relative_to(bundle)))
    extracted=art/'extracted'
    with zipfile.ZipFile(archive) as z:z.extractall(extracted)
    def run(folder):
        cmd=[sys.executable,'-I','-S',str(folder/'scripts/replay_h2_v84_portable.py')];r=subprocess.run(cmd,capture_output=True,text=True,timeout=120,cwd=folder)
        return {'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    base=run(extracted);assert base['exit_code']==0,base
    corruptions=[]
    for name in ['metric','budget','denominator']:
        # Sequentially mutate one file in the extracted COPY; restore exact bytes.
        rel='results/v84_h2_classical/summary.json' if name=='denominator' else 'results/v84_h2_analysis/summary.json'
        p=extracted/rel;original=p.read_bytes();m=extracted/'manifest.json';original_manifest=m.read_bytes();data=json.loads(original)
        if name=='metric':data['cases'][0]['arms']['rf_lcb']['median_seconds']+=1
        elif name=='budget':data['cases'][0]['arms']['rf_lcb']['logical_evaluations']=19
        else:data['charged_trials']=164
        p.write_text(json.dumps(data));mf=json.loads(original_manifest);mf['files'][rel]={'sha256':sha(p),'bytes':p.stat().st_size};m.write_text(json.dumps(mf))
        result=run(extracted);assert result['exit_code']!=0,(name,result);corruptions.append({'mutation':name,**result})
        p.write_bytes(original);m.write_bytes(original_manifest)
    report={'archive':str(archive.relative_to(ROOT)),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'python':sys.version,'valid_replay':base,'synthetic_corruption_rejections':corruptions,'scope':'isolated standard-library saved-outcome replay, not clean-machine/native/optimizer replication'}
    (art/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['valid_replay','synthetic_corruption_rejections']},indent=2))
if __name__=='__main__':main()
