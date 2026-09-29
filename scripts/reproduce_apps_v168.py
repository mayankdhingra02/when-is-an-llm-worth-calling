"""Saved-data analysis reproduction only. Never runs objective/model collectors."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v168'
FILES=['reports/feasibility_v166.md','reports/feasibility_v167.md','artifacts/study_v166/analysis.json','artifacts/study_v167/analysis.json','reports/apps_v168.md','results/v168_native/comparison.json','results/v168_native/paired_gains.png','results/v168_native/paired_gains.svg','artifacts/study_v168/replay.json','reports/cost_v168.md','results/v168_native/cost_diagnostic.json','results/v168_native/representation_diagnostic.json']
def digest(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
def main():
    before={n:digest(n) for n in FILES};env=dict(os.environ,MPLCONFIGDIR='/tmp/mpl-v168')
    for script in ['analyze_apps_v166.py','analyze_apps_v167.py','report_apps_v168.py','verify_apps_v168.py','cost_apps_v168.py','diagnose_apps_v168.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,env=env,check=True,timeout=180,stdout=subprocess.DEVNULL)
    after={n:digest(n) for n in FILES};assert before==after
    (A/'reproduction.json').write_text(json.dumps({'byte_identical':True,'artifacts':after,'new_model_requests':0,'new_native_outcomes':0,'scope':'Internal saved-data replay, not fresh collection/host replication'},indent=2)+'\n')
    print(json.dumps({'byte_identical':True,'artifacts':len(after)}))
if __name__=='__main__':main()
