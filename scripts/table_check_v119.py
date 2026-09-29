"""Frozen recorded-label extension helpers. No stronger native-data admission."""
import sys
from pathlib import Path
from collect_smollm_v47 import ROOT,read,write,append,sha,now
sys.path.insert(0,str(ROOT/'src'))
MODES=('batch_3nn','full_sequential_3nn','random_full','single_portfolio')
SEEDS=(11,23,37,53,71)

def frozen():
    for n,h in read(ROOT/'reports/protocol_v119.freeze.json')['sha256'].items():
        assert sha(ROOT/n)==h,n

def candidates(root=ROOT):
    from escalation.finite_v6 import load_candidates
    from escalation.transfer_v41 import restrict
    s=read(root/'data/manifest_v119.json')['datasets'][0]
    local={**s,'path':str(root/s['path'])}
    c,subset=restrict(load_candidates(local),s['fixed_features'])
    assert len(c.x)==1024 and subset['eligible_before_subsample']==1080
    return local,c,subset
