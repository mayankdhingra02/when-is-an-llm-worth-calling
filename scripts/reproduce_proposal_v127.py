"""Byte-level analysis replay; no model calls or outcome acquisition."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
names=['reports/proposals_v127.md','results/v127_analysis/comparison.json','results/v127_analysis/proposals.png','reports/capacity_correction_v127.md','results/v127_analysis/repair_bound.json']
def hashes():return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
before=hashes();env=dict(os.environ,MPLCONFIGDIR='/private/tmp/llm-study-v127-mpl')
for script in ['report_proposal_v127.py','render_proposal_v127.py','audit_repair_bound_v127.py']:subprocess.run([sys.executable,str(ROOT/'scripts'/script)],cwd=ROOT,env=env,check=True,stdout=subprocess.DEVNULL)
assert before==hashes();(ROOT/'artifacts/study_v127/reproduction.json').write_text(json.dumps({'byte_identical':True,'sha256':before,'new_requests':0,'new_objective_acquisitions':0},indent=2)+'\n');print('Corrected report,comparison,figure and repair bound reproduce byte-identically')
