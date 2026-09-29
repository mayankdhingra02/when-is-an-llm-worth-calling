"""Independent standard-library audit of acquired targets and request denominators.

No project optimizer imports, no unacquired objective parsing. Supports the
existing classical journal and, once available, the real V41 model journal.
"""
import argparse,csv,hashlib,json,math
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load(path):return json.loads((ROOT/path).read_text())
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def verify(kind):
    path=f'results/v41_{"transfer" if kind=="classical" else "models"}/acquisitions.jsonl'
    if not (ROOT/path).exists():raise ValueError('No measured acquisition journal exists: '+path)
    specs={r['id']:r for r in load('data/manifest_v41.json')['datasets']}
    events=[json.loads(line) for line in (ROOT/path).read_text().splitlines()]
    wanted={name:set() for name in specs}
    for event in events:
        name=event['dataset'];spec=specs[name];row=event['row_id']
        if event['system_group']!=spec['system_group'] or type(row) is not int or not 0<=row<len(spec['subset']['source_lines']):raise ValueError('Unknown source identity')
        if event['source_line']!=spec['subset']['source_lines'][row]:raise ValueError('Subset/source row mismatch')
        if event['seed'] not in load('data/manifest_v41.json')['seeds']:raise ValueError('Unregistered seed')
        wanted[name].add(event['source_line'])
    actual={}
    for name,spec in specs.items():
        if sha(spec['path'])!=spec['sha256']:raise ValueError('Changed pinned source')
        with (ROOT/spec['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=spec['delimiter']),2):
                if line not in wanted[name]:continue
                if any(row[k]!=str(v) for k,v in spec['filters'].items()):raise ValueError('Revision/workload mismatch')
                if any(float(row[k])!=value for k,value in spec['fixed_features'].items()):raise ValueError('Fixed workload mismatch')
                actual[(name,line)]=row[spec['primary_objective']]
    counts=Counter();seen=set()
    for event in events:
        key=(event['dataset'],event['seed'],event['arm'] if kind=='classical' else event['model_size'])
        if (key,event['row_id']) in seen:raise ValueError('Duplicate charged acquisition inside arm')
        seen.add((key,event['row_id']));counts[key]+=1
        raw=actual[(event['dataset'],event['source_line'])]
        if raw!=event['raw_target'] or not math.isfinite(float(raw)) or float(raw)<=0:raise ValueError('Recorded target differs from source')
        expected_namespace='measured_v41' if kind=='classical' else 'measured_v41_llm'
        if event['namespace']!=expected_namespace:raise ValueError('Synthetic/unknown namespace in measured journal')
    branches=('prefix','full_classical','static_rank','batch_3nn','sequential_3nn','full_sequential_3nn','random_shortlist','random_full') if kind=='classical' else ('0.5','1.5')
    intended={(name,seed,branch) for name in specs for seed in load('data/manifest_v41.json')['seeds'] for branch in branches}
    if set(counts)!=intended or any(n!=10 for n in counts.values()):raise ValueError('Incomplete intended acquisition denominator')
    return {'kind':kind,'verified_events':len(events),'groups':len(specs),'verified_ten_access_blocks':len(counts),
        'unique_source_rows_checked':len(actual),'no_unacquired_targets_parsed':True,
        'journal_sha256':sha(path),'scope':'Independent acquired-source consistency and denominators; not optimizer or model inference reproduction'}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--kind',choices=('classical','model'),default='classical')
    args=parser.parse_args();print(json.dumps(verify(args.kind),indent=2))
