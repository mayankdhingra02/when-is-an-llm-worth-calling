"""Retrospective evaluation and deterministic replay of new classical controls."""
import sys,csv,math,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines
from escalation.data import sha
from escalation.finite_v6 import load_candidates
from escalation.study_v8 import verify,run_config
from escalation.resources import Resources
from escalation.quality_controls_v12 import choose
OUT=Path('results/v12_controls')

def main(resources):
    verify()
    for p,h in read('reports/protocol_v12_controls.freeze.json')['sha256'].items():assert sha(p)==h,p
    progress=read(OUT/'progress.json');assert progress['complete'] and len(progress['intended'])==20
    m=read('data/manifest_v8.json');journal=lines(OUT/'acquisitions.jsonl');assert len(journal)==300
    records=[]
    for d in m['datasets']:
        if d['id'] not in ['brotli','lrzip']:continue
        c=load_candidates(d)
        with Path(d['path']).open(newline='') as f:raw={line:[float(r['performance']),float(r['size'])] for line,r in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2)}
        values={i:raw[line] for i,line in enumerate(c.source_ids)}
        for seed in m['seeds']:
            resources.check();key=d['id']+'_'+str(seed);p=read(OUT/'prefixes'/(key+'.json'));old=read('results/v6/prefixes/'+key+'.json')['state']
            assert p['ids']==old['ids'] and p['labels']==[values[i] for i in p['ids']]
            assert p['order']==old['order'];anchor=min(p['ids'],key=lambda i:values[i][0]);assert p['size_cap']==values[anchor][1]
            results={}
            for arm in ['joint_3nn','random']:
                r=read(OUT/arm/(key+'.json'));ids=list(p['ids']);labels=[list(x) for x in p['labels']]
                assert r['ids'][:10]==ids and r['labels'][:10]==labels and r['logical_evaluations']==20 and r['actual_new_vector_accesses']==10
                for event in r['events']:
                    i,prediction=choose(c,p['order'],ids,labels,p['size_cap'],arm)
                    assert i==event['row_id'] and all(event[k]==v for k,v in prediction.items())
                    ids.append(i);labels.append(values[i])
                assert len(ids)==len(set(ids))==20 and ids==r['ids'] and labels==r['labels']
                feasible=[i for i in ids if values[i][1]<=p['size_cap']];best=min(feasible,key=lambda i:values[i][0])
                assert best==r['best_row'] and r['best_runtime']==values[best][0] and r['best_size']==values[best][1]
                assert r['infeasible_new_acquisitions']==sum(values[i][1]>p['size_cap'] for i in ids[10:])
                events=[e for e in journal if e['dataset']==d['id'] and e['seed']==seed and e['arm']==arm]
                assert [e['row_id'] for e in events]==ids[10:]
                results[arm]=r
            initial=[e for e in journal if e['dataset']==d['id'] and e['seed']==seed and e['arm']=='shared_prefix']
            assert [e['row_id'] for e in initial]==p['ids']
            for e in [e for e in journal if e['dataset']==d['id'] and e['seed']==seed]:
                assert e['source_line']==c.source_ids[e['row_id']] and e['vector_charge']==1
                assert [float(e['raw_runtime']),float(e['raw_size'])]==values[e['row_id']]
            a=results['joint_3nn'];b=results['random'];ideal=min(v[0] for v in values.values() if v[1]<=p['size_cap'])
            records.append({'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'size_cap':p['size_cap'],
                'joint_3nn_runtime':a['best_runtime'],'random_runtime':b['best_runtime'],'ideal_runtime_diagnostic':ideal,
                'joint_3nn_gain_over_random':(b['best_runtime']-a['best_runtime'])/b['best_runtime'],
                'remaining_headroom_over_joint_3nn':(a['best_runtime']-ideal)/a['best_runtime'],
                'joint_3nn_infeasible_acquisitions':a['infeasible_new_acquisitions'],'random_infeasible_acquisitions':b['infeasible_new_acquisitions']})
    summaries=[]
    for g in ['brotli','lrzip','all_two_groups']:
        rs=[r for r in records if g=='all_two_groups' or r['system_group']==g]
        summaries.append({'group':g,'cases':len(rs),'mean_relative_gain_over_random':sum(r['joint_3nn_gain_over_random'] for r in rs)/len(rs),
            'mean_relative_remaining_headroom':sum(r['remaining_headroom_over_joint_3nn'] for r in rs)/len(rs),
            'wins':sum(r['joint_3nn_gain_over_random']>0 for r in rs),'losses':sum(r['joint_3nn_gain_over_random']<0 for r in rs),
            'gain_above_10pct':sum(r['joint_3nn_gain_over_random']>.1 for r in rs),'headroom_above_10pct':sum(r['remaining_headroom_over_joint_3nn']>.1 for r in rs)})
    summary={'namespace':'measured_joint_classical_v12','complete':True,'records':records,'summaries':summaries,'new_vector_accesses':len(journal),
        'prefix_vectors':100,'continuation_vectors':200,'new_model_requests':0,'scope':'exploratory two-family classical feasibility; not LLM evidence',
        'infeasible_new_acquisitions':{arm:sum(r[arm+'_infeasible_acquisitions'] for r in records) for arm in ['joint_3nn','random']}}
    write(OUT/'summary.json',summary)
    with (OUT/'outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(records[0]));w.writeheader();w.writerows(records)
    write('artifacts/study_v12/verification.json',{'verified':True,'prefixes':10,'branches':20,'joint_vector_acquisitions':300,'inclusive_arm_budget':20,
        'checkpoint':10,'deterministic_acquired_only_replay':True,'source_values_and_labels_checked':True,'old_freezes_intact':True,'new_model_calls':0})
    resources.check();print(json.dumps({'summaries':summaries,'infeasible':summary['infeasible_new_acquisitions'],'new_vector_accesses':300,'new_model_calls':0},indent=2))

if __name__=='__main__':
    with Resources(run_config(),'artifacts/resource_ledger_v2.json') as r:main(r)
