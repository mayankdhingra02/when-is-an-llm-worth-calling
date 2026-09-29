"""Independent stdlib V34 replay. No study imports, network, inference or writes.
Prefix and token helpers retained from the independently implemented V26 verifier.
Full-source labels stay in replay/scoring; decision helpers receive acquired labels.
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

def digest(value):return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def choose_joint(xs,order,ids,labels,cap):
    available=[i for i in order if i not in ids];pred=[]
    for pos,i in enumerate(available):
        near=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(xs[i],xs[ids[j]])),j))[:3]
        rt=sum(labels[j][0] for j in near)/3;size=sum(labels[j][1] for j in near)/3
        pred.append((i,pos,rt,size))
    feasible=[p for p in pred if p[3]<=cap]
    return min(feasible,key=lambda p:(p[2],p[1]))[0] if feasible else min(pred,key=lambda p:(p[3],p[2],p[1]))[0]

def choose_runtime(xs,order,ids,labels,pool):
    from decimal import Decimal,localcontext
    with localcontext() as ctx:
        ctx.prec=40;available=[i for i in order if i in pool and i not in ids]
        def score(i):
            near=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(xs[i],xs[ids[j]])),j))[:3]
            return sum((Decimal(str(labels[j][0])) for j in near),Decimal(0))/3
        return min(available,key=score)

def selected_metrics(ids,labels,cap):
    require(len(ids)==len(labels)==len(set(ids))==20,'Twenty unique acquisitions')
    feasible=[j for j,y in enumerate(labels) if y[1]<=cap];require(feasible,'Feasible incumbent')
    best=min(feasible,key=lambda j:labels[j][0]);raw=min(range(20),key=lambda j:labels[j][0])
    return {'best_row':ids[best],'best_runtime':labels[best][0],'best_size':labels[best][1],
        'runtime_only_best_row':ids[raw],'runtime_only_best_runtime':labels[raw][0],'runtime_only_best_size':labels[raw][1],
        'runtime_only_best_violates_cap':labels[raw][1]>cap,'infeasible_new_acquisitions':sum(y[1]>cap for y in labels[10:])}

def main():
    from decimal import Decimal
    manifest=read('REPRODUCTION_MANIFEST.json')
    for name,entry in manifest['files'].items():
        path=PurePosixPath(name);require(not path.is_absolute() and '..' not in path.parts,'Unsafe path')
        local=ROOT/name;require(local.is_file() and not local.is_symlink(),'Missing/nonregular file: '+name)
        require(local.stat().st_size==entry['bytes'] and sha(name)==entry['sha256'],'Changed bundle file: '+name)
    freeze_count=0
    for name in manifest['files']:
        if name.endswith('.freeze.json'):
            for n,h in read(name)['sha256'].items():require(sha(n)==h,'Frozen dependency: '+n);freeze_count+=1
    m=read('data/constrained_v34.json')
    for n,h in m['source_sha256'].items():require(sha(n)==h,'Source binding: '+n)
    require(len(m['cases'])==10 and len(m['datasets'])==2,'Ten cases/two families')
    jobs=read('data/larger_probe_v22.json')['jobs'];requests=lines('results/v22_larger/requests.jsonl');starts=lines('results/v22_larger/request_starts.jsonl')
    require(len(jobs)==len(requests)==len(starts)==60,'Original request denominator')
    require([r['request_id'] for r in requests]==[r['request_id'] for r in starts]==list(range(141,201)),'Request sequence')
    model=read('artifacts/model_manifest_v22.json');tokenizer=read('models/Qwen2.5-1.5B-Instruct/tokenizer.json');decoded={}
    for j,r,start in zip(jobs,requests,starts):
        require(j['job_id']==r['job_id']==start['job_id'] and j['messages']==r['messages']==start['messages'],'Prepared request identity')
        require(r['model_id']==model['model_id'] and r['revision']==model['revision'] and r['provider']=='local_transformers','Model provenance')
        require(r['status']=='response' and r['retry']==0,'Response status')
        require(decode_tokens(r['generated_token_ids'],tokenizer)==r['raw_output'],'Independent output decoding')
        require(len(r['generated_token_ids'])==r['output_tokens']==20,'Output token usage')
        ids=r['raw_output'].splitlines();require(len(ids)==len(set(ids))==10 and set(ids)<=set(j['mapping']),'Distinct response IDs')
        used=[];trace=[];require(len(r['grammar_schedule'])==20,'Grammar schedule')
        for pos,(token,domain) in enumerate(zip(r['generated_token_ids'],r['grammar_schedule'])):
            allowed=[t for t in domain if t not in used] if pos%2==0 else domain
            require(token in allowed,'Grammar support')
            if pos%2==0:trace.append({'position':pos,'allowed':allowed,'chosen':token});used.append(token)
        require(trace==r['selection_trace'],'Grammar trace')
        context={k:v for k,v in j.items() if k!='messages'};context.update(namespace='measured_v22',prompt_version='larger_v22',grammar_mode='candidate_order_v19',retry=0)
        require(r['cache_key']==digest({'messages':j['messages'],'model':r['model_id'],'revision':r['revision'],'parameters':r['parameters'],
            'context':context,'parser_projection':'larger_v22','grammar_domains':None,'grammar_mode':'candidate_order_v19'}),'Cache binding')
        decoded[j['job_id']]=[j['mapping'][i] for i in ids]
    modes=('joint_shortlist','joint_full','static_rank','runtime_3nn','cached_llm_assigned_ids','cached_llm_reverse_display','cached_llm_reassigned_ids')
    out='results/v34_constrained';expected=[];records=[];pairs=[];adaptive=0
    for d in m['datasets']:
        xs,ys,source_lines=table(d);joint=[];raw=[]
        with (ROOT/d['path']).open(newline='') as f:
            for line,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
                if line in source_lines:joint.append([float(row['performance']),float(row['size'])]);raw.append([row['performance'],row['size']])
        for case in [c for c in m['cases'] if c['dataset']==d['id']]:
            seed=case['seed'];key=f"{d['id']}_{seed}";order=list(range(len(xs)));random.Random(seed).shuffle(order)
            original={'order':order,'ids':[],'labels':[],'best':[],'rest':[]}
            for _ in range(10):
                i=ranked(xs,original)[0];observe(original,i,ys[i],d['direction'])
            require(original==read(case['prefix_path'])['state'] and digest(original)==case['original_prefix_hash'],'Independent prefix reconstruction')
            pool=ranked(xs,original)[:20];require(pool==case['pool'],'Independent shortlist reconstruction')
            saved=read(f'{out}/prefixes/{key}.json');prefix=saved['prefix']
            anchor=min(original['ids'],key=lambda i:ys[i]);cap=joint[anchor][1]
            require(prefix=={'ids':original['ids'],'labels':[joint[i] for i in original['ids']],'order':order,'anchor_row':anchor,'size_cap':cap},'Acquired-prefix size cap and vectors')
            require(saved['prefix_hash']==digest(prefix),'Joint prefix hash')
            for i in prefix['ids']:expected.append((d['id'],seed,'prefix',i,source_lines[i],*raw[i]))
            arms={}
            for mode in modes:
                arm=read(f'{out}/arms/{key}_{mode}.json');ids=prefix['ids'][:];labels=copy.deepcopy(prefix['labels'])
                require(arm['status']=='completed' and arm['prefix_hash']==digest(prefix) and arm['size_cap']==cap,'Completed shared-prefix branch')
                require(arm['logical_evaluations']==20 and arm['actual_new_accesses']==10,'Inclusive evaluation budget')
                joint_order=order if mode=='joint_full' else [i for i in order if i in set(pool)|set(ids)]
                if mode.startswith('cached_llm_'):
                    condition=mode[len('cached_llm_'):];job=next(j for j in jobs if (j['dataset'],j['seed'],j['condition'])==(d['id'],seed,condition))
                    req=next(r for r in requests if r['job_id']==job['job_id']);fixed=decoded[job['job_id']]
                    require(job['prefix_hash']==case['original_prefix_hash'] and set(job['mapping'].values())==set(pool),'LLM matched prefix/pool')
                    require(fixed==case['selected'][mode]==read(f"results/v22_larger/arms/{job['job_id']:02d}_llm.json")['selected_rows'],'Decoded action selection')
                    require(arm['cached_request']==case['provenance'][mode] and all(req[k]==v for k,v in arm['cached_request'].items()),'Cached request identity')
                else:require(arm['cached_request'] is None,'No model provenance on classical arm')
                require(len(arm['events'])==10,'Ten continuation decisions')
                for step,event in enumerate(arm['events']):
                    if mode.startswith('joint_'):i=choose_joint(xs,joint_order,ids,labels,cap);adaptive+=1
                    elif mode=='runtime_3nn':i=choose_runtime(xs,order,ids,labels,pool);adaptive+=1
                    elif mode=='static_rank':i=pool[step]
                    else:i=fixed[step]
                    require(event['row_id']==i and i not in ids,'Independent acquired-only decision')
                    ids.append(i);labels.append(joint[i]);expected.append((d['id'],seed,mode,i,source_lines[i],*raw[i]))
                require(arm['ids']==ids and arm['labels']==labels,'Source-bound acquired states')
                if mode in ('static_rank','runtime_3nn'):require(ids[10:]==case['selected'][mode],'Classical selected actions')
                metrics=selected_metrics(ids,labels,cap);require(all(arm[k]==v for k,v in metrics.items()),'Feasible terminal metrics')
                record={'dataset':d['id'],'seed':seed,'arm':mode,'size_cap':cap,**metrics};records.append(record);arms[mode]=record
            for mode in modes[4:]:
                for base in modes[:4]:
                    b=arms[base];l=arms[mode];db=Decimal(raw[b['best_row']][0]);dl=Decimal(raw[l['best_row']][0]);rb=Decimal(raw[b['runtime_only_best_row']][0]);rl=Decimal(raw[l['runtime_only_best_row']][0])
                    pairs.append({'dataset':d['id'],'seed':seed,'condition':mode[len('cached_llm_'):],'baseline':base,
                        'classical_feasible_runtime':b['best_runtime'],'llm_feasible_runtime':l['best_runtime'],
                        'constrained_relative_gain':(b['best_runtime']-l['best_runtime'])/b['best_runtime'],
                        'unconstrained_relative_gain':(b['runtime_only_best_runtime']-l['runtime_only_best_runtime'])/b['runtime_only_best_runtime'],
                        'decimal_constrained_gain':str((db-dl)/db),'decimal_unconstrained_gain':str((rb-rl)/rb)})
    journal=lines(out+'/acquisitions.jsonl');require(len(journal)==800 and all(r['vector_charge']==1 for r in journal),'Charged acquisition denominator')
    # Collection case order is manifest order, which equals dataset/seed order here.
    require([(r['dataset'],r['seed'],r['arm'],r['row_id'],r['source_line'],r['raw_runtime'],r['raw_size']) for r in journal]==expected,'Ordered source journal')
    progress=read(out+'/progress.json');require(progress['complete'] and len(progress['arms'])==70 and all(r['status']=='completed' for r in progress['arms']),'Completed intended denominator')
    saved=read(out+'/summary.json');require(records==saved['records'] and pairs==saved['pairs'],'Independent case/score summary')
    summaries=[]
    for mode in modes[4:]:
        condition=mode[len('cached_llm_'):]
        for base in modes[:4]:
            rows=[r for r in pairs if r['condition']==condition and r['baseline']==base];groups=[]
            for dataset in ('brotli','lrzip'):
                group=[r for r in rows if r['dataset']==dataset]
                groups.append({'dataset':dataset,'cases':len(group),'mean_constrained_gain':mean(r['constrained_relative_gain'] for r in group),'mean_unconstrained_gain':mean(r['unconstrained_relative_gain'] for r in group)})
            summaries.append({'condition':condition,'baseline':base,'cases':len(rows),'groups':groups,
                'equal_family_constrained_gain':mean(g['mean_constrained_gain'] for g in groups),'equal_family_unconstrained_gain':mean(g['mean_unconstrained_gain'] for g in groups),
                'wins':sum(r['constrained_relative_gain']>0 for r in rows),'ties':sum(r['constrained_relative_gain']==0 for r in rows),'harms':sum(r['constrained_relative_gain']<0 for r in rows)})
    require(summaries==saved['summaries'],'Independent aggregate summary')
    reliability=[{'arm':mode,'cases':10,'runtime_only_best_violations':sum(r['runtime_only_best_violates_cap'] for r in records if r['arm']==mode),
        'infeasible_continuation_vectors':sum(r['infeasible_new_acquisitions'] for r in records if r['arm']==mode)} for mode in modes]
    require(reliability==saved['reliability'],'Independent reliability summary')
    print(json.dumps({'verified':True,'files_checked':len(manifest['files']),'frozen_references_checked':freeze_count,
        'source_tables_reconstructed':2,'prefixes_replayed':10,'shortlists_replayed':10,'adaptive_decisions_replayed':adaptive,
        'model_outputs_decoded_and_grammar_checked':60,'llm_selections_replayed':30,'arms_replayed':70,'charged_vectors_verified':800,
        'paired_scores_verified':120,'decimal_scores_verified':240,'summaries':summaries,'reliability':reliability,
        'runtime':sys.version,'stdlib_only':True,'isolated_flag':sys.flags.isolated,'site_disabled':sys.flags.no_site,
        'scope':'Independent saved-result reconstruction, no new inference, physical execution or fresh-machine test'},indent=2))

if __name__=='__main__':main()
