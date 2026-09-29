"""Independent Python-stdlib V25 reconstruction from a local extracted bundle.

No study imports, installed packages, inference, network or file writes.
Full-table targets are used only by replay/scoring, not recommendation functions.
"""
import copy,csv,hashlib,json,math,random,sys
from collections import Counter
from pathlib import Path,PurePosixPath
from statistics import mean
ROOT=Path(__file__).resolve().parents[1]
sys.dont_write_bytecode=True

def require(ok,message):
    if not ok:raise ValueError(message)
def read(name):return json.loads((ROOT/name).read_text())
def lines(name):return [json.loads(x) for x in (ROOT/name).read_text().splitlines() if x.strip()]
def sha(name):return hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
def close(a,b):return math.isclose(a,b,rel_tol=1e-12,abs_tol=1e-12)

def observe(state,index,target,direction):
    require(index not in state['ids'],'Duplicate evaluation')
    state['ids'].append(index);state['labels'].append([target])
    values=[y[0] for y in state['labels']];lo,hi=min(values),max(values)
    scores=[0. if hi==lo else ((v-lo)/(hi-lo) if direction=='-' else (hi-v)/(hi-lo)) for v in values]
    if len(values)==4:
        order=sorted(range(4),key=lambda j:(scores[j],j))
        state['best']=[state['ids'][j] for j in order[:2]];state['rest']=[state['ids'][j] for j in order[2:]]
    elif len(values)>4:
        state['best'].append(index)
        if len(state['best'])>int(math.sqrt(len(values))):
            worst=max(state['best'],key=lambda i:(scores[state['ids'].index(i)],state['ids'].index(i)))
            state['best'].remove(worst);state['rest'].append(worst)

def ranked(features,state):
    available=[i for i in state['order'] if i not in state['ids']]
    require(available,'No remaining candidates')
    if len(state['ids'])<4:return available
    def mode(ids):return tuple(min(Counter(features[i][j] for i in ids).items(),key=lambda p:(-p[1],p[0]))[0] for j in range(len(features[0])))
    best,rest=mode(state['best']),mode(state['rest'])
    def dist(a,b):return math.sqrt(sum(x!=y for x,y in zip(a,b))/len(a))
    return sorted(available,key=lambda i:dist(features[i],best)-dist(features[i],rest))

def decode_tokens(tokens,tokenizer):
    require(tokenizer['decoder']['type']=='ByteLevel','Only pinned byte-level decoder supported')
    byte_values=list(range(33,127))+list(range(161,173))+list(range(174,256))
    characters=byte_values[:];offset=0
    for b in range(256):
        if b not in byte_values:byte_values.append(b);characters.append(256+offset);offset+=1
    mapping={chr(c):b for b,c in zip(byte_values,characters)}
    inverse={v:k for k,v in tokenizer['model']['vocab'].items()}
    special={t['id'] for t in tokenizer['added_tokens'] if t['special']}
    return bytes(mapping[ch] for t in tokens if t not in special for ch in inverse[t]).decode('utf-8')

def table(spec):
    require(sha(spec['path'])==spec['sha256'],'Source table hash')
    features=[];targets=[];source_lines=[];seen=set();duplicates=0
    with (ROOT/spec['path']).open(newline='') as f:
        reader=csv.DictReader(f,delimiter=spec['delimiter'])
        require(set(reader.fieldnames)==set(spec['feature_names'])|set(spec['objective_columns'])|set(spec['metadata_columns']),'Schema columns')
        for line,row in enumerate(reader,2):
            if any(row[k]!=str(v) for k,v in spec['filters'].items()):continue
            x=tuple(float(row[k]) for k in spec['feature_names'])
            if x in seen:duplicates+=1;continue
            seen.add(x);features.append(x);targets.append(float(row[spec['primary_objective']]));source_lines.append(line)
    require(len(features)==spec['rows'] and duplicates==spec['duplicates'],'Filtered table dimensions')
    return features,targets,source_lines

