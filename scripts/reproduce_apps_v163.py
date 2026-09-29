"""Regenerate analysis only and compare bytes; no native/model requests."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v163'
FILES=['reports/apps_v163.md','reports/apps_feasibility_v163.md','results/v163_native/comparison.json','results/v163_native/paired_gains.png','results/v163_native/paired_gains.svg','results/v163_native/representation_diagnostic.json','artifacts/study_v163/feasibility_replay.json','artifacts/study_v163/feasibility.png','artifacts/study_v163/feasibility.svg','artifacts/study_v163/replay.json']
def digest(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
def main():
 before={n:digest(n) for n in FILES};env=dict(os.environ,MPLCONFIGDIR='/tmp/mpl-v163')
 for script in ['report_apps_v163.py','report_apps_feasibility_v163.py','diagnose_apps_v163.py','verify_apps_v163.py']:
  subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,env=env,check=True,timeout=120,stdout=subprocess.DEVNULL)
 after={n:digest(n) for n in FILES};assert before==after
 (A/'reproduction.json').write_text(json.dumps({'byte_identical':True,'artifacts':after,'new_model_requests':0,'new_native_outcomes':0,'scope':'Internal saved-data replay; not fresh collection or external replication'},indent=2)+'\n');print(json.dumps({'byte_identical':True,'artifacts':len(after)}))
if __name__=='__main__':main()
