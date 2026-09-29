"""Post-decision source/token verification and all prespecified V38 comparisons."""
import argparse,csv,hashlib,json,os,sys
from decimal import Decimal
from pathlib import Path
from statistics import mean
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'));os.environ.update(HF_HUB_OFFLINE='1',TRANSFORMERS_OFFLINE='1',TOKENIZERS_PARALLELISM='false',MPLCONFIGDIR=str(ROOT/'.cache/matplotlib'))
from escalation.io import read,write,lines,digest
from escalation.config import load_config
from escalation.size_prompt_v38 import authorization_config
from escalation.larger_v22 import MODEL_ID,REVISION
from escalation.resources import Resources
OUT=Path('results/v38_size_prompt');BASES=('runtime_only_llm','exact_joint_shortlist','exact_joint_full','runtime_3nn','static_rank')
def need(ok,message):
    if not ok:raise ValueError(message)

def calculate():
    for p,h in read('reports/protocol_v38_size_prompt.freeze.json')['sha256'].items():need(hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'Frozen input: '+p)
    progress=read(OUT/'progress.json');need(progress['complete'] and len(progress['arms'])==30,'Incomplete study: retain intended denominator without complete-case aggregate')
    jobs=read('data/size_prompt_v38.json')['jobs'];manifest=read('data/arithmetic_v36.json');requests=lines(OUT/'requests.jsonl');starts=lines(OUT/'request_starts.jsonl')
    need(len(jobs)==len(requests)==len(starts)==30,'Thirty request denominator')
    need([r['request_id'] for r in requests]==[r['request_id'] for r in starts]==list(range(201,231)),'Request sequence')
    began=read(OUT/'started.json');approval=began['approval'];freezehash=hashlib.sha256(Path('reports/protocol_v38_size_prompt.freeze.json').read_bytes()).hexdigest()
    authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'),approval,freezehash)
    need(approval['recorded_at']<began['at']<min(r['started'] for r in requests),'Approval before execution')
    from transformers import AutoTokenizer
    from escalation.grammar_v8 import CandidateIDGrammar
    tok=AutoTokenizer.from_pretrained('models/Qwen2.5-1.5B-Instruct',local_files_only=True,trust_remote_code=False);grammar=CandidateIDGrammar(tok)
    tables={}
    for d in manifest['datasets']:
        ys=[];source=[];seen=set()
        with Path(d['path']).open(newline='') as f:
            for number,row in enumerate(csv.DictReader(f,delimiter=d['delimiter']),2):
                if any(row[k]!=str(v) for k,v in d['filters'].items()):continue
                x=tuple(float(row[n]) for n in d['feature_names'])
                if x in seen:continue
                seen.add(x);ys.append([row['performance'],row['size']]);source.append(number)
        need(len(ys)==d['rows'],'Source dimensions');tables[d['id']]=(ys,source)
    records=[];comparisons=[];expected=[]
    for job,req,start in zip(jobs,requests,starts):
        ctx=job['context'];dataset=ctx['dataset'];seed=ctx['seed'];condition=ctx['condition'];key=f'{dataset}_{seed}';ys,source=tables[dataset]
        need(req['job_id']==start['job_id']==ctx['job_id'] and req['messages']==start['messages']==job['messages'],'Prompt identity')
        need((req['model_id'],req['revision'],req['provider'])==(MODEL_ID,REVISION,'local_transformers'),'Model provenance')
        need(req['status']=='response' and req['retry']==0 and req['device']=='cpu' and req['dtype']=='torch.float32','Real successful bounded CPU response')
        need(req['parameters']=={'do_sample':False,'max_new_tokens':20},'Frozen generation parameters')
        rendered=tok.apply_chat_template(job['messages'],tokenize=False,add_generation_prompt=True)
        need(hashlib.sha256(rendered.encode()).hexdigest()==req['rendered_prompt_sha256']==job['rendered_prompt_sha256'],'Rendered prompt hash')
        need(len(tok(rendered)['input_ids'])==req['input_tokens']==job['expected_input_tokens'],'Input tokens')
        need(len(req['generated_token_ids'])==req['output_tokens']==20 and tok.decode(req['generated_token_ids'],skip_special_tokens=True)==req['raw_output'],'Output provenance')
        need(grammar.replay(req['generated_token_ids'])==req['selection_trace'] and req['grammar_sha256']==grammar.sha256,'Grammar replay')
        computed=digest({'messages':job['messages'],'model':MODEL_ID,'revision':REVISION,'parameters':req['parameters'],'context':ctx,
            'parser_projection':'size_prompt_v38','grammar_domains':None,'grammar_mode':'candidate_order_v19'})
        need(req['cache_key']==job['expected_cache_key']==computed,'New prompt cache key')
        case=next(c for c in manifest['cases'] if (c['dataset'],c['seed'])==(dataset,seed));p=case['prefix'];cap=Decimal(p['size_cap'])
        selected=[ctx['mapping'][s] for s in req['raw_output'].strip().splitlines()]
        need(len(selected)==len(set(selected))==10 and set(selected)<=set(case['pool']) and not set(selected)&set(p['ids']),'Ten new candidate rows')
        arm=read(OUT/'arms'/f"{ctx['job_id']:02d}.json");ids=p['ids']+selected
        need(arm['status']=='completed' and arm['ids']==ids and arm['labels']==[ys[i] for i in ids] and len(set(ids))==20,'Source-bound state')
        need(arm['logical_evaluations']==20 and arm['actual_new_accesses']==10 and arm['prefix_hash']==case['prefix_hash'],'Inclusive budget/shared prefix')
        for i in selected:expected.append((ctx['job_id'],i,source[i],*ys[i]))
        def best(indices):return min((i for i in indices if Decimal(ys[i][1])<=cap),key=lambda i:Decimal(ys[i][0]))
        win=best(ids);runtime=Decimal(ys[win][0]);raw=min(ids,key=lambda i:Decimal(ys[i][0]));infeasible=sum(Decimal(ys[i][1])>cap for i in selected)
        need((win,ys[win][0],ys[win][1])==(arm['best_row'],arm['best_runtime'],arm['best_size']) and infeasible==arm['infeasible_new_acquisitions'],'Feasible terminal')
        old=read(f'results/v34_constrained/arms/{key}_cached_llm_{condition}.json')
        records.append({'dataset':dataset,'seed':seed,'condition':condition,'job_id':ctx['job_id'],'best_row':win,'best_runtime':str(runtime),
            'selected_set_changed':set(selected)!=set(old['ids'][10:]),'infeasible_continuation_vectors':infeasible,
            'runtime_only_best_violates_cap':Decimal(ys[raw][1])>cap,'request_seconds':req['wall_seconds'],'input_tokens':req['input_tokens'],'output_tokens':req['output_tokens']})
        for base in BASES:
            if base=='runtime_only_llm':other=old
            elif base.startswith('exact_'):other=read(f"results/v36_arithmetic/arms/{key}_{base.removeprefix('exact_')}.json")
            else:other=read(f'results/v34_constrained/arms/{key}_{base}.json')
            need(other['ids'][:10]==p['ids'],'Baseline shared prefix')
            b=best(other['ids']);baseline=Decimal(ys[b][0]);gain=(baseline-runtime)/baseline
            comparisons.append({'dataset':dataset,'seed':seed,'condition':condition,'baseline':base,'baseline_runtime':str(baseline),
                'size_aware_runtime':str(runtime),'relative_gain':float(gain),'gain_decimal':str(gain)})
    journal=lines(OUT/'acquisitions.jsonl');need(len(journal)==300 and all(r['vector_charge']==1 for r in journal),'300 charged vectors')
    need([(r['job_id'],r['row_id'],r['source_line'],r['raw_runtime'],r['raw_size']) for r in journal]==expected,'Source journal')
    summaries=[]
    for condition in ('assigned_ids','reverse_display','reassigned_ids'):
        for base in BASES:
            rr=[r for r in comparisons if r['condition']==condition and r['baseline']==base]
            families=[{'dataset':d,'mean_gain':mean(r['relative_gain'] for r in rr if r['dataset']==d)} for d in ('brotli','lrzip')]
            summaries.append({'condition':condition,'baseline':base,'families':families,'equal_family_mean_gain':mean(f['mean_gain'] for f in families),
                'wins':sum(r['relative_gain']>0 for r in rr),'ties':sum(r['relative_gain']==0 for r in rr),'harms':sum(r['relative_gain']<0 for r in rr)})
    return {'scope':'size-aware prompt adaptation on two exposed development families; not held-out routing','records':records,'comparisons':comparisons,'summaries':summaries,
        'actual_new_requests':30,'actual_new_joint_vectors':300,'logical_evaluations':600,'input_tokens':sum(r['input_tokens'] for r in requests),
        'output_tokens':sum(r['output_tokens'] for r in requests),'request_seconds':sum(r['wall_seconds'] for r in requests),
        'startup_seconds':read(OUT/'model_runtime.json')['startup_wall_seconds'],'new_external_spend_usd':0}