def main():
    manifest=read('REPRODUCTION_MANIFEST.json')
    for name,entry in manifest['files'].items():
        path=PurePosixPath(name)
        require(not path.is_absolute() and '..' not in path.parts,'Unsafe path')
        local=ROOT/name
        require(local.is_file() and not local.is_symlink(),'Missing/nonregular file: '+name)
        require(local.stat().st_size==entry['bytes'] and sha(name)==entry['sha256'],'Changed bundle file: '+name)
    for name,h in read('reports/protocol_v25_shortlist.freeze.json')['sha256'].items():require(sha(name)==h,'Frozen input mismatch: '+name)
    spec=read('data/manifest_v8.json');require(len(spec['datasets'])==3 and len(spec['cases'])==15,'Data denominator')
    jobs=read('data/larger_probe_v22.json')['jobs'];requests=lines('results/v22_larger/requests.jsonl');starts=lines('results/v22_larger/request_starts.jsonl')
    require(len(jobs)==len(requests)==len(starts)==60,'Model request denominator')
    require([r['request_id'] for r in requests]==[r['request_id'] for r in starts]==list(range(141,201)),'Model request identity')
    tokenizer=read('models/Qwen2.5-1.5B-Instruct/tokenizer.json');model=read('artifacts/model_manifest_v22.json')
    decoded={}
    for job,r,start in zip(jobs,requests,starts):
        require(job['job_id']==r['job_id']==start['job_id'],'Job identity')
        require(r['messages']==job['messages']==start['messages'],'Exact messages')
        require(r['model_id']==model['model_id'] and r['revision']==model['revision'],'Model provenance identity')
        require(r['status']=='response' and r['retry']==0,'Response status')
        require(decode_tokens(r['generated_token_ids'],tokenizer)==r['raw_output'],'Independent raw output decoding')
        ids=r['raw_output'].splitlines();require(len(ids)==len(set(ids))==10 and set(ids)<=set(job['mapping']),'Ten distinct IDs')
        tokens=r['generated_token_ids'];require(len(tokens)==r['output_tokens']==20,'Output usage')
        used=[];trace=[]
        for pos,(token,domain) in enumerate(zip(tokens,r['grammar_schedule'])):
            allowed=[t for t in domain if t not in used] if pos%2==0 else domain
            require(token in allowed,'Grammar support')
            if pos%2==0:trace.append({'position':pos,'allowed':allowed,'chosen':token});used.append(token)
        require(trace==r['selection_trace'],'Selection trace')
        decoded[job['job_id']]=[job['mapping'][i] for i in ids]
    journal=lines('results/v25_shortlist/acquisitions.jsonl');require(len(journal)==150,'Acquisition denominator')
    progress=read('results/v25_shortlist/progress.json');require(progress['complete'] and len(progress['arms'])==15 and all(r['status']=='completed' for r in progress['arms']),'All arms complete')
    saved=read('results/v25_shortlist/summary.json');records=[];choices=0;scored_llm=0
    for d in spec['datasets']:
        x,y,source_lines=table(d);low,high=min(y),max(y)
        def loss(ids):return 0. if high==low else min((y[i]-low)/(high-low) if d['direction']=='-' else (high-y[i])/(high-low) for i in ids)
        for seed in spec['seeds']:
            key=f"{d['id']}_{seed}";prefix=read(f'results/v6/prefixes/{key}.json')['state']
            order=list(range(len(x)));random.Random(seed).shuffle(order)
            state={'order':order,'ids':[],'labels':[],'best':[],'rest':[]}
            for _ in range(10):
                i=ranked(x,state)[0];observe(state,i,y[i],d['direction'])
            require(state==prefix,'Independent ten-evaluation prefix replay')
            case=next(c for c in spec['cases'] if c['dataset']==d['id'] and c['seed']==seed)
            pool=ranked(x,state)[:20];require(pool==case['pool']['ranked'],'Feature/acquired-label shortlist replay')
            full=copy.deepcopy(prefix)
            for _ in range(10):
                i=ranked(x,full)[0];observe(full,i,y[i],d['direction'])
            require(full==read(f'results/v6/classical/{key}.json')['arms']['centroid_nominal']['state'],'Original classical replay')
            static=copy.deepcopy(prefix)
            for i in pool[:10]:observe(static,i,y[i],d['direction'])
            require(static==read(f'results/v8/static_rank/{key}.json')['state'],'Static rank replay')
            state=copy.deepcopy(prefix);state['order']=[i for i in state['order'] if i in set(pool)|set(prefix['ids'])]
            events=[e for e in journal if e['dataset']==d['id'] and e['seed']==seed];require(len(events)==10,'Per-arm acquisition count')
            for e in events:
                i=ranked(x,state)[0]
                require(i==e['row_id'] and e['source_line']==source_lines[i] and float(e['raw_target'])==y[i],'Adaptive decision/source label replay')
                observe(state,i,y[i],d['direction']);choices+=1
            arm=read(f'results/v25_shortlist/arms/{key}.json');require(state==arm['state'] and arm['actual_new_accesses']==10,'New classical final state')
            llm=[]
            for job in [j for j in jobs if j['dataset']==d['id'] and j['seed']==seed]:
                require(set(job['mapping'].values())==set(pool),'Matched LLM candidate space')
                branch=copy.deepcopy(prefix)
                for i in decoded[job['job_id']]:observe(branch,i,y[i],d['direction'])
                require(branch==read(f"results/v22_larger/arms/{job['job_id']:02d}_llm.json")['state'],'Raw-output LLM arm replay')
                if job['condition']!='assigned_ids_repeat':llm.append(loss(branch['ids']))
                scored_llm+=1
            record={'dataset':d['id'],'system_group':d['system_group'],'seed':seed,'restricted_loss':loss(state['ids']),
                    'full_classical_loss':loss(full['ids']),'static_rank_loss':loss(static['ids']),'llm_mean_loss':mean(llm),
                    'llm_best_presentation_loss':min(llm),'llm_worst_presentation_loss':max(llm)}
            original=next(r for r in saved['cases'] if r['dataset']==d['id'] and r['seed']==seed)
            for field in record:
                require(close(record[field],original[field]) if isinstance(record[field],float) else record[field]==original[field],'Result table value: '+field)
            records.append(record)
    fields=['restricted_loss','full_classical_loss','static_rank_loss','llm_mean_loss']
    family_means=[]
    for g in sorted({r['system_group'] for r in records}):
        group=[r for r in records if r['system_group']==g];require(len(group)==5,'Five seeds per family')
        row={'system_group':g,**{f:mean(r[f] for r in group) for f in fields}}
        old=next(r for r in saved['families'] if r['system_group']==g)
        require(all(close(row[f],old[f]) for f in fields),'Family result')
        family_means.append(row)
    print(json.dumps({'verified':True,'files_checked':len(manifest['files']),'source_tables_reconstructed':3,
       'prefixes_replayed':15,'full_classical_arms_replayed':15,'static_rank_arms_replayed':15,
       'adaptive_shortlist_arms_replayed':15,'new_branch_journal_entries_verified':choices,
       'model_outputs_decoded_and_grammar_checked':60,'llm_arms_replayed':scored_llm,
       'family_means':family_means,'equal_family_means':{f:mean(r[f] for r in family_means) for f in fields},
       'runtime':sys.version,'stdlib_only':True,'isolated_flag':sys.flags.isolated,'site_disabled':sys.flags.no_site,
       'scope':'Independent saved-result reconstruction; no fresh inference, model-weight verification or new objective collection',
       'new_model_calls':0,'new_objective_acquisitions':0},indent=2))

if __name__=='__main__':main()
