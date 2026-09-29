from pathlib import Path
import sys,subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from escalation.io import lines,read,write,now
from escalation.data import validate_manifest
root=Path(__file__).resolve().parents[1]
completed=subprocess.run([sys.executable,'-m','pytest','-q'],cwd=root,capture_output=True,text=True)
(root/'artifacts/tests_pre_llm.txt').write_text(completed.stdout+completed.stderr)
assert completed.returncode==0
r=lines(root/'results/classical/runs.jsonl');validate_manifest(read(root/'data/manifest.json'))
assert len(r)==30 and all(x['status']=='completed' and x['logical_evaluations']==20 and len(set(x['ids']))==20 for x in r)
write(root/'artifacts/classical_gate.json',{'passed':True,'at':now(),'runs':30,'unique_system_groups':3,'test_log':'artifacts/tests_pre_llm.txt'})
print('Classical gate passed')
