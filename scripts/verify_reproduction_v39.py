"""Portable V38 evidence reconstruction. Standard library; no optimizer/model imports."""
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import math
import platform
import sys
from fractions import Fraction as F
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
BASES = ('runtime_only_llm', 'exact_joint_shortlist', 'exact_joint_full', 'runtime_3nn', 'static_rank')
CONDITIONS = ('assigned_ids', 'reverse_display', 'reassigned_ids')

def need(ok, message):
    if not ok:
        raise ValueError(message)

def read(name):
    return json.loads((ROOT / name).read_text())

def lines(name):
    return [json.loads(x) for x in (ROOT / name).read_text().splitlines() if x.strip()]

def sha(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def near(a, b):
    return math.isclose(float(a), float(b), rel_tol=1e-12, abs_tol=1e-12)

def main():
    index = read('REPRODUCTION_MANIFEST.json')
    for name, entry in index['files'].items():
        path = PurePosixPath(name)
        need(not path.is_absolute() and '..' not in path.parts and not (ROOT/name).is_symlink(), 'Unsafe bundle path')
        need((ROOT/name).is_file() and (ROOT/name).stat().st_size == entry['bytes'] and sha(name) == entry['sha256'], 'Bundle checksum: '+name)
        if name.endswith('.freeze.json'):
            for p, h in read(name)['sha256'].items():
                need(sha(p) == h, 'Frozen source: '+p)
    spec = importlib.util.spec_from_file_location('historical_replay', ROOT/'scripts/verify_reproduction_v35_1.py')
    history = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(history)
    out = 'results/v38_size_prompt'
    manifest = read('data/arithmetic_v36.json')
    jobs = read('data/size_prompt_v38.json')['jobs']
    requests, starts = lines(out+'/requests.jsonl'), lines(out+'/request_starts.jsonl')
    summary, progress = read(out+'/summary.json'), read(out+'/progress.json')
    need(len(jobs) == len(requests) == len(starts) == 30, 'Request denominator')
    need(progress['complete'] and progress['actual_attempts'] == 30 and progress['actual_new_vectors'] == 300 and
         progress['arms'] == [{'job_id': i, 'status': 'completed'} for i in range(30)], 'Completed denominator')
    need([r['request_id'] for r in requests] == [r['request_id'] for r in starts] == list(range(201,231)), 'Request sequence')
    began = read(out+'/started.json'); approval = read('configs/authorization_v38.json')
    need(began['approval'] == approval and approval['granted'] and approval['request_cap'] == 230 and
         approval['protocol_freeze_sha256'] == sha('reports/protocol_v38_size_prompt.freeze.json') and
         approval['recorded_at'] < began['at'] < min(r['started'] for r in requests), 'Approval binding')
    tables = {}
    for d in manifest['datasets']:
        xs, values, source, seen = [], [], [], set()
        with (ROOT/d['path']).open(newline='') as stream:
            for lineno, row in enumerate(csv.DictReader(stream, delimiter=d['delimiter']), 2):
                if any(row[k] != str(v) for k,v in d['filters'].items()): continue
                x = tuple(F(row[n]) for n in d['feature_names'])
                if x in seen: continue
                seen.add(x); xs.append(x); values.append([row['performance'],row['size']]); source.append(lineno)
        need(len(xs) == d['rows'], 'Source schema')
        tables[d['id']] = xs, values, source
    tokenizer = read('models/Qwen2.5-1.5B-Instruct/tokenizer.json')
    model = read('artifacts/model_manifest_v22.json')
    original_jobs = {j['job_id']:j for j in read('data/larger_probe_v22.json')['jobs']}
    expected_journal, gains, records = [], {}, []
    for job, req, start in zip(jobs, requests, starts):
        ctx = job['context']; d, seed, condition = (ctx[k] for k in ('dataset','seed','condition')); key=f'{d}_{seed}'
        case = next(c for c in manifest['cases'] if (c['dataset'],c['seed']) == (d,seed))
        prefix = case['prefix']; xs, values, source = tables[d]; cap = F(prefix['size_cap'])
        need(digest(prefix) == case['prefix_hash'] == ctx['prefix_hash'], 'Prefix identity')
        need(req['job_id'] == start['job_id'] == ctx['job_id'] and req['messages'] == start['messages'] == job['messages'], 'Prompt identity')
        need(req['status'] == 'response' and req['retry'] == 0 and req['provider'] == 'local_transformers' and
             req['model_id'] == model['model_id'] and req['revision'] == model['revision'] and
             req['parameters'] == {'do_sample':False,'max_new_tokens':20} and req['device']=='cpu' and req['dtype']=='torch.float32', 'Model provenance')
        need(history.decode_tokens(req['generated_token_ids'],tokenizer) == req['raw_output'], 'Output token decoding')
        need(len(req['generated_token_ids']) == req['output_tokens'] == 20, 'Output usage')
        chosen = req['raw_output'].splitlines()
        need(len(chosen) == len(set(chosen)) == 10 and set(chosen) <= set(ctx['mapping']), 'Distinct response IDs')
        used, trace = [], []
        need(len(req['grammar_schedule']) == 20, 'Grammar length')
        for pos,(token,domain) in enumerate(zip(req['generated_token_ids'],req['grammar_schedule'])):
            allowed = [t for t in domain if t not in used] if pos%2 == 0 else domain
            need(token in allowed, 'Grammar support')
            if pos%2 == 0: trace.append({'position':pos,'allowed':allowed,'chosen':token}); used.append(token)
        need(trace == req['selection_trace'], 'Grammar trace')
        need(req['cache_key'] == job['expected_cache_key'] == digest({'messages':job['messages'],'model':model['model_id'],
             'revision':model['revision'],'parameters':req['parameters'],'context':ctx,'parser_projection':'size_prompt_v38',
             'grammar_domains':None,'grammar_mode':'candidate_order_v19'}), 'Cache identity')
        need(req['input_tokens'] == job['expected_input_tokens'] and req['rendered_prompt_sha256'] == job['rendered_prompt_sha256'], 'Recorded input binding')
        old_job = original_jobs[ctx['source_v22_job_id']]
        body = json.loads(job['messages'][-1]['content'].split('\n',1)[1])
        old_body = json.loads(old_job['messages'][-1]['content'].split('\n',1)[1])
        need(body['constraint']['max_output_size'] == prefix['size_cap'] and body['constraint']['inclusive'], 'Acquired constraint')
        need(len(body['observations']) == 10, 'Observation denominator')
        for observation, pair in zip(body['observations'],prefix['labels']):
            need(observation.pop('output_size') == pair[1], 'Acquired size observation')
        del body['constraint']
        need(body == old_body and ctx['mapping'] == old_job['mapping'], 'Preserved candidate inputs')
        selected = [ctx['mapping'][v] for v in chosen]; ids = prefix['ids']+selected
        arm = read(f"{out}/arms/{ctx['job_id']:02d}.json")
        need(len(ids)==len(set(ids))==20 and set(selected)<=set(case['pool']) and arm['ids']==ids and arm['labels']==[values[i] for i in ids], 'Source-bound response selection')
        need(arm['logical_evaluations']==20 and arm['actual_new_accesses']==10 and arm['status']=='completed', 'Inclusive budget')
        def best(ii):return min((i for i in ii if F(values[i][1])<=cap), key=lambda i:F(values[i][0]))
        win=best(ids);runtime=F(values[win][0]);raw=min(ids,key=lambda i:F(values[i][0]))
        need((arm['best_row'],arm['best_runtime'],arm['best_size'])==(win,*values[win]), 'Feasible terminal')
        infeasible=sum(F(values[i][1])>cap for i in selected)
        need(infeasible==arm['infeasible_new_acquisitions'], 'Constraint count')
        old=read(f'results/v34_constrained/arms/{key}_cached_llm_{condition}.json')
        records.append({'dataset':d,'seed':seed,'condition':condition,'job_id':ctx['job_id'],'best_row':win,'best_runtime':values[win][0],
                        'selected_set_changed':set(selected)!=set(old['ids'][10:]),'infeasible_continuation_vectors':infeasible,
                        'runtime_only_best_violates_cap':F(values[raw][1])>cap,'request_seconds':req['wall_seconds'],
                        'input_tokens':req['input_tokens'],'output_tokens':req['output_tokens']})
        for i in selected:expected_journal.append((ctx['job_id'],i,source[i],*values[i]))
        for base in BASES:
            if base=='runtime_only_llm':other=old
            elif base.startswith('exact_'):other=read(f'results/v36_arithmetic/arms/{key}_{base[6:]}.json')
            else:other=read(f'results/v34_constrained/arms/{key}_{base}.json')
            need(other['ids'][:10]==prefix['ids'], 'Paired prefix')
            baseline=F(values[best(other['ids'])][0]);gains[(d,seed,condition,base)]=(baseline-runtime)/baseline
    need(records == summary['records'], 'Independent records')
    need(len(summary['comparisons'])==len(gains)==150, 'Comparison denominator')
    seen=set()
    for row in summary['comparisons']:
        key=tuple(row[k] for k in ('dataset','seed','condition','baseline'))
        need(key not in seen and key in gains and near(row['relative_gain'],gains[key]) and near(row['gain_decimal'],gains[key]), 'Independent paired gain')
        seen.add(key)
    need(len(summary['summaries'])==15,'Summary denominator');seen=set(); scientific=[]
    for row in summary['summaries']:
        key=(row['condition'],row['baseline']);need(key not in seen,'Unique summary');seen.add(key)
        rr=[v for (d,seed,c,b),v in gains.items() if (c,b)==key]
        need(len(rr)==10 and near(sum(rr)/10,row['equal_family_mean_gain']) and
             (sum(v>0 for v in rr),sum(v==0 for v in rr),sum(v<0 for v in rr))==(row['wins'],row['ties'],row['harms']), 'Independent aggregate')
        need(len(row['families'])==2 and {f['dataset'] for f in row['families']}=={'brotli','lrzip'},'Family denominator')
        for f in row['families']:
            vv=[v for (d,seed,c,b),v in gains.items() if (c,b)==key and d==f['dataset']]
            need(len(vv)==5 and near(sum(vv)/5,f['mean_gain']), 'Family mean')
        scientific.append({'condition':key[0],'baseline':key[1],'mean_gain_fraction':str(sum(rr)/10),'wins':row['wins'],'ties':row['ties'],'harms':row['harms']})
    journal=lines(out+'/acquisitions.jsonl')
    need(len(journal)==300 and all(x['vector_charge']==1 for x in journal) and
         [(x['job_id'],x['row_id'],x['source_line'],x['raw_runtime'],x['raw_size']) for x in journal]==expected_journal, 'Acquisition charges')
    need(summary['actual_new_requests']==30 and summary['actual_new_joint_vectors']==300 and summary['logical_evaluations']==600 and
         summary['input_tokens']==sum(r['input_tokens'] for r in requests)==55302 and summary['output_tokens']==600 and
         near(summary['request_seconds'],sum(r['wall_seconds'] for r in requests)), 'Cost totals')
    # Reconstruct both exact joint controls using acquired labels alone for predictions.
    decisions=0
    for case in manifest['cases']:
        xs,values,_=tables[case['dataset']];p=case['prefix'];cap=F(p['size_cap'])
        for mode in ('joint_shortlist','joint_full'):
            ids=p['ids'][:];labels=[[F(t),F(s)] for t,s in p['labels']]
            order=p['order'] if mode=='joint_full' else [i for i in p['order'] if i in set(case['pool'])|set(ids)]
            for _ in range(10):
                scores=[]
                for position,i in enumerate(order):
                    if i in ids:continue
                    near_ids=sorted(range(len(ids)),key=lambda j:(sum(a!=b for a,b in zip(xs[i],xs[ids[j]])),j))[:3]
                    t=sum(labels[j][0] for j in near_ids);size=sum(labels[j][1] for j in near_ids)
                    scores.append((i,position,t,size))
                feasible=[v for v in scores if v[3]<=3*cap]
                choice=min(feasible,key=lambda v:(v[2],v[1])) if feasible else min(scores,key=lambda v:(v[3],v[2],v[1]))
                i=choice[0];ids.append(i);labels.append([F(v) for v in values[i]]);decisions+=1
            arm=read(f"results/v36_arithmetic/arms/{case['dataset']}_{case['seed']}_{mode}.json")
            need(ids==arm['ids'] and labels==[[F(v) for v in pair] for pair in arm['labels']], 'Exact classical trajectory')
    # Reuse the independently implemented V35.1 historical verifier, not optimizer code.
    captured=io.StringIO()
    with contextlib.redirect_stdout(captured):history.main()
    historical=json.loads(captured.getvalue())
    print(json.dumps({'verified':True,'runtime':{'python':platform.python_version(),'system':platform.system()},
          'bundle_files':len(index['files']),'new_response_decodings':30,'new_source_bound_arms':30,
          'new_acquisition_entries':300,'paired_comparisons':150,'exact_classical_decisions':decisions,
          'summaries':scientific,'historical_replay':{k:v for k,v in historical.items() if k!='runtime'},
          'new_model_calls':0,'new_objective_acquisitions':0,
          'limitations':['saved-evidence reconstruction, not regeneration of model logits',
                         'input token counts bound to frozen records, not independently retokenized',
                         'same physical host; no independent-machine or held-out-system claim']},indent=2))

if __name__=='__main__':main()
