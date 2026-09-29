"""Rebuild report/figures from saved observations only."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];A=ROOT/'artifacts/study_v165'
FILES=['reports/headroom_v165.md','results/v165_headroom/comparison.json','results/v165_headroom/prefix_headroom.png','results/v165_headroom/prefix_headroom.svg','results/v165_headroom/selection_validation.png','results/v165_headroom/selection_validation.svg','artifacts/study_v165/replay.json','results/v165_headroom/posthoc_validation_minimum.json']
def dig(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
def main():
 before={n:dig(n) for n in FILES}
 for script in ['report_headroom_v165.py','posthoc_headroom_v165.py','verify_headroom_v165.py']:subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,env=dict(os.environ,MPLCONFIGDIR='/tmp/mpl-v165'),check=True,stdout=subprocess.DEVNULL,timeout=120)
 after={n:dig(n) for n in FILES};assert before==after;(A/'reproduction.json').write_text(json.dumps({'byte_identical':True,'artifacts':after,'new_outcomes':0,'new_model_requests':0},indent=2)+'\n');print(json.dumps({'byte_identical':True,'artifacts':len(after)}))
if __name__=='__main__':main()
