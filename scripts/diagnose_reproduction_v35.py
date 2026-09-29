"""Locate version-sensitive float summation without altering any study evidence."""
import importlib.util,json,sys,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('independent',ROOT/'scripts/verify_reproduction_v35.py');v=importlib.util.module_from_spec(s);s.loader.exec_module(v)
def linear(values):
    total=0.
    for value in values:total+=value
    return total
findings=[]
m=v.read('data/constrained_v34.json')
for d in m['datasets']:
    xs,ys,source=v.table(d);joint=[]
    with (ROOT/d['path']).open(newline='') as f:
        for line,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
            if line in source:joint.append([float(row['performance']),float(row['size'])])
    for case in [c for c in m['cases'] if c['dataset']==d['id']]:
        key=f"{d['id']}_{case['seed']}";prefix=v.read(f'results/v34_constrained/prefixes/{key}.json')['prefix']
        for mode in ('joint_shortlist','joint_full'):
            arm=v.read(f'results/v34_constrained/arms/{key}_{mode}.json');ids=prefix['ids'][:];labels=[joint[i] for i in ids]
            order=prefix['order'] if mode=='joint_full' else [i for i in prefix['order'] if i in set(case['pool'])|set(ids)]
            for step,event in enumerate(arm['events']):
                picked=v.choose_joint(xs,order,ids,labels,prefix['size_cap']);actual=event['row_id']
                if picked!=actual:
                    scores=[]
                    for i in (actual,picked):
                        near=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(xs[i],xs[ids[j]])),j))[:3]
                        rt=[labels[j][0] for j in near];sz=[labels[j][1] for j in near]
                        scores.append({'candidate':i,'neighbor_ids':[ids[j] for j in near],'runtime_values':rt,'size_values':sz,
                            'builtin_mean_runtime':sum(rt)/3,'left_fold_mean_runtime':linear(rt)/3,
                            'builtin_mean_size':sum(sz)/3,'left_fold_mean_size':linear(sz)/3})
                    findings.append({'case':key,'arm':mode,'step':step,'saved_choice':actual,'verifier_choice':picked,'size_cap':prefix['size_cap'],'predictions':scores})
                ids.append(actual);labels.append(joint[actual])
print(json.dumps({'runtime':sys.version,'mismatches_against_saved_trajectory':len(findings),'findings':findings},indent=2))
