"""Independently rebuild saved development fits and verify no test-family fitting."""
from table_check_v121 import ROOT,read,write,sha
from fit_router_v121 import train
from escalation.io import digest

def main():
    rows=read(ROOT/'results/v121_router/development_outcomes.json');assert len(rows)==35 and len({r['system_group'] for r in rows})==7 and all(r['system_group']!='mongodb' for r in rows)
    for target,name in [('gain_primary','router_seal'),('gain_first10','router_first10_seal')]:
        got=train(rows,target);saved=read(ROOT/f'results/v121_router/{name}.json');got.pop('at');saved.pop('at');assert got==saved and saved['development_rows_sha256']==digest(rows)
        assert all(f['held_development_family'] not in f['training_families'] for f in saved['oof']['folds'])
    for n,h in read(ROOT/'artifacts/study_v121/router_inputs.freeze.json')['sha256'].items():assert sha(ROOT/n)==h
    freeze=read(ROOT/'reports/protocol_v121.freeze.json')['at'];fitted=read(ROOT/'artifacts/study_v121/router_inputs.freeze.json')['at'];classical=read(ROOT/'results/v121_classical/started.json')['at'];policy=read(ROOT/'results/v121_classical/policy_precommit.json')['at'];events=[__import__('json').loads(x) for x in (ROOT/'results/v121_classical/acquisitions.jsonl').read_text().splitlines()]
    assert freeze<fitted<classical<policy and all(e['at']>policy for e in events if e['arm']!='prefix')
    result={'verified':True,'development_cases':35,'development_groups':7,'test_groups_in_fitting':0,'saved_fits_exactly_reproduced':2,'chronology_verified':True,'new_model_requests':0,'new_acquisitions':0}
    write(ROOT/'artifacts/study_v121/router_verification.json',result);print(result)
if __name__=='__main__':main()
