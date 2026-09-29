"""Write admission/resource report and return 2 if blocked. Never collect labels."""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.study_plan import preflight
from escalation.config import load_config
config=json.loads((ROOT/'configs/study_v4.json').read_text())
registry=json.loads((ROOT/config['registry']).read_text())
ledger=json.loads((ROOT/config['existing_resource_ledger']).read_text())
result=preflight(config,registry,ledger,load_config(ROOT/config['existing_resource_config']))
(ROOT/'artifacts/registry_v4/preflight.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(0 if result['ready'] else 2)
