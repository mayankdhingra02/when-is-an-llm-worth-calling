"""Replay V99 from saved acquired labels, without any new objective access."""
import json,statistics,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from collect_smollm_v47 import read,sha,write
from escalation.core import State
from escalation.transfer_v41 import best,relative_gain
from reasoning_v98_common import audit_case

def main():
    for name in ['reports/protocol_v99.freeze.json']:
        for n,h in read(ROOT/name)['sha256'].items():assert sha(ROOT/n)==h,n
    model=ROOT/'results/v99_reasoning';out=ROOT/'results/v99_analysis'
    s=read(out/'summary.json');cases={r['key']:r for r in s['cases']}
    specs={d['id']:d for d in read(ROOT/'data/manifest_v41.json')['datasets']}
    acquisitions=[json.loads(r) for r in (out/'acquisitions.jsonl').read_text().splitlines()]
    assert len(acquisitions)==360 and len(cases)==36
    responses=[json.loads(r) for r in (model/'responses.jsonl').read_text().splitlines()]
    starts=[json.loads(r) for r in (model/'generation_starts.jsonl').read_text().splitlines()]
    sm={r['identity']:r for r in starts};rm={r['key']:r for r in responses}
    assert len(sm)==s['requests'] and len(rm)==s['responses']
    for job in read(ROOT/'artifacts/study_v99/jobs.json'):
        r=cases[job['key']];p=read(ROOT/job['prefix']);state=State(**p['state'])
        arm=read(out/'arms'/f"{job['key']}.json")
        acqs=[a for a in acquisitions if a['case']==job['key']]
        assert len(acqs)==10 and r['selected_rows']==[a['row_id'] for a in acqs]
        for a in acqs:state.observe(a['row_id'],[float(a['raw_target'])],(specs[job['dataset']]['direction'],))
        assert len(state.ids)==len(set(state.ids))==20 and state.record()==arm['state']
        assert arm['prefix_sha256']==sha(ROOT/job['prefix'])
        value=best(state,specs[job['dataset']]['direction']);assert value==r['target']
        for name,ref in r['references'].items():assert relative_gain(ref,value,specs[job['dataset']]['direction'])==r['gains'][name]
        pfpath=model/'preflight'/f"{job['key']}.json"
        cp=model/'choices'/f"{job['key']}.json"
        choice=read(cp) if cp.exists() else {'status':'unattempted','selected_ids':[]}
        if pfpath.exists():
            parsed=audit_case(job,read(pfpath),sm,rm,choice)
            if parsed and parsed['valid']:
                assert [p['pool']['mapping'][k] for k in parsed['selected_ids']]==r['selected_rows']
        if r['fallback']:
            # Frozen fallback is the independently saved original batch3NN path.
            old=read(ROOT/'results/v41_transfer/arms'/f"{job['base_key']}_batch_3nn.json")
            assert r['selected_rows']==old['state']['ids'][10:]
    for mode,m in s['modes'].items():
        rows=[r for r in cases.values() if r['mode']==mode]
        assert m['valid']==sum(r['status']=='completed' for r in rows)
        for family,means in s['family_means'][mode].items():
            for key,value in means.items():assert value==statistics.mean(r['gains'][key] for r in rows if r['family']==family)
    write(ROOT/'artifacts/study_v99/replay_verification.json',{'verified':True,'intended_conditions':36,'acquired_cells_replayed':360,
        'requests':len(starts),'responses':len(responses),'new_objective_acquisitions':0,'new_model_calls':0})
    print('Verified all 36 conditions and 360 saved acquisitions; zero new labels/calls')
if __name__=='__main__':main()
