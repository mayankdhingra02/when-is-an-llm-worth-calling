"""Read-only replay, without regenerating sealed figures."""
import json
from analyze_kanzi_v77 import verify,ROOT
if __name__=='__main__':
    result=verify();assert result==json.loads((ROOT/'results/v77_kanzi_analysis/summary.json').read_text())
    print(json.dumps({'verified':True,'physical_trials':result['physical_evaluations'],'logical_charges':result['logical_arm_charges'],'families':result['families']}))
