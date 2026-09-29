"""Byte-level saved-evidence replay; no generation or outcome acquisition."""
import hashlib,json,os,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def hashes(names):return {n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}
def run(stage,names,commands,receipt):
 before=hashes(names);env=dict(os.environ,MPLCONFIGDIR='/private/tmp/llm-study-v126-mpl')
 for args in commands:subprocess.run([sys.executable,*args],cwd=ROOT,env=env,check=True,stdout=subprocess.DEVNULL)
 after=hashes(names);assert before==after
 (ROOT/receipt).write_text(json.dumps({'byte_identical':True,'sha256':after,'stage':stage,'new_requests':0,'new_objective_acquisitions':0},indent=2)+'\n')
run('V124 corrected interpretation wrapper',['reports/surrogate_v124.md','results/v124_analysis/comparison.json','results/v124_analysis/surrogate.png'],[['scripts/report_surrogate_v124.py']],'artifacts/study_v124/reproduction_corrected.json')
run('V126 saved coverage analysis and scientific figure',['reports/domain_audit_v126.md','results/v126_domain_audit/comparison.json','results/v126_domain_audit/headroom.png'],[['scripts/domain_audit_v126.py','--evaluate'],['scripts/render_domain_v126.py']],'artifacts/study_v126/reproduction.json')
print('Both reports, both comparison JSONs and both figures reproduced byte-identically')
