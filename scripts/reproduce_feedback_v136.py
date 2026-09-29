"""Regenerate descriptive artifacts twice and compare bytes; no collection."""
import subprocess,sys
from collect_smollm_v47 import ROOT,write,sha
def main():
 names=['reports/feedback_v136.md','results/v136_feedback/comparison.json','results/v136_feedback/comparison.png','results/v136_feedback/comparison.svg','results/v136_feedback/followup_trace.json']
 before={n:sha(ROOT/n) for n in names}
 for repeat in range(2):
  p=subprocess.run([sys.executable,str(ROOT/'scripts/analyze_feedback_v136.py')],cwd=ROOT,capture_output=True,text=True,timeout=60)
  assert p.returncode==0,p.stderr
  after={n:sha(ROOT/n) for n in names};assert after==before,(repeat,after,before)
 write(ROOT/'artifacts/study_v136/reproduction.json',{'byte_identical':True,'repeat_runs':2,'sha256':before,'new_requests':0,'new_acquisitions':0})
 print('Five analysis artifacts reproduced byte-identically twice; zero new collection.')
if __name__=='__main__':main()