def render(r):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,ax=plt.subplots(figsize=(10,4.5))
    for offset,condition,color in [(-.24,'assigned_ids','#176b93'),(0,'reverse_display','#b56143'),(.24,'reassigned_ids','#668054')]:
        vals=[next(s['equal_family_mean_gain']*100 for s in r['summaries'] if s['condition']==condition and s['baseline']==base) for base in BASES]
        ax.bar([i+offset for i in range(5)],vals,width=.24,label=condition.replace('_',' '),color=color)
    ax.set_xticks(range(5),['Old runtime-only\nLLM','Exact joint3NN\nshortlist','Exact joint3NN\nfull domain','Runtime3NN','Static rank']);ax.axhline(0,color='black',linewidth=.8)
    ax.set_ylabel('Mean feasible-runtime gain (%)');ax.set_title('V38: real size-aware prompts versus frozen comparators');ax.legend(fontsize=8);ax.grid(axis='y',alpha=.2)
    fig.text(.5,.015,'Two exposed families; fixed prefix-size research cap; not unseen-system routing.',ha='center',fontsize=8);fig.tight_layout(rect=[0,.05,1,1])
    for ext in ('png','svg'):fig.savefig(OUT/f'comparison.{ext}',dpi=180)
    plt.close(fig)

def main():
    p=argparse.ArgumentParser();p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    if a.verify_only:
        need(calculate()==read(OUT/'summary.json'),'Saved summary');print('Verified30real responses,300vectors and150paired comparisons.');return
    need(not (OUT/'summary.json').exists(),'Preserve completed analysis')
    freezehash=hashlib.sha256(Path('reports/protocol_v38_size_prompt.freeze.json').read_bytes()).hexdigest()
    cfg=authorization_config(load_config('configs/followup_v3.yaml'),read('configs/authorization_v22.json'),read('configs/authorization_v38.json'),freezehash);before=read('artifacts/resource_ledger_v2.json')
    with Resources(cfg,'artifacts/resource_ledger_v2.json') as resource:
        need(resource.remaining()>60,'Analysis reserve');r=calculate();write(OUT/'summary.json',r)
        for name,rows in [('arms',r['records']),('comparisons',r['comparisons'])]:
            with (OUT/f'{name}.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
        render(r);resource.check()
    after=read('artifacts/resource_ledger_v2.json');write('artifacts/study_v38/analysis_accounting.json',{'charged_seconds':after['experiment_seconds']-before['experiment_seconds'],'cumulative_seconds':after['experiment_seconds'],'remaining_seconds':3600-after['experiment_seconds'],'active_since':after['active_since']})
    print(json.dumps(r['summaries'],indent=2))
if __name__=='__main__':main()
