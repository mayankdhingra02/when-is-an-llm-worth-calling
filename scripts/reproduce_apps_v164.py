"""Recompute saved evidence only; never call native applications or an LLM."""
import hashlib,json,subprocess,os,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v164'
FILES=['reports/apps_v164.md','results/v164_native/comparison.json','results/v164_native/interface_gains.png','results/v164_native/interface_gains.svg','artifacts/study_v164/replay.json','results/v164_native/mechanism.json','results/v164_native/mechanism.png','results/v164_native/mechanism.svg']
def dig(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
def main():
 before={n:dig(n) for n in FILES}
 for script in ['report_apps_v164.py','verify_apps_v164.py','mechanism_apps_v164.py']:subprocess.run([sys.executable,str(ROOT/'scripts'/script)],check=True,cwd=ROOT,env=dict(os.environ,MPLCONFIGDIR='/tmp/mpl-v164'),stdout=subprocess.DEVNULL,timeout=120)
 after={n:dig(n) for n in FILES};assert before==after
 result={'byte_identical':True,'artifacts':after,'new_requests':0,'new_native_evaluations':0,'scope':'Internal replay, not independent-host replication'};(A/'reproduction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'byte_identical':True,'artifacts':len(after)}))
if __name__=='__main__':main()
