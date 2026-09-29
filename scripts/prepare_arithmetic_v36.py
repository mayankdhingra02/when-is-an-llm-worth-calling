"""Create exact prefix inputs from previously charged prefix events, no new labels."""
import sys,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from escalation.io import read,write,lines,digest

def main():
    if Path('data/arithmetic_v36.json').exists():raise FileExistsError('Preserve inputs')
    old=read('data/constrained_v34.json');journal=lines('results/v34_constrained/acquisitions.jsonl');cases=[]
    for case in old['cases']:
        key=f"{case['dataset']}_{case['seed']}";saved=read(f'results/v34_constrained/prefixes/{key}.json')
        events=[e for e in journal if e['dataset']==case['dataset'] and e['seed']==case['seed'] and e['arm']=='prefix']
        p=saved['prefix'];assert [e['row_id'] for e in events]==p['ids'] and all(e['vector_charge']==1 for e in events)
        labels=[[e['raw_runtime'],e['raw_size']] for e in events];assert [[float(v) for v in pair] for pair in labels]==p['labels']
        prefix={**p,'labels':labels,'size_cap':labels[p['ids'].index(p['anchor_row'])][1]}
        cases.append({'dataset':case['dataset'],'seed':case['seed'],'pool':case['pool'],'prefix':prefix,'prefix_hash':digest(prefix),'v34_prefix_hash':saved['prefix_hash']})
    write('data/arithmetic_v36.json',{'scope':'exposed-group exact-arithmetic robustness ablation','datasets':old['datasets'],'cases':cases,
        'new_vector_cap':200,'stage_seconds_cap':120,'input_v34_journal_sha256':hashlib.sha256(Path('results/v34_constrained/acquisitions.jsonl').read_bytes()).hexdigest()})
    print('Prepared ten previously acquired exact prefixes; no new labels.')
if __name__=='__main__':main()
