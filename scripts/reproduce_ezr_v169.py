"""Rebuild analysis/figures and compare bytes without any new native/model label."""
import hashlib,os,subprocess,sys
from collect_smollm_v47 import ROOT,write
FILES=['reports/ezr_v169.md','results/v169_ezr/comparison.json','results/v169_ezr/baseline_gains.png','results/v169_ezr/baseline_gains.svg','artifacts/study_v169/replay.json']
def digest(n):return hashlib.sha256((ROOT/n).read_bytes()).hexdigest()
def main():
    before={n:digest(n) for n in FILES}
    for s in ['report_ezr_v169.py','verify_ezr_v169.py']:
        subprocess.run([sys.executable,str(ROOT/'scripts'/s)],cwd=ROOT,env=dict(os.environ,MPLCONFIGDIR='/tmp/mpl-v169'),check=True,timeout=120,stdout=subprocess.DEVNULL)
    after={n:digest(n) for n in FILES};assert before==after
    write(ROOT/'artifacts/study_v169/reproduction.json',{'byte_identical':True,'files':after,'new_native_outcomes':0,'new_model_requests':0,'source_replay_only':True});print('5artifactsbyteidentical')
if __name__=='__main__':main()
