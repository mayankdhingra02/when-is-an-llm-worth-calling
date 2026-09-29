"""Create a bounded portable analysis bundle and test reconstruction/corruptions."""
import hashlib,json,shutil,subprocess,sys,zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    art=ROOT/'artifacts/reproduction_v86_1';art.mkdir(exist_ok=False);bundle=art/'bundle';bundle.mkdir()
    freeze=json.loads((ROOT/'reports/protocol_v86.freeze.json').read_text());names=set(freeze['sha256'])|{'reports/protocol_v86.freeze.json','reports/frontier_v86.md','reports/source_followup_v86.md','reports/source_followup_v86_addendum.md','scripts/replay_frontier_v86.py','scripts/report_frontier_v86.py','requirements.lock.txt'}
    names.update(str(p.relative_to(ROOT)) for p in (ROOT/'results/v86_frontier').iterdir() if p.is_file())
    for n in sorted(names):
        dst=bundle/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/n,dst)
    (bundle/'README.md').write_text('''# V86 control-aware opportunity reconstruction

Run `python3 -I -S scripts/replay_frontier_v86.py` with Python3.10+.
No installation, network or model needed. Recomputes all65,664 masks from
included saved summaries. Three exposed software families,25cases; not25
independent systems. H2 prior differs in budget and is standalone substitution.
This does not reconstruct native trials, original RF choices or LLM outputs.
Original full repository retains raw provenance. Figures need matplotlib
from the full repository pinned requirements; replay itself uses only stdlib.
No third-party binaries/model weights/corpus or paper text are redistributed.
''')
    def manifest():
        return {'scope':'saved-summary exact frontier replay only','files':{str(p.relative_to(bundle)):{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(bundle.rglob('*')) if p.is_file() and p.name!='manifest.json'}}
    (bundle/'manifest.json').write_text(json.dumps(manifest(),indent=2)+'\n')
    archive=ROOT/'output/frontier_v86_1_reproduction.zip';assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(bundle.rglob('*')):
            if p.is_file():
                info=zipfile.ZipInfo(str(p.relative_to(bundle)),date_time=(2026,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o644<<16;z.writestr(info,p.read_bytes())
    extracted=art/'extracted'
    with zipfile.ZipFile(archive) as z:z.extractall(extracted)
    def run():
        cmd=[sys.executable,'-I','-S',str(extracted/'scripts/replay_frontier_v86.py')];r=subprocess.run(cmd,cwd=extracted,capture_output=True,text=True,timeout=60)
        return {'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr}
    base=run();assert base['exit_code']==0,base;mutations=[]
    for kind in ['reported_oracle','dropped_case','inconsistent_source_median']:
        n='results/v86_frontier/summary.json' if kind=='reported_oracle' else 'results/v80_kanzi_analysis/summary.json'
        p=extracted/n;f=extracted/'reports/protocol_v86.freeze.json';m=extracted/'manifest.json';old={q:q.read_bytes() for q in [p,f,m]};data=json.loads(p.read_text())
        if kind=='reported_oracle':data['comparisons'][0]['observed_oracle_gain_pct']=99
        elif kind=='dropped_case':data['cases'].pop()
        else:data['cases'][0]['arms']['llm']['median_bytes']+=1
        p.write_text(json.dumps(data));ff=json.loads(f.read_text())
        if n in ff['sha256']:ff['sha256'][n]=sha(p);f.write_text(json.dumps(ff))
        mm=json.loads(m.read_text())
        for q in [p,f]:mm['files'][str(q.relative_to(extracted))]={'sha256':sha(q),'bytes':q.stat().st_size}
        m.write_text(json.dumps(mm));r=run();assert r['exit_code']!=0,(kind,r);mutations.append({'synthetic_mutation':kind,**r})
        for q,b in old.items():q.write_bytes(b)
    report={'archive':str(archive.relative_to(ROOT)),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,'python':sys.version,'valid_replay':base,'synthetic_corruptions_rejected_after_rehashing':mutations,'scope':'same-host isolated extracted stdlib analysis replay; not independent native replication'}
    (art/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['valid_replay','synthetic_corruptions_rejected_after_rehashing']},indent=2))
if __name__=='__main__':main()
